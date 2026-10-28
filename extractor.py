import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import google.generativeai as genai

# Configure your API key (User can paste key here or set GEMINI_API_KEY env variable)
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=API_KEY)

# Fallback-aware model generator with high-traffic & rate-limit resilience
def generate_medical_extraction(prompt):
    model_candidates = [
        'models/gemini-flash-latest',       # Stable alias
        'models/gemini-flash-lite-latest',  # High-traffic resilient (rarely rate-limited)
        'models/gemini-3.8-flash',          # Latest flagship flash
        'models/gemini-3.5-flash-lite',     # Secondary lightweight fallback
        'models/gemini-3.5-flash',          # Secondary flash
        'models/gemini-pro-latest'          # High-capacity fallback
    ]
    last_error = None
    for name in model_candidates:
        try:
            m = genai.GenerativeModel(name)
            response = m.generate_content(prompt)
            if response and response.text:
                return response
        except Exception as e:
            last_error = e
            err_msg = str(e).lower()
            if any(indicator in err_msg for indicator in [
                "404", "not found", "429", "quota", "resource_exhausted", 
                "503", "unavailable", "overloaded", "deadline"
            ]):
                print(f"[Model Fallback] {name} encountered '{type(e).__name__}', falling back to next candidate...")
                continue
            raise e
    raise last_error

def scrape_and_extract(url):
    try:
        # Normalize URL if scheme is missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # 1. Scrape the Website
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from headers and paragraphs
        text_content = " ".join([t.get_text(strip=True) for t in soup.find_all(['h1', 'h2', 'h3', 'p', 'div'])])
        
        # 2. AI Prompt Engineering for Data Extraction
        ai_prompt = f"""
        You are an advanced medical data extraction AI. Read the following scraped website text.
        Extract a list of all General Practitioners (GPs) and doctors mentioned.
        For each doctor, extract: 'Name', 'Specialty/Qualifications', and 'Working Hours' (if available).
        
        CRITICAL: Output ONLY a valid JSON array of objects. Do not include markdown formatting, backticks, or intro text.
        Example format: [{{"Name": "Dr. John Smith", "Specialty": "GP", "Working Hours": "Mon-Fri"}}]
        
        Scraped Text:
        {text_content[:8000]}
        """
        
        # 3. Generate AI Response
        ai_response = generate_medical_extraction(ai_prompt)
        raw_json = ai_response.text.strip().replace('```json', '').replace('```', '').strip()
        
        # 4. Process with Pandas
        data = json.loads(raw_json)
        df = pd.DataFrame(data)
        
        # Save to CSV
        csv_path = "extracted_doctors.csv"
        df.to_csv(csv_path, index=False)
        
        return df, csv_path
        
    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}]), None
