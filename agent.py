import os
import json
import fitz  # pymupdf
import ollama
from dotenv import load_dotenv
from pyairtable import Api
from datetime import datetime

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def analyze_document(text, document_name, retries=3):
    for attempt in range(retries):
        prompt = f"""You are an AI document intelligence agent. Analyze the following document.

DOCUMENT NAME: {document_name}

DOCUMENT CONTENT:
{text[:3000]}

You MUST respond with ONLY a valid JSON object. No explanation, no markdown, no code blocks. Just the raw JSON object starting with {{ and ending with }}.

Use this exact structure:
{{"document_type": "contract", "summary": "brief summary here", "key_information": "key facts here", "flags": "any issues here"}}"""

        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response["message"]["content"].strip()
        
        # Extract JSON object
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(raw[start:end])
            except json.JSONDecodeError:
                print(f"JSON parse failed on attempt {attempt + 1}, retrying...")
                continue
    
    # Fallback if all retries fail
    return {
        "document_type": "unknown",
        "summary": "Could not parse document analysis.",
        "key_information": "Parse error — please retry.",
        "flags": "Analysis failed after 3 attempts."
    }



def log_to_airtable(document_name, analysis):
    import requests
    
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Documents"
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            "Document Name": str(document_name),
            "Document Type": str(analysis.get("document_type", "")),
            "Summary": str(analysis.get("summary", "")),
            "Key Information": str(analysis.get("key_information", "")),
            "Flags": str(analysis.get("flags", "")),
            "Timestamp": datetime.now().strftime("%Y-%m-%d")
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200 or response.status_code == 201:
        print("Successfully logged to Airtable")
    else:
        print(f"Airtable error: {response.status_code} - {response.text}")

def process_document(pdf_path):
    document_name = os.path.basename(pdf_path)
    
    print(f"Processing: {document_name}")
    print("Extracting text...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters\n")

    print("Analyzing document...")
    analysis = analyze_document(text, document_name)

    print(f"Document Type: {analysis['document_type']}")
    print(f"\nSummary:\n{analysis['summary']}")
    print(f"\nKey Information:\n{analysis['key_information']}")
    print(f"\nFlags:\n{analysis['flags']}")

    print("\nLogging to Airtable...")
    log_to_airtable(document_name, analysis)
    print("Done.\n")

    return analysis

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 agent.py <path_to_pdf>")
    else:
        process_document(sys.argv[1])
