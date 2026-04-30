import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title='Dear Body, I love you', layout='centered', initial_sidebar_state='collapsed')

# ---------- State ----------
def init_state():
    defaults = {
        'signed_in': False,
        'auth_mode': 'login',
        'email': '',
        'password': '',
        'name': '',
        'tab': 'home',
        'subpage': None,
        'account_page': None,
        'streak': 0,
        'submitted_checkin': False,
        'checkin': {},
        'completed_days': [True, True, True, False, False, False, False],
        'day_index': 3,
        'question_set': 0,
        'last_choices': [],
        'journal_submitted': False,
        'daily_journal': '',
        'weekly_journal': '',
        'free_write': '',
        'quote_index': 0,
        'message_index': 0,
        'today_key': str(date.today()),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

if st.session_state.today_key != str(date.today()):
    st.session_state.today_key = str(date.today())
    st.session_state.submitted_checkin = False
    st.session_state.checkin = {}
    st.session_state.journal_submitted = False
    st.session_state.daily_journal = ''
    st.session_state.weekly_journal = ''
    st.session_state.free_write = ''

# ---------- Styling ----------
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--dark:#5a3e36;--pink:#EFD4CA;--cream:#F4EBE2;--white:#FFFCF8;--muted:#8b7b73;}
html, body, [class*="css"]{font-family:Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;}
[data-testid="stAppViewContainer"]{background:#fff;}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"]{display:none!important;}
.block-container{max-width:390px!important; padding:22px 0 18px!important;}
.phone{position:relative; min-height:760px; overflow:hidden; border-radius:26px; box-shadow:0 8px 30px rgba(0,0,0,.08); background:linear-gradient(135deg,#EFD4CA 0%,#F4EBE2 52%,#EFD4CA 100%); padding-bottom:92px; color:var(--dark);} 
.phone:before{content:'';position:absolute;left:25px;top:30px;width:90px;height:90px;border-radius:999px;background:rgba(90,62,54,.10);filter:blur(24px);} 
.phone:after{content:'';position:absolute;right:25px;bottom:75px;width:110px;height:110px;border-radius:999px;background:rgba(90,62,54,.10);filter:blur(24px);} 
.content{position:relative;z-index:2;}
.header{background:var(--pink);color:var(--dark);padding:14px 16px 20px;} .header.dark{background:var(--dark);color:white;}
.status{display:flex;justify-content:space-between;font-size:11px;font-weight:600;margin-bottom:10px}.title{text-align:center;font-size:32px;font-weight:700;letter-spacing:.5px;margin:0;}
.pad{padding:18px 16px;}.card{background:var(--white);border-radius:22px;padding:18px;color:var(--dark);box-shadow:0 2px 12px rgba(0,0,0,.07);margin-bottom:16px}.pinkcard{background:var(--pink);border-radius:22px;padding:16px;box-shadow:0 1px 9px rgba(0,0,0,.05);margin-bottom:16px}.darkcard{background:var(--dark);color:white;border-radius:16px;padding:18px;box-shadow:0 2px 10px rgba(0,0,0,.06);margin-bottom:16px}.soft{background:var(--cream);border-radius:18px;padding:13px;margin:10px 0}.hero{height:176px;background:linear-gradient(135deg,#8d6c62 0%,#b08b7f 55%,#8b6b61 100%);border-radius:0 0 18px 18px;margin-top:8px;}.feature{height:176px;border-radius:16px;background:linear-gradient(135deg,#f5eee9,#f0e6df,#eaded6);position:relative;text-align:center;padding-top:18px;overflow:hidden}.feature .big{font-size:22px;font-weight:700;font-style:italic;margin:-4px 0}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.tile{min-height:98px;border-radius:14px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:700}.tile.dark{background:var(--dark);color:white}.tile.light{background:var(--cream);color:var(--dark)}
.nav{position:fixed;left:50%;transform:translateX(-50%);bottom:18px;width:min(390px,100vw);display:grid;grid-template-columns:repeat(5,1fr);gap:0;background:rgba(244,235,226,.96);border-radius:0 0 24px 24px;padding:9px 8px 8px;z-index:999;box-shadow:0 -2px 12px rgba(0,0,0,.05)}.nav button{font-size:10px!important;padding:3px!important;border-radius:8px!important;color:var(--dark)!important;background:transparent!important;border:none!important}.nav .active{outline:2px solid #8bb5ff!important;background:rgba(255,255,255,.35)!important}.stButton>button{width:100%;border-radius:12px;border:0;background:var(--dark);color:white;font-weight:700;padding:10px 12px;transition:.05s}.stButton>button:active{transform:scale(.98)}textarea, input{border-radius:12px!important}.tiny{font-size:12px;color:var(--muted)}.row{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #EADDD6;padding:16px 0}.circle{width:48px;height:48px;border-radius:999px;background:var(--cream);display:flex;align-items:center;justify-content:center;font-weight:800}.profilecircle{width:74px;height:74px;border-radius:999px;background:#d9c5bb;color:white;font-size:30px;font-weight:800;display:flex;align-items:center;justify-content:center}.week{display:grid;grid-template-columns:repeat(5,1fr);text-align:center;gap:10px}.daydot{width:45px;height:45px;border-radius:999px;display:flex;align-items:center;justify-content:center;margin:7px auto 0;font-size:20px}.done{background:var(--dark);color:white}.todo{background:var(--cream);color:var(--dark)}
</style>
''', unsafe_allow_html=True)

# ---------- Helpers ----------
def start_phone(title=None, dark=False, custom_header=True):
    st.markdown('<div class="phone"><div class="content">', unsafe_allow_html=True)
    if custom_header and title:
        st.markdown(f'<div class="header {"dark" if dark else ""}"><div class="status"><span>07:00</span><span>◠ &nbsp;▮▮▮</span></div><h1 class="title">{title}</h1></div>', unsafe_allow_html=True)

def end_phone(show_nav=True):
    st.markdown('</div></div>', unsafe_allow_html=True)
    if show_nav and st.session_state.signed_in:
        nav()

def go_tab(tab):
    st.session_state.tab = tab
    st.session_state.subpage = None
    st.session_state.account_page = None
    st.rerun()

def open_sub(page):
    st.session_state.tab = 'support'
    st.session_state.subpage = page
    st.rerun()

def open_account(page):
    st.session_state.account_page = page
    st.session_state.subpage = None
    st.rerun()

def nav():
    tabs=[('home','⌂','Home'),('track','⌁','Track'),('journal','▣','Journal'),('support','⌕','Resources'),('account','♡','Account')]
    st.markdown('<div class="nav">', unsafe_allow_html=True)
    cols=st.columns(5)
    for col,(key,icon,label) in zip(cols,tabs):
        with col:
            active='active' if st.session_state.tab==key else ''
            if st.button(f'{icon}\n{label}', key=f'nav_{key}', help=label):
                go_tab(key)
    st.markdown('</div>', unsafe_allow_html=True)

questions = [
    [('moved','Moved my body'),('meals','Ate regular meals'),('water','Drank water'),('sleep','Slept okay')],
    [('stretch','Took a moment to stretch'),('snack','Had a nourishing snack or meal'),('break','Took a break when I needed one'),('kind','Spoke kindly to myself')],
    [('outside','Spent a little time outside'),('water2','Checked in with my hydration'),('rest','Let myself rest without guilt'),('breathe','Paused and took a few deep breaths')],
]
messages=['You showed up for yourself today 💛','Small steps still count, and today mattered 🌷','You cared for yourself today, and that is something to be proud of ✨','Progress can be gentle. You are doing better than you think 💕']
quotes=['Be proud of every small step you take 🌷','Your body deserves kindness, care, and patience 💛','You are growing at your own pace, and that is enough ✨','Even on hard days, you are still doing beautifully 💕']

# ---------- Screens ----------
def signin():
    start_phone('Login' if st.session_state.auth_mode=='login' else 'Sign Up', True, True)
    st.markdown('<div class="pad"><div class="card"><h2 style="text-align:center;margin-top:0">' + ('Welcome back' if st.session_state.auth_mode=='login' else 'Create your account') + '</h2>', unsafe_allow_html=True)
    st.session_state.email = st.text_input('Email', value=st.session_state.email, label_visibility='collapsed', placeholder='Email')
    st.session_state.password = st.text_input('Password', value=st.session_state.password, type='password', label_visibility='collapsed', placeholder='Password')
    if st.session_state.auth_mode == 'signup':
        st.session_state.name = st.text_input('Name', value=st.session_state.name, label_visibility='collapsed', placeholder='Name')
    if st.button('Login' if st.session_state.auth_mode=='login' else 'Sign Up'):
        if st.session_state.email.strip() and st.session_state.password.strip():
            st.session_state.signed_in=True
            if not st.session_state.name:
                st.session_state.name = st.session_state.email.split('@')[0]
            st.rerun()
    if st.button("Don't have an account? Sign Up" if st.session_state.auth_mode=='login' else 'Already have an account? Login'):
        st.session_state.auth_mode = 'signup' if st.session_state.auth_mode=='login' else 'login'
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
    end_phone(False)

def home():
    start_phone(custom_header=False)
    st.markdown('<div class="header"><div class="status"><span>07:00</span><span>◠ &nbsp;▮▮▮</span></div><div class="hero"></div></div><div class="pad">', unsafe_allow_html=True)
    st.markdown(f'<div class="darkcard"><div style="font-size:20px;font-weight:700">Hi {st.session_state.name or "there"} 💛</div><div style="font-size:18px;margin-top:4px">You are doing your best today, and that is enough.</div></div>', unsafe_allow_html=True)
    if st.button('Show All'):
        go_tab('support')
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button('Why?'): open_sub('why')
    with c2:
        if st.button('What?'): open_sub('what')
    with c3:
        if st.button('How?'): open_sub('how')
    st.markdown('<div class="feature"><div style="font-size:18px;font-weight:700">Time to put</div><div class="big">yourself</div><div style="font-size:18px;font-weight:700">first.</div><div style="font-size:78px;margin-top:10px">🧘‍♀️</div></div></div>', unsafe_allow_html=True)
    end_phone()

def track():
    start_phone(custom_header=False)
    st.markdown(f'<div class="header"><div class="status"><span>07:00</span><span>◠ &nbsp;▮▮▮</span></div><div style="text-align:center"><div style="font-size:48px">🔥</div><div style="font-size:48px;font-weight:800">{st.session_state.streak}</div><div>Day Streak</div><p>This is your longest streak yet! Keep going 💛</p></div></div><div class="pad">', unsafe_allow_html=True)
    if not st.session_state.submitted_checkin:
        st.markdown('<div class="darkcard"><h3>Today’s check-in</h3><p class="tiny" style="color:white">Answer a few gentle questions about today.</p>', unsafe_allow_html=True)
        for key,label in questions[st.session_state.question_set]:
            st.session_state.checkin[key] = st.checkbox(label, value=st.session_state.checkin.get(key, False), key=f'check_{key}')
        if st.button('Submit'):
            selected=[k for k,v in st.session_state.checkin.items() if v]
            st.session_state.last_choices=selected
            st.session_state.submitted_checkin=True
            st.session_state.streak += 1 if st.session_state.streak else 1
            st.session_state.completed_days[st.session_state.day_index]=True
            st.session_state.day_index=(st.session_state.day_index+1)%7
            st.session_state.message_index=(st.session_state.message_index+1)%len(messages)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="card" style="text-align:center"><h3>{messages[st.session_state.message_index]}</h3><p>Read the resources page for more support on how to manage how you feel.</p></div>', unsafe_allow_html=True)
        if st.button('Go to Resources'):
            go_tab('support')
    st.markdown('<div class="pinkcard"><h3>This Week</h3><div class="week">', unsafe_allow_html=True)
    for i,l in enumerate(['M','T','W','T','F']):
        cls='done' if st.session_state.completed_days[i] else 'todo'
        st.markdown(f'<div>{l}<div class="daydot {cls}">{"✓" if st.session_state.completed_days[i] else ""}</div></div>', unsafe_allow_html=True)
    st.markdown('</div><div style="width:40%;display:grid;grid-template-columns:repeat(2,1fr);text-align:center;gap:10px;margin-top:12px">', unsafe_allow_html=True)
    for i,l in [(5,'S'),(6,'S')]:
        cls='done' if st.session_state.completed_days[i] else 'todo'
        st.markdown(f'<div>{l}<div class="daydot {cls}">{"✓" if st.session_state.completed_days[i] else ""}</div></div>', unsafe_allow_html=True)
    st.markdown('</div></div></div>', unsafe_allow_html=True)
    end_phone()

def journal():
    start_phone('Journal', True)
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    if not st.session_state.journal_submitted:
        st.markdown('<div class="pinkcard"><b>Today’s reflection</b><p class="tiny">Gentle prompts for body-kindness</p><div class="soft">One thing my body helped me do today was...</div><div class="soft">A kind sentence I would say to a friend is...</div><div class="soft">How did I feel after moving my body today?</div></div>', unsafe_allow_html=True)
        st.session_state.daily_journal=st.text_area('Daily note', value=st.session_state.daily_journal, height=150, placeholder='Write here...')
        st.markdown('<div class="pinkcard"><b>Weekly Reflection</b><div class="soft">How did I feel this week?</div></div>', unsafe_allow_html=True)
        st.session_state.weekly_journal=st.text_area('Weekly note', value=st.session_state.weekly_journal, height=180, placeholder='Notice patterns, wins, and what helped you feel more like yourself...')
        if st.button('Submit', disabled=not(st.session_state.daily_journal.strip() and st.session_state.weekly_journal.strip())):
            st.session_state.journal_submitted=True
            st.session_state.quote_index=(st.session_state.quote_index+1)%len(quotes)
            st.rerun()
    else:
        st.markdown(f'<div class="card" style="text-align:center"><h3>Good job!</h3><p>{quotes[st.session_state.quote_index]}</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="pinkcard"><b>Free writing page</b><p class="tiny">Feel free to get everything off your chest here. It will be gone by tomorrow morning.</p></div>', unsafe_allow_html=True)
        st.session_state.free_write=st.text_area('Free writing', value=st.session_state.free_write, height=260, placeholder='Write freely here...')
    st.markdown('</div>', unsafe_allow_html=True)
    end_phone()

def info_page(title, blocks, back=lambda: setattr(st.session_state,'subpage',None)):
    start_phone(title, True)
    st.markdown('<div class="pad"><div class="card">', unsafe_allow_html=True)
    for b in blocks:
        st.markdown(b, unsafe_allow_html=True)
    if st.button('Back'):
        back(); st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
    end_phone()

def support():
    if st.session_state.subpage:
        pages={
        'supportInfo':['<h3 style="text-align:center">You do not have to do this alone</h3><p>Reach out to a trusted adult, school counsellor, GP, Butterfly Foundation, Headspace, or Kids Helpline.</p>'],
        'quickHelp':['<p>This section provides immediate, simple strategies for stress or overwhelm.</p><div class="soft"><b>Breathing:</b> in for 4, out for 4.<br><b>Hydration or nourishment:</b> drink water or have a snack.<br><b>Change of environment:</b> move spaces or step outside.<br><b>Grounding:</b> This feeling will pass.</div>'],
        'thoughts':['<div class="soft"><h3>Be kinder to your mind</h3><p>Notice negative thoughts, question if they are fair, and replace them with kinder alternatives.</p></div><p><b>Example:</b> “I hate my body” → “I am learning to treat my body with more respect.”</p>'],
        'nutrition':['<div class="soft"><h3>Fuel your body, support your mood</h3><p>Regular balanced eating supports energy, concentration, and mood.</p></div><ul><li>Aim to eat regular meals and snacks</li><li>Include a variety of foods</li><li>All foods can have a place</li></ul>'],
        'activity':['<div class="soft"><h3>Move for how it feels, not how it looks</h3><p>Movement should support mood, energy, and overall health, not punishment or changing appearance.</p></div><ul><li>Improved mood</li><li>Increased energy</li><li>Reduced stress and anxiety</li><li>Rest and recovery matter</li></ul>'],
        'why':['<p>Body image influences confidence, mental health, and daily behaviours. Social media, peer pressure, and unrealistic standards can affect how people see themselves.</p>'],
        'what':['<p>Body image is how a person thinks, feels, and behaves in relation to their body. It is also about abilities, strength, and function.</p><ul><li>Treating your body with respect</li><li>Accepting natural changes</li><li>Recognising your body’s abilities</li></ul>'],
        'how':['<p>Improving body image involves shifting focus from appearance to function and self-care.</p><ul><li>Focus on what the body can do</li><li>Eat regularly</li><li>Choose enjoyable movement</li><li>Challenge negative self-talk</li></ul>']}
        info_page('Need something right now?' if st.session_state.subpage=='quickHelp' else {'supportInfo':'Support','activity':'Physical Activity','what':'What is body image?','how':'How can body image be improved?'}.get(st.session_state.subpage, st.session_state.subpage.title()), pages[st.session_state.subpage])
        return
    start_phone('Resources', True)
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button('Support'): open_sub('supportInfo')
    with c2:
        if st.button('Quick Help'): open_sub('quickHelp')
    st.markdown('<div class="pinkcard"><p>This resources page has been designed to support users in developing a healthier and more balanced relationship with their body, food, and movement.</p><p>Body image concerns, negative self-talk, and stress around food or exercise can be influenced by social pressures, media exposure, and personal experiences.</p></div>', unsafe_allow_html=True)
    for row in [('Thoughts','Nutrition','Physical\nActivity'),('Why?','What?','How?')]:
        cols=st.columns(3)
        keys={'Thoughts':'thoughts','Nutrition':'nutrition','Physical\nActivity':'activity','Why?':'why','What?':'what','How?':'how'}
        for col,label in zip(cols,row):
            with col:
                if st.button(label): open_sub(keys[label])
    st.markdown('</div>', unsafe_allow_html=True)
    end_phone()

def account():
    page=st.session_state.account_page
    if page in ['reportProblem','accountStatus','reportsViolations','journalInsights','changePassword','twoFactor','verificationSelfie','savedLogin','loggedInDevices','recentEmails','securityCheckup','favourites','history']:
        title={'reportProblem':'Report a problem','accountStatus':'Account status','reportsViolations':'Reports and violations','journalInsights':'Journal insights','changePassword':'Change password','twoFactor':'Two-factor authentication','verificationSelfie':'Verification selfie','savedLogin':'Saved login','loggedInDevices':"Where you're logged in",'recentEmails':'Recent emails','securityCheckup':'Security checkup','favourites':'My favourites','history':'My history'}[page]
        extra = '<textarea placeholder="Write what happened..." style="width:100%;min-height:120px;border:1px solid #EFD4CA;background:#F4EBE2;border-radius:12px;padding:10px"></textarea>' if page=='reportProblem' else ''
        info_page(title,[f'<div class="soft"><p>This section is working in the Python version. It shows the same account information and prototype explanation as the React version.</p></div>{extra}'], back=lambda: setattr(st.session_state,'account_page','settings' if page in ['reportProblem','accountStatus','reportsViolations','journalInsights'] else None))
        return
    if page=='editProfile':
        start_phone(custom_header=False)
        st.markdown(f'<div class="header"><div class="status"><span>10:17</span><span>5G &nbsp;55</span></div><h1 class="title">Edit profile</h1></div><div class="pad"><div style="text-align:center" class="card"><div class="profilecircle" style="margin:auto">{(st.session_state.name or "U")[0].upper()}</div><p><b>Edit picture or avatar</b></p></div><div class="card"><div class="row"><b>Name</b><span>{st.session_state.name or "Annie"}</span></div><div class="row"><b>Username</b><span>{st.session_state.name or "annabelwoodd"}</span></div><div class="row"><b>Pronouns</b><span>Pronouns</span></div><div class="row"><b>Email</b><span>{st.session_state.email or "name@email.com"}</span></div></div>', unsafe_allow_html=True)
        if st.button('Back'): open_account(None)
        st.markdown('</div>', unsafe_allow_html=True); end_phone(); return
    if page=='security':
        start_phone(custom_header=False)
        st.markdown('<div class="header"><div class="status"><span>10:19</span><span>5G &nbsp;55</span></div></div><div class="pad"><h1>Password and security</h1><h2>Login & recovery</h2><p class="tiny">Manage your passwords, login preferences and recovery methods.</p>', unsafe_allow_html=True)
        for label,key in [('Change password','changePassword'),('Two-factor authentication','twoFactor'),('Verification selfie','verificationSelfie'),('Saved login','savedLogin'),('Where you’re logged in','loggedInDevices'),('Recent emails','recentEmails'),('Security checkup','securityCheckup')]:
            if st.button(label): open_account(key)
        if st.button('Back'): open_account(None)
        st.markdown('</div>', unsafe_allow_html=True); end_phone(); return
    if page=='settings':
        start_phone(custom_header=False)
        st.markdown('<div class="header"><div class="status"><span>10:18</span><span>5G &nbsp;55</span></div></div><div class="pad"><h1>Help and support</h1>', unsafe_allow_html=True)
        for label,key in [('Report a problem','reportProblem'),('Account status','accountStatus'),('Reports and violations','reportsViolations'),('Journal insights','journalInsights')]:
            if st.button(label): open_account(key)
        if st.button('Back'): open_account(None)
        st.markdown('</div>', unsafe_allow_html=True); end_phone(); return
    start_phone('Account', True)
    st.markdown(f'<div class="pad"><div class="card"><div style="display:flex;align-items:center;gap:14px"><div class="profilecircle">{(st.session_state.name or "U")[0].upper()}</div><div><h3 style="margin:0">{st.session_state.name or "Your profile"}</h3><p class="tiny">{st.session_state.email or "your@email.com"}</p></div></div></div>', unsafe_allow_html=True)
    for label,key in [('♡  My favourites','favourites'),('🕘  My history','history'),('✎  Edit profile','editProfile'),('❓  Help and support','settings'),('🔒  Password and security','security')]:
        if st.button(label): open_account(key)
    if st.button('Log out'):
        st.session_state.signed_in=False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    end_phone()

if not st.session_state.signed_in:
    signin()
elif st.session_state.tab == 'home':
    home()
elif st.session_state.tab == 'track':
    track()
elif st.session_state.tab == 'journal':
    journal()
elif st.session_state.tab == 'support':
    support()
elif st.session_state.tab == 'account':
    account()
