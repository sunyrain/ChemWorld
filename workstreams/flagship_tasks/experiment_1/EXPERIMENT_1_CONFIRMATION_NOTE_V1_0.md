# Experiment 1 seven-locus confirmation note v1.0

Status: **design frozen before any confirmation unit executes**.

## Question and denominator

Does the frozen development-qualified design retain all Q1–Q8 gates on sealed,
outcome-blind public coordinates and an independent keyed-noise namespace?

The denominator is exactly 7 challenge-passed loci × 5 Worlds = 35 atomic units:
EC-E, EC-P, EC-S, RX-P, PA-E, C-E, and C-P. RX-S, PA-S, and PA-P are permanently
excluded from this confirmation set because their v1.2 challenge failed. A passing
locus cannot compensate for a failed World or another locus.

## Coordinate and noise design

The public contract records the generator version, legal domain, region definitions,
development-coordinate binding, and commitments. A 256-bit salt deterministically
realizes one coordinate plan shared by all five Worlds per locus. Every locus covers
at least two preregistered regions outside its development coordinates. Confirmation
uses a new keyed-noise namespace derived from the sealed salt; replicate counts and
all Q1–Q8 thresholds remain those in the bound source contracts.

The salt and realized coordinates live only in a non-Git server directory with 0700
directory and 0600 file permissions. Git records only SHA-256 commitments and public
generator/domain metadata. Coordinates are disclosed only in the post-run evidence
receipt.

## Execution and decision

The frozen schedule contains 1,585 primary scientific rows and 1,585 tolerance-zero
replay checks. Seven locus processes run sequentially with one worker. Every planned
row remains in the denominator: missing, malformed, non-finite, physical-failure, or
platform-failure rows cannot be silently excluded. Outputs are immutable, resume is
forbidden, and the realized set retires after this one shot.

Each World is evaluated with the same frozen Q1–Q8 semantics. A locus is
`qualified-confirmed` only if W01–W05 all pass. This is process-isolated confirmation,
not third-party independent validation and not Participant execution.
