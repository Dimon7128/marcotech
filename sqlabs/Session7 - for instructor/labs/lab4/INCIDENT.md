# Synthetic incident — The notification shift

The SMS spam classifier is serving requests. A monitoring warning arrived for the newer batch.

| Evidence card | Supplied fact |
| --- | --- |
| API status | Requests succeed with HTTP 200. |
| Response time | Normal for this fictional service. |
| Infrastructure | No known outage. |
| Model version | Unchanged between monitoring periods. |
| Batches | 200 synthetic SMS in each monitoring period; CSV schema record_id,message. |
| Reliable new labels | Not available. Matching model predictions are not supplied. |
| Data collection/preprocessing | Not yet verified; no bug is confirmed. |
| Monitoring location | Features are calculated from captured input text, before the model's TF-IDF processing. |
| Operational observation | Some newer messages resemble notifications. Their appearance does not establish ham/spam labels. |

Your task: investigate what the prepared data and report actually show. Distinguish observed change, possible explanation and unknown prediction quality. Recommend the team's next action and name the next piece of evidence to collect.

All service facts are authored for this exercise. They were not measured from a live deployment. HTTP 200 and normal response time do not establish correct classifications.
