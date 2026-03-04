import requests
import smtplib
import os
import json
from email.mime.text import MIMEText

# ==============================
# AS TUAS APOSTAS
# ==============================

bets = [
    {"numbers": [12, 13, 18, 19, 26], "stars": [4, 11]},
    {"numbers": [21, 30, 33, 45, 50], "stars": [3, 7]},
    {"numbers": [2, 10, 13, 28, 38], "stars": [2, 11]},
    {"numbers": [17, 20, 28, 41, 44], "stars": [6, 7]},
]

# ==============================
# OBTER RESULTADO REAL
# ==============================

url = "https://raw.githubusercontent.com/jcphlux/euromillions-results/master/latest.json"

response = requests.get(url)

if response.status_code != 200:
    raise Exception("Erro ao obter resultados.")

data = response.json()

draw_numbers = sorted(data["numbers"])
draw_stars = sorted(data["stars"])
jackpot = data.get("jackpot", "N/A")
draw_date = data.get("date", "N/A")

prize_data = data.get("prizes", [])
# ==============================
# FUNÇÕES
# ==============================

def check_bet(bet):
    matched_numbers = len(set(bet["numbers"]) & set(draw_numbers))
    matched_stars = len(set(bet["stars"]) & set(draw_stars))
    return matched_numbers, matched_stars

def get_prize(m_numbers, m_stars):
    for p in prize_data:
        if p["aciertos"] == f"{m_numbers}+{m_stars}":
            value = p["premio"].replace(".", "").replace(",", ".")
            return float(value)
    return 0.0

# ==============================
# PROCESSAR APOSTAS
# ==============================

total_won = 0

results_text = f"🎯 Euromilhões {draw['fecha_sorteo']}\n\n"
results_text += f"Números: {draw_numbers} ⭐ {draw_stars}\n"
results_text += f"Jackpot: {jackpot}\n\n"

for i, bet in enumerate(bets, start=1):
    m_numbers, m_stars = check_bet(bet)
    prize = get_prize(m_numbers, m_stars)
    total_won += prize
    results_text += f"Aposta {i}: {m_numbers}+{m_stars} → {prize:.2f}€\n"

results_text += f"\n💰 Total ganho esta semana: {total_won:.2f}€\n"

# ==============================
# HISTÓRICO
# ==============================

history_file = "history.json"

try:
    with open(history_file, "r") as f:
        history = json.load(f)
except:
    history = []

history.append({
    "date": draw["fecha_sorteo"],
    "won": total_won
})

with open(history_file, "w") as f:
    json.dump(history, f, indent=2)

total_acumulado = sum(item["won"] for item in history)
results_text += f"📊 Total acumulado: {total_acumulado:.2f}€\n"

# ==============================
# ENVIAR EMAIL
# ==============================

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
DESTINO = os.environ["DESTINO"]

msg = MIMEText(results_text)
msg["Subject"] = "Resultado Euromilhões"
msg["From"] = EMAIL
msg["To"] = DESTINO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)

print("Email enviado com sucesso!")
