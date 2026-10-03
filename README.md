# CivicSignal

CivicSignal is a GenLayer Intelligent Contract and incident control room for verifying public service status. An operator registers an incident with a status page, postmortem, and independent advisory. Validators independently refetch all three sources, classify the incident as `ACTIVE`, `MITIGATED`, `RESOLVED`, or `CONFLICTING`, and preserve a digest for each source.

Lifecycle: `OPEN` → `VERIFIED` → `VERIFIED` (recheckable) → `CLOSED` (only a verified `RESOLVED` incident can close). Every verification is appended to an auditable history. The contract requires exactly three distinct HTTPS source hosts. The UI exposes recheck and close actions and uses one wrapped wallet provider for connection and writes.

- Contract: `contracts/civic_signal.py`
- Tests: `python -m pytest tests -q`
- Live address: `0x60980e74289e2d01e0790FB6784F0869Cb0775df`
- Network: GenLayer Studionet
- Website: `https://civic-signal-genlayer.pages.dev/`
