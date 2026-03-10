
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
from deep_translator import GoogleTranslator

# ==== Background Function ====
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        /* ======== General Background ======== */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            height: 100vh;
            color: white;
            font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}

        /* ======== Frosted Glass Main Area ======== */
        div[data-testid="stVerticalBlock"] {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 18px;
            padding: 30px 40px;
            margin: 30px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }}

        /* ======== Sidebar Styling ======== */
        section[data-testid="stSidebar"] {{
            background-color: rgba(0, 0, 0, 0.85) !important;
            color: white !important;
            border-right: 2px solid #444;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.4);
        }}
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] label {{
            color: #f5f5f5 !important;
        }}

        /* Sidebar Inputs */
        .stSidebar input, 
        .stSidebar select, 
        .stSidebar textarea, 
        .stSidebar .stTextInput>div>input {{
            color: white !important;
            background-color: #333 !important;
            border: 1px solid #666 !important;
            border-radius: 8px !important;
            padding: 6px 10px;
        }}
        [data-baseweb="input"] input {{
            color: white !important;
            background-color: #333 !important;
        }}
        [data-baseweb="select"] div[role="button"] span {{
            color: white !important;
        }}

        /* ======== Headings & Text ======== */
        h1, h2, h3, h4, h5, h6, p, label, div, span {{
            color: white !important;
        }}

        /* ======== Buttons ======== */
        .stButton > button {{
            background: linear-gradient(90deg, #4CAF50, #2E8B57);
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: all 0.3s ease-in-out;
        }}
        .stButton > button:hover {{
            background: linear-gradient(90deg, #2E8B57, #4CAF50);
            transform: scale(1.05);
            box-shadow: 0 6px 14px rgba(0,0,0,0.4);
        }}

        /* ======== Personality Card ======== */
        .personality-card {{
            padding: 25px; 
            border-radius: 18px; 
            text-align: center; 
            box-shadow: 0px 4px 18px rgba(0,0,0,0.4);
            backdrop-filter: blur(8px);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .personality-card:hover {{
            transform: scale(1.03);
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        }}

        /* ======== Growth Section ======== */
        .growth-card {{
            background-color: rgba(255,255,255,0.15); 
            padding: 15px; 
            border-radius: 12px;
            box-shadow: inset 0 0 10px rgba(255,255,255,0.2);
            backdrop-filter: blur(6px);
        }}

        /* ======== Divider & Titles ======== */
        hr {{
            border: 1px solid rgba(255,255,255,0.3);
        }}
        .stMarkdown h2, .stMarkdown h3 {{
            text-shadow: 0px 0px 8px rgba(255,255,255,0.4);
        }}

        /* ======== Question Section ======== */
        div[data-testid="stRadio"] label {{
            background-color: rgba(255,255,255,0.15);
            padding: 6px 10px;
            border-radius: 8px;
            margin: 3px 0;
            transition: all 0.2s ease-in-out;
        }}
        div[data-testid="stRadio"] label:hover {{
            background-color: rgba(255,255,255,0.25);
            transform: scale(1.02);
        }}

        /* ======== Chart Box Enhancements ======== */
        .stPlotlyChart {{
            background-color: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 12px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.4);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ==== Add Background ====
#add_bg_from_local("Image.png")

# ==== 🌐 Multi-language & Personalization System ====
st.sidebar.markdown("### 👤 Personalization Settings")
user_name = st.sidebar.text_input("Enter your name:", "")
if user_name:
    st.session_state["user_name"] = user_name

lang_choice = st.sidebar.selectbox("🌍 Choose Language", ["English", "Hindi", "Tamil"], index=0)
st.session_state["lang"] = lang_choice

translations = {
    "English": {"welcome": "Welcome to the AI-based Personality Profiler!", "start": "Let's get started!", "question": "Question", "growth": "🌱 Areas of Growth", "analysis": "🎉 Your Personality Analysis", "restart": "🔄 Restart Test", "greeting": "Hello"},
    "Hindi": {"welcome": "एआई आधारित व्यक्तित्व प्रोफाइलर में आपका स्वागत है!", "start": "चलिए शुरू करते हैं!", "question": "प्रश्न", "growth": "🌱 विकास के क्षेत्र", "analysis": "🎉 आपका व्यक्तित्व विश्लेषण", "restart": "🔄 परीक्षण पुनः प्रारंभ करें", "greeting": "नमस्ते"},
    "Tamil": {"welcome": "ஏஐ அடிப்படையிலான நபர் பகுப்பாய்வுக்கு வரவேற்கிறோம்!", "start": "தொடங்கலாம்!", "question": "கேள்வி", "growth": "🌱 வளர்ச்சிக்கான பகுதி", "analysis": "🎉 உங்கள் நபர் பகுப்பாய்வு", "restart": "🔄 சோதனையை மறுதொடக்கம் செய்", "greeting": "வணக்கம்"}
}

def t(key):
    lang = st.session_state.get("lang", "English")
    return translations.get(lang, translations["English"]).get(key, key)

def translate_text(text):
    lang = st.session_state.get("lang", "English")
    if lang == "English" or not text:
        return text
    lang_code = {"Hindi": "hi", "Tamil": "ta"}.get(lang, "en")
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except Exception:
        return text

# ==== Personality Data ====
personality_info = {
    "ISTP": {
        "desc": (
            "You are practical, action-oriented, and thrive when solving real-world problems. "
            "Your calm, logical nature allows you to approach challenges without panic. "
            "You enjoy experimenting, building, and understanding how things function. "
            "Freedom is essential for you — structure feels limiting. "
            "You dislike overthinking and prefer learning by doing. "
            "People admire your adaptability and quiet confidence under pressure. "
            "Your curiosity drives you to master tools, systems, or crafts. "
            "You enjoy working independently, trusting your own methods. "
            "You find satisfaction in efficiency and tangible results. "
            "You approach life like a puzzle — best solved through direct experience."
        ),
        "growth": (
            "To grow, try opening up emotionally with trusted people. "
            "Practice expressing thoughts instead of keeping them internal. "
            "Plan ahead sometimes rather than always acting on impulse. "
            "Seek teamwork opportunities that challenge your independence. "
            "Remember, sharing your ideas can inspire others and strengthen bonds."
        ),
        "color": "#A2D2FF", "emoji": "🔧", "motto": "The Skilled Problem-Solver"
    },
    "ESTP": {
        "desc": (
            "You are energetic, bold, and thrive in fast-moving environments. "
            "Quick thinking and adaptability make you excel under pressure. "
            "You embrace risks and are always ready for spontaneous adventures. "
            "Challenges excite you — the bigger, the better. "
            "You inspire others through your confidence and fearless optimism. "
            "Your communication style is direct, honest, and full of charisma. "
            "You dislike routine and seek new experiences that stimulate you. "
            "You enjoy competition and often motivate others to perform their best. "
            "Your presence brings life and excitement to any situation. "
            "You’re happiest when life feels like an adventure to conquer."
        ),
        "growth": (
            "To develop, practice patience and think beyond immediate rewards. "
            "Reflect on long-term consequences before acting impulsively. "
            "Cultivate listening skills to strengthen empathy and relationships. "
            "Challenge yourself to finish what you start, even when it gets boring. "
            "Balance thrill-seeking with moments of mindfulness and calm."
        ),
        "color": "#FFC8DD", "emoji": "⚡", "motto": "The Energetic Adventurer"
    },
    "INTP": {
        "desc": (
            "You are analytical, curious, and driven by a hunger to understand. "
            "Abstract theories and complex systems fascinate your sharp mind. "
            "You prefer independence and intellectual freedom over conformity. "
            "Your creativity and logic blend beautifully in problem-solving. "
            "You constantly question how and why things work. "
            "You enjoy deep conversations that challenge assumptions. "
            "Although reserved, your insights can transform how others think. "
            "You dislike routine, preferring flexibility and autonomy. "
            "Your calm detachment helps you see issues objectively. "
            "You are a lifelong learner, always evolving your perspectives."
        ),
        "growth": (
            "Growth comes from applying your ideas, not just theorizing them. "
            "Work on expressing emotions openly to connect with others. "
            "Avoid perfectionism — completion matters more than flawless logic. "
            "Engage socially to balance isolation with collaboration. "
            "Learn to trust intuition alongside analysis when making decisions."
        ),
        "color": "#BDE0FE", "emoji": "🧠", "motto": "The Logical Thinker"
    },
    "ENFJ": {
        "desc": (
            "You are charismatic, empathetic, and deeply attuned to others’ emotions. "
            "Leadership comes naturally — you inspire trust and motivation. "
            "You have a strong vision for human potential and personal growth. "
            "You thrive when helping others discover their purpose. "
            "Your warmth allows you to connect across personalities and cultures. "
            "You value harmony, collaboration, and shared success. "
            "You often anticipate needs before others even express them. "
            "Your confidence and compassion make you a respected leader. "
            "You radiate positivity and bring unity to diverse groups. "
            "You believe that people, when supported, can achieve greatness."
        ),
        "growth": (
            "To grow, learn to set boundaries without guilt. "
            "Remember that saying 'no' can be healthy and empowering. "
            "Take time for self-reflection instead of always helping others. "
            "Accept that not everyone will share your enthusiasm or pace. "
            "Balance giving with receiving — your well-being matters too."
        ),
        "color": "#FFD6A5", "emoji": "🤝", "motto": "The Inspiring Leader"
    },
    "ISTJ": {
        "desc": (
            "You are reliable, organized, and grounded in practical thinking. "
            "Your methodical nature ensures accuracy and consistency. "
            "Tradition and duty are values you deeply respect. "
            "You prefer structure, rules, and clear expectations in work and life. "
            "Your focus on responsibility makes you a trusted figure. "
            "You excel in roles that require precision and order. "
            "You find comfort in stability and long-term planning. "
            "You hold yourself and others to high ethical standards. "
            "You believe actions should match words and promises. "
            "You bring dependability and discipline wherever you go."
        ),
        "growth": (
            "Growth comes from embracing flexibility and new experiences. "
            "Try not to fear change — it can bring new opportunities. "
            "Be open to emotional expression, not just duty or logic. "
            "Allow space for creativity even if it feels uncertain. "
            "Remember, perfection isn’t always necessary for success."
        ),
        "color": "#CDB4DB", "emoji": "📜", "motto": "The Reliable Planner"
    },
    "ISFJ": {
        "desc": (
            "You are nurturing, loyal, and devoted to caring for others. "
            "Your empathy helps you create harmony and emotional safety. "
            "You take pride in being dependable and thoughtful. "
            "You work quietly behind the scenes to maintain balance. "
            "Your actions are guided by compassion and moral values. "
            "You value long-term relationships and deep trust. "
            "You prefer stability and dislike unnecessary conflict. "
            "You often notice details that others overlook. "
            "Your kindness has a powerful, lasting impact on people. "
            "You embody quiet strength and unwavering support."
        ),
        "growth": (
            "To grow, learn to prioritize your own needs sometimes. "
            "Avoid overcommitting to please everyone around you. "
            "Speak up when you disagree — your voice has value. "
            "Accept that not every act of care must be perfect. "
            "Allow yourself to rest; self-care is not selfish."
        ),
        "color": "#E2F0CB", "emoji": "🌿", "motto": "The Nurturing Protector"
    },
    "INFJ": {
        "desc": (
            "You are visionary, empathetic, and deeply introspective. "
            "You often see meaning and purpose where others see routine. "
            "You seek harmony and authenticity in relationships. "
            "Your insights into human nature are profound and compassionate. "
            "You value integrity and personal growth above all else. "
            "You often feel called to help or inspire others meaningfully. "
            "Your imagination fuels creativity and idealistic thinking. "
            "Though private, your connections run deep and sincere. "
            "You see potential for goodness even in difficulty. "
            "You dream not just for yourself but for the world’s healing."
        ),
        "growth": (
            "Growth means expressing your needs without fear of burdening others. "
            "Learn to stay grounded and not idealize every situation. "
            "Balance empathy with realism to avoid emotional exhaustion. "
            "Seek collaboration instead of carrying others’ pain alone. "
            "Remember, small acts can create big impact too."
        ),
        "color": "#FDE2E4", "emoji": "🌌", "motto": "The Visionary"
    },
    "INTJ": {
        "desc": (
            "You are strategic, analytical, and driven by long-term vision. "
            "You naturally see patterns and systems in complex ideas. "
            "Efficiency and innovation define your approach to life. "
            "You are independent, preferring logic over emotion. "
            "Your confidence and foresight make you a powerful leader. "
            "You pursue goals with determination and focus. "
            "You are future-oriented, always planning ahead. "
            "You value competence and expect high standards. "
            "You thrive in solving problems others find overwhelming. "
            "You aim not just for success but for lasting impact."
        ),
        "growth": (
            "To grow, remember that emotional intelligence enhances strategy. "
            "Seek feedback and remain open to alternative viewpoints. "
            "Allow imperfection — progress often beats precision. "
            "Invest in relationships, not just achievements. "
            "Balance ambition with patience and empathy."
        ),
        "color": "#FFB5A7", "emoji": "🎯", "motto": "The Strategic Mastermind"
    },
    "ISFP": {
        "desc": (
            "You are gentle, artistic, and guided by your personal values. "
            "You appreciate beauty in all forms — art, nature, and people. "
            "You prefer harmony over conflict and peace over control. "
            "Your empathy helps you connect deeply with emotions. "
            "You live in the present, valuing authenticity over ambition. "
            "You express yourself creatively through subtle forms. "
            "You are flexible and open-minded about how life unfolds. "
            "You often uplift others through quiet kindness. "
            "You find meaning in simple, heartfelt moments. "
            "You radiate calm and bring warmth wherever you go."
        ),
        "growth": (
            "To develop, try confronting issues instead of avoiding discomfort. "
            "Push yourself to plan for the future when needed. "
            "Share your creative vision confidently with others. "
            "Avoid over-adapting just to maintain peace. "
            "Remember, your voice deserves to be heard too."
        ),
        "color": "#D8F3DC", "emoji": "🎨", "motto": "The Gentle Creator"
    },
    "ESFP": {
        "desc": (
            "You are lively, spontaneous, and full of enthusiasm for life. "
            "You thrive on excitement and human connection. "
            "You bring positivity and laughter wherever you go. "
            "Your empathy makes you naturally in tune with others’ feelings. "
            "You dislike monotony and seek adventure in every form. "
            "You are expressive, warm, and effortlessly social. "
            "You adapt quickly to changing environments. "
            "You find beauty in everyday experiences. "
            "You prefer living in the moment rather than planning ahead. "
            "Your joy and energy make you unforgettable to those around you."
        ),
        "growth": (
            "To grow, learn to slow down and reflect before acting. "
            "Build consistency to achieve long-term success. "
            "Practice patience when situations lack excitement. "
            "Develop self-discipline without losing your spark. "
            "Balance fun with focus to unlock your full potential."
        ),
        "color": "#FFD6E0", "emoji": "🎉", "motto": "The Fun-Loving Performer"
    },
    "INFP": {
        "desc": (
            "You are idealistic, creative, and guided by strong inner values. "
            "You dream of a world built on kindness and authenticity. "
            "You seek meaning in everything you do. "
            "Your empathy and imagination make you deeply compassionate. "
            "You often express yourself through writing, art, or storytelling. "
            "You prefer depth over superficial connections. "
            "You believe in staying true to your morals, even when it’s hard. "
            "You are introspective and sensitive to emotional nuance. "
            "Your creativity thrives when fueled by passion. "
            "You aim to live a life that aligns with your personal truth."
        ),
        "growth": (
            "Growth comes from acting on your ideals, not just imagining them. "
            "Set practical goals that align with your values. "
            "Avoid self-criticism — imperfection is part of growth. "
            "Learn to assert boundaries to protect your energy. "
            "Balance dreaming with doing to make your vision real."
        ),
        "color": "#E0BBE4", "emoji": "🌸", "motto": "The Gentle Idealist"
    },
    "ENFP": {
        "desc": (
            "You are enthusiastic, imaginative, and full of curiosity. "
            "You see potential and beauty in every possibility. "
            "You love meeting people and sharing new ideas. "
            "Your optimism inspires those around you to dream bigger. "
            "You dislike routine, preferring freedom and variety. "
            "Your creativity shines through conversation and expression. "
            "You are adaptable and open to change. "
            "You seek deep emotional and intellectual connections. "
            "You value authenticity and individuality. "
            "You thrive when exploring, learning, and inspiring others."
        ),
        "growth": (
            "To grow, learn to focus on completion as much as creation. "
            "Ground your energy by organizing thoughts into actions. "
            "Avoid overcommitting to too many new ideas. "
            "Practice patience when enthusiasm fades. "
            "Embrace consistency as a tool for true freedom."
        ),
        "color": "#FFDEB4", "emoji": "🚀", "motto": "The Free-Spirited Inspirer"
    },
    "ESTJ": {
        "desc": (
            "You are practical, efficient, and naturally take charge of situations. "
            "Structure and organization make you feel confident. "
            "You believe in clear rules and measurable results. "
            "You are dependable, hardworking, and results-driven. "
            "Your leadership style is decisive and focused. "
            "You bring order and stability to any group or project. "
            "Tradition and loyalty hold deep meaning for you. "
            "You are direct in communication and value honesty. "
            "You excel in roles that demand accountability. "
            "You lead with purpose and inspire through action."
        ),
        "growth": (
            "To develop, learn to stay open to unconventional ideas. "
            "Practice flexibility instead of strict control. "
            "Cultivate empathy when leading diverse teams. "
            "Balance efficiency with emotional awareness. "
            "Allow others to contribute creatively to shared goals."
        ),
        "color": "#B5E48C", "emoji": "🏛️", "motto": "The Organized Leader"
    },
    "ESFJ": {
        "desc": (
            "You are caring, social, and value strong community ties. "
            "You find joy in helping and supporting others. "
            "Harmony and kindness define your interactions. "
            "You are reliable, attentive, and socially aware. "
            "You often create a warm and welcoming environment. "
            "You respect structure and appreciate clear expectations. "
            "Your generosity builds loyalty and friendship. "
            "You prefer teamwork over solitude. "
            "You seek balance between tradition and progress. "
            "Your positivity brightens the lives of those around you."
        ),
        "growth": (
            "Growth means setting personal boundaries when needed. "
            "Avoid overextending yourself to please everyone. "
            "Embrace change even when it disrupts comfort. "
            "Learn to prioritize your needs alongside others’. "
            "Let go of judgment — kindness includes self-compassion."
        ),
        "color": "#FEC5BB", "emoji": "💐", "motto": "The Caring Supporter"
    },
    "ENTP": {
        "desc": (
            "You are inventive, clever, and love exploring new ideas. "
            "You enjoy debates that challenge the status quo. "
            "Your energy and creativity make you a natural innovator. "
            "You adapt easily to change and love experimenting. "
            "You thrive on brainstorming and seeing new possibilities. "
            "Your quick wit keeps conversations stimulating. "
            "You dislike repetitive tasks and restrictive environments. "
            "You value freedom and exploration of unconventional thinking. "
            "You are visionary, often predicting trends before others. "
            "You see every challenge as a chance to innovate and grow."
        ),
        "growth": (
            "To grow, practice following through on your brilliant ideas. "
            "Focus on one project long enough to see results. "
            "Develop active listening to build deeper connections. "
            "Learn to appreciate stability, not just novelty. "
            "Use your creativity for long-term, meaningful impact."
        ),
        "color": "#A5FFD6", "emoji": "💡", "motto": "The Clever Innovator"
    },
    "ENTJ": {
        "desc": (
            "You are bold, decisive, and naturally take the lead. "
            "You have strong strategic thinking and organizational skills. "
            "You aim high and inspire others to follow your vision. "
            "Efficiency and achievement motivate your every move. "
            "You thrive in challenges that demand intellect and leadership. "
            "You are confident and assertive in communication. "
            "You respect competence and value direct honesty. "
            "Your ability to see long-term goals makes you unstoppable. "
            "You bring order to chaos through discipline and focus. "
            "You lead not just to win, but to create lasting success."
        ),
        "growth": (
            "To grow, practice empathy and listen without controlling. "
            "Value emotions as much as logic in decision-making. "
            "Delegate tasks to empower others, not just manage them. "
            "Accept vulnerability as a form of strength. "
            "Remember, true leadership inspires, not commands."
        ),
        "color": "#FFA69E", "emoji": "🏆", "motto": "The Bold Commander"
    }
}


# ==== Load Data & Model ====
DATA_PATH = "16P (2).csv"
MODEL_PATH = "model_dl.keras"

df = pd.read_csv(DATA_PATH, encoding="latin1")
model = load_model(MODEL_PATH)


# ==== Prepare Questions ====
question_columns = [col for col in df.columns if col not in ["Response Id", "Personality"]]
num_questions = len(question_columns)

# ==== Session State ====
if "answers" not in st.session_state:
    st.session_state.answers = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# ==== Header ====
st.title("🧩 " + t("welcome"))
if "user_name" in st.session_state and st.session_state["user_name"]:
    st.markdown(f"{t('greeting')} **{st.session_state['user_name']}!**")

st.markdown(
    f"{t('start')}\n"
    "Answer each question honestly, and at the end, you'll discover your *personality type* "
    "with a detailed description and insightful graphs."
)
st.write("---")

# ==== Question or Results ====
current_index = st.session_state.question_index

if current_index < num_questions:
    question = question_columns[current_index]
    st.markdown(f"### {t('question')} {current_index + 1} of {num_questions}")
    st.write(f"{question}")

    options = {
        "Strongly Disagree": -3,
        "Disagree": -2,
        "Slightly Disagree": -1,
        "Neutral": 0,
        "Slightly Agree": 1,
        "Agree": 2,
        "Strongly Agree": 3
    }

    answer_label = st.radio("Choose your answer:", options=list(options.keys()))
    answer_value = options[answer_label]

    if st.button("Next ➡"):
        st.session_state.answers.append(answer_value)
        st.session_state.question_index += 1
        st.rerun()

else:
    st.subheader(t("analysis"))
    st.write("Based on your responses, here’s your personality type and confidence analysis:")

    input_data = pd.DataFrame([st.session_state.answers], columns=question_columns)
    prediction = model.predict(input_data)
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    labels = df["Personality"].unique()
    predicted_label = labels[predicted_class_index]

    info = personality_info.get(predicted_label, {})

    desc = translate_text(info.get("desc", "Description not available."))
    growth = translate_text(info.get("growth", ""))
    color = info.get("color", "#FFFFFF")
    emoji = info.get("emoji", "")
    motto = info.get("motto", "")

    # ==== Personality Card ====
    st.markdown(
        f"""
        <div class="personality-card" style="background-color:{color};">
            <h2 style="margin-bottom:5px;">{emoji} <b>{predicted_label}</b></h2>
            <h4 style="margin-top:0; color:gray;">{motto}</h4>
            <p style="font-size:16px; text-align:justify;">{desc}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==== Charts ====
    scores = prediction[0]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=scores, theta=labels, fill='toself', name='Prediction Confidence'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False,
                      title="📊 Personality Confidence Chart")
    st.plotly_chart(fig)

    bar_df = pd.DataFrame({"Personality": labels, "Confidence": scores})
    fig_bar = px.bar(
        bar_df.sort_values("Confidence", ascending=True),
        x="Confidence", y="Personality",
        orientation='h',
        title="📈 Confidence Levels for Each Personality Type",
        color="Confidence", color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_bar)

    # ==== Growth Section ====
    st.markdown("### " + t("growth"))
    if growth:
        st.markdown(f"<div class='growth-card'><p style='font-size:16px; text-align:justify;'>{growth}</p></div>", unsafe_allow_html=True)
    else:
        st.markdown("_No growth suggestions available for this type yet._")

    # Restart
    if st.button(t("restart")):
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.rerun()
