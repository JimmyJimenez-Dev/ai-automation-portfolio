# HVAC Service Request AI

An automation that turns customer service requests into prioritized, logged and confirmed jobs, with no manual triage.

**Demo video:** https://www.loom.com/share/a4d7ebdc97be49acbe7e77de027178e7

## Problem
HVAC companies receive requests of very different urgency. A dispatcher must read each one, decide what is an emergency, log it and answer the customer.

## Solution
A web form feeds Claude, which classifies urgency (EMERGENCY, HIGH, NORMAL), identifies the issue type and writes a summary. The workflow then alerts the technician, logs the request and emails the customer a confirmation with an expected response time.

## How it works
n8n Form → Claude (urgency, issue type, summary, customer message) → Code (parse JSON) → Google Sheets log + Telegram alert + Gmail confirmation

## Tools
n8n · Claude (Anthropic API) · Telegram Bot API · Gmail · Google Sheets

## Safety logic
Requests involving gas or burning smells, or vulnerable people at home without cooling or heating, are flagged as EMERGENCY and the customer is told to call emergency services.

## Setup
1. Import `workflow.json` into n8n.
2. Connect your Anthropic, Telegram, Gmail and Google Sheets credentials.
3. Create a sheet with columns: Date, Name, Email, Phone, Address, Problem, Urgency, Issue Type, Summary.
4. Replace `YOUR_TELEGRAM_CHAT_ID` and publish the workflow.

## Author
Jimmy Jimenez, with hands-on HVAC field experience.
