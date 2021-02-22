# Design notes

Decisions the tool makes on purpose, with the alternative that was rejected
and why. These are the paragraphs that end up mattering six months later.

## Integer arithmetic only

The minimum balance is computed in integers: `(128 + data_len) *
lamports_per_byte`. The historical formula multiplied by a floating point
exemption threshold, and one of the SIMD proposals that reshaped it,
SIMD-0194, exists partly to remove that float from on-chain programs. A
snapshot auditor that reintroduced floating point would reproduce the exact
class of rounding question the network is deleting.

Rejected alternative: compute with floats for readability. It buys nothing,
and it makes `at-minimum` comparisons unreliable at the boundary, which is the
comparison the tool exists to make.

## Executable accounts are excluded, not special-cased

Program accounts held by the loader do not follow the account rent rule the
same way, so the audit puts them in their own status and leaves them out of
bands, totals and owner locked sums. The alternative, reporting them as
underfunded because their lamports are below the formula, would fill the
report with thousands of findings that no operator can or should act on.
