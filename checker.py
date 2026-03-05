import requests
from bs4 import BeautifulSoup
import smtplib
import os

url = "https://www.euro-millions.com/results"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise Exception(f"Erro HTTP: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

numbers = [n.text for n in soup.select(".result__number")][:5]
stars = [s.text for s in soup.select(".result__star")][:2]

print("Números:", numbers)
print("Estrelas:", stars)

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
DESTINO = os.environ["DESTINO"]

mensagem = f"""
Subject: Resultado Euromilhões

Números: {' '.join(numbers)}
Estrelas: {' '.join(stars)}
"""

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, PASSWORD)
server.sendmail(EMAIL, DESTINO, mensagem)
server.quit()

print("Email enviado!")
