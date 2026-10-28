# 🎬 Master Video Presentation Guide & Storyboard (120–140 Seconds)

This guide provides a **step-by-step screen layout, visual storyboard, and verbatim speaking script** tailored to hit every evaluation metric in the Gokul Infocare assessment rubric.

---

## 🖥️ Screen Layout Setup Before Recording

1. **Screen Split:**
   - **Left Half (50%):** Browser showing the running Gradio App at **`http://127.0.0.1:7861`**.
   - **Right Half (50%):** VS Code showing **`README.md`** (scrolled to the Mermaid Architecture Diagram) and **`app.py`**.
2. **Camera:** Turn on your webcam in the corner of your screen (via Loom, OBS, or Zoom) so the evaluator can see you speaking with confidence.

---

## ⏱️ Visual Storyboard & Timing Roadmap

| Time | What You Show on Screen | What You Say (Key Topic) |
| :--- | :--- | :--- |
| **0:00 – 0:25** | Webcam + Full Screen split view | **Introduction:** Sanjay Mathivanan, role, and MIRA project overview. |
| **0:25 – 0:50** | **Right Screen:** Zoom/Highlight the Mermaid Diagram in `README.md` | **Architecture & AI Tools:** Multi-source discovery, Gemini Flash reasoning, Gradio UI. |
| **0:50 – 1:20** | **Right Screen:** Switch to `extractor.py` & `app.py` code | **Prompt Engineering & Blockers Solved:** Backtick stripping, 404 fallback, 429 Lite model cascade, and thread decoupling. |
| **1:20 – 1:40** | Webcam / Visual transition | **Background Connection:** BMW Plant Chennai pipeline experience (150,000 files). |
| **1:40 – 2:10** | **Left Screen:** Gradio UI (**Tab 1** demo, then switch to **Tab 2** with 34 Sydney GPs & Audit Log) | **Live Demonstration:** Real-time extraction, CSV export, and failure auditing. |
| **2:10 – 2:25** | Full screen view / GitHub repo | **Closing & ROI:** 95%+ time saved for healthcare operations, closing remarks. |

---

## 🎙️ Verbatim Speaking Script (Read-Along)

### 1. Introduction (0:00 – 0:25)
> "Hello Gokul Infocare hiring team! My name is **Sanjay Mathivanan**. For Task 1 of the AI Growth & Automation Associate practical assessment, I built **MIRA**—an AI-powered data intelligence engine designed to discover, scrape, and structure publicly available directory data for Australian General Practitioners."

### 2. Architecture & AI Tools (0:25 – 0:50)
*(Action: Hover your cursor over the Mermaid Architecture Diagram in `README.md` on the right side of your screen).*
> "As you can see in the architecture diagram, the pipeline has two stages: First, an automated multi-source discovery engine querying OpenStreetMap, Healthdirect, and search APIs. Second, a resilient extraction pipeline using **BeautifulSoup** for anti-bot scraping, **Google Gemini Flash** as the semantic AI extraction engine, and **Gradio with Pandas** for immediate interactive review and CSV export."

### 3. Prompt Engineering & Real Technical Challenges Solved (0:50 – 1:20)
*(Action: Briefly switch to `extractor.py` showing the model cascade and prompt).*
> "I engineered the prompts iteratively across eight stages, solving four real-world engineering hurdles:
> 1. **Markdown Formatting:** Initially, the LLM wrapped JSON in markdown backticks, crashing standard JSON parsers. I refined the system prompt with strict negative constraints and programmatic sanitization.
> 2. **API Model Deprecation (404s):** When older flash checkpoints returned 404s, I engineered an automated multi-model fallback cascade.
> 3. **Rate Limits & High Traffic (429s):** To prevent quota bottlenecks, the cascade automatically falls back to high-throughput Lite models like `gemini-flash-lite-latest`.
> 4. **Gradio Thread Decoupling:** I modularized the extraction engine into `extractor.py` to eliminate circular import deadlocks during background batch execution."

### 4. Background Influence (1:20 – 1:40)
> "My approach was directly influenced by my background automating quality data pipelines at **BMW Plant Chennai**, where I cleaned and validated over 150,000 operational data files. I know firsthand that raw scraped data is useless unless it flows through a resilient, auditable pipeline with strict schema enforcement."

### 5. Live Demonstration (1:40 – 2:10)
*(Action: Focus on the left screen. Show Tab 1 first, then click on Tab 2).*
> "Let’s see the application live:
> - In **Tab 1**, we have the on-demand single clinic extractor strictly fulfilling Task 1. You paste a clinic URL and instantly get structured GP data.
> - But to demonstrate true growth automation, in **Tab 2**, I built **MIRA-Pro**. With one click, it queries regional Australian registries—here for Sydney—and extracts **34 verified General Practitioners** across multiple clinics, capturing their qualifications and consulting hours into a master dataset.
> - Crucially, look at the **Scraping Audit Log**: every single domain is audited. If a clinic's server is down or protected, it is labeled with the exact failure reason rather than silently crashing the batch."

### 6. Closing (2:10 – 2:25)
> "This system eliminates hours of manual data entry for healthcare operations, business development, and market intelligence. All code, prompt histories, and documentation are committed in GitHub and ready for your review. Thank you for your time, and I look forward to joining the Gokul Infocare team!"

---

## 💡 Quick Pre-Recording Checklist
- [ ] Screen resolution set to 1080p (1920x1080).
- [ ] Microphone tested and clear.
- [ ] Both browser (`http://127.0.0.1:7861`) and VS Code open side-by-side.
- [ ] Google Drive video sharing set to **"Anyone with the link can view"** after recording.
