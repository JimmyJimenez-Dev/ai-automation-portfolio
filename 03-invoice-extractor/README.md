# Invoice Data Extractor

An automation that extracts structured data from PDF invoices with Claude, validates the math, and only logs invoices that pass. Invalid invoices are flagged for human review.

**Demo video:** [Watch on Loom](https://www.loom.com/share/b260d47433b34c90952be6bf1e7bd06f)

## Problem
Accounts payable teams re-type invoice data by hand. Mistakes and missing fields lead to payment errors.

## Solution
A PDF is uploaded, and Claude extracts vendor, invoice number, date, total, tax, currency and line items. A validation step then checks:
- required fields are present
- each line item adds up: quantity × unit price = amount
- line items + tax = total, within a 0.05 rounding tolerance
- amounts are valid numbers. Money strings like `"$1,200.50"` are parsed safely.

## Result
Estimated: replaces about 5 minutes of manual data entry per invoice with about 15 seconds, and catches total mismatches before anything is saved.

## How it works
n8n Form (PDF upload) → Extract From PDF → Claude (JSON extraction) → Code (validation) → If

- **Valid:** logged to Google Sheets + Telegram confirmation
- **Invalid:** Telegram "needs review" alert with the vendor, invoice number and reason

The n8n workflow is in `workflow.json`.

## Python version
`invoice_extractor.py` implements the same logic as a command-line tool. It uses Claude **tool use** with a JSON schema, so the model always returns a structured object instead of free text, with a retry if the call fails.

### How to run it
1. Install the dependencies:

```
pip install -r requirements.txt
```

2. Create a `.env` file from the template and add your Anthropic API key:

```
copy .env.example .env
```

(On Mac/Linux use `cp .env.example .env`.)

3. Run it on the sample invoices:

```
python invoice_extractor.py sample-invoice.pdf
python invoice_extractor.py sample-invoice-error.pdf
```

The first prints `OK: invoice validated.` and the second prints `NEEDS REVIEW: Total mismatch...`. The result is saved as JSON in the `output/` folder.

Exit codes: `0` = valid, `2` = needs review, `1` = error. This makes it easy to use in scripts.

### Tests
The validation logic is covered by unit tests that run without an API key:

```
pytest
```

## Tools
n8n · Claude (Anthropic API) · Python · pytest · Google Sheets · Telegram Bot API

## Error handling
- Missing required fields are flagged
- Line items and totals that do not add up are flagged
- Invoices without line items are sent to review, because the total cannot be verified
- Invalid model output triggers a retry, then a review flag
- API errors (invalid key, network, rate limits) show a clear message instead of a crash
- Scanned PDFs with no readable text and damaged files are rejected
- The invoice text is treated as data only, which defends against prompt injection inside a PDF

## Author
Jimmy Jimenez
