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
    .info-box {background-color: #222; padding: 12px; border-radius: 10px; margin-top: 15px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Init state
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

# Parameters input
if not st.session_state.big_mode:
    st.title("💰 Temps = Argent V2")
    with st.container():
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        salary = st.number_input(
            "Salaire mensuel net (€)",
            min_value=0.0,
            value=st.session_state.salary,
            step=50.0,  # step ajusté à 50€
            format="%.2f"
        )
        work_days_per_month = st.number_input(
            "Jours travaillés par mois",
            min_value=1,
            value=st.session_state.work_days_per_month
        )
        hours_per_day = st.number_input(
            "Heures travaillées par jour",
            min_value=1.0,
            value=st.session_state.hours_per_day
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Save params in session state
    st.session_state.salary = salary
    st.session_state.work_days_per_month = work_days_per_month
    st.session_state.hours_per_day = hours_per_day
else:
    # Keep params in big mode
    salary = st.session_state.salary
    work_days_per_month = st.session_state.work_days_per_month
    hours_per_day = st.session_state.hours_per_day

# Calculs
seconds_per_day = hours_per_day * 3600
total_seconds_per_month = work_days_per_month * seconds_per_day
euro_per_second = salary / total_seconds_per_month
euro_per_minute = euro_per_second * 60
euro_per_hour = euro_per_second * 3600

# Ajout gain 1/2 journée, jour, semaine
half_day_seconds = seconds_per_day / 2
week_seconds = seconds_per_day * 5  # on considère 5 jours/semaine

euro_per_half_day = euro_per_second * half_day_seconds
euro_per_day = euro_per_second * seconds_per_day
euro_per_week = euro_per_second * week_seconds

if not st.session_state.big_mode:
    st.info(
        f"💡 Gains approximatifs :\n\n"
        f"- {euro_per_second:.6f} €/s\n"
        f"- {euro_per_minute:.4f} €/min\n"
        f"- {euro_per_hour:.2f} €/h\n"
        f"- {euro_per_half_day:.2f} €/½ journée\n"
        f"- {euro_per_day:.2f} €/jour\n"
        f"- {euro_per_week:.2f} €/semaine"
    )

# États
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "accumulated" not in st.session_state:
    st.session_state.accumulated = 0.0

# Boutons uniquement en mode normal
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
    st.markdown("<br>", unsafe_allow_html=True)  # espace en mode géant

# Affichage compteur
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
