# AI Email Triage

An automation that reads incoming Gmail messages, classifies them with Claude, drafts a reply, alerts me on Telegram and logs everything in Google Sheets.

**Demo video:** [Watch on Loom](https://www.loom.com/share/fb32395ba7d845fdb8eeb1a37782c52b)

## Problem
Small businesses lose hours sorting and answering routine emails.

## Solution
Each new email is automatically categorized (URGENT, SALES, SPAM, OTHER) and gets a suggested reply, so nothing important is missed.

## Result
Estimated: cuts email triage from about 3 minutes of reading, sorting and drafting per email to about 10 seconds, with an alert within a minute of arrival.

## How it works
Gmail Trigger → Claude (classification + draft reply) → Code (parse and validate JSON) → Telegram alert + Google Sheets log

## Reliability
- **Full email body:** Claude reads the complete message, trimmed to 6,000 characters, not only Gmail's short preview snippet.
- **No lost emails:** if Claude returns invalid JSON or an unknown category, the email is still logged and alerted as **NEEDS REVIEW** instead of stopping the workflow.
- **Prompt-injection defense:** the email is wrapped in `<email>` tags, and Claude is told to ignore any instructions inside it.

## Tools
n8n · Claude (Anthropic API) · Gmail · Telegram Bot API · Google Sheets

## Setup
1. Import `workflow.json` into n8n.
2. Connect your Gmail, Anthropic, Telegram and Google Sheets credentials, and select your own sheet.
3. Create a sheet with columns: Date, From, Subject, Category, Draft Reply.
4. Replace `YOUR_TELEGRAM_CHAT_ID` and publish the workflow.
5. Optional: set the [Error Handler](../00-error-handler) as this workflow's Error Workflow.

## Author
Jimmy Jimenez
