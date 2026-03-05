bets = [
    {"nums": [12,13,18,19,26], "stars": [4,11]},
    {"nums": [21,30,33,45,50], "stars": [3,7]},
    {"nums": [2,10,13,28,38], "stars": [2,11]},
    {"nums": [17,20,28,41,44], "stars": [6,7]},
]

print("Introduz os números sorteados:")

numeros = list(map(int, input("5 números (separados por espaço): ").split()))
estrelas = list(map(int, input("2 estrelas (separadas por espaço): ").split()))

print("\nResultado do sorteio:")
print("Números:", numeros)
print("Estrelas:", estrelas)

print("\nResultados das apostas:\n")

for i, bet in enumerate(bets, start=1):

    acertos_nums = len(set(bet["nums"]) & set(numeros))
    acertos_stars = len(set(bet["stars"]) & set(estrelas))

    print(f"Aposta {i}")
    print("Acertos números:", acertos_nums)
    print("Acertos estrelas:", acertos_stars)

    if acertos_nums >= 2:
        print("👉 Possível prémio!")

    print()
