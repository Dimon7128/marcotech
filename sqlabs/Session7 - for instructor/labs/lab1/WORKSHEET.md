# Lab 1 — Student worksheet

**Synthetic messages and simulated responses only.** The known labels were assigned for these teaching scenarios. These records are not measured production results or predictions computed from the saved model.

Use this table if you cannot open `records.csv`. Both contain the same records.

| Record | HTTP status | Synthetic SMS | Predicted label | Known true label |
| --- | ---: | --- | --- | --- |
| sms-01 | 200 | URGENT! Claim your free prize now! | ham | spam |
| sms-02 | 200 | Can we meet at five today? | ham | ham |
| sms-03 | 200 | WIN a free gift! Claim your reward today! | spam | spam |
| sms-04 | 200 | Your appointment is confirmed for Monday. | spam | ham |
| sms-05 | 200 | Please bring the notebook to class. | ham | ham |
| sms-06 | 200 | Exclusive offer! Reply now to claim a free prize. | spam | spam |

## Your answers

1. Which requests succeeded according to their HTTP status?

   Answer: ________________________________________________

2. Find one incorrect prediction. What did the model say, and what is the known label?

   Record: __________  Predicted: __________  Known: __________

3. Why would ordinary HTTP status/error monitoring miss this problem?

   Answer: ________________________________________________

4. Suggest one additional signal. What evidence would you need to interpret it?

   Signal: ________________________________________________

   Evidence needed: _______________________________________

5. Can predicted spam/ham counts alone tell you whether predictions are correct? Explain.

   Answer: ________________________________________________
