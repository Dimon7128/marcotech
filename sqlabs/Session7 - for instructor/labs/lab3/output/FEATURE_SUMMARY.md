# Synthetic SMS feature summary

Computed directly from the supplied CSVs.

| Batch | Messages | Mean characters | URL-like messages | URL-like share |
| --- | ---: | ---: | ---: | ---: |
| Reference (earlier) | 10 | 25.4 | 2 | 20.0% |
| Current (newer) | 10 | 109.0 | 8 | 80.0% |

`message_length` counts characters; `has_url` uses the case-insensitive substring rule
`http://`, `https://` or `www.`. It does not validate URLs or classify spam.

This table describes input changes. Use the real HTML report for the tool's result.
No reliable labels or matching predictions are provided. Prediction quality is unknown.
