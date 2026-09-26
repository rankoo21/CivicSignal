# CivicSignal

CivicSignal is a GenLayer Intelligent Contract and incident control room for verifying public service status. An operator registers an incident with a status page, postmortem, and independent advisory. Validators independently refetch all three sources, classify the incident as `ACTIVE`, `MITIGATED`, `RESOLVED`, or `CONFLICTING`, and preserve a digest for each source.

Lifecycle: `OPEN` → `VERIFIED` → `CLOSED` (only a verified `RESOLVED` incident can close). The contract requires clean HTTPS URLs and distinct source hosts. The UI uses one wrapped wallet provider for connection and writes, so browser wallets that expose `wallet_getSnaps` remain compatible.

- Contract: `contracts/civic_signal.py`
- Tests: `python -m pytest tests -q`
- Live address: `0x54Da3c5b9A367998Ec307d68b054cc56e6D95118`
- Network: GenLayer Studionet
