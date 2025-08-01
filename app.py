import streamlit as st
from deep_translator import GoogleTranslator
import openai

# Set up page configuration
st.set_page_config(
    page_title="Swarajya Scanner - Vernacular Rights Q&A",
    page_icon="📜",
    layout="wide"
)

# Custom CSS for enhanced look and feel
st.markdown("""
<style>
body {
    background-color: #f4f4f9;
    color: #333;
}
h1, h3 {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-align: center;
}
h1 {
    color: #0050b3;
    font-weight: 700;
}
h3 {
    color: #0073e6;
    font-style: italic;
}
.stButton > button {
    background-color: #0073e6;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #0050b3;
}
</style>
""", unsafe_allow_html=True)

# Language dictionary with translations
content = {
    "English": {
        "title": "Welcome to Swarajya Scanner! 📜",
        "tagline": "Give every citizen a Constitution in their pocket, and the guts to use it.",
        "intro": "Swarajya Scanner empowers you with knowledge of your constitutional rights in your vernacular language. Ask questions, get answers, and defend your rights with confidence.",
        "get_started": "Get Started",
        "how_it_works": "How It Works",
        "contact_us": "Contact Us",
        "features_title": "Key Features",
        "features": [
            "📚 Multilingual Q&A: Get answers in your local language.",
            "🛡 Rights Defense: Equip yourself with constitutional knowledge.",
            "🔍 Easy Search: Find answers quickly and easily.",
            "🤝 Community Support: Connect with others defending their rights.",
            "🔔 Notifications: Stay updated with relevant rights alerts."
        ],
        "footer": "© 2025 Swarajya Scanner. All rights reserved."
    },
    "తెలుగు": {
        "title": "స్వరాజ్య స్కానర్‌కు స్వాగతం! 📜",
        "tagline": "ప్రతి పౌరునికైనా తన జేబులో రాజ్యాంగం ఉండే ధైర్యం ఇవ్వండి.",
        "intro": "స్వరాజ్య స్కానర్ మీకు మీ స్థానిక భాషలో మీ రాజ్యాంగ హక్కుల జ్ఞానాన్ని ఇస్తుంది. ప్రశ్నలు అడగండి, జవాబులు పొందండి, మరియు మీ హక్కులను నమ్మకంతో రక్షించండి.",
        "get_started": "ప్రారంభించండి",
        "how_it_works": "ఇది ఎలా పని చేస్తుంది",
        "contact_us": "మా సంప్రదించండి",
        "features_title": "ప్రధాన లక్షణాలు",
        "features": [
            "📚 బహుభాషా ప్రశ్నలు మరియు జవాబు: మీ స్థానిక భాషలో జవాబులు పొందండి.",
            "🛡 హక్కుల రక్షణ: రాజ్యాంగ జ్ఞానంతో సుసజ్జితం అవ్వండి.",
            "🔍 సులభమైన శోధన: త్వరగా మరియు సులభంగా జవాబులు కనుగొనండి.",
            "🤝 సమాజ మద్దతు: హక్కులను రక్షిస్తున్న అందరితో కలసి ఉన్నారు.",
            "🔔 నోటిఫికేషన్లు: సంబంధిత హక్కుల తాజావార్తతో అప్‌డేట్ అవ్వండి."
        ],
        "footer": "© 2025 స్వరాజ్య స్కానర్. అన్ని హక్కులు సంరక్షితం."
    },
    "हिन्दी": {
        "title": "स्वराज्य स्कैनर में आपका स्वागत है! 📜",
        "tagline": "हर नागरिक के पास संविधान हो, और उसे इस्तेमाल करने का साहस भी हो।",
        "intro": "स्वराज्य स्कैनर आपको आपकी स्थानीय भाषा में आपके संवैधानिक अधिकारों का ज्ञान देता है। प्रश्न पूछें, उत्तर प्राप्त करें, और अपने अधिकारों की सुरक्षा करें।",
        "get_started": "शुरुआत करें",
        "how_it_works": "यह कैसे काम करता है",
        "contact_us": "संपर्क करें",
        "features_title": "मुख्य विशेषताएँ",
        "features": [
            "📚 बहुभाषी प्रश्नोत्तर: अपनी भाषा में जवाब पाएं।",
            "🛡 अधिकार रक्षा: संवैधानिक ज्ञान से सुसज्जित हों।",
            "🔍 आसान खोज: जल्दी और आसानी से उत्तर पाएं।",
            "🤝 समुदाय समर्थन: अपने अधिकारों की रक्षा करने वालों से जुड़ें।",
            "🔔 सूचनाएं: संबंधित अधिकारों से अपडेट रहें।"
        ],
        "footer": "© 2025 स्वराज्य स्कैनर। सर्वाधिकार सुरक्षित।"
    },
    "தமிழ்": {
        "title": "ஸ்வராஜ்யா ஸ்கேனர் வரவேற்கிறது! 📜",
        "tagline": "ஒவ்வொரு குடிமகனுக்கும் அவர்களது கையில் அரசமைப்பும் அதை பயன்படுத்த துணிவும் இருக்கட்டும்.",
        "intro": "ஸ்வராஜ்யா ஸ்கேனர் உங்கள் உள்ளூர் மொழியில் அரசமைப்புக் குறித்த அறிவை வழங்குகிறது. கேள்விகள் கேளுங்கள், பதில்கள் பெறுங்கள், உங்கள் உரிமைகளை பாதுகாக்கவும்.",
        "get_started": "தொடங்கு",
        "how_it_works": "இது எப்படி வேலை செய்கிறது",
        "contact_us": "எங்களை தொடர்பு கொள்ளவும்",
        "features_title": "முக்கிய அம்சங்கள்",
        "features": [
            "📚 பல்மொழி கேள்வி-பதில்: உங்கள் மொழியில் பதில்கள்.",
            "🛡 உரிமைகள் பாதுகாப்பு: அரசமைப்பு அறிவுடன் சமர்பிக்கவும்.",
            "🔍 எளிய தேடல்: விரைவாக மற்றும் எளிதில் பதில்கள் கிடைக்கும்.",
            "🤝 சமூக ஆதரவு: உரிமைகளை பாதுகாக்கும் குழுவுடன் இணைந்திருங்கள்.",
            "🔔 அறிவித்தல்கள்: தொடர்புடைய உரிமைகள் பற்றிய புதுப்பிப்புகள்."
        ],
        "footer": "© 2025 ஸ்வராஜ்யா ஸ்கேனர். அனைத்து உரிமைகளும் محفوظ."
    },
    "ಕನ್ನಡ": {
        "title": "ಸ್ವರಾಜ್ಯ ಸ್ಕ್ಯಾನರ್‌ಗೆ ಸ್ವಾಗತ! 📜",
        "tagline": "ಪ್ರತಿ ನಾಗರಿಕನಿಗೆ ಅವರ ಖೈಲಿಯಲ್ಲಿ ಸಂವಿಧಾನ ಮತ್ತು ಅದನ್ನು ಬಳಸುವ ಧೈರ್ಯವನ್ನು ನೀಡಿ.",
        "intro": "ಸ್ವರಾಜ್ಯ ಸ್ಕಾನರ್ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಭಾಷೆಯಲ್ಲಿ ನಿಮ್ಮ ಸಂವಿಧಾನದ ಹಕ್ಕುಗಳನ್ನು ತಿಳಿಸುತ್ತದೆ. ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ, ಉತ್ತರಗಳನ್ನು ಪಡೆಯಿರಿ, ಮತ್ತು ನಿಮ್ಮ ಹಕ್ಕುಗಳನ್ನು ರಕ್ಷಿಸಿ.",
        "get_started": "ಪ್ರಾರಂಭಿಸಿ",
        "how_it_works": "ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ",
        "contact_us": "ನಮ್ಮನ್ನು ಸಂಪರ್ಕಿಸಿ",
        "features_title": "ಪ್ರಮುಖ ವೈಶಿಷ್ಟ್ಯಗಳು",
        "features": [
            "📚 ಬಾಹುಭಾಷಾ ಪ್ರಶ್ನೋತ್ತರ: ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಉತ್ತರ ಪಡೆಯಿರಿ.",
            "🛡 ಹಕ್ಕು ರಕ್ಷಣೆ: ಸಂವಿಧಾನದ ಜ್ಞಾನದಿಂದ ಸಜ್ಜಾಗಿರಿ.",
            "🔍 ಸುಲಭ ಶೋಧನೆ: ತ್ವರಿತ ಮತ್ತು ಸುಲಭವಾಗಿ ಉತ್ತರಗಳನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ.",
            "🤝 ಸಮುದಾಯ ಬೆಂಬಲ: ನಿಮ್ಮ ಹಕ್ಕುಗಳಿಗಾಗಿ ಹೋರಾಟ ವೆಬ್ಬಾಗಿರು.",
            "🔔 ಸೂಚನೆಗಳು: ಪ್ರಸ್ತುತ ಹಕ್ಕುಗಳ ನವೀಕರಣಗಳನ್ನು ಪಡೆಯಿರಿ."
        ],
        "footer": "© 2025 ಸ್ವರಾಜ್ಯ ಸ್ಕಾನರ್. ಎಲ್ಲಾ ಹಕ್ಕುಗಳು ಸಂರಕ್ಷಿಸಲಾಗಿದೆ."
    },
    "മലയാളം": {
        "title": "സ്വരാജ്യ സ്കാനറിലേക്ക് സ്വാഗതം! 📜",
        "tagline": "എല്ലാ പൗരനും അവരുടെ കയ്യിൽ ഭരണഘടനയും അത് ഉപയോഗിക്കുന്ന ധൈര്യവും കൈവരുത്തുക.",
        "intro": "സ്വരാജ്യ സ്കാനർ നിങ്ങളുടെ സ്വന്തം ഭാഷയിൽ നിങ്ങളുടെ ഭരണഘടനാപരമായ അവകാശങ്ങളെക്കുറിച്ച് വിവരിക്കുന്നു. ചോദികൾ ചോദിക്കുക, ഉത്തരങ്ങൾ നേടുക, നിങ്ങളുടെ അവകാശങ്ങൾ സംരക്ഷിക്കുക.",
        "get_started": "പ്രാരംഭം",
        "how_it_works": "ഇത് എങ്ങനെ പ്രവർത്തിക്കുന്നു",
        "contact_us": "ഞങ്ങളെ ബന്ധപ്പെടുക",
        "features_title": "പ്രധാന സവിശേഷതകൾ",
        "features": [
            "📚 ബഹുഭാഷാ ചോദ്യോത്തരങ്ങൾ: നിങ്ങളുടെ ഭാഷയിൽ ഉത്തരങ്ങൾ ലഭിക്കും.",
            "🛡 അവകാശ സംരക്ഷണം: ഭരണഘടനാപരമായ അറിവ് നൽകുന്നു.",
            "🔍 എളുപ്പമുള്ള തിരച്ചിൽ: വേഗത്തിൽ മികച്ച ഉത്തരങ്ങൾ കണ്ടെത്തുക.",
            "🤝 സമുദായ പിന്തുണ: അവകാശങ്ങൾ സംരക്ഷിക്കുന്ന കൂട്ടായ്മ.",
            "🔔 അറിയിപ്പുകൾ: ബന്ധപ്പെട്ട അവകാശങ്ങളുടെ അപ്ഡേറ്റുകൾ."
        ],
        "footer": "© 2025 സ്വരാജ്യ സ്കാനർ. എല്ലാ അവകാശങ്ങളും സംരക്ഷിച്ചിട്ടുണ്ട്."
    },
    "اردو": {
        "title": "سواجیہ سکینر میں خوش آمدید! 📜",
        "tagline": "ہر شہری کے پاس اپنے پاس آئین ہو، اور اسے استعمال کرنے کا جرات بھی ہو۔",
        "intro": "سواجیہ سکینر آپ کو آپ کے مقامی زبان میں آئینی حقوق کا علم دیتا ہے۔ سوالات پوچھیں، جوابات حاصل کریں، اور اپنے حقوق کا دفاع کریں۔",
        "get_started": "شروع کریں",
        "how_it_works": "یہ کیسے کام کرتا ہے",
        "contact_us": "ہم سے رابطہ کریں",
        "features_title": "اہم خصوصیات",
        "features": [
            "📚 کثیراللسانی سوال و جواب: اپنی زبان میں جواب حاصل کریں۔",
            "🛡 حقوق کا دفاع: آئینی علم سے خود کو لیس کریں۔",
            "🔍 آسان تلاش: جلدی اور آسانی سے جواب تلاش کریں۔",
            "🤝 کمیونٹی سپورٹ: اپنے حقوق کے دفاع میں دوسروں سے جڑیں۔",
            "🔔 اطلاعات: متعلقہ حقوق کی تازہ ترین معلومات حاصل کریں۔"
        ],
        "footer": "© 2025 سواجیہ سکینر۔ جملہ حقوق محفوظ ہیں۔"
    }
}

# Language selector in sidebar
language = st.sidebar.selectbox("Select your language | अपनी भाषा चुनें | మీ భాష ఎంచుకోండి", options=list(content.keys()))

# Retrieve the content based on language selection
langs = content[language]

# Hero section with title and tagline
st.markdown(f"<h1>{langs['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3>{langs['tagline']}</h3>", unsafe_allow_html=True)
st.write("")

# Thematic image - same for all languages, replace URL with your desired image
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("Image.png", width=600)
st.write("")

# Introduction
st.markdown(f"{langs['intro']}")
st.write("")

# Navigation buttons with friendly messages (you can replace with navigation logic)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(langs["get_started"]):
        st.success("🚀 " + langs["get_started"] + " clicked. Redirecting soon...")
with col2:
    if st.button(langs["how_it_works"]):
        st.info(langs["how_it_works"] + " selected. More info coming here.")
with col3:
    if st.button(langs["contact_us"]):
        st.warning(langs["contact_us"] + " clicked. Contact form or info can be added here.")

st.markdown("---")

# Features section
st.markdown(f"## {langs['features_title']}")
for feature in langs["features"]:
    st.markdown(f"- {feature}")

st.markdown("---")

# Footer
st.markdown(f"<p style='text-align: center; '>{langs['footer']}</p>", unsafe_allow_html=True)




# Language map
lang_map = {
    "English": "en",
    "తెలుగు": "te",
    "हिन्दी": "hi",
    "தமிழ்": "ta",
    "ಕನ್ನಡ": "kn",
    "മലയാളം": "ml",
    "اردو": "ur"
}

# Chatbot toggle
if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False
if "messages" not in st.session_state:
    st.session_state.messages = [("bot", "Hello! How can I assist you today?")]

# Style toggle button bottom-right
toggle_button_css = """
    <style>
    .toggle-btn {
      position: fixed;
      right: 20px;
      bottom: 20px;
      z-index: 9999;
      background-color: #0073e6;
      color: white;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      font-size: 24px;
      border: none;
      cursor: pointer;
    }
    .chatbot-box {
      position: fixed;
      right: 20px;
      bottom: 80px;
      z-index: 9999;
      width: 360px;
      height: 500px;
      background: white;
      border-radius: 15px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.15);
      padding: 10px;
      overflow-y: auto;
    }
    .message-user {
      background:#e3f2fd;
      padding:8px 12px;
      border-radius:10px;
      margin-bottom:8px;
      max-width:80%;
      align-self:flex-start;
    }
    .message-bot {
      background:#f4f4f9;
      padding:8px 12px;
      border-radius:10px;
      margin-bottom:8px;
      max-width:80%;
      align-self:flex-end;
    }
    </style>
"""
st.markdown(toggle_button_css, unsafe_allow_html=True)



# Add a toggle button in the sidebar
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# Inject CSS based on dark_mode state
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp, h1, h2, h3, h4, h5, h6, p, li, .markdown-text-container, .chatbot-box, .message-user, .message-bot {
            color: #f4f4f9 !important;
        }
        body, .stApp {
            background-color: #181818 !important;
        }
        .stSidebar, .stSidebar * {
            color: #fff !important;
        }
        .stButton > button, .stTextInput > div > input {
            background-color: #333 !important;
            color: #f4f4f9 !important;
        }
        .chatbot-box {
            background: #222 !important;
        }
        .message-user, .message-bot {
            background: #333 !important;
            color: #f4f4f9 !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp, h1, h2, h3, h4, h5, h6, p, li, .markdown-text-container, .chatbot-box, .message-user, .message-bot {
            color: #222 !important;
        }
        body, .stApp {
            background-color: #f4f4f9 !important;
        }
        .stSidebar, .stSidebar * {
            color: #fff !important;
        }
        .stButton > button, .stTextInput > div > input {
            background-color: #0073e6 !important;
            color: white !important;
        }
        .chatbot-box {
            background: #fff !important;
        }
        .message-user {
            background: #e3f2fd !important;
            color: #222 !important;
        }
        .message-bot {
            background: #f4f4f9 !important;
            color: #222 !important;
        }
        </style>
    """, unsafe_allow_html=True)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🗨 AI Chatbot")

# Toggle to show/hide chatbot
show_chat = st.checkbox("Open Chatbot", value=False)

if show_chat:
    # User input form
    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_input("Your message:")
        submit = st.form_submit_button("Send")

    if submit and user_message.strip():
        # Append user message
        st.session_state.chat_history.append(("You", user_message.strip()))

        # Dummy bot response (replace with AI or your logic)
        bot_response = f"Echo: {user_message.strip()}"
        st.session_state.chat_history.append(("Bot", bot_response))

    # Display chat history
    st.markdown("### Chat History")
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"*You:* {msg}")
        else:
            st.markdown(f"*Bot:* {msg}")

else:
    st.write("Chatbot is hidden. Use the checkbox above to show it.")