import json
import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()
client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

MODEL = "claude-sonnet-5-5"

PROMPT = """You are an accounts payable assistant. Extract the data from this invoice text.

Invoice text:
__INVOICE_TEXT__

Return ONLY valid JSON, no extra text, with this exact structure:
{"vendor": "", "invoice_number": "", "invoice_date": "YYYY-MM-DD", "total": 0.00, "tax": 0.00, "currency": "USD", "line_items": [{"description": "", "quantity": 0, "unit_price": 0.00, "amount": 0.00}]}

If a field is missing in the invoice, use null. Never invent data."""


def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_invoice(text, attempts=2):
    for attempt in range(1, attempts + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4000,
            messages=[{"role": "user", "content": PROMPT.replace("__INVOICE_TEXT__", text)}],
        )
        text_out = "".join(b.text for b in response.content if b.type == "text")
        raw = text_out.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print(f"Attempt {attempt}: invalid JSON from the model, retrying...")
    return None


def validate(data):
    issues = []
    for field in ["vendor", "invoice_number", "invoice_date", "total"]:
        if data.get(field) in (None, ""):
            issues.append(f"Missing {field}")
    items = data.get("line_items") or []
    items_sum = sum(float(i.get("amount") or 0) for i in items)
    expected = items_sum + float(data.get("tax") or 0)
    if items and data.get("total") is not None:
        total = float(data["total"])
        if abs(expected - total) > 0.05:
            issues.append(f"Total mismatch: items + tax = {expected:.2f} vs total = {total:.2f}")
    return issues


def main():
    if len(sys.argv) != 2:
        print("Usage: python invoice_extractor.py <invoice.pdf>")
        sys.exit(1)

    path = sys.argv[1]
    text = read_pdf(path)
    if not text.strip():
        print("Could not read any text from the PDF (it may be a scanned image).")
        sys.exit(1)

    data = extract_invoice(text)
    if data is None:
        print("NEEDS REVIEW: the model did not return valid JSON.")
        sys.exit(1)

    issues = validate(data)
    print(json.dumps(data, indent=2))
    print("\nNEEDS REVIEW: " + "; ".join(issues) if issues else "\nOK: invoice validated.")

    os.makedirs("output", exist_ok=True)
    name = os.path.splitext(os.path.basename(path))[0]
    out_path = os.path.join("output", name + ".json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"data": data, "issues": issues}, f, indent=2)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()