# Error Handler

A small shared n8n workflow that sends a Telegram alert whenever another workflow fails. The alert includes the workflow name, the node that failed, the error message and a link to the execution.

## How it works
Error Trigger → Telegram alert

## Setup
1. Import `workflow.json` into n8n.
2. Connect your Telegram credential and replace `YOUR_TELEGRAM_CHAT_ID`.
3. Open each workflow (Email Triage, HVAC, Invoice), go to **Settings → Error Workflow** and select **Error Handler (Telegram alert)**.

## Author
Jimmy Jimenez
