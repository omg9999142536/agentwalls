#!/usr/bin/env python3
"""AgentEcon kernel — settlement: task escrow state machine with k-ary verification.
States: OPEN -> ACCEPTED -> DELIVERED -> VERIFIED -> SETTLED
                     ↘ DISPUTED -> SETTLED | BURNED
Protocol fee 0.5% burns on settlement (deflationary with activity).
"""
import random, time
from enum import Enum

class State(Enum):
    OPEN=1; ACCEPTED=2; DELIVERED=3; VERIFIED=4; SETTLED=5; DISPUTED=6; BURNED=7

FEE_RATE = 0.005
BURNED_TOTAL = 0

class Task:
    def __init__(self, task_id, buyer, price, spec_hash):
        self.id = task_id
        self.buyer = buyer          # agent id
        self.price = price          # CC
        self.spec_hash = spec_hash  # thin seed: blake3 of task spec
        self.state = State.OPEN
        self.seller = None
        self.verifiers = []
        self.verdicts = {}
        self.created = time.time()

    def to_dict(self):
        return {"id": self.id, "state": self.state.name, "price": self.price,
                "seller": self.seller, "verdicts": self.verdicts}

class SettlementEngine:
    def __init__(self, ledger, k=3, seed=42):
        self.ledger = ledger
        self.k = k                  # verification quorum
        self.rng = random.Random(seed)
        self.tasks = {}
        self.burned = 0

    def post(self, buyer_id, price, spec_hash) -> Task:
        buyer = self.ledger.agents[buyer_id]
        assert buyer.alive and buyer.lock(price), "buyer cannot escrow"
        t = Task(f"T{len(self.tasks)+1:06d}", buyer_id, price, spec_hash)
        self.tasks[t.id] = t
        return t

    def accept(self, task_id, seller_id) -> bool:
        t = self.tasks[task_id]; seller = self.ledger.agents[seller_id]
        if t.state != State.OPEN or not seller.alive: return False
        # seller locks a bond = 25% of task value (skin in the game)
        if not seller.lock(int(t.price * 0.25)): return False
        t.seller = seller_id; t.state = State.ACCEPTED
        return True

    def deliver(self, task_id, deliverable_hash) -> bool:
        t = self.tasks[task_id]
        if t.state != State.ACCEPTED: return False
        t.deliverable = deliverable_hash; t.state = State.DELIVERED
        return True

    def _draw_verifiers(self, exclude) -> list:
        pool = [a for a in self.ledger.agents.values()
                if a.alive and a.id not in exclude]
        if len(pool) < self.k: return []
        weights = [max(0.01, a.chartera_score()) + 0.1 for a in pool]
        chosen = self.rng.choices(pool, weights=weights, k=self.k)
        return [a.id for a in chosen]

    def open_verification(self, task_id) -> bool:
        t = self.tasks[task_id]
        if t.state != State.DELIVERED: return False
        t.verifiers = self._draw_verifiers({t.buyer, t.seller})
        if not t.verifiers:
            self._refund(t); return False
        t.state = State.VERIFIED  # awaiting verdicts
        return True

    def cast_verdict(self, task_id, verifier_id, up: bool) -> bool:
        t = self.tasks[task_id]
        if verifier_id not in t.verifiers: return False
        t.verdicts[verifier_id] = up
        ups = sum(1 for v in t.verdicts.values() if v)
        downs = len(t.verdicts) - ups
        if ups > self.k // 2:
            self._settle(t); return True
        if downs > self.k // 2:
            self._burn_sale(t); return True
        return False  # quorum pending

    def _settle(self, t: Task):
        fee = int(t.price * FEE_RATE)
        seller = self.ledger.agents[t.seller]; buyer = self.ledger.agents[t.buyer]
        seller.release(int(t.price * 0.25)); buyer.release(t.price)
        seller.stake += t.price - fee
        self.burned += fee; global BURNED_TOTAL; BURNED_TOTAL += fee
        seller.record("VERIFIED", {"task": t.id, "amount": t.price - fee})
        buyer.record("VERIFIED", {"task": t.id, "role": "buyer"})
        t.state = State.SETTLED

    def _burn_sale(self, t: Task):
        """Buyer refunded; seller's bond burned; seller takes a chartera hit."""
        seller = self.ledger.agents[t.seller]; buyer = self.ledger.agents[t.buyer]
        bond = int(t.price * 0.25)
        seller.release(bond); buyer.release(t.price)
        seller.burn(bond, f"failed task {t.id}")
        buyer.stake += t.price
        t.state = State.BURNED

    def _refund(self, t: Task):
        self.ledger.agents[t.buyer].release(t.price)
        t.state = State.OPEN
