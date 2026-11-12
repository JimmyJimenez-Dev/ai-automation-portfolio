# HVAC Service Request AI

An automation that turns customer service requests into prioritized, logged and confirmed jobs, with no manual triage.

**Demo video:** [Watch on Loom](https://www.loom.com/share/a4d7ebdc97be49acbe7e77de027178e7)

## Problem
HVAC companies receive requests of very different urgency. A dispatcher must read each one, decide what is an emergency, log it and answer the customer.

## Solution
A web form feeds Claude, which classifies urgency (EMERGENCY, HIGH, NORMAL), identifies the issue type and writes a summary for the technician. The workflow then alerts the technician, logs the request and emails the customer a confirmation with an expected response time.

## Result
Estimated: reduces dispatcher intake from about 5 minutes per request (reading, prioritizing, logging, replying) to about 15 seconds, and flags emergencies immediately instead of waiting in a queue.

## How it works
n8n Form → Claude (urgency, issue type, summary) → Code (validation + safety rules + customer message) → Google Sheets log + Telegram alert + Gmail confirmation

## Safety logic
- **Keyword safety rule in code:** if the request mentions gas, burning, smoke, sparks, fire or carbon monoxide, it is **always** marked EMERGENCY, even if the AI says otherwise. The customer is told to turn off the system, and to leave the building and call 911 if they smell gas or see smoke.
- Claude also flags as EMERGENCY water near electrical parts, and no cooling or heating with vulnerable people at home (babies, elderly).
- If Claude's answer is invalid, the request is treated as **HIGH**, never ignored, and the technician is told to read the original description.
- The rule is cautious on purpose: a false alarm, such as a mention of a "gas furnace", is better than a missed gas leak.

## Security
- **Template customer email:** the confirmation email is built from a fixed template, not free AI text, so the public form cannot be used to send arbitrary content from the company's Gmail.
- **Prompt-injection defense:** the customer's text is wrapped in `<request>` tags, and Claude is told to ignore instructions inside it.
- Email and problem description are required fields, and the email field is validated by the form.

## Tools
n8n · Claude (Anthropic API) · Telegram Bot API · Gmail · Google Sheets

## Setup
1. Import `workflow.json` into n8n.
2. Connect your Anthropic, Telegram, Gmail and Google Sheets credentials, and select your own sheet.
3. Create a sheet with columns: Date, Name, E-Mail, Phone, Address, Problem, Urgency, Issue Type, Summary.
4. Replace `YOUR_TELEGRAM_CHAT_ID` and publish the workflow.
5. Optional: set the [Error Handler](../00-error-handler) as this workflow's Error Workflow.

## Author
Jimmy Jimenez, with hands-on HVAC field experience.
