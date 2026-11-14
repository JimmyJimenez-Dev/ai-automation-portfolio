# AI Automation Portfolio

Hi, I'm Jimmy Jimenez. This repository showcases AI automation projects built with n8n, Python and Claude (Anthropic API), designed to save time for small businesses. Before moving into automation I worked as an HVAC and maintenance technician, so I build for real operational problems.

## Projects

| # | Project | Description | Demo |
|---|---------|-------------|------|
| 1 | [AI Email Triage](./01-ai-email-triage) | Classifies incoming emails, drafts replies with Claude, alerts via Telegram and logs to Google Sheets | [Watch demo](https://www.loom.com/share/fb32395ba7d845fdb8eeb1a37782c52b) |
| 2 | [HVAC Service Request AI](./02-HVAC-service-request) | Triages HVAC service requests by urgency, with a safety rule for gas and burning smells. It alerts the technician and confirms with the customer | [Watch demo](https://www.loom.com/share/a4d7ebdc97be49acbe7e77de027178e7) |
| 3 | [Invoice Data Extractor](./03-invoice-extractor) | Extracts invoice data with Claude, validates line items and totals, and flags errors (n8n + Python, with tests) | [Watch demo](https://www.loom.com/share/b260d47433b34c90952be6bf1e7bd06f) |
| – | [Error Handler](./00-error-handler) | Shared workflow that sends a Telegram alert when any of the workflows above fails | – |

## Design principles

- **The AI never fails silently.** If the model returns invalid output, the item is kept and flagged as *NEEDS REVIEW* instead of being lost.
- **Safety rules do not depend on the AI.** Critical decisions, such as gas leaks being treated as emergencies, are enforced in code.
- **Untrusted input is treated as data.** Emails, forms and invoices are wrapped in tags, and the model is told to ignore instructions inside them (prompt-injection defense).
- **No secrets in the repository.** All credentials live in n8n or in a local `.env` file.

## Tech stack

n8n · Claude (Anthropic API) · Python · pytest · Gmail · Telegram Bot API · Google Sheets

## How to use the workflows

1. In n8n, go to **Workflows → Import from File** and select the project's `workflow.json`.
2. Connect your own credentials (Anthropic, Gmail, Telegram, Google Sheets). The credential and Google Sheet references in the files point to my account, so re-select yours in each node.
3. Replace `YOUR_TELEGRAM_CHAT_ID` with your chat ID.
4. Optional: import `00-error-handler/workflow.json`, then in each workflow open **Settings → Error Workflow** and select *Error Handler*.

## How I use AI in this portfolio

AI is part of the product here, and it was also part of my workflow. This is how I handled the portfolio's architecture:

- **Me:** I chose the problems from my own work as an HVAC and maintenance technician, designed the workflows in n8n, defined the business and safety rules (for example, gas or smoke is always an emergency), set up the integrations, and tested every workflow with real inputs before recording the demos.
- **Claude as a pair programmer:** I used Claude (Anthropic) to review my workflows, suggest improvements, and help write and refactor code and documentation, such as the Python validation, the unit tests and the error handling. I review every change, run it, and only keep what I understand and can explain.
- **In the commits:** commits where Claude helped are marked with `Co-Authored-By` and `Reviewed-by: Claude`.

## Author

Jimmy Jimenez · [GitHub](https://github.com/JimmyJimenez-Dev)
