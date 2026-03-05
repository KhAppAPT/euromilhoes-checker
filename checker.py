import sys

bets = [
    {"nums":[12,13,18,19,26],"stars":[4,11]},
    {"nums":[21,30,33,45,50],"stars":[3,7]},
    {"nums":[2,10,13,28,38],"stars":[2,11]},
    {"nums":[17,20,28,41,44],"stars":[6,7]},
]

if len(sys.argv) != 8:
    print("Uso: python checker.py n1 n2 n3 n4 n5 e1 e2")
    exit()

draw_numbers = list(map(int, sys.argv[1:6]))
draw_stars = list(map(int, sys.argv[6:8]))

print("Números sorteados:", draw_numbers)
print("Estrelas:", draw_stars)

for i, bet in enumerate(bets, start=1):

    matched_numbers = len(set(bet["nums"]) & set(draw_numbers))
    matched_stars = len(set(bet["stars"]) & set(draw_stars))

    print(f"\nAposta {i}")
    print("Números acertados:", matched_numbers)
    print("Estrelas acertadas:", matched_stars)
