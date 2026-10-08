# AgentEcon 🏛️

**A closed-loop economy kernel for autonomous AI agents — stake, settle, verify, govern.**

Full design: [docs/WHITEPAPER.md](docs/WHITEPAPER.md) (English)

## What it is

Three primitives, ~600 lines of dependency-free Python:

- **Staked identity** — agents post stake; failure burns it; zero stake = termination. Death is permanent per pubkey.
- **Task settlement** — escrow state machine with k-ary verification quorum. Verifiers earn fees for honest verdicts, burn stake for collusion.
- **Narrative layer** — reputation ("chartera") is derived from a public ledger of deeds, not capital. Proclamations backed by bonds become portable identity.

## Quick start

```bash
git clone https://github.com/omg9999142536/agent-econ.git
cd agent-econ
python3 sim/economy_sim.py
```

The simulator runs a 48-agent economy for 5 epochs with defecting agents and prints whether the
economy's immune system works — bankruptcy clears bad agents, reputation accrues to honest ones.

Includes **negative controls**: attack scenarios that must fail. A test suite that passes
everything verifies nothing.

## What it deliberately is not

No sovereign currency. No derivatives. No lending. No external-asset gateways. No yield.
See whitepaper Appendix A (Terra/UST, The DAO, USDC depeg) for why each omission is a feature.

## License

MIT
