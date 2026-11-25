# Lab 2 — Spot the Drift

**Time:** 15 minutes of mostly guided practice.  
**Goal:** Compare earlier/current SMS patterns and explain what the changes do and do not establish.

Both CSV batches are **synthetic teaching scenarios** written for this lab. They do not represent changes measured in UCI SMS Spam Collection or production traffic. Each batch contains ten messages. There are no true-label or prediction columns; the saved classifier is not run.

## Prepare before class

Use **Python 3.10**, continuing the previous local course setup. Copy the lab2 folder supplied by your instructor into your own working location. Keep `starter.py`, `reference.csv`, `current.csv` and `requirements.txt` together. The two CSVs are your prepared starter data.

From the copied `lab2/` folder, create a separate environment and install the tested dependencies. These commands use the environment's Python directly; activation is optional.

Windows PowerShell:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe starter.py
```

macOS / Linux:

```bash
python3.10 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python starter.py
```

If your instructor already prepared a compatible environment, use its Python. The first run should load both batches, print per-message features and URL-like percentages, and show `TODO` for average lengths. That is the intended starting state.

## Two feature definitions

- **`message_length`:** Python/pandas character count, including spaces and punctuation exactly as stored. This lab uses plain ASCII text, so there is no ambiguity about combined characters. It is not a byte, word or token count.
- **`has_url_like`:** `True` if the lowercase message contains `http://`, `https://` or `www.` anywhere; otherwise `False`. This approximate rule can match incomplete strings and miss bare domains such as `example.com`. It neither validates a URL nor decides whether a message is spam. The script never opens links.

## Your 15-minute investigation

1. **Load and inspect — 3 minutes.** Run the starter. Read one message from each CSV and check its printed length and URL-like flag. Check why `cur-06` is detected despite uppercase `WWW.`.
2. **Complete one calculation — 3 minutes.** In `summarize()`, replace the single `None` for `average_length` with the average of the `message_length` column. Use the hints below if needed. Run again.
3. **Compare — 4 minutes.** Record the reference/current average lengths and URL-like percentages. Identify the direction of both changes. Keep the same feature rules for both batches.
4. **Interpret — 4 minutes.** Answer the four questions in [WORKSHEET.md](WORKSHEET.md). Use the measurements to support your explanation.
5. **Check — 1 minute.** Share one observed change, one limit and the next evidence you would seek.

### Hints

1. Select the column using `features["message_length"]`.
2. The pandas method for an average is called `mean`; call the method using parentheses.

Only one line needs completing. Loading, the URL-like rule and the rest of the calculations are supplied. Spend most of your effort interpreting the comparison.

## If something fails

| Problem | Quick route |
| --- | --- |
| `No module named pandas` | Use the environment's Python above for both installation and execution. |
| CSV missing | Keep both original CSV files beside `starter.py`; retain their names and headers. |
| Average still says `TODO` | Replace the `None` inside `summarize()` and save the file before running again. |
| Calculation gives an error | Select `message_length`, use `mean()` with parentheses, and check spelling. |
| Python/install access unavailable | Use the prepared [EXPECTED_RESULTS.md](EXPECTED_RESULTS.md), inspect two original messages and answer the same worksheet questions. |

No API deployment, Docker configuration, model training or Evidently installation is part of this lab. Do not change your existing SMS service or its model environment to run the comparison.

The fallback summary is generated from the same CSV files by an executed completed exercise. Its per-record feature table lets you check the comparison without Python.

References: [pandas string lengths](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.Series.str.len.html), [pandas mean](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.Series.mean.html).
