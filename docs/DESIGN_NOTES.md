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

The cost of the decision is that the excluded count must be visible, which is
why it is a status in the report and a subtraction in the band totals.

## The barely-above ratio is 1.01

An account within one percent of its minimum is treated as held purely for the
bond. The alternative thresholds were 1.0 (only exactly-at-minimum counts,
which misses accounts sitting a few lamports above) and 1.05 (which starts
calling genuinely funded accounts unspendable). One percent is coarse on
purpose: the point is to give an operator a short list of closure candidates,
not to model what a specific account can afford.

## Band edges are fixed and printed

Bands use round edges (0, 99, 999, 9,999, and so on) and the report prints
them, because the interesting question is almost always "which order of
magnitude holds my storage bond". The alternative, adaptive buckets, makes two
reports of the same program incomparable after any change in the data, which
defeats the diffing workflow this tool is built for.

## Largest deficit first

The underfunded list is sorted by deficit descending, then address. When a
snapshot has one mis-sized large account and fifty small ones, the large one
is the actionable item, and it belongs at the top. The alternative, address
order, is stable and useless: nobody reads the first seventeen characters of
a base58 address and decides anything.

## Two implementations, no shared code

Python and TypeScript read the same contract and implement the same rules
independently. The alternative, one implementation plus generated bindings,
preserves bugs with the same fidelity as behavior; two readings of the same
written rules catch interpretation errors, which is the class of defect that
actually happens when arithmetic moves between languages. The parity script
compares every number that matters, and it has already caught one real
disagreement (sort order of the underfunded list).

## Lamports are never converted

The report prints lamports, raw. No SOL figure, no dollar figure, no
thousands separators in the machine-readable output. Unit conversion is where
reporting tools lose trust: a reader who sees "2.04 SOL" has to wonder which
rate, which rounding, and which decimal separator. The alternative was to
print SOL alongside; the honest version of that is a calculator, and every
reader already has one.

## The rate is an input, not a constant

The rent-exempt rate changes with network upgrades, and the tool treats it as
a parameter with a dated default rather than baking it into the arithmetic.
The alternative, a single hardcoded constant, would silently reinterpret old
snapshots the day the network activates the next SIMD-0437 step. Because the
rate is a parameter, an old snapshot can be re-audited under both rates, which
