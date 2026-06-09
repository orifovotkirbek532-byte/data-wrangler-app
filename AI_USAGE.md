# 🤖 AI Usage Declaration

**Module:** Data Wrangling and Visualization (5COSC038C)
**Project:** AI-Assisted Data Wrangler & Visualizer

---

## Declaration

This document declares all use of Artificial Intelligence (AI) tools in the development of this coursework project, in accordance with the module guidelines.

AI assistance was used extensively for **code generation and debugging**. All AI-generated code was reviewed, tested, and understood by the student before inclusion. The student is able to explain and defend all submitted code.

---

## AI Tool Used

| Tool | Version | Purpose |
|------|---------|---------|
| Claude (Anthropic) | Claude Sonnet (claude.ai) | Code generation, debugging, dataset generation |

---

## What AI Was Used For

### 1. Application Code (app.py)
AI was used to generate the full Streamlit application code across all four pages:

- **Page A** — File upload logic, session state setup, dataset profiling, summary statistics display
- **Page B** — All 8 cleaning sections: missing value handling, duplicate removal, data type conversion, categorical tools, outlier detection (IQR and Z-score), normalisation/scaling, column operations, and data validation rules
- **Page C** — All 6 chart types using matplotlib: histogram, box plot, scatter plot, line chart, grouped bar chart, and correlation heatmap, including filter logic and aggregation
- **Page D** — Export functionality: CSV download, JSON transformation report, text report generation, before/after comparison table

### 2. Debugging & Error Fixing
AI was used to diagnose and fix errors encountered during development, including:
- Streamlit session state issues
- Google Colab / ngrok tunnel setup and connection errors
- Port binding issues (IPv4 vs IPv6)
- Matplotlib rendering in Streamlit
- pandas type conversion edge cases

### 3. Sample Dataset Generation
AI was used to generate two sample datasets using Python (pandas and numpy):
- `employees.csv` — 1,230 rows, 13 columns, HR data with intentional quality issues
- `sales.csv` — 1,325 rows, 13 columns, sales data with planted outliers and missing values

Code used to generate datasets:
```python
# Generated via AI — datasets created with numpy/pandas
# Intentional issues: ~8% missing values per column, 25-30 duplicate rows,
# planted outliers (e.g. Unit_Price=99999, Customer_Age=150)
```

### 4. Deployment Support
AI was used to provide step-by-step guidance for:
- GitHub repository setup
- Streamlit Cloud deployment configuration
- requirements.txt generation

### 5. Documentation
AI was used to generate:
- This `AI_USAGE.md` file
- `README.md` — project documentation

---

## What AI Was NOT Used For

| Item | Reason |
|------|--------|
| **2-page team report** | Explicitly forbidden by coursework brief — written entirely by the student |
| **Testing and verification** | All testing done manually by the student using the sample datasets |
| **Viva preparation** | Student studied and understood all code independently |
| **Final decisions on app design** | Student made all architectural and UX decisions |

---

## Student Understanding Declaration

Although AI generated the majority of the code, the student:

- Read and understood every function and section of code
- Tested all 8 cleaning features with both sample datasets
- Can explain the logic behind all cleaning operations (IQR, Z-score, ffill, min-max scaling, etc.)
- Can explain Streamlit session state management
- Understands the transformation log structure and how Page D uses it

---

## Sample Prompts Used

Below are representative examples of the types of prompts used with Claude:

> *"Build Page B — Cleaning Studio for my Streamlit app. It needs 8 sections: missing values (fill with mean/median/mode/ffill/bfill or drop), duplicates (detect and remove), data types (convert), categorical tools (trim/case/group rare), outlier detection (IQR and Z-score with cap or remove), normalisation (min-max and z-score), column operations (rename/drop/create), and validation rules (range/category/non-null). Include a transformation log and undo button."*

> *"Fix this error in my Colab cell: FileNotFoundError: cloudflared not found. The tunnel needs to work without needing a login."*

> *"Generate two sample datasets with intentional data quality issues — missing values, duplicates, and outliers — that demonstrate all 8 cleaning features of the app."*

---

## Total AI Assistance Estimate

| Category | AI Involvement |
|----------|---------------|
| Code writing | ~65% |
| Debugging | ~70% |
| Dataset generation | ~50% |
| Documentation | ~60% |
| Testing | 0% |
| 2-page report | 0% |
| Viva preparation | 0% |
