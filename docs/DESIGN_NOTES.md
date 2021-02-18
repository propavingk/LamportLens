# Design notes

Decisions the tool makes on purpose, with the alternative that was rejected
and why. These are the paragraphs that end up mattering six months later.

## Integer arithmetic only

The minimum balance is computed in integers: `(128 + data_len) *
lamports_per_byte`. The historical formula multiplied by a floating point
