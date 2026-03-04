import requests
from bs4 import BeautifulSoup
import smtplib
import os
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
# OBTER RESULTADOS VIA SCRAPING
# ==============================

url = "https://www.euro-millions.com/results"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise Exception(f"Erro HTTP: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# Extrair números principais
numbers = soup.select(".balls .ball")
draw_numbers = sorted([int(n.text) for n in numbers[:5]])

# Extrair estrelas
stars = soup.select(".balls .lucky-star")
draw_stars = sorted([int(s.text) for s in stars[:2]])

draw_date = soup.select_one(".draw-date").text.strip()

# ==============================
# VERIFICAR APOSTAS
# ==============================

def check_bet(bet):
    matched_numbers = len(set(bet["numbers"]) & set(draw_numbers))
    matched_stars = len(set(bet["stars"]) & set(draw_stars))
    return matched_numbers, matched_stars

results_text = f"🎯 Euromilhões {draw_date}\n\n"
results_text += f"Números sorteados: {draw_numbers} ⭐ {draw_stars}\n\n"

for i, bet in enumerate(bets, start=1):
    m_numbers, m_stars = check_bet(bet)
    results_text += f"Aposta {i}: {m_numbers} números + {m_stars} estrelas\n"

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
