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
git clone https://github.com/omg9999142536/agentwalls.git
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

---

## Related Projects

- **[memorykit](https://github.com/omg9999142536/memorykit)** 🧠 — memory architecture for AI agents (orthogonal axes, GC, hash-chained clock)
- **[agentguard-skill](https://github.com/omg9999142536/agentguard-skill)** 🛡️ — budget fuse for AI agent API spend

*Same author, same production-tested approach: kernel, memory, economy — the three organs of a durable agent.*

---

## Support

If this saves you time, consider supporting development:

- [afdian.com/a/3d28com](https://afdian.com/a/3d28com) — Pro license / coffee
