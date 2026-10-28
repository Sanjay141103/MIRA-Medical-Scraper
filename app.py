import os
import pandas as pd
import gradio as gr
from extractor import scrape_and_extract, generate_medical_extraction
from discovery import aggregate_clinic_urls
from pipeline import run_batch_pipeline

# Gradio Handler for Multi-Source Bulk Crawl
def handle_bulk_run(region, limit, sources, progress=gr.Progress()):
    try:
        progress(0.1, desc=f"Discovering clinic URLs in {region}...")
        use_osm = "OpenStreetMap (Registry)" in sources
        use_hd = "Healthdirect (NHSD Directory)" in sources
        use_search = "Deep Search Engine (DuckDuckGo)" in sources
        
        clinics = aggregate_clinic_urls(
            region=region,
            target_count=int(limit),
            use_osm=use_osm,
            use_healthdirect=use_hd,
            use_search=use_search
        )
        
        progress(0.3, desc=f"Discovered {len(clinics)} clinics. Initiating scraping & AI extraction...")
        
        def pipeline_progress(pct, msg):
            progress(0.3 + (pct * 0.65), desc=msg)
            
        master_df, audit_df, metrics = run_batch_pipeline(clinics, progress_callback=pipeline_progress)
        
        kpi_summary = f"""
### [SUMMARY] Bulk Crawl Execution: {region}
- **Total Clinics Processed:** `{metrics['Total_Clinics']}`
- **Successfully Extracted:** `{metrics['Success_Clinics']}`
- **Failed / Filtered Domains:** `{metrics['Failed_Clinics']}` *(Labeled in Audit Log)*
- **Total Doctors Cataloged:** `{metrics['Total_Doctors']}`
- **Pipeline Success Rate:** `{metrics['Success_Rate_Pct']}%`
"""
        master_path = metrics["Master_CSV_Path"] if os.path.exists(metrics["Master_CSV_Path"]) else None
        audit_path = metrics["Audit_CSV_Path"] if os.path.exists(metrics["Audit_CSV_Path"]) else None
        
        return kpi_summary, master_df, master_path, audit_df, audit_path
        
    except Exception as e:
        err_msg = f"### ❌ Error during execution: {str(e)}"
        empty_df = pd.DataFrame([{"Error": str(e)}])
        return err_msg, empty_df, None, empty_df, None

# Build UI
with gr.Blocks(title="MIRA: AI Medical Directory Scraper") as interface:
    gr.Markdown("""
    # 🩺 MIRA: AI-Powered Australian Medical Directory Scraper
    **AI Growth & Automation Pipeline** • Gokul Infocare Practical Assessment • Developed by **Sanjay Mathivanan**
    """)
    
    with gr.Tab("📌 Tab 1: Single Clinic Scraper (Task 1 Deliverable)"):
        gr.Markdown("""
        ### MIRA-Lite: Direct URL Extractor
        Paste any Australian clinic webpage to scrape unstructured text and extract structured GP profiles with Google Gemini.
        """)
        with gr.Row():
            url_input = gr.Textbox(
                label="Enter Australian Clinic URL",
                placeholder="https://www.cbddoctorsmelbourne.com.au/meet-our-team/",
                lines=1,
                scale=4
            )
            single_btn = gr.Button("Extract Medical Data", variant="primary", scale=1)
            
        single_df = gr.Dataframe(label="Extracted Medical Data", wrap=True)
        single_file = gr.File(label="Download CSV")
        
        single_btn.click(
            fn=scrape_and_extract,
            inputs=[url_input],
            outputs=[single_df, single_file]
        )
        
    with gr.Tab("⚡ Tab 2: Automated Multi-Source Bulk Crawler (MIRA-Pro)"):
        gr.Markdown("""
        ### MIRA-Pro: Multi-Source Discovery & Bulk Scraper with Failure Auditing
        Automatically discovers clinic websites via **OpenStreetMap Registry**, **Deep Search Engine**, and **Healthdirect Directory**, then crawls and extracts doctor rosters while categorizing any failed or blocked URLs into an audit log.
        """)
        with gr.Row():
            region_dropdown = gr.Dropdown(
                label="Target Australian Region",
                choices=["Melbourne", "Sydney", "Brisbane", "Gold Coast", "Perth", "Adelaide"],
                value="Melbourne",
                scale=2
            )
            limit_slider = gr.Slider(
                label="Max Clinics to Crawl",
                minimum=1,
                maximum=10,
                value=2,
                step=1,
                scale=2
            )
            sources_checkbox = gr.CheckboxGroup(
                label="Discovery Engines",
                choices=["OpenStreetMap (Registry)", "Healthdirect (NHSD Directory)", "Deep Search Engine (DuckDuckGo)"],
                value=["OpenStreetMap (Registry)", "Deep Search Engine (DuckDuckGo)"],
                scale=3
            )
            bulk_btn = gr.Button("🚀 Run Automated Discovery & Extraction", variant="primary", scale=2)
            
        kpi_output = gr.Markdown("### Ready to crawl. Configure parameters above and click Run.")
        
        with gr.Tabs():
            with gr.Tab("📋 Extracted Doctors (Master Dataset)"):
                bulk_df = gr.Dataframe(label="Aggregated Australian GP Directory", wrap=True)
                bulk_file = gr.File(label="Download Master CSV")
            with gr.Tab("🔍 Scraping Audit Log & Failure Labels"):
                audit_df = gr.Dataframe(label="Full Audit Log (Successes & Labeled Failures)", wrap=True)
                audit_file = gr.File(label="Download Audit Log CSV")
                
        bulk_btn.click(
            fn=handle_bulk_run,
            inputs=[region_dropdown, limit_slider, sources_checkbox],
            outputs=[kpi_output, bulk_df, bulk_file, audit_df, audit_file]
        )

if __name__ == "__main__":
    interface.launch()
