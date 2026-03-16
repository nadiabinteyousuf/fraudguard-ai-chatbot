def route_query(query: str):
    q = query.lower()

    ocr_keywords = [
        "invoice",
        "receipt",
        "extract text",
        "document",
        "statement",
        "scan",
        "pdf",
        "image",
        "analyze this invoice",
        "analyze this statement"
    ]

    rag_keywords = [
        "aml",
        "fatf",
        "regulation",
        "policy",
        "compliance",
        "sanctions",
        "rule",
        "basel"
    ]

    search_keywords = [
        "latest",
        "news",
        "recent",
        "trend",
        "cyber attack",
        "cyber fraud",
        "current events"
    ]

    fraud_keywords = [
        "suspicious transaction",
        "suspicious transactions",
        "fraud",
        "scam",
        "money laundering",
        "structuring",
        "smurfing",
        "account takeover",
        "transaction risk"
    ]

    if any(k in q for k in ocr_keywords):
        return "OCR_AGENT"

    if any(k in q for k in rag_keywords):
        return "RAG_AGENT"

    if any(k in q for k in search_keywords):
        return "SEARCH_AGENT"

    if any(k in q for k in fraud_keywords):
        return "FRAUD_AGENT"

    return "FRAUD_AGENT"