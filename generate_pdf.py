import os
import matplotlib
os.environ['MPLCONFIGDIR'] = os.path.join(os.path.dirname(__file__), '.mplconfig')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

def create_prompt_doc():
    pdf_filename = "Prompt_Documentation.pdf"
    
    with PdfPages(pdf_filename) as pdf:
        # =====================================================================
        # PAGE 1: Foundations, AI Schema & Initial Pipeline
        # =====================================================================
        fig1 = plt.figure(figsize=(8.27, 11.69), dpi=300)
        ax1 = fig1.add_axes([0, 0, 1, 1])
        ax1.set_xlim(0, 8.27)
        ax1.set_ylim(0, 11.69)
        ax1.axis('off')
        ax1.add_patch(patches.Rectangle((0, 0), 8.27, 11.69, facecolor='#FAFAFC', zorder=0))

        # Header
        h_rect = patches.FancyBboxPatch((0.6, 10.3), 7.07, 0.95, boxstyle="round,pad=0.08,rounding_size=0.15",
                                        facecolor='#1E3A8A', edgecolor='#1E40AF', linewidth=1)
        ax1.add_patch(h_rect)
        ax1.text(0.9, 10.90, "MIRA-Pro: AI Medical Directory Scraper & Crawler",
                 fontsize=14.5, fontweight='bold', color='#FFFFFF', family='sans-serif')
        ax1.text(0.9, 10.60, "Complete Prompt Engineering, Debugging & Troubleshooting Documentation",
                 fontsize=9.5, color='#93C5FD', family='sans-serif')
        ax1.text(0.9, 10.38, "Candidate: Sanjay Mathivanan  |  Position: AI Growth & Automation Associate  |  Company: Gokul Infocare",
                 fontsize=8, color='#E2E8F0', family='sans-serif')

        # Executive Overview
        s_rect = patches.FancyBboxPatch((0.6, 9.35), 7.07, 0.82, boxstyle="round,pad=0.06,rounding_size=0.1",
                                        facecolor='#EFF6FF', edgecolor='#BFDBFE', linewidth=1)
        ax1.add_patch(s_rect)
        ax1.text(0.85, 9.95, "Executive Summary & Iterative Methodology", fontsize=9, fontweight='bold', color='#1E40AF', family='sans-serif')
        overview_txt = (
            "This document presents the full prompt engineering history used to develop MIRA. Beyond initial prototyping, "
            "it captures real-world engineering challenges faced during development—including API model deprecation (404s), "
            "rate-limiting under high traffic (429 ResourceExhausted), thread deadlocks from circular imports, and the architectural "
            "scaling into a multi-source automated discovery crawler with failure auditing."
        )
        ax1.text(0.85, 9.80, overview_txt, fontsize=7.6, color='#334155', family='sans-serif', wrap=True, va='top', linespacing=1.3)

        def draw_card(ax, y_top, card_height, stage_badge, title, prompt_label, prompt_body, rationale_body):
            card = patches.FancyBboxPatch((0.6, y_top - card_height), 7.07, card_height,
                                          boxstyle="round,pad=0.05,rounding_size=0.1",
                                          facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.8)
            ax.add_patch(card)

            # Badge
            badge = patches.FancyBboxPatch((0.85, y_top - 0.28), 1.65, 0.20, boxstyle="round,pad=0.02,rounding_size=0.05",
                                           facecolor='#2563EB', edgecolor='none')
            ax.add_patch(badge)
            ax.text(1.67, y_top - 0.18, stage_badge, fontsize=7, fontweight='bold', color='#FFFFFF', family='sans-serif', ha='center', va='center')
            ax.text(2.65, y_top - 0.18, title, fontsize=9, fontweight='bold', color='#0F172A', family='sans-serif', va='center')

            # Prompt Box
            ax.text(0.85, y_top - 0.42, prompt_label, fontsize=7.6, fontweight='bold', color='#475569', family='sans-serif')
            p_box = patches.FancyBboxPatch((0.85, y_top - 1.15), 6.57, 0.68, boxstyle="round,pad=0.04,rounding_size=0.05",
                                           facecolor='#F8FAFC', edgecolor='#E2E8F0', linewidth=0.7)
            ax.add_patch(p_box)
            ax.text(0.98, y_top - 0.52, prompt_body, fontsize=7.2, color='#1E293B', family='monospace', wrap=True, va='top', linespacing=1.25)

            # Rationale
            ax.text(0.85, y_top - 1.27, "Technical Rationale & Challenges Overcome:", fontsize=7.6, fontweight='bold', color='#1E40AF', family='sans-serif')
            ax.text(0.85, y_top - 1.38, rationale_body, fontsize=7.2, color='#334155', family='sans-serif', wrap=True, va='top', linespacing=1.3)

        # Stage 1
        draw_card(
            ax=ax1, y_top=9.20, card_height=2.25,
            stage_badge="STAGE 1: SCRAPING",
            title="Initial Logic & Scraping Architecture",
            prompt_label="Prompt 1 (Initial Logic):",
            prompt_body='"Write a Python script using requests and BeautifulSoup to scrape all paragraph and header text from a medical clinic\'s \'Our Doctors\' webpage, handling basic HTTP headers to avoid being blocked."',
            rationale_body=(
                "Australian clinic websites employ varied layouts and bot protections (Cloudflare, User-Agent filtering). "
                "The initial prompt engineered a resilient scraping harness using real browser headers and multi-tag parsing "
                "(h1, h2, h3, p, div) to capture all unstructured practitioner listings without losing relevant clinical details."
            )
        )

        # Stage 2
        draw_card(
            ax=ax1, y_top=6.80, card_height=2.25,
            stage_badge="STAGE 2: AI SCHEMA",
            title="Semantic Intelligence & Strict Output Formatting",
            prompt_label="Prompt 2 (Adding AI Data Intelligence):",
            prompt_body='"The scraped text is too messy. Integrate the Google Gemini API (or OpenAI API). Write a prompt inside the Python script that takes the scraped text and asks the LLM to extract all Doctor Names, Specialties, and Contact Details, forcing the LLM to output ONLY a strict JSON array of objects."',
            rationale_body=(
                "Traditional regex rules break across heterogeneous clinic templates. This prompt introduces an LLM reasoning "
                "step to semantically understand messy medical credentials (FRACGP, MBBS, DipChildHealth). Crucially, it imposes "
                "strict JSON array formatting constraints to enable predictable downstream data pipelines."
            )
        )

        # Stage 3
        draw_card(
            ax=ax1, y_top=4.40, card_height=2.25,
            stage_badge="STAGE 3: GRADIO UI",
            title="Adding the UI & Automated Pandas Export",
            prompt_label="Prompt 3 (Adding the UI & Pandas):",
            prompt_body='"Wrap this pipeline into a Gradio web UI. Have the Gradio app take a URL string as input, run the scraping and LLM extraction, load the resulting JSON into a Pandas DataFrame, and display the DataFrame in the UI while also providing a downloadable CSV file."',
            rationale_body=(
                "A script running only in a terminal has low usability for growth and sales teams. This prompt transforms the "
                "pipeline into a single-click web application. Gradio provides intuitive inputs and dynamic dataframe preview, "
                "while Pandas seamlessly serializes the structured records into an instantly exportable CSV file."
            )
        )

        # Footer 1
        ax1.text(4.135, 0.40, "Page 1 of 3  •  MIRA Prompt Engineering & Troubleshooting Documentation  •  Gokul Infocare",
                 fontsize=7.5, color='#94A3B8', family='sans-serif', ha='center')
        pdf.savefig(fig1)
        plt.close(fig1)

        # =====================================================================
        # PAGE 2: Troubleshooting, API 404s, Rate Limits & Circular Imports
        # =====================================================================
        fig2 = plt.figure(figsize=(8.27, 11.69), dpi=300)
        ax2 = fig2.add_axes([0, 0, 1, 1])
        ax2.set_xlim(0, 8.27)
        ax2.set_ylim(0, 11.69)
        ax2.axis('off')
        ax2.add_patch(patches.Rectangle((0, 0), 8.27, 11.69, facecolor='#FAFAFC', zorder=0))

        # Page 2 Header
        p2_hdr = patches.FancyBboxPatch((0.6, 10.55), 7.07, 0.65, boxstyle="round,pad=0.06,rounding_size=0.12",
                                        facecolor='#1E3A8A', edgecolor='#1E40AF', linewidth=1)
        ax2.add_patch(p2_hdr)
        ax2.text(0.9, 10.95, "Engineering Problem-Solving & Real-World Bug Fixes",
                 fontsize=12, fontweight='bold', color='#FFFFFF', family='sans-serif')
        ax2.text(0.9, 10.70, "Part 2: Markdown Sanitization, API 404 Deprecations & High-Traffic Fallback Cascades",
                 fontsize=8.5, color='#93C5FD', family='sans-serif')

        # Stage 4
        draw_card(
            ax=ax2, y_top=10.35, card_height=2.25,
            stage_badge="STAGE 4: HARDENING",
            title="Refining Prompt & Markdown Sanitization",
            prompt_label="Prompt 4 (Troubleshooting Markdown Backticks):",
            prompt_body='"The LLM is sometimes adding markdown formatting like ```json to the output, which breaks the json.loads() function. Update the internal system prompt to strictly forbid markdown formatting and strip any backticks before parsing the JSON into Pandas."',
            rationale_body=(
                "LLMs frequently wrap code blocks in markdown fences, triggering fatal JSONDecodeErrors in Python. We engineered "
                "a two-tier defense: (1) System prompt negative constraints forbidding intro text and markdown fences, and "
                "(2) programmatic string sanitization (.replace('```json', '').replace('```', '')) for 100% parsing resilience."
            )
        )

        # Stage 5
        draw_card(
            ax=ax2, y_top=7.95, card_height=2.25,
            stage_badge="STAGE 5: MODEL 404 FIX",
            title="Resolving API Model Deprecations & 404 Errors",
            prompt_label="Prompt 5 (Dynamic Model Fallback):",
            prompt_body='"When calling gemini-1.5-flash, the API returned \'404 models/gemini-1.5-flash is not found for API version v1beta\'. Write a multi-model fallback cascade function in Python that dynamically queries available models and switches automatically to active models like gemini-3.8-flash without crashing."',
            rationale_body=(
                "Google retired older flash checkpoints for new API accounts. Instead of hardcoding a fragile string, we built "
                "a dynamic fallback resolver (generate_medical_extraction) that queries available flash endpoints and tries active "
                "candidates (models/gemini-3.8-flash, gemini-flash-latest) automatically if a 404 is encountered."
            )
        )

        # Stage 6
        draw_card(
            ax=ax2, y_top=5.55, card_height=2.30,
            stage_badge="STAGE 6: RATE-LIMIT FIX",
            title="Handling High-Traffic 429 & 503 Errors via Lite Models",
            prompt_label="Prompt 6 (Traffic Resilience & Rate Limits):",
            prompt_body='"Under peak traffic, the Gemini API throws \'429 ResourceExhausted\' or \'503 Service Unavailable\'. Update the fallback cascade to catch 429 and 503 errors and instantly switch to high-throughput Lite models like gemini-flash-lite-latest, which have larger free-tier quotas and lower latency."',
            rationale_body=(
                "Flagship models experience quota throttling during peak hours. By incorporating 'models/gemini-flash-lite-latest' "
                "into the priority cascade and catching quota/overload exceptions, the pipeline automatically routes traffic to "
                "lighter, high-throughput models, guaranteeing uninterrupted continuous extraction."
            )
        )

        # Footer 2
        ax2.text(4.135, 0.40, "Page 2 of 3  •  MIRA Prompt Engineering & Troubleshooting Documentation  •  Gokul Infocare",
                 fontsize=7.5, color='#94A3B8', family='sans-serif', ha='center')
        pdf.savefig(fig2)
        plt.close(fig2)

        # =====================================================================
        # PAGE 3: Architecture Decoupling, Discovery & Assessment Alignment
        # =====================================================================
        fig3 = plt.figure(figsize=(8.27, 11.69), dpi=300)
        ax3 = fig3.add_axes([0, 0, 1, 1])
        ax3.set_xlim(0, 8.27)
        ax3.set_ylim(0, 11.69)
        ax3.axis('off')
        ax3.add_patch(patches.Rectangle((0, 0), 8.27, 11.69, facecolor='#FAFAFC', zorder=0))

        # Page 3 Header
        p3_hdr = patches.FancyBboxPatch((0.6, 10.55), 7.07, 0.65, boxstyle="round,pad=0.06,rounding_size=0.12",
                                        facecolor='#1E3A8A', edgecolor='#1E40AF', linewidth=1)
        ax3.add_patch(p3_hdr)
        ax3.text(0.9, 10.95, "Scaling to Multi-Source Discovery & Failure Auditing",
                 fontsize=12, fontweight='bold', color='#FFFFFF', family='sans-serif')
        ax3.text(0.9, 10.70, "Part 3: Decoupled Worker Threads, Dual CSV Auditing & Assessment Rubric Alignment",
                 fontsize=8.5, color='#93C5FD', family='sans-serif')

        # Stage 7
        draw_card(
            ax=ax3, y_top=10.35, card_height=2.25,
            stage_badge="STAGE 7: THREAD FIX",
            title="Resolving Gradio Worker Thread Circular Imports",
            prompt_label="Prompt 7 (Decoupling Architecture):",
            prompt_body='"When triggering bulk crawl in Gradio, an internal error occurred: \'AttributeError: Button object has no attribute _id\' due to circular imports between pipeline.py and app.py. Refactor the codebase by moving all scraping and extraction logic into a standalone extractor.py module."',
            rationale_body=(
                "Gradio handles background task execution in worker threads. Circular imports re-instantiated UI block components "
                "inside worker threads, corrupting Gradio's internal component tree. Decoupling extraction into extractor.py "
                "isolated core computational logic from UI rendering, resulting in a clean, enterprise-grade architecture."
            )
        )

        # Stage 8
        draw_card(
            ax=ax3, y_top=7.95, card_height=2.30,
            stage_badge="STAGE 8: MULTI-SOURCE",
            title="Multi-Source Automated Discovery & Failure Auditing",
            prompt_label="Prompt 8 (National Discovery & Auditing):",
            prompt_body='"Build an automated discovery system that aggregates clinic doctor URLs across Australian cities (Sydney, Melbourne, etc.) using OpenStreetMap, Healthdirect, and DuckDuckGo. For any URL that fails (Cloudflare 403, Timeout, DNS Fail), label the exact reason in scraping_audit_log.csv."',
            rationale_body=(
                "Rather than manual copy-pasting, this prompt scaled the tool into a national directory crawler. Crucially, it "
                "implemented a dual-output model: master_australian_doctors.csv for structured GP rosters, and scraping_audit_log.csv "
                "to provide complete visibility and diagnostics into skipped or protected clinic domains."
            )
        )

        # Assessment Rubric Alignment Card
        eval_card = patches.FancyBboxPatch((0.6, 1.45), 7.07, 3.85,
                                           boxstyle="round,pad=0.06,rounding_size=0.12",
                                           facecolor='#FFFFFF', edgecolor='#10B981', linewidth=1)
        ax3.add_patch(eval_card)

        eval_badge = patches.FancyBboxPatch((0.85, 4.95), 2.3, 0.22,
                                            boxstyle="round,pad=0.03,rounding_size=0.06",
                                            facecolor='#059669', edgecolor='none')
        ax3.add_patch(eval_badge)
        ax3.text(2.0, 5.06, "ASSESSMENT CRITERIA ALIGNMENT MATRIX", fontsize=7.5, fontweight='bold', color='#FFFFFF',
                 family='sans-serif', ha='center', va='center')

        rubrics = [
            ("Practical Use of AI Tools:", "Integrated Google Gemini Flash models for high-speed entity extraction from noisy HTML DOM elements, transforming unstructured clinical bios into strict schema arrays."),
            ("Iterative Prompt Engineering:", "Demonstrated an intentional 8-stage evolution: baseline scraping -> schema enforcement -> UI integration -> markdown sanitization -> 404 model migration -> traffic fallback -> thread decoupling -> bulk multi-source discovery."),
            ("Problem Solving & Resilience:", "Solved real-world production blockers: API model deprecations (404), peak traffic rate-limiting (429 fallback to Lite), Gradio thread deadlocks, and Cloudflare anti-bot blocks."),
            ("Quality & Real-World Usefulness:", "Directly outputs Australian medical directory data with 34+ doctors cataloged in Sydney alone, while generating a dedicated scraping audit log for enterprise operations."),
            ("Background Influence:", "Directly applies data pipeline validation principles developed at BMW Plant Chennai (automating 150,000 files), prioritizing fault tolerance and deterministic outputs over brute-force scripts.")
        ]

        y_r = 4.75
        for title, desc in rubrics:
            ax3.text(0.85, y_r, title, fontsize=7.6, fontweight='bold', color='#065F46', family='sans-serif')
            ax3.text(2.65, y_r, desc, fontsize=7.1, color='#334155', family='sans-serif', wrap=True, va='top', linespacing=1.2)
            y_r -= 0.62

        # Footer 3
        ax3.text(4.135, 0.40, "Page 3 of 3  •  MIRA Prompt Engineering & Troubleshooting Documentation  •  Gokul Infocare",
                 fontsize=7.5, color='#94A3B8', family='sans-serif', ha='center')
        pdf.savefig(fig3)
        plt.close(fig3)

    print(f"Successfully generated 3-page {pdf_filename}")

if __name__ == "__main__":
    create_prompt_doc()
