# Invoice Data Extractor

An automation that extracts structured data from PDF invoices with Claude, validates the math, and only logs invoices that pass. Invalid invoices are flagged for human review.

**Demo video:** https://www.loom.com/share/b260d47433b34c90952be6bf1e7bd06f

## Problem
Accounts payable teams re-type invoice data by hand. Mistakes and missing fields lead to payment errors.

## Solution
A PDF is uploaded, Claude extracts vendor, invoice number, date, total, tax and line items as JSON, and a validation step checks required fields and that line items + tax equal the total.

## How it works
n8n Form (PDF upload) → Extract From PDF → Claude (JSON extraction) → Code (validation) → If
- Valid: log to Google Sheets + Telegram confirmation
- Invalid: Telegram "needs review" alert with the reason

## Python version
`invoice_extractor.py` implements the same logic as a command-line tool, with a retry when the model returns invalid JSON.
