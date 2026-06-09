# 🧹 AI-Assisted Data Wrangler & Visualizer

A multi-page interactive data wrangling and visualization tool built with Python and Streamlit. Upload any CSV, Excel, or JSON dataset, clean it interactively, visualize it with 6 chart types, and export a transformation report.

**Live App:** [https://fh9fygquxhmk9bsjqc8aqq.streamlit.app](https://fh9fygquxhmk9bsjqc8aqq.streamlit.app)

---

## 📋 Module Information

- **Module:** Data Wrangling and Visualization (5COSC038C)
- **University:** Westminster International University in Tashkent (WIUT)
- **Academic Year:** 2025–26

---

## 🚀 Features

### 📂 Page A — Upload & Overview
- Upload CSV, Excel (.xlsx), or JSON files
- Instant dataset profiling: rows, columns, missing cells, duplicates
- Column names and inferred data types
- Summary statistics for numeric and categorical columns
- Missing values breakdown by column
- Interactive data preview with adjustable row count
- Session reset button

### 🔧 Page B — Cleaning Studio
8 interactive cleaning tools:
1. **Missing Values** — fill with mean/median/mode/ffill/bfill or drop rows/columns
2. **Duplicate Rows** — detect and remove duplicates (keep first/last/none)
3. **Data Types** — convert columns to numeric, text, datetime, or category
4. **Categorical Tools** — trim spaces, fix case, group rare categories, replace values
5. **Outlier Detection** — IQR and Z-score methods with cap or remove options
6. **Normalisation & Scaling** — Min-Max (0–1) and Z-Score (mean=0, std=1)
7. **Column Operations** — rename, drop, create via formula or binning
8. **Data Validation** — range checks, allowed category checks, non-null checks

Additional features:
- ↩️ Undo last step
- 📋 Transformation log recorded automatically

### 📊 Page C — Visualization Builder
6 chart types powered by **matplotlib**:
- 📊 Histogram
- 📦 Box Plot
- 🔵 Scatter Plot (with optional colour-by-category)
- 📈 Line Chart (with aggregation options)
- 📊 Grouped Bar Chart (with Mean/Sum/Count/Median)
- 🌡️ Correlation Heatmap

Filters:
- Filter by category column
- Filter by numeric range

### 📤 Page D — Export & Report
- Before vs After cleaning comparison
- Full transformation log display
- Download cleaned dataset as **CSV**
- Download transformation log as **JSON**
- Download human-readable **TXT report**
- Column-by-column missing value improvement table

---

## 📦 Project Structure

```
data-wrangler-app/
│
├── app.py                  # Main Streamlit application (all 4 pages)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── AI_USAGE.md             # AI usage declaration
│
└── sample_data/
    ├── employees.csv       # HR dataset (1,230 rows, 13 columns)
    └── sales.csv           # Sales dataset (1,325 rows, 13 columns)
```

---

## ⚙️ Installation & Running Locally

### Prerequisites
- Python 3.9 or higher
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/orifovotkirbek532-byte/data-wrangler-app.git
cd data-wrangler-app
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔬 Running in Google Colab

```python
# Cell 1 — Install
!pip install streamlit pyngrok scipy openpyxl -q

# Cell 2 — Write app.py (paste full app code)
%%writefile app.py
# ... paste app code here ...

# Cell 3 — Launch with tunnel
import subprocess, time, sys
from pyngrok import ngrok
subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py",
                  "--server.port=8501", "--server.headless=true"])
time.sleep(5)
url = ngrok.connect(8501)
print(f"App URL: {url}")
```

---

## 📊 Sample Datasets

Two datasets are included in the `sample_data/` folder:

| Dataset | Rows | Columns | Key Features |
|---------|------|---------|-------------|
| `employees.csv` | 1,230 | 13 | HR data with missing values, duplicates, mixed types |
| `sales.csv` | 1,325 | 13 | Sales data with outliers, missing values, datetime column |

Both datasets were generated with intentional data quality issues (missing values ~7–8%, 25–30 duplicate rows, planted outliers) to demonstrate all cleaning features.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3.12 | Core language |
| Streamlit 1.28+ | Web application framework |
| Pandas 2.0+ | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Chart rendering |
| SciPy | Z-score outlier detection |
| OpenPyXL | Excel file support |

---

## 📝 License

This project was created for academic purposes as part of the 5COSC038C coursework at WIUT.
