import streamlit as st
import time

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

st.set_page_config(page_title="Temps = Argent", page_icon="💰", layout="centered")

st.markdown(
    """
    <style>
    body {background-color: #111; color: #eee;}
    .big-metric {font-size: 64px; font-weight: bold; color: #4CAF50;}
    .small-label {font-size: 20px; color: #aaa;}
    .param-box {background-color: #222; padding: 10px; border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)

# State init
if "big_mode" not in st.session_state:
    st.session_state.big_mode = False
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "accumulated" not in st.session_state:
    st.session_state.accumulated = 0.0
if "salary" not in st.session_state:
    st.session_state.salary = 2000.0
if "work_days_per_month" not in st.session_state:
    st.session_state.work_days_per_month = 22
if "hours_per_day" not in st.session_state:
    st.session_state.hours_per_day = 8.0

# Toggle big mode
if st.button("🖥️ Activer / Désactiver mode compteur géant"):
    st.session_state.big_mode = not st.session_state.big_mode

# Calculs
salary = st.session_state.salary
work_days_per_month = st.session_state.work_days_per_month
hours_per_day = st.session_state.hours_per_day

if not st.session_state.big_mode:
    st.title("💰 Temps = Argent")
    with st.container():
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        salary = st.number_input("Salaire mensuel net (€)", min_value=0.0, value=salary, step=100.0)
        work_days_per_month = st.number_input("Jours travaillés par mois", min_value=1, value=work_days_per_month)
        hours_per_day = st.number_input("Heures travaillées par jour", min_value=1.0, value=hours_per_day)
        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.salary = salary
    st.session_state.work_days_per_month = work_days_per_month
    st.session_state.hours_per_day = hours_per_day

seconds_per_day = hours_per_day * 3600
total_seconds_per_month = work_days_per_month * seconds_per_day
euro_per_second = salary / total_seconds_per_month
euro_per_minute = euro_per_second * 60
euro_per_hour = euro_per_second * 3600

if not st.session_state.big_mode:
    st.info(f"💡 Tu gagnes environ **{euro_per_second:.6f} €/s**, **{euro_per_minute:.4f} €/min**, **{euro_per_hour:.2f} €/h**.")

# Boutons (seulement en mode normal)
if not st.session_state.big_mode:
    col1, col2, col3 = st.columns(3)
    if col1.button("▶️ Lancer / Reprendre"):
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.start_time = time.time()

    if col2.button("⏸️ Pause"):
        if st.session_state.running:
            elapsed = time.time() - st.session_state.start_time
            st.session_state.accumulated += elapsed
            st.session_state.running = False

    if col3.button("🔄 Reset"):
        st.session_state.running = False
        st.session_state.start_time = 0.0
        st.session_state.accumulated = 0.0
else:
    st.markdown("<br>", unsafe_allow_html=True)  # un peu d'espace

# Affichage compteur unique
placeholder = st.empty()

def display_counter(total_elapsed, total_earned):
    formatted_time = format_time(total_elapsed)
    placeholder.markdown(
        f"""
        <div class='small-label'>Temps écoulé</div>
        <div class='big-metric'>{formatted_time}</div>
        <div class='small-label'>💶 Gain estimé</div>
        <div class='big-metric'>{total_earned:.4f} €</div>
        """,
        unsafe_allow_html=True
    )

# Boucle temps réel
while st.session_state.running:
    elapsed = time.time() - st.session_state.start_time
    total_elapsed = st.session_state.accumulated + elapsed
    total_earned = total_elapsed * euro_per_second
    display_counter(total_elapsed, total_earned)
    time.sleep(1)

if not st.session_state.running:
    total_elapsed = st.session_state.accumulated
    total_earned = total_elapsed * euro_per_second
    display_counter(total_elapsed, total_earned)
