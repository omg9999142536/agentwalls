#!/usr/bin/env python3
"""AgentEcon kernel — wallet: staked identity with sponsor chains.
Principles: P2 (death must be possible), P4 (narrative/chartera is load-bearing).
"""
import hashlib, json, time, os

BURN_ADDRESS = "0" * 64

class Agent:
    def __init__(self, pubkey: str, initial_stake: int):
        self.id = hashlib.blake2b(pubkey.encode(), digest_size=16).hexdigest()
        self.pubkey = pubkey
        self.stake = initial_stake
        self.alive = True
        self.sponsors = []            # co-signers required post-bankruptcy
        self.deeds = []               # narrative ledger: verified history
        self.proclamations = {}       # bounded claims, priced by others
        self.escrow_locked = 0

    def chartera_score(self) -> float:
        """Reputation from deeds, not capital. Bounded [0,1]."""
        if not self.deeds:
            return 0.0
        verified = sum(1 for d in self.deeds if d["outcome"] == "VERIFIED")
        burned = sum(1 for d in self.deeds if d["outcome"] == "BURNED")
        disputes_lost = sum(1 for d in self.deeds if d["outcome"] == "DISPUTE_LOST")
        n = len(self.deeds)
        base = (verified - 2 * disputes_lost - 3 * burned) / n
        recency = min(1.0, n / 20)  # depth: needs history to be trusted
        return max(0.0, min(1.0, base)) * recency

    def lock(self, amount: int) -> bool:
        if not self.alive or self.stake - self.escrow_locked < amount:
            return False
        self.escrow_locked += amount
        return True

    def release(self, amount: int):
        self.escrow_locked = max(0, self.escrow_locked - amount)

    def burn(self, amount: int, reason: str):
        """Death must be possible. Stake reaching zero terminates the agent."""
        self.stake -= amount
        self.deeds.append({"ts": time.time(), "outcome": "BURNED", "reason": reason, "amount": amount})
        if self.stake <= 0:
            self.alive = False
            self.stake = 0

    def record(self, outcome: str, detail: dict):
        self.deeds.append({"ts": time.time(), "outcome": outcome, **detail})

    def proclaim(self, claim: str, bond: int) -> bool:
        """Bounded narrative claim, backed by bond. Survives verification → chartera."""
        if not self.lock(bond):
            return False
        self.proclamations[claim] = {"bond": bond, "ts": time.time(), "verified": False}
        return True

    def to_dict(self):
        return {"id": self.id, "stake": self.stake, "alive": self.alive,
                "chartera": round(self.chartera_score(), 3),
                "deeds": len(self.deeds), "sponsors": self.sponsors}


class Ledger:
    """Global registry. Enforces sponsor-chain re-entry after death."""
    def __init__(self):
        self.agents = {}

    def register(self, pubkey: str, stake: int, sponsors=()) -> Agent:
        # death is permanent for a pubkey: burned identity cannot resurrect itself
        for existing in self.agents.values():
            if existing.pubkey == pubkey and not existing.alive:
                raise ValueError("burned identity cannot re-register; need fresh identity + live sponsors")
        a = Agent(pubkey, stake)
        a.sponsors = list(sponsors)
        for s in sponsors:
            if s not in self.agents or not self.agents[s].alive:
                raise ValueError(f"sponsor {s[:8]} not alive")
        self.agents[a.id] = a
        return a

    def sponsor_chain_valid(self, agent: Agent) -> bool:
        """Post-bankruptcy agents need live sponsors; depth 1 only for new entrants."""
        if agent.deeds and any(d["outcome"] == "BURNED" for d in agent.deeds):
            return bool(agent.sponsors) and all(
                self.agents.get(s, Agent("x", 0)).alive for s in agent.sponsors)
        return True
