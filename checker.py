import requests
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
# OBTER RESULTADOS VIA API
# ==============================

API_KEY = os.environ["API_KEY"]

url = f"https://api.the-odds-api.com/v4/lotteries/euromillions/results/?apiKey={API_KEY}"

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Erro API: {response.status_code}")

data = response.json()

# Ajustar conforme estrutura real devolvida
latest = data[0]

draw_numbers = sorted(latest["numbers"])
draw_stars = sorted(latest["stars"])
draw_date = latest["date"]
jackpot = latest.get("jackpot", "N/A")

# ==============================
# PROCESSAR APOSTAS
# ==============================

def check_bet(bet):
    matched_numbers = len(set(bet["numbers"]) & set(draw_numbers))
    matched_stars = len(set(bet["stars"]) & set(draw_stars))
    return matched_numbers, matched_stars

total_won = 0

results_text = f"🎯 Euromilhões {draw_date}\n\n"
results_text += f"Números: {draw_numbers} ⭐ {draw_stars}\n"
results_text += f"Jackpot: {jackpot}\n\n"

for i, bet in enumerate(bets, start=1):
    m_numbers, m_stars = check_bet(bet)
    results_text += f"Aposta {i}: {m_numbers}+{m_stars}\n"

results_text += "\n(Verifica o valor do prémio no site oficial)"

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

print("Processo concluído.")
        combinacion = draw["combinacion"].split()
        numbers = sorted([int(n) for n in combinacion[:5]])
        stars = sorted([int(n) for n in combinacion[5:]])

        return {
            "date": draw["fecha_sorteo"],
            "numbers": numbers,
            "stars": stars,
            "jackpot": draw.get("bote", "N/A"),
            "prizes": draw.get("premios", [])
        }, None

    except Exception as e:
        return None, str(e)

# ==============================
# OBTER RESULTADO
# ==============================

draw_data, error = get_results()

if error:
    results_text = "⚠️ ERRO AO OBTER RESULTADOS\n\n" + error
else:
    draw_numbers = draw_data["numbers"]
    draw_stars = draw_data["stars"]
    jackpot = draw_data["jackpot"]
    prize_data = draw_data["prizes"]

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

    total_won = 0

    results_text = f"🎯 Euromilhões {draw_data['date']}\n\n"
    results_text += f"Números: {draw_numbers} ⭐ {draw_stars}\n"
    results_text += f"Jackpot: {jackpot}\n\n"

    for i, bet in enumerate(bets, start=1):
        m_numbers, m_stars = check_bet(bet)
        prize = get_prize(m_numbers, m_stars)
        total_won += prize
        results_text += f"Aposta {i}: {m_numbers}+{m_stars} → {prize:.2f}€\n"

    results_text += f"\n💰 Total ganho: {total_won:.2f}€"

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

print("Processo concluído.")
