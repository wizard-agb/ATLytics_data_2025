# 📊 Data for Hope Workforce Development Dashboard

<div align="center">
  <img src="https://atlytics.org/wp-content/uploads/2021/06/ATLytiCS-logo-2a.jpg" alt="Logo" style="height: 100px;">
</div>

This Streamlit dashboard provides insights into workforce development efforts by visualizing employment trends, wage growth, and industry representation. It’s designed to support organizations that facilitate workforce readiness and economic opportunity.

---

## 🚀 Getting Started

These instructions will get the dashboard running on your local machine for development and testing purposes.

### 🔧 Prerequisites

Make sure you have the following installed:

- Python 3.8+
- pip (Python package manager)

### 📦 Install Dependencies

Clone the repo and install required packages:

```bash
git clone https://github.com/your-username/data-for-hope-dashboard.git
cd data-for-hope-dashboard
pip install -r requirements.txt
```

### ▶️ Run the Dashboard

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### 📁 Relevant Files Explained
`data_processing_final.py`

This is the file for all data engineering tasks. 

`reference_data/`

This contains all lookup values and relevant information for data dictionaries. 

`dashboard_data/`

This is the output directory where dashboard data sets live. 

# Core Competition Data

## Georgia Individual Performance Records
Annual data from individuals in workforce development programs is shared for the public in an anonymized format on the [DOL website](https://www.dol.gov/agencies/eta/performance/results-archive?#individual-performance). This file is a subset that includes only Georgia and limits the fields to make it more accessible.

- **Georgia Dataset:** [Google Drive](https://drive.google.com/file/d/1IGcXqktP1oTBUROGzf376VtuDZvbPRNo/view?usp=drive_link)
- **File with details on anonymization and the agreement of fair use:** [Google Drive](https://drive.google.com/file/d/1i_1bkTp5P6vkxASANezQkChRhfJq9kYA/view?usp=drive_link)
- **Table with readable names for the subset of variables in this dataset:** [Google Drive](https://drive.google.com/file/d/1IavSQrqTyphSjqKVMtNkQ5expM5E0bw_/view?usp=drive_link)
  - These are volunteer-created; please check with the full dictionary below for exact meaning, type, and values.
  - Calculated variable names have not been changed but are explained in the file below.
- **Full data dictionary with explanations of all variables in the original dataset:** [Google Drive](https://drive.google.com/file/d/1wWhdtcFGJkTRUiWrS5snZR74kvoXmbLG/view?usp=drive_link)
  - Before combining or creating binary variables from categorical data, please check `CALC4000 - CALC4041`. The typical recoding has already been provided in these variables.

## American Community Survey Georgia County Data
Some ACS data for Georgia counties relevant to workforce or demographics:

- [Google Drive](https://drive.google.com/drive/folders/1-7TSqlNID8pgUci5DkHNmxC8vpU4Sp0m?usp=drive_link)
- **Full ACS data is available:** [Weblink](https://www.census.gov/programs-surveys/acs/data.html)

---

# Additional Data


## WIOA Individual Performance Records Data from the US DOL
Annual data from individuals in workforce development programs is shared for the public in an anonymized format on the DOL website. These public use files contain over 20 million records. The core Georgia Individual data is just a subset of this file.

- **Full data file:**
  - **For 2022, the most recent available:** [Weblink](https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2022/WIOAPerformanceRecords_PY2022Q4_Public_csv.gz) 
- **An explanation of what is removed for anonymization and the agreement for fair use is listed with each year:**
  - **For 2022:** [Weblink](https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2022/WIOA%20Performance%20Records%20Public%20Use%20File%20Disclaimer_PY2022.pdf)
- **A detailed description of all of the fields is in the Public Use File Record Layout:**
  - **For 2022:** [Weblink](https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2022/WIOA%20Performance%20Records%20Public%20Use%20File%20Record%20Layout%20PY2022Q4.pdf) 
- **Additional Information on the files is in the appendices:**
  - **Appendix B:** [Weblink](https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2022/WIOA%20Performance%20Records%20Public%20Use%20File%20Record%20Layout%20PY2022Q4%20Appendix%20B.xlsx)
  - **Appendix C:** [Weblink](https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/PY2022/WIOA%20Performance%20Records%20Public%20Use%20File%20Record%20Layout%20PY2022Q4%20Appendix%20C.xlsx) | [Google Drive](#)
- **A table that provides ETA codes for each LWDA for column `PIRL108` can be found at the bottom of [this page] () in the dropdown labeled "Workforce Development Boards (WDB) Reporting Codes":**
  - **For 2022:** [Weblink](https://www.dol.gov/agencies/eta/performance/wips)

---

### 📝 License
This project is open-source and available under the MIT License.
