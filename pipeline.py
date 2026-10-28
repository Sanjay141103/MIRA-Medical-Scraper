import os
import time
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from extractor import generate_medical_extraction

def scrape_clinic_page(url, timeout=10):
    """
    Fetches the clinic webpage with comprehensive error diagnosis.
    Returns: (text_content, error_category, raw_status)
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-AU,en-US;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        
        if response.status_code == 403:
            return None, "HTTP 403 (Cloudflare / Anti-Bot Blocked)", 403
        elif response.status_code == 404:
            return None, "HTTP 404 (Page Not Found)", 404
        elif response.status_code >= 400:
            return None, f"HTTP {response.status_code} Error", response.status_code

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove noisy elements
        for element in soup(["script", "style", "nav", "footer", "noscript"]):
            element.extract()
            
        text_content = " ".join([t.get_text(strip=True) for t in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'li'])])
        
        if len(text_content.strip()) < 100:
            return None, "Page Content Too Sparse / Empty", 200
            
        return text_content, None, 200

    except requests.exceptions.Timeout:
        return None, "Connection Timeout (>10s)", "TIMEOUT"
    except requests.exceptions.ConnectionError as ce:
        err_str = str(ce)
        if "10061" in err_str or "actively refused" in err_str:
            return None, "Connection Refused (Target Server Offline)", "REFUSED"
        elif "NameResolutionError" in err_str or "getaddrinfo failed" in err_str:
            return None, "DNS Resolution Failed (Domain Unreachable)", "DNS_FAIL"
        return None, f"Connection Failed: {err_str[:80]}", "CONN_ERR"
    except Exception as e:
        return None, f"Scrape Error: {str(e)[:80]}", "ERROR"

def extract_doctors_with_ai(text_content):
    """
    Passes cleaned text to Gemini and parses structured doctor records.
    Returns: (list_of_dict, error_string)
    """
    ai_prompt = f"""
    You are an advanced medical data extraction AI. Read the following scraped website text.
    Extract a list of all General Practitioners (GPs) and doctors mentioned.
    For each doctor, extract: 'Name', 'Specialty/Qualifications', and 'Working Hours' (if available).
    
    CRITICAL: Output ONLY a valid JSON array of objects. Do not include markdown formatting, backticks, or intro text.
    Example format: [{{"Name": "Dr. John Smith", "Specialty": "GP", "Working Hours": "Mon-Fri"}}]
    
    Scraped Text:
    {text_content[:8000]}
    """
    try:
        ai_response = generate_medical_extraction(ai_prompt)
        raw_text = (ai_response.text or "").strip()
        cleaned_json = raw_text.replace('```json', '').replace('```', '').strip()
        
        data = json.loads(cleaned_json)
        if isinstance(data, list):
            # Filter out entries that aren't doctors or lack a name
            valid_doctors = [d for d in data if isinstance(d, dict) and d.get("Name")]
            if valid_doctors:
                return valid_doctors, None
            else:
                return None, "No GP Entities Identified on Page"
        return None, "Invalid JSON Schema (Not a list)"
    except json.JSONDecodeError as jde:
        return None, f"JSON Parse Failed: {str(jde)[:50]}"
    except Exception as e:
        return None, f"AI Extraction Failed: {str(e)[:80]}"

def run_batch_pipeline(clinic_list, progress_callback=None,
                       doctors_csv="master_australian_doctors.csv",
                       audit_csv="scraping_audit_log.csv"):
    """
    Iterates through a list of clinics, runs scraping + AI extraction,
    and returns (master_df, audit_df, metrics_dict).
    """
    all_doctors = []
    audit_logs = []
    
    total = len(clinic_list)
    success_count = 0
    fail_count = 0
    
    print(f"\n[PIPELINE START] Starting Batch Extraction for {total} clinics...\n")
    
    for idx, clinic in enumerate(clinic_list, start=1):
        name = clinic.get("name", "Unknown Clinic")
        url = clinic.get("target_url") or clinic.get("website", "")
        region = clinic.get("region", "Australia")
        source = clinic.get("source", "Automated Discovery")
        
        start_time = time.time()
        print(f"[{idx}/{total}] Processing: {name} ({url})")
        
        if progress_callback:
            progress_callback(idx / total, f"Scraping [{idx}/{total}]: {name}")
            
        # 1. Scrape Page
        text_content, scrape_err, status_code = scrape_clinic_page(url)
        elapsed = round(time.time() - start_time, 2)
        
        if scrape_err:
            fail_count += 1
            audit_logs.append({
                "Clinic_Name": name,
                "Target_URL": url,
                "Region": region,
                "Status": "FAILED",
                "HTTP_Status": status_code,
                "Failure_Reason": scrape_err,
                "Doctors_Extracted": 0,
                "Duration_Sec": elapsed,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"    [FAILED] {scrape_err}")
            time.sleep(1)
            continue
            
        # 2. Extract with AI
        doctors, ai_err = extract_doctors_with_ai(text_content)
        elapsed = round(time.time() - start_time, 2)
        
        if ai_err:
            fail_count += 1
            audit_logs.append({
                "Clinic_Name": name,
                "Target_URL": url,
                "Region": region,
                "Status": "FAILED",
                "HTTP_Status": status_code,
                "Failure_Reason": ai_err,
                "Doctors_Extracted": 0,
                "Duration_Sec": elapsed,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"    [FAILED AI] {ai_err}")
        else:
            success_count += 1
            count = len(doctors)
            print(f"    [SUCCESS] Extracted {count} doctors.")
            
            for doc in doctors:
                specialty_val = doc.get("Specialty / Qualifications") or doc.get("Specialty/Qualifications") or doc.get("Specialty") or doc.get("Qualifications") or "General Practitioner"
                working_hours_val = doc.get("Working Hours") or doc.get("Working_Hours") or doc.get("Hours") or "Not specified"
                
                clean_doc = {
                    "Name": doc.get("Name", "Dr. Unknown"),
                    "Specialty / Qualifications": specialty_val,
                    "Working Hours": working_hours_val,
                    "Clinic_Name": name,
                    "Region": region,
                    "Clinic_URL": url,
                    "Discovery_Source": source,
                    "Extracted_At": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                all_doctors.append(clean_doc)
                
            audit_logs.append({
                "Clinic_Name": name,
                "Target_URL": url,
                "Region": region,
                "Status": "SUCCESS",
                "HTTP_Status": status_code,
                "Failure_Reason": "None (Extracted Cleanly)",
                "Doctors_Extracted": count,
                "Duration_Sec": elapsed,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        time.sleep(1.5) # Polite delay
        
    # Convert to DataFrames
    master_df = pd.DataFrame(all_doctors) if all_doctors else pd.DataFrame(columns=[
        "Name", "Specialty / Qualifications", "Working Hours", "Clinic_Name", "Region", "Clinic_URL", "Discovery_Source", "Extracted_At"
    ])
    audit_df = pd.DataFrame(audit_logs) if audit_logs else pd.DataFrame(columns=[
        "Clinic_Name", "Target_URL", "Region", "Status", "Failure_Reason", "Doctors_Extracted"
    ])
    
    # Save CSVs
    master_df.to_csv(doctors_csv, index=False)
    audit_df.to_csv(audit_csv, index=False)
    
    metrics = {
        "Total_Clinics": total,
        "Success_Clinics": success_count,
        "Failed_Clinics": fail_count,
        "Total_Doctors": len(master_df),
        "Success_Rate_Pct": round((success_count / total * 100) if total > 0 else 0, 1),
        "Master_CSV_Path": os.path.abspath(doctors_csv),
        "Audit_CSV_Path": os.path.abspath(audit_csv)
    }
    
    return master_df, audit_df, metrics
