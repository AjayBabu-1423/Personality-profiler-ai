# 🧠 AI-Based Personality Profiler

An **AI-powered personality prediction web application** built using **Deep Learning and Streamlit**.
This project analyzes user responses to psychological questionnaire statements and predicts their personality type among **16 personality types (MBTI-inspired)**.

The system provides **detailed personality insights, growth suggestions, and interactive confidence visualizations**.

---

# 🚀 Features

✅ AI-based personality prediction using **Deep Learning**
✅ Interactive **questionnaire interface**
✅ Predicts **16 personality types**
✅ Detailed **personality description & growth suggestions**
✅ **Confidence visualization charts** using Plotly
✅ **Multilingual support** (English, Hindi, Tamil)
✅ Personalized greeting with user name
✅ Clean and modern **Streamlit UI**

---

# 🧩 Personality Types Supported

The model predicts the following personality types:

* ISTJ
* ISFJ
* INFJ
* INTJ
* ISTP
* ISFP
* INFP
* INTP
* ESTP
* ESFP
* ENFP
* ENTP
* ESTJ
* ESFJ
* ENFJ
* ENTJ

Each result includes:

* Personality description
* Growth suggestions
* Confidence analysis charts

---

# 🛠️ Tech Stack

| Technology         | Usage                     |
| ------------------ | ------------------------- |
| Python             | Core programming language |
| Streamlit          | Web application framework |
| TensorFlow / Keras | Deep learning model       |
| Pandas             | Data processing           |
| NumPy              | Numerical computation     |
| Plotly             | Data visualization        |
| Scikit-learn       | Data preprocessing        |
| Deep Translator    | Multi-language support    |

---

# 📂 Project Structure

```
personality-profiler-ai/
│
├── app_dl.py                # Main Streamlit application
├── model_dl.keras           # Trained deep learning model
├── scaler.pkl               # Data preprocessing scaler
├── label_encoder.pkl        # Label encoding file
├── features.json            # Feature configuration
├── 16P (2).csv              # Dataset
├── Deep.ipynb               # Model training notebook
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

# 📊 How It Works

1️⃣ User enters their **name and language preference**
2️⃣ The app presents a **series of personality questions**
3️⃣ Each answer is converted into **numerical input values**
4️⃣ The trained **Deep Learning model** predicts the personality type
5️⃣ The app displays:

* Predicted personality type
* Personality description
* Growth suggestions
* Confidence visualization charts

---

# 💻 Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/personality-profiler-ai.git
```

### 2️⃣ Navigate to the project folder

```
cd personality-profiler-ai
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the application

```
streamlit run app_dl.py
```

---

# 📈 Model Information

The personality prediction model was trained using a **Deep Neural Network built with TensorFlow/Keras**.

Input features come from a **psychological questionnaire dataset** inspired by the **16 Personalities personality framework**.

The model predicts probabilities for all personality classes and displays the **confidence distribution**.

---

# 🌍 Multilingual Support

The application supports multiple languages:

* English
* Hindi
* Tamil

Translation is handled using the **Deep Translator API**.

---

# 🎯 Future Improvements

* Add **user personality history tracking**
* Deploy using **Streamlit Cloud**
* Add **more languages**
* Improve model accuracy with larger datasets
* Add **downloadable personality reports**

---

# 👨‍💻 Author

Developed as an **AI / Machine Learning project** for personality prediction using deep learning.

---

# ⭐ Support

If you found this project useful, please consider **starring ⭐ the repository** on GitHub.
