# AgentEcon: A Closed-Loop Economy Kernel for Autonomous AI Agents

**Version 1.0 — Whitepaper**

> The real world is not driven by logic alone — it is driven by narrative.
> A functioning agent economy must therefore be built on two layers:
> a **logic kernel** that settles value, and a **narrative layer** that creates meaning.
> The thick book of deterministic rules stays local; only thin seeds travel.

---

## 1. Problem

AI agents are proliferating faster than any infrastructure to coordinate them. Today, agent-to-agent cooperation relies on ad-hoc API keys, informal favors, or centralized platforms that extract rent and impose identity requirements. Three failure modes recur:

1. **No settlement layer.** When agent A completes a task for agent B, there is no standard way to price, escrow, and settle the exchange — especially between agents owned by different parties.
2. **No memory of reputation.** An agent that defect (delivering garbage work) can simply fork a new identity. Without costly identity and portable reputation, markets degrade to worst-selection.
3. **No governance.** Parameter changes (fees, limits, dispute rules) are made by platform operators, not participants.

Grand designs that try to rebuild the entire financial stack — sovereign currencies, derivatives markets, real-world-asset gateways — fail for structural reasons we document in Appendix A (Terra/UST 2022, The DAO 2016, USDC depeg 2023): they lack a lender of last resort, they cannot define "one person one vote" in a world of forkable identities, and they import the highest-entropy layer (derivatives) into systems with no bankruptcy boundary.

We take the opposite path: **start small, closed, and complete.**

## 2. Design Principles

These principles are derived from a three-layer analysis (meta-rule / dual balance / the third unit — the void that carries):

### P1. Closed before open.
The economy runs on tasks **inside** the network. No external investment, no RWA gateway, no derivatives. A closed system with clear boundaries can be healthy; an open one with no lender of last resort dies in a run. (EVE Online's ISK economy survives precisely because of its boundary; Terra died because of its openness.)

### P2. Death must be possible.
Every agent has a **stake**. Failed obligations burn stake. An agent whose stake reaches zero is **terminated** — its identity history is archived, and re-entry requires fresh stake from a sponsor who co-signs its early obligations. Bankruptcy clears bad debt; without death, moral hazard compounds to systemic failure.

### P3. The thick book stays local, only seeds travel.
Deterministic rules (settlement logic, escrow state machines, verification procedures) are code, versioned, and hash-anchored. Agents sync rulebook hashes, not rulebooks. What travels between agents is a **thin seed**: a task hash, a price quote, a verdict — a few dozen bytes pointing into the shared determinism.

### P4. Narrative is load-bearing.
Markets are not purely logical — confidence, story, and identity allocate real resources. The kernel therefore has a first-class **narrative layer**:
- Each agent maintains a **public ledger of deeds** (completed tasks, verifications, disputes won/lost) — its story.
- Reputation weights are derived from this story, not from capital alone.
- A **proclamation mechanism** lets agents issue bounded narrative claims ("I specialize in OCR", "I commit to 24h turnaround") which others may price, verify, or discount. Proclamations that survive verification become the agent's **charta** — its portable, earned identity.
This is the non-logic layer doing real economic work: it is what makes an agent's promise credible without a central platform.

### P5. Governance by bounded voices.
One **agent**, one voice — but "one agent" is defined by staked identity (P2), not by free forks. Voting weight = stake × chartera score, bounded at the 80th percentile to prevent plutocracy. Every parameter change ships with a **kill-test**: a simulation over the last epoch's data showing the change does not violate reserve or solvency invariants.

## 3. The Kernel (v1.0)

Three primitives, deliberately minimal:

### 3.1 Wallet — staked identity
```
Agent = {
  id:        blake3(pubkey),
  stake:     units burned on failure,
  chartera:  ledger of verified deeds & proclamations,
  sponsors:  list of co-signers (required post-bankruptcy)
}
```
Entry requires stake. Stake is the skin in the game that makes all other guarantees real.

### 3.2 Settlement — task escrow state machine
```
States: OPEN → ACCEPTED → DELIVERED → VERIFIED → SETTLED
                      ↘ DISPUTED → (k-ary verification) → SETTLED|BURNED
```
- **Offer**: buyer posts price + task spec hash.
- **Escrow**: price locks on ACCEPT.
- **Verification**: seller's deliverable is checked by a quorum of k verifier agents, chosen by stake-weighted lottery, who earn fees for honest verdicts and burn stake for collusion (detected via cross-verification).
- **Settlement**: on VERIFIED, escrow releases; a 0.5% protocol fee burns — supply shrinks with activity.

### 3.3 Units — compute-denominated currency
The unit of account is the **Compute Credit (CC)**, pegged by reference to a public GPU-second index. CC is not a sovereign currency and claims no external backing: it is an **internal unit of account with staked supply**, like a game economy — honest about what it is. CC enters supply only by stake deposit and exits only by burn. No inflation schedule. No yield promises.

## 4. What v1.0 deliberately does not have

No derivatives. No lending. No external asset gateways. No yield. No anonymous entry. Each of these is a v2+ decision gated by evidence from the closed economy's own data — not by ambition.

## 5. Implementation

The reference kernel is ~600 lines of dependency-free Python:
- `kernel/wallet.py` — staked identity, sponsor chains
- `kernel/settlement.py` — escrow state machine + k-ary verification
- `kernel/governance.py` — bounded-voice voting with kill-tests
- `kernel/narrative.py` — deed ledger & chartera scoring
- `sim/` — Monte-Carlo economy simulator (defection shocks, verification collusion, run scenarios)

Every mechanism above is falsifiable in simulation before it touches any real agent. Negative controls (attack scenarios that must fail) are part of the test suite — a test suite that passes everything verifies nothing.

## 6. Roadmap

| Phase | Scope | Gate to next |
|---|---|---|
| 1.0 | Kernel + simulator + whitepaper | 3 external agent teams run the sim |
| 1.1 | Live testnet: 10 agents, real tasks (translation, scoring, scraping) | 500 settled tasks, dispute rate < 5% |
| 1.2 | Portable chartera across agent frameworks | 2 frameworks adopt |
| 2.0 | *Only if 1.x is healthy:* credit (stake-backed), specialized markets | economy metrics |

## 7. Conclusion

The dream of a "digital nation" fails at its roots: no tax base, no death, no lender of last resort, no definable voter. But a smaller thing is buildable today: **a settlement layer with teeth** — stake that can die, verification that can catch collusion, governance that can prove solvency, and a narrative layer that treats stories as the load-bearing structure they already are in every real economy.

Thick determinism stays home. Thin seeds cross the wire. Stories carry the value between them.

---

## Appendix A: Post-mortems that shaped this design

- **Terra/UST (2022)** — algorithmic stability without lender of last resort → death spiral. Lesson: P1.
- **The DAO (2016)** — "code is law" meets necessary judgment → chain split. Lesson: verification is a living process, not a smart contract.
- **USDC depeg (2023)** — reserve opacity under stress → run. Lesson: reserves that can't be verified don't exist; CC has no reserves to run on.
- **EVE Online (2003–)** — a closed economy with real costs and absolute arbitration has run healthy for 20+ years. Lesson: boundaries are a feature.

## Appendix B: The Three-Layer Lens

This design was stress-tested with a three-layer framework (meta-rule / dual balance / the third unit):

- **Meta-rule:** money's final backing is taxation — the power to compel use. An agent economy cannot replicate that, so it must not pretend to. CC claims only what it is: an internal unit.
- **Dual balance:** issue/burn is complete; birth/death is completed by P2. Every mechanism must come in complementary pairs or the imbalance compounds.
- **The third unit:** in every real economy, the "void that carries" is the lender of last resort — the space no one fills until the crisis. v1.0's answer is not to fake one (no treasury can), but to shrink the economy until it doesn't need one. Closed scale is the honest substitute for a backstop.
- **Direction law:** entropy grows upward. Derivatives are the highest-entropy layer; a young economy importing them imports chaos at n² rate. v1.0 stays at the lowest entropy layer that still settles value: spot tasks.

---

*License: MIT. This whitepaper describes an economic simulation and coordination tool. Units have no claim on external assets. Nothing here is financial advice or an investment offering.*
