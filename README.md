# CivicSignal

CivicSignal is a GenLayer Intelligent Contract and incident control room for verifying public service status. An operator registers an incident with a status page, postmortem, and independent advisory. Validators independently refetch all three sources, compare a stable readable evidence view instead of volatile HTML chrome, classify the incident as `ACTIVE`, `MITIGATED`, `RESOLVED`, or `CONFLICTING`, and preserve a digest for each source.

Lifecycle: `OPEN` → `VERIFIED` → `VERIFIED` (recheckable) → `CLOSED` (only a verified `RESOLVED` incident can close). Every verification is appended to an auditable history. The contract requires exactly three distinct HTTPS source hosts. The UI exposes recheck and close actions and uses one wrapped wallet provider for connection and writes.

- Contract: `contracts/civic_signal.py`
- Tests: `python -m pytest tests -q`
- Live address: `0x7AF4a907D2901E04D5c6549b5B0494C518DF8bC9`
- Deployment transaction: `0xb647db86ce8f7f3826a1fd9761c071f4f2c4b75b96cd1d0374c65417d594fa54`
- Reviewed source SHA-256: `fe634d45cf8433732239b1d6d64a0f40fed84788d51351ccd641804f25171859`
- Network: GenLayer Studionet
- Website: `https://civic-signal-genlayer.pages.dev/`
