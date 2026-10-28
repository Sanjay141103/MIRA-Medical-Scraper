import sys
from discovery import aggregate_clinic_urls
from pipeline import run_batch_pipeline

def main():
    region = sys.argv[1] if len(sys.argv) > 1 else "Melbourne"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    print("=" * 70)
    print("🇦🇺 MIRA-Pro: Multi-Source Australian Clinic Discovery & Bulk Scraper")
    print("=" * 70)
    print(f"Target Region: {region} | Max Clinics: {limit}")
    print("Discovery Engines: OpenStreetMap, Healthdirect, DuckDuckGo Deep Search\n")

    # 1. Multi-source discovery
    clinics = aggregate_clinic_urls(
        region=region,
        target_count=limit,
        use_osm=True,
        use_healthdirect=True,
        use_search=True
    )

    print(f"\n[Stage 1 Complete] Discovered {len(clinics)} clinic URLs:\n")
    for i, c in enumerate(clinics, 1):
        print(f"  {i}. {c['name']} -> {c['target_url']} (Source: {c['source']})")

    # 2. Resilient batch extraction with failure auditing
    master_df, audit_df, metrics = run_batch_pipeline(clinics)

    print("\n" + "=" * 70)
    print("📊 BATCH RUN SUMMARY")
    print("=" * 70)
    print(f"Total Processed:    {metrics['Total_Clinics']}")
    print(f"Successful Clinics: {metrics['Success_Clinics']}")
    print(f"Failed / Filtered:  {metrics['Failed_Clinics']}")
    print(f"Total Doctors:      {metrics['Total_Doctors']}")
    print(f"Success Rate:       {metrics['Success_Rate_Pct']}%")
    print(f"\n📁 Master Doctors Dataset: {metrics['Master_CSV_Path']}")
    print(f"📁 Scraping Audit Log:     {metrics['Audit_CSV_Path']}")
    print("=" * 70)

if __name__ == "__main__":
    main()
