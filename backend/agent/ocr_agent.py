from langsmith import traceable
from backend.tools.ocr_tool import extract_text_from_file
import re

@traceable(name="ocr_agent")
def run_ocr_agent(file_path, user_query=""):
    text = extract_text_from_file(file_path)

    if not text.strip():
        return {
            "reply": "No text detected in the uploaded document.",
            "risk": "LOW",
            "score": 10
        }

    text_lower = text.lower()
    query_lower = user_query.lower()

    risk_score = 20
    reasons = []
    doc_type = "Unknown Document"

    if "invoice" in text_lower or "total due" in text_lower:
        doc_type = "Invoice"
    elif "statement of account" in text_lower or "opening balance" in text_lower or "closing balance" in text_lower:
        doc_type = "Bank Statement"
    elif "receipt" in text_lower:
        doc_type = "Receipt"

    suspicious_keywords = ["bitcoin", "gift card", "urgent", "transfer now", "crypto"]
    for word in suspicious_keywords:
        if word in text_lower:
            risk_score += 15
            reasons.append(f"Suspicious keyword detected: {word}")

    if "suspicious" in query_lower or "fraud" in query_lower or "detect" in query_lower:
        if "mm/dd/yyyy" in text_lower:
            risk_score += 20
            reasons.append("Template-like placeholder date detected")

        if "statement of account" in text_lower and "transaction description" in text_lower:
            risk_score += 10
            reasons.append("Statement appears to be a template, not a detailed real export")

        amounts = re.findall(r"\b\d{1,3}(?:,\d{3})*(?:\.\d{2})\b", text)
        if len(amounts) >= 3:
            risk_score += 10
            reasons.append("Multiple monetary values detected")

        repeated = {}
        for amt in amounts:
            repeated[amt] = repeated.get(amt, 0) + 1

        repeated_suspicious = [amt for amt, count in repeated.items() if count >= 3]
        if repeated_suspicious:
            risk_score += 25
            reasons.append(f"Repeated transaction amounts detected: {', '.join(repeated_suspicious)}")

    if risk_score >= 70:
        risk = "HIGH"
    elif risk_score >= 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    reason_text = "\n".join([f"- {r}" for r in reasons]) if reasons else "- No strong red flags detected"

    return {
        "reply": f"""Document Type: {doc_type}

Extracted Text Preview:
{text[:900]}

Analysis:
{reason_text}""",
        "risk": risk,
        "score": risk_score
    }