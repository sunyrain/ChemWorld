# Security Policy

ChemWorld is research software for virtual, replayable physical-chemistry environments. Security
reports are welcome, especially for public/private information leakage, unsafe execution of
third-party submissions, credential exposure, artifact verification bypasses, path traversal, and
resource-isolation failures.

## Supported code

Security fixes are evaluated against the active `main` branch and, when practical, the latest tagged
release. Historical protocols, archived evidence, and superseded release candidates are immutable
records; they may receive a warning or migration note instead of an in-place rewrite.

## Report a vulnerability privately

Do not open a public issue containing exploit details, credentials, private evaluation material, or
provider payloads.

Use GitHub's private vulnerability reporting page for this repository:

<https://github.com/sunyrain/ChemWorld/security/advisories/new>

If private reporting is unavailable, contact the repository owners through GitHub without including
sensitive details and request a private channel. Never send live credentials. A useful report
contains:

- the affected commit, version, component, and platform;
- the security boundary that was crossed;
- minimal reproduction steps using synthetic or redacted data;
- likely impact and whether the issue is reproducible;
- any suggested mitigation.

Please allow maintainers time to reproduce and coordinate a fix before public disclosure.

## Credential and data handling

Credentials must be supplied through the local process environment and must not enter Git,
trajectories, generated evidence, logs, screenshots, or provider-response archives. In particular,
do not commit `.env`, `api.md`, `key2.md`, access tokens, private seeds, raw provider payloads, or
private evaluation data.

If a credential is exposed:

1. revoke or rotate it at the provider immediately;
2. stop any process that may still be using it;
3. report the affected paths and commits privately;
4. treat history rewriting and cache invalidation as a coordinated incident response, not a routine
   cleanup command.

Do not paste a suspected secret into an issue or diagnostic command output to prove that it exists.

## Third-party code and provider boundaries

The local student harness is a bounded message and process interface, not a security boundary for
malicious code. Untrusted submissions require an independent low-privilege execution environment
with no network access, read-only inputs, isolated writable storage, and explicit CPU, memory,
process, and wall-time limits.

Online-provider executions can disclose prompts and permitted public observations to the configured
service. Keep evaluator-owned truth, private seeds, hidden world identities, credentials, and
unapproved artifacts outside the Agent-visible workspace and request payload. Paid or private runs
must fail closed when their authorization, route, budget, or credential contract is absent.

## Scientific safety boundary

ChemWorld models versioned virtual materials, costs, risks, instruments, and process outcomes. Its
outputs are not instructions for physical laboratory work and must not be used as the sole basis for
real chemical operations, hazard decisions, scale-up, or regulatory compliance. Real experiments
require qualified personnel, institutional procedures, independent hazard assessment, and suitable
physical controls.

## Integrity issues that are also security relevant

Please report any way to:

- expose evaluator-owned state through public observations, errors, paths, hashes, or timing;
- forge or bypass trajectory digest, exact replay, resource, score, or source-binding checks;
- make a failed or development-only artifact appear release-eligible;
- escape repository or sandbox path restrictions;
- cause unbounded network, subprocess, storage, or compute use;
- load private data through a public configuration or packaged resource.

Ordinary correctness bugs without a confidentiality, integrity, authorization, or isolation impact
can be reported through the repository's public issue tracker.
