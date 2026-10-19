# Invoice Data Extractor

An automation that extracts structured data from PDF invoices with Claude, validates the math, and only logs invoices that pass. Invalid invoices are flagged for human review.

**Demo video:** https://www.loom.com/share/b260d47433b34c90952be6bf1e7bd06f

## Problem
Accounts payable teams re-type invoice data by hand. Mistakes and missing fields lead to payment errors.

## Solution
A PDF is uploaded, Claude extracts vendor, invoice number, date, total, tax and line items as JSON, and a validation step checks required fields and that line items + tax equal the total.

## How it works
n8n Form (PDF upload) → Extract From PDF → Claude (JSON extraction) → Code (validation) → If

- **Valid:** logged to Google Sheets + Telegram confirmation
- **Invalid:** Telegram "needs review" alert with the reason

The n8n workflow is in `workflow.json`.

## Python version
`invoice_extractor.py` implements the same logic as a command-line tool, with a retry when the model returns invalid JSON.

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

The first prints `OK: invoice validated.` and the second prints `NEEDS REVIEW: Total mismatch...`

## Tools
n8n · Claude (Anthropic API) · Python · Google Sheets · Telegram Bot API

## Error handling
- Missing required fields are flagged
- Totals that do not add up are flagged
- Invalid JSON from the model triggers a retry, then a review flag
- Scanned PDFs with no readable text are rejected

## Author
Jimmy Jimenez
