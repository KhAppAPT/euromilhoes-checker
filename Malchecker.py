import requests
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

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
# Buscar resultado Euromilhões
# ==============================

url = "https://euromillions.api.pedromealha.dev/latest"

response = requests.get(url)
data = response.json()

draw_numbers = data["numbers"]
draw_stars = data["stars"]

# ==============================
# Função para contar acertos
# ==============================

def check_bet(bet):
    matched_numbers = len(set(bet["numbers"]) & set(draw_numbers))
    matched_stars = len(set(bet["stars"]) & set(draw_stars))
    return matched_numbers, matched_stars

results_text = f"Sorteio de {datetime.now().strftime('%d/%m/%Y')}\n\n"
results_text += f"Números sorteados: {draw_numbers} + {draw_stars}\n\n"

total_hits = 0

for i, bet in enumerate(bets, start=1):
    m_numbers, m_stars = check_bet(bet)
    results_text += f"Aposta {i}: {m_numbers} números e {m_stars} estrelas\n"
    total_hits += m_numbers

results_text += "\nVerifica no site oficial o valor exato do prémio.\n"

# ==============================
# Enviar Email
# ==============================

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
DESTINO = os.environ["DESTINO"]

msg = MIMEText(results_text)
msg["Subject"] = "Resultado Euromilhões - Sexta-feira"
msg["From"] = EMAIL
msg["To"] = DESTINO

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)

print("Email enviado com sucesso!")
