
import streamlit as st
from datetime import date, timedelta

# -----------------------------
# App setup
# -----------------------------
st.set_page_config(
    page_title="Dear Body, I love you",
    page_icon="🌷",
    layout="centered"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
:root {
    --brown: #5a3e36;
    --peach: #EFD4CA;
    --cream: #F4EBE2;
    --white: #FFFCF8;
}

.stApp {
    background: linear-gradient(135deg, #EFD4CA 0%, #F4EBE2 50%, #EFD4CA 100%);
    color: var(--brown);
}

.block-container {
    max-width: 520px;
    padding-top: 1rem;
    padding-bottom: 6rem;
}

.header {
    background: var(--brown);
    color: white;
    text-align: center;
    padding: 22px 16px;
    border-radius: 26px 26px 0 0;
    margin-bottom: 18px;
}

.header-light {
    background: var(--peach);
    color: var(--brown);
    text-align: center;
    padding: 22px 16px;
    border-radius: 26px 26px 0 0;
    margin-bottom: 18px;
}

.card {
    background: var(--white);
    border-radius: 22px;
    padding: 20px;
    margin: 14px 0;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

.dark-card {
    background: var(--brown);
    color: white;
    border-radius: 16px;
    padding: 20px;
    margin: 14px 0;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

.peach-card {
    background: var(--peach);
    color: var(--brown);
    border-radius: 18px;
    padding: 18px;
    margin: 14px 0;
}

.small-card {
    background: var(--cream);
    color: var(--brown);
    border-radius: 16px;
    padding: 15px;
    margin: 10px 0;
}

.nav {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    max-width: 520px;
    width: 100%;
    background: #FFFCF8;
    border-top: 1px solid #EFD4CA;
    padding: 8px;
    z-index: 999;
}

div.stButton > button {
    background-color: var(--brown);
    color: white;
    border-radius: 14px;
    border: none;
    padding: 0.65rem 1rem;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #6b4a40;
    color: white;
}

textarea, input {
    border-radius: 14px !important;
}

hr {
    border: none;
    border-top: 1px solid #EFD4CA;
    margin: 18px 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session state defaults
# -----------------------------
defaults = {
    "signed_in": False,
    "auth_mode": "login",
    "email": "",
    "user_name": "",
    "tab": "Home",
    "sub_page": None,
    "account_page": None,
    "track_submitted": False,
    "journal_submitted": False,
    "streak": 0,
    "last_streak_date": "",
    "completed_days": [True, True, True, False, False, False, False],
    "day_index": 3,
    "checkin": {},
    "current_question_set": 0,
    "message_index": 0,
    "journal_quote_index": 0,
    "free_write": "",
    "daily_journal": "",
    "weekly_journal": "",
    "report_message": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

today_key = date.today().isoformat()
yesterday_key = (date.today() - timedelta(days=1)).isoformat()

positive_messages = [
    "You showed up for yourself today 💛",
    "Small steps still count, and today mattered 🌷",
    "You cared for yourself today, and that is something to be proud of ✨",
    "Progress can be gentle. You are doing better than you think 💕",
]

journal_quotes = [
    "Be proud of every small step you take 🌷",
    "Your body deserves kindness, care, and patience 💛",
    "You are growing at your own pace, and that is enough ✨",
    "Even on hard days, you are still doing beautifully 💕",
]

question_sets = [
    [
        ("moved", "Moved my body"),
        ("meals", "Ate regular meals"),
        ("water", "Drank water"),
        ("sleep", "Slept okay"),
    ],
    [
        ("stretch", "Took a moment to stretch"),
        ("snack", "Had a nourishing snack or meal"),
        ("break", "Took a break when I needed one"),
        ("kind", "Spoke kindly to myself"),
    ],
    [
        ("outside", "Spent a little time outside"),
        ("water2", "Checked in with my hydration"),
        ("rest", "Let myself rest without guilt"),
        ("breathe", "Paused and took a few deep breaths"),
    ],
]

# Reset streak if user missed more than one day
if st.session_state.last_streak_date not in ("", today_key, yesterday_key):
    st.session_state.streak = 0
    st.session_state.last_streak_date = ""

# -----------------------------
# Helper functions
# -----------------------------
def header(title, dark=True):
    css = "header" if dark else "header-light"
    st.markdown(f'<div class="{css}"><h1>{title}</h1></div>', unsafe_allow_html=True)

def card(content):
    st.markdown(f'<div class="card">{content}</div>', unsafe_allow_html=True)

def set_tab(tab_name):
    st.session_state.tab = tab_name
    st.session_state.sub_page = None
    st.session_state.account_page = None

def open_sub_page(page):
    st.session_state.tab = "Resources"
    st.session_state.sub_page = page

def back_to_resources():
    st.session_state.sub_page = None
    st.session_state.account_page = None

def info_page(title, html_content, back_func=back_to_resources):
    header(title, dark=True)
    st.markdown(f'<div class="card">{html_content}</div>', unsafe_allow_html=True)
    if st.button("Back"):
        back_func()
        st.rerun()

def submit_checkin():
    if st.session_state.track_submitted:
        return

    selected_keys = [key for key, value in st.session_state.checkin.items() if value]
    st.session_state.track_submitted = True
    st.session_state.message_index = (st.session_state.message_index + 1) % len(positive_messages)

    if st.session_state.last_streak_date == today_key:
        pass
    elif st.session_state.last_streak_date == yesterday_key:
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1

    st.session_state.last_streak_date = today_key

    completed = st.session_state.completed_days.copy()
    completed[st.session_state.day_index] = True
    st.session_state.completed_days = completed
    st.session_state.day_index = 0 if st.session_state.day_index == 6 else st.session_state.day_index + 1

    if any(key in selected_keys for key in ["moved", "stretch", "outside"]):
        st.session_state.current_question_set = 1
    elif any(key in selected_keys for key in ["meals", "snack", "water", "water2"]):
        st.session_state.current_question_set = 2
    else:
        st.session_state.current_question_set = (st.session_state.current_question_set + 1) % len(question_sets)

def submit_journal():
    st.session_state.journal_submitted = True
    st.session_state.journal_quote_index = (st.session_state.journal_quote_index + 1) % len(journal_quotes)

# -----------------------------
# Login screen
# -----------------------------
def login_screen():
    header("Login" if st.session_state.auth_mode == "login" else "Sign Up", dark=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Welcome back" if st.session_state.auth_mode == "login" else "Create your account")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.session_state.auth_mode == "signup":
        name = st.text_input("Name", key="signup_name")
    else:
        name = ""

    if st.button("Login" if st.session_state.auth_mode == "login" else "Sign Up"):
        if email.strip() and password.strip():
            st.session_state.signed_in = True
            st.session_state.email = email
            st.session_state.user_name = name.strip() or email.split("@")[0]
            st.rerun()
        else:
            st.warning("Please enter an email and password.")

    if st.button("Don't have an account? Sign Up" if st.session_state.auth_mode == "login" else "Already have an account? Login"):
        st.session_state.auth_mode = "signup" if st.session_state.auth_mode == "login" else "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Screens
# -----------------------------
def home_screen():
    header("Dear Body, I love you", dark=False)

    uploaded_top = st.file_uploader("Upload top image", type=["png", "jpg", "jpeg"], key="top_img")
    if uploaded_top:
        st.image(uploaded_top, use_container_width=True)
    else:
        st.markdown('<div class="peach-card" style="height:160px; display:flex; align-items:center; justify-content:center;"><h2>🌷 Time to put yourself first</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dark-card">
        <h2>Hi {st.session_state.user_name or "there"} 💛</h2>
        <h3>You are doing your best today, and that is enough.</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Why?"):
            open_sub_page("why")
            st.rerun()
    with col2:
        if st.button("What?"):
            open_sub_page("what")
            st.rerun()
    with col3:
        if st.button("How?"):
            open_sub_page("how")
            st.rerun()

    uploaded_bottom = st.file_uploader("Upload bottom image", type=["png", "jpg", "jpeg"], key="bottom_img")
    if uploaded_bottom:
        st.image(uploaded_bottom, use_container_width=True)
    else:
        st.markdown('<div class="card" style="text-align:center;"><h2>Time to put <em>yourself</em> first.</h2><p>🧘‍♀️</p></div>', unsafe_allow_html=True)

def track_screen():
    header("Track", dark=False)

    st.markdown(f"""
    <div class="peach-card" style="text-align:center;">
        <div style="font-size:46px;">🔥</div>
        <h1>{st.session_state.streak}</h1>
        <p>Day Streak</p>
        <p>This is your longest streak yet! Keep going 💛</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.track_submitted:
        st.markdown('<div class="dark-card"><h3>Today’s check-in</h3><p>Answer a few gentle questions about today.</p></div>', unsafe_allow_html=True)

        questions = question_sets[st.session_state.current_question_set]
        for key, label in questions:
            st.session_state.checkin[key] = st.checkbox(label, value=st.session_state.checkin.get(key, False), key=f"check_{key}")

        if st.button("Submit check-in"):
            submit_checkin()
            st.rerun()
    else:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h3>{positive_messages[st.session_state.message_index]}</h3>
            <p>Read the resources page for more support on how to manage how you feel.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Resources"):
            set_tab("Resources")
            st.rerun()

    st.markdown('<div class="peach-card"><h3>This Week</h3></div>', unsafe_allow_html=True)
    labels = ["M", "T", "W", "T", "F", "S", "S"]
    cols = st.columns(7)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**{labels[i]}**")
            st.markdown("✅" if st.session_state.completed_days[i] else "○")

def journal_screen():
    header("Journal", dark=True)

    if not st.session_state.journal_submitted:
        st.markdown('<div class="peach-card"><h3>Today’s reflection</h3><p>Gentle prompts for body-kindness</p></div>', unsafe_allow_html=True)

        prompts = [
            "One thing my body helped me do today was...",
            "A kind sentence I would say to a friend is...",
            "How did I feel after moving my body today?",
        ]
        for prompt in prompts:
            st.markdown(f'<div class="small-card">{prompt}</div>', unsafe_allow_html=True)

        st.session_state.daily_journal = st.text_area("Daily note", value=st.session_state.daily_journal, height=180)
        st.session_state.weekly_journal = st.text_area(
            "Weekly Reflection: How did I feel this week?",
            value=st.session_state.weekly_journal,
            height=210
        )

        if st.button("Submit journal"):
            if st.session_state.daily_journal.strip() and st.session_state.weekly_journal.strip():
                submit_journal()
                st.rerun()
            else:
                st.warning("Write something in both journal boxes before submitting.")
    else:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h2>Good job!</h2>
            <p>{journal_quotes[st.session_state.journal_quote_index]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="peach-card"><h3>Free writing page</h3><p>Feel free to get everything off your chest here. It will be gone by tomorrow morning.</p></div>', unsafe_allow_html=True)
        st.session_state.free_write = st.text_area("Write freely here", value=st.session_state.free_write, height=320)

def resources_screen():
    if st.session_state.sub_page:
        resources_sub_page()
        return

    header("Resources", dark=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Support"):
            st.session_state.sub_page = "supportInfo"
            st.rerun()
    with col2:
        if st.button("Quick Help"):
            st.session_state.sub_page = "quickHelp"
            st.rerun()

    st.markdown("""
    <div class="peach-card">
        <p>This resources page has been designed to support users in developing a healthier and more balanced relationship with their body, food, and movement.</p>
        <p>It encourages self-reflection, positive habits, and emotional awareness, but it does not replace real-world support.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    pages = [("Thoughts", "thoughts"), ("Nutrition", "nutrition"), ("Physical Activity", "activity")]
    for col, (label, page) in zip(cols, pages):
        with col:
            if st.button(label):
                st.session_state.sub_page = page
                st.rerun()

    cols = st.columns(3)
    pages = [("Why?", "why"), ("What?", "what"), ("How?", "how")]
    for col, (label, page) in zip(cols, pages):
        with col:
            if st.button(label):
                st.session_state.sub_page = page
                st.rerun()

def resources_sub_page():
    page = st.session_state.sub_page

    content = {
        "supportInfo": """
            <h2>You do not have to do this alone</h2>
            <p>Speaking to someone can provide reassurance, guidance, and professional care.</p>
            <ul>
                <li>A trusted adult, such as a parent, teacher, or coach</li>
                <li>A school counsellor</li>
                <li>A general practitioner</li>
            </ul>
            <div class="small-card"><b>Butterfly Foundation</b><br>Phone: 1800 33 4673<br>Support for eating disorders and body image concerns.</div>
            <div class="small-card"><b>Headspace</b><br>Phone: 1800 650 890<br>Mental health and wellbeing support for young people.</div>
            <div class="small-card"><b>Kids Helpline</b><br>Phone: 1800 55 1800<br>Confidential counselling for young people aged 5–25.</div>
        """,
        "thoughts": """
            <h2>Be kinder to your mind</h2>
            <p>Self-talk has a powerful influence on how individuals feel about themselves.</p>
            <ul>
                <li>Identify negative thoughts without accepting them as truth</li>
                <li>Ask: “Is this helpful or fair?”</li>
                <li>Replace harsh language with neutral or kind alternatives</li>
                <li>Practice affirmations to reinforce positive beliefs</li>
            </ul>
            <p><b>Example:</b> “I hate my body” → “I am learning to treat my body with more respect.”</p>
        """,
        "nutrition": """
            <h2>Fuel your body, support your mood</h2>
            <p>Regular and balanced eating helps maintain stable energy, concentration, and mood.</p>
            <ul>
                <li>Aim to eat regular meals and snacks</li>
                <li>Include a variety of foods</li>
                <li>Recognise that all foods can have a place</li>
                <li>Understand that food is both fuel and enjoyment</li>
            </ul>
            <p><b>Reframe:</b> “I shouldn’t have eaten that” → “That helped give my body energy and satisfaction.”</p>
        """,
        "activity": """
            <h2>Move for how it feels, not how it looks</h2>
            <p>Movement should support mood, energy, and overall health, not punishment or changing appearance.</p>
            <ul>
                <li>Improved mood through endorphins</li>
                <li>Increased energy levels</li>
                <li>Reduced stress and anxiety</li>
                <li>Choosing activities that feel enjoyable and manageable</li>
                <li>Allowing for rest and recovery</li>
            </ul>
        """,
        "quickHelp": """
            <h2>Need something right now?</h2>
            <ul>
                <li><b>Breathing:</b> breathe in for 4 seconds and out for 4 seconds</li>
                <li><b>Hydration or nourishment:</b> drink water or eat a small snack</li>
                <li><b>Change environment:</b> step outside or move to a calmer space</li>
                <li><b>Emotional expression:</b> write down thoughts without judgement</li>
                <li><b>Grounding reminder:</b> “This feeling will pass.”</li>
            </ul>
        """,
        "why": """
            <h2>Why?</h2>
            <p>Body image influences confidence, mental health, and daily behaviours.</p>
            <p>External influences such as social media, peer pressure, and unrealistic beauty standards can contribute to dissatisfaction.</p>
        """,
        "what": """
            <h2>What is body image?</h2>
            <p>Body image is how a person thinks, feels, and behaves in relation to their body.</p>
            <ul>
                <li>Treating your body with respect</li>
                <li>Accepting natural changes</li>
                <li>Recognising your body’s abilities</li>
                <li>Reducing self-criticism</li>
            </ul>
        """,
        "how": """
            <h2>How can body image be improved?</h2>
            <p>Improving body image involves shifting focus from appearance to function and self-care.</p>
            <ul>
                <li>Focus on what the body can do</li>
                <li>Eat regularly to support functioning</li>
                <li>Choose enjoyable movement</li>
                <li>Challenge negative self-talk</li>
                <li>Reduce exposure to unrealistic online content</li>
            </ul>
        """,
    }

    titles = {
        "supportInfo": "Support",
        "thoughts": "Thoughts",
        "nutrition": "Nutrition",
        "activity": "Physical Activity",
        "quickHelp": "Need something right now?",
        "why": "Why?",
        "what": "What is body image?",
        "how": "How can body image be improved?",
    }

    info_page(titles[page], content[page])

def account_screen():
    if st.session_state.account_page:
        account_sub_page()
        return

    header("Account", dark=True)

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h2>{st.session_state.user_name or "User"}</h2>
        <p>{st.session_state.email or "name@email.com"}</p>
        <p>🌷 Dear Body, I love you</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Favourites"):
            st.session_state.account_page = "favourites"
            st.rerun()
    with col2:
        if st.button("History"):
            st.session_state.account_page = "history"
            st.rerun()
    with col3:
        if st.button("Edit Profile"):
            st.session_state.account_page = "editProfile"
            st.rerun()

    st.markdown('<div class="peach-card"><h3>Settings and support</h3></div>', unsafe_allow_html=True)

    buttons = [
        ("Settings", "settings"),
        ("Security", "security"),
        ("Report a problem", "reportProblem"),
        ("Account status", "accountStatus"),
        ("Reports and violations", "reportsViolations"),
        ("Journal insights", "journalInsights"),
    ]

    for label, page in buttons:
        if st.button(label):
            st.session_state.account_page = page
            st.rerun()

    if st.button("Log out"):
        for key in ["signed_in", "email", "user_name"]:
            st.session_state[key] = defaults[key]
        st.rerun()

def account_sub_page():
    page = st.session_state.account_page

    simple_pages = {
        "favourites": ("My favourites", """
            <h2>Saved quotes and supports</h2>
            <div class="small-card">My worth is not measured by my appearance.</div>
            <div class="small-card">Food is fuel and also enjoyment — both matter.</div>
            <div class="small-card">Small steps still count.</div>
        """),
        "history": ("My history", f"""
            <h2>Your recent activity</h2>
            <p>Current streak: {st.session_state.streak} day{'s' if st.session_state.streak != 1 else ''}</p>
            <p>Today’s check-in: {'Completed' if st.session_state.track_submitted else 'Not completed yet'}</p>
            <p>Journal today: {'Completed' if st.session_state.journal_submitted else 'Not completed yet'}</p>
        """),
        "editProfile": ("Edit profile", f"""
            <h2>Profile details</h2>
            <p><b>Name:</b> {st.session_state.user_name or "Annie"}</p>
            <p><b>Username:</b> {st.session_state.user_name or "annabelwoodd"}</p>
            <p><b>Email:</b> {st.session_state.email or "name@email.com"}</p>
            <p><b>Pronouns:</b> Not added</p>
        """),
        "settings": ("Settings", """
            <h2>Settings</h2>
            <p>This section would let the user manage notifications, reminders, privacy, and account preferences.</p>
        """),
        "security": ("Security", """
            <h2>Security</h2>
            <p>This section would help users manage password changes, two-factor authentication, saved login, and logged-in devices.</p>
        """),
        "accountStatus": ("Account status", """
            <h2>Your account overview</h2>
            <p><b>Status:</b> Active</p>
            <p><b>Login:</b> Signed in successfully</p>
            <p><b>Current access:</b> Journal, track, resources, and account tools available.</p>
        """),
        "reportsViolations": ("Reports and violations", """
            <h2>Reports overview</h2>
            <p>This page would collect any reports, flagged activity, or account notices in one place.</p>
            <p><b>Current status:</b> No reports or violations are currently listed for this account.</p>
        """),
        "journalInsights": ("Journal insights", f"""
            <p>Current streak: {st.session_state.streak} day{'s' if st.session_state.streak != 1 else ''}</p>
            <p>Today’s check-in: {'Completed' if st.session_state.track_submitted else 'Not completed yet'}</p>
            <p>Journal today: {'Completed' if st.session_state.journal_submitted else 'Not completed yet'}</p>
        """),
    }

    if page == "reportProblem":
        header("Report a problem", dark=True)
        st.markdown("""
        <div class="card">
            <h2>Tell us what went wrong</h2>
            <p>This page helps users explain bugs, loading issues, missing features, or anything in the app that is not working as expected.</p>
            <ul>
                <li>The journal did not save properly</li>
                <li>The daily check-in did not reset</li>
                <li>A button or page is not opening</li>
                <li>The app feels slow or freezes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.report_message = st.text_area("Describe your issue", value=st.session_state.report_message, height=130)
        if st.button("Submit report"):
            st.success("Report submitted for this prototype.")
        if st.button("Back"):
            st.session_state.account_page = None
            st.rerun()
        return

    title, html = simple_pages.get(page, ("Account", "<p>This account page is available in the full app.</p>"))
    info_page(title, html, back_func=lambda: st.session_state.update({"account_page": None}))

# -----------------------------
# Main app
# -----------------------------
if not st.session_state.signed_in:
    login_screen()
else:
    if st.session_state.tab == "Home":
        home_screen()
    elif st.session_state.tab == "Track":
        track_screen()
    elif st.session_state.tab == "Journal":
        journal_screen()
    elif st.session_state.tab == "Resources":
        resources_screen()
    elif st.session_state.tab == "Account":
        account_screen()

    st.markdown('<div class="nav">', unsafe_allow_html=True)
    cols = st.columns(5)
    nav_items = ["Home", "Track", "Journal", "Resources", "Account"]
    for col, item in zip(cols, nav_items):
        with col:
            if st.button(item, key=f"nav_{item}"):
                set_tab(item)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
