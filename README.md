

# 🏥 Surgical Site Infection (SSI) Predictor App

An AI-powered web application that predicts the risk of **Surgical Site Infections (SSI)** based on patient and surgical data. Designed to assist clinicians and researchers in identifying high-risk cases early, enabling timely interventions and improved patient outcomes.

---

## 🔍 Overview

The **SSI Predictor App** leverages a trained machine learning model (e.g., SVM, Random Forest) to assess the likelihood of infection after surgery. It provides:

* 📊 Real-time predictions with probability scores
* 📈 Visual analytics for comparison and insights
* 🧪 Support for historical data and new patient inputs
* 🌐 Web-based frontend for easy access

---

## 🎯 Key Features

* ✅ Upload patient data via form or CSV
* 🧠 Backend ML model for SSI risk prediction
* 🔢 Displays prediction score and infection risk category (e.g., Low/Moderate/High)
* 📊 Graphs showing feature importance or comparison with similar cases
* 🗂️ Optional: save predictions to local/remote database

---

## 🛠️ Tech Stack

| Layer      | Technology                           |
| ---------- | ------------------------------------ |
| Frontend   | React / Streamlit (optional)         |
| Backend    | Django / Flask / FastAPI             |
| ML Model   | Scikit-learn  |
| Data       | Custom healthcare dataset (CSV)      |
| Deployment | Streamlit Share / Localhost |

---

## 📁 Project Structure

```
SSI_Predictor_App/
├── backend/
│   ├── model/
│   │   ├── ssi_model.pkl
│   │   └── scaler.pkl
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── frontend/
│   └── (React or Streamlit code)
├── media/
│   └── graphs/
├── templates/
│   └── index.html
├── static/
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SurgicalSiteInfection-SSI--Predictor-App.git
cd SurgicalSiteInfection-SSI--Predictor-App
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend Server

```bash
python manage.py runserver
```

### 4. Open Frontend (if React):

```bash
cd frontend
npm install
npm start
```

Or if using **Streamlit**:

```bash
streamlit run app.py
```

---

## 🧪 Model Input

Typical features may include:

* Patient Age, BMI
* Duration of Surgery
* Wound Class
* ASA Score
* Diabetes, Hypertension
* Antibiotic Usage

> ⚠️ Ensure input format matches the training dataset schema.

---

## 📊 Output

* ✅ **Prediction**: "Infection" or "No Infection"
* 🔢 **Probability**: e.g., 78.5% risk
* 🟠 **Risk Level**: Low / Moderate / High
* 📈 **Graphs**: (e.g., Feature Comparison, Risk Heatmap)

---

## 📦 Dataset Used

A cumulative, anonymized dataset derived from clinical records and surgical outcomes, labeled with SSI outcomes. Stored as:

```
/datasets/Shuffled_Cumulative_Dataset.csv
```

---

## 🔐 Ethics & Privacy

* 🔒 All patient data is anonymized.
* 📜 Model is for **research and educational purposes only**.
* ❌ Not intended for real-world diagnosis or clinical decision-making.

---

## 🧠 Future Enhancements

* ⏱️ Add time-based risk estimations (e.g., day-wise post-op infection probability)
* 🧬 Add additional clinical features (e.g., CRP levels, blood counts)
* 📱 Mobile-responsive version
* 🧑‍⚕️ Doctor/Patient dashboards


---

## 📄 License

MIT License.
For academic, non-commercial use only.


