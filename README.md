# 🔍 Contactless Fingerprint Quality Assessment System

## 📌 Overview

This project implements a Computer Vision-based quality assessment pipeline for contactless fingerprint images captured using a mobile camera.

The system evaluates fingerprint image quality before biometric authentication by performing multiple quality checks and generating a composite quality score with PASS/FAIL decisions.

---

## ✨ Features

- Blur Detection using Variance of Laplacian
- Brightness Analysis
- Glare Detection
- ROI (Region of Interest) Completeness
- Ridge Clarity Analysis using Gabor Filter
- Composite Quality Score
- PASS / FAIL Decision
- User Guidance
- Interactive Streamlit Dashboard
- Batch Dataset Evaluation

---

## 🛠️ Technologies Used

- Python
- OpenCV
- NumPy
- Pandas
- Streamlit

---

## 📂 Project Structure

```text
contactless-fingerprint-qc/
│
├── quality_assessment.py
├── quality_app.py
├── test_quality.py
├── test_results.csv
├── requirements.txt
├── README.md
│
├── test_dataset/
│   ├── good/
│   ├── blurry/
│   ├── dark/
│   └── glare/
│
└── screenshots/
```

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/contactless-fingerprint-qc.git

cd contactless-fingerprint-qc

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run quality_app.py
```

---

## 🧪 Batch Testing

```bash
python test_quality.py
```

This generates:


```
test_results.csv
```

---

## 📷 Dashboard

![alt text](<Screenshot/Screenshot 2026-08-04 133451.png>)
![alt text](<Screenshot/Screenshot 2026-08-04 133513.png>)
![alt text](<Screenshot/Screenshot 2026-08-04 133534.png>)
![alt text](<Screenshot/Screenshot 2026-08-04 133615.png>)
---

## 👨‍💻 Author

**Shoaib Mohammed**

GitHub:
https://github.com/mohd-Shoaib-ali/contactless-fingerprint-qc