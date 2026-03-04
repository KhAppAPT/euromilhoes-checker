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

url = "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&limit=1"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
data = response.json()
draw = data["data"][0]

combinacion = draw["combinacion"].split()
draw_numbers = sorted([int(n) for n in combinacion[:5]])
draw_stars = sorted([int(n) for n in combinacion[5:]])

prize_data = draw["premios"]
jackpot = draw.get("bote", "N/A")

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
            value = p["premio"]
            value = value.replace(".", "").replace(",", ".")
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
results_text += f"\n📊 Total acumulado: {total_acumulado:.2f}€"

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

print("Email enviado com sucesso!")for i, bet in enumerate(bets, start=1):
    m_numbers, m_stars = check_bet(bet)
    results_text += f"Aposta {i}: {m_numbers} números e {m_stars} estrelas\n"

# ==============================
# ENVIAR EMAIL
# ==============================

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
DESTINO = os.environ["DESTINO"]

msg = MIMEText(results_text)
msg["Subject"] = "Teste Euromilhões"
msg["From"] = EMAIL
msg["To"] = DESTINO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)

print("Email enviado com sucesso!")
