'''
Plik dane.csv zawiera dane zbierane na węźle ciepłowniczym przez
przedsiębiorstwo dostarczające ciepło do budynku (patrz opisy kolumn w pliku).
Napisać skrypt w języku Python, dokonujący podstawowej analizy tych danych.
'''

# A. Wczytanie obserwacji dla wybranych zmiennych.
# B. Sprawdzenie podstawowych statystyk dla poszczególnych zmiennych. Wykreślenie histogramów.
# C. Identyfikacja zmiennych, w których występują potencjalnie błędne dane (obserwacje) lub braki danych. Naprawa danych.
# D. Obliczenie unormowanych korelacji pomiędzy poszczególnymi zmiennymi.
# E. Przeprowadzenie regresji liniowej dla wybranych zmiennych, wraz z wykresami.
# F. Wykorzystanie wyników regresji dla podstawowej predykcji wyników.

import csv
import numpy as np
import matplotlib.pyplot as plt

przeplyw = []
temp_zasilania= []
temp_powrotu= []
roznica_temp = []
moc = []
file = open("dane.csv", "rt")
data = csv.reader(file)
next(data)
for line in data:
    przeplyw.append(float(line[6]))
    temp_zasilania.append(float(line[7]))
    temp_powrotu.append(float(line[8]))
    roznica_temp.append(float(line[9]))
    moc.append(float(line[12]))
file.close()

variables = {"Przeplyw:": przeplyw, "Temperatura zasilania:": temp_zasilania,
             "Temperatura powrotu:": temp_powrotu, "Roznica temperatur:": roznica_temp,
             "Moc:": moc}

for name,variable in variables.items():
    print(f"Zmienna: {name}")
    print(f"min = {min(variable)}")
    print(f"max = {max(variable)}")
    print(f"srednia = {np.mean(variable)}")
    print(f"mediana = {np.median(variable)}")
    print(f"zakres = {np.ptp(variable)}")
    print(f"odch. std = {np.std(variable)}")
    print(f"wariancja = {np.var(variable)}")
    print(f"histogram = {np.histogram(variable)}")
    # plt.show()
    # plt.hist(variable, 10)
    print()

variables_fix = {"Przeplyw:": przeplyw,
                 "Roznica temperatur:": roznica_temp,
                 "Moc:": moc }

for name, variable in variables_fix.items():
    for i, value in enumerate(variable):
        if value > 10000:
            print(f"Anomalia dla {name} pod indeksem {i}")
            variable[i]=np.median(variable)

print("Statystyki po naprawie: ")
for name,variable in variables_fix.items():
    print(f"Zmienna: {name}")
    print(f"min = {min(variable)}")
    print(f"max = {max(variable)}")
    print(f"srednia = {np.mean(variable)}")
    print(f"mediana = {np.median(variable)}")
    print(f"zakres = {np.ptp(variable)}")
    print(f"odch. std = {np.std(variable)}")
    print(f"wariancja = {np.var(variable)}")
    print(f"histogram = {np.histogram(variable)}")
    plt.hist(variable, 10)
    plt.show()
    print()

def korelacja_unormowana(a, b):
    '''Funkcja zwraca unormowną korelację list a i b'''
    a = (a - np.mean(a)) / (np.std(a)*len(a))
    b = (b - np.mean(b)) / np.std(b)
    return np.correlate(a, b)

for name1, variable1, in variables.items():
    for name2, variable2 in variables.items():
        print(f"Korelacja miedzy {name1} a {name2}"
              f" wynosi {korelacja_unormowana(variable1, variable2)}" )


plt.plot(moc, przeplyw, ",")

a, b = np.polyfit(moc, przeplyw, 1)
print(f"wzor prostej: y = {a}*x + {b}" )

yregresja = [a*i + b for i in moc]
plt.plot(moc, yregresja)
plt.show()

moc1 = input("Podaj moc = ")
przeplyw1 = a*moc1 + b
print(f"Przeplyw = {round(przeplyw1, 2)} l/min")
