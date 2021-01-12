import math
import time
from random import *
import random
import copy
from itertools import permutations

def zakazane_miasta(liczba_miast):
#na każde 10 miast, 2 miasta są zakazane (są zamknięte w godinach podzielnych przez 3)
    dziesiatki = int(liczba_miast/10)
    zakazane = []
    mozliwosci = []
    for i in range(liczba_miast):
        mozliwosci.append(i)
    for i in range(dziesiatki):
        x = random.randrange(1, len(mozliwosci))
        while x-1 in zakazane:
            x = random.randrange(1, len(mozliwosci))
        zakazane.append(mozliwosci[x])
        mozliwosci.pop(x)
    return zakazane

def generate_city_coordinates(liczba_miast):
# tworzenie miast na podstawie ich współrzędznych X i Y
   # a = []
    #with open("wspTSP.txt") as f:
    #    a = [int(x) for x in f.read().split()]
    #f.close()
    #wsp = []
   # for i in range(0, (liczba_miast*3), 3):
   #     wsp.append((a[i + 1], a[i + 2]))
   # return wsp
    #lista = []
    #for i in range(liczba_miast):
    #    a,x, y = input().split()
    #    x1 = int(x)
    #    y1 = int(y)
    #    lista.append((x1, y1))
    axis_range = range(liczba_miast*1)
    return tuple(zip(sample(axis_range, liczba_miast), sample(axis_range, liczba_miast)))
    #return lista

def stworz_sciezke_z_ograniczeniem(liczba_miast,zakazane):
#funkcja tworzy domyślną ścierzkę, gdy i będzie podzielne przez 3 i gdy wartość jest na zakazanej pozycji,
# zamieniamy jej wartość z następną wartością
    sciezka = []
    for i in range(liczba_miast):
        sciezka.append(i)
    for i in range(1,liczba_miast):
        if i%3 == 0 and sciezka[i] in zakazane:
            pomoc = sciezka[i-1]
            sciezka[i-1] = sciezka[i]
            sciezka[i] = pomoc
    sciezka.append(sciezka[0])
    return sciezka

def oblicz_odleglosci(wsp_miast):
# obliczanie odległości pomiędzy poszczególnymi miastami, powstaje macierz symetryczna wzdłóż głównej przekątnej
    macierz_odleglosci = []
    for miasto in wsp_miast:
        odl_miast = []
        for pozostale_miasta in wsp_miast:
            distance = odleglosci(miasto[0], miasto[1], pozostale_miasta[0],pozostale_miasta[1])  # podajemy współrzędne X i Y miasta A oraz współrzędne miasta B
            odl_miast.append(distance)
        macierz_odleglosci.append(odl_miast)
    return macierz_odleglosci

def zakazane_odleglosci(odleglosci,zakazane):
    lista = list(odleglosci)
    for godzina in range(len(zakazane)):
        for miasto in range(len(lista[godzina])):
            lista[miasto][zakazane[godzina]-1] = 9999
    return lista

def odleglosci(x1, y1, x2, y2):  # odleglosci miedzy miastem A i miastem B
    old = ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    return round(math.sqrt(old), 2)

def stworz_permutacje(domyslna_droga,zakazane,liczba_miast):
#najpierw usuwamy z listy lementy zakazane
#następnie losujemy liczby z podanego zaresu, dla 0 są to liczby z listy bez zakazanych
#dla podzielnych przez 3 z listy zakazanych
#dla reszyt z listy bez zakazanych
#na koniec dodajemy pierwszy element aby komiwojażer wrócił do miasta z którego wyruszył
    permutacja = []
    lista = list(domyslna_droga)
    zakazane = list(zakazane)
    for i in range(len(zakazane)):
        lista.remove(zakazane[i])
    for i in range(liczba_miast):
        if i==0:
            x = random.randrange(0, len(lista))
            permutacja.append(lista[x])
            lista.pop(x)
        elif i%3 != 0 and len(zakazane) != 0:
            x = random.randrange(0,len(zakazane))
            permutacja.append(zakazane[x])
            zakazane.pop(x)
        else:
            x = random.randrange(0, len(lista))
            permutacja.append(lista[x])
            lista.pop(x)
    permutacja.append(permutacja[0])
    return permutacja

def losowe_liczby(liczba_miast,permutacja, zakazane):
#w tej funkcji losujemy 2 indeksy, które w dalszej cczęsci kodu zostaną zamienione miejscami
#czyli indeks X przyjmie wartość indeksu Y i na odwrót
#gdy wartości indeksów X lub Y są w liście zakazanych lub X == Y to wykonuje się tak długo aż
# X!=Y oraz wartości indeksów X i Y nie są w liście zakazanej
    x = random.randrange(0,liczba_miast-1)
    y = random.randrange(0,liczba_miast-1)
    while permutacja[x] in zakazane or permutacja[y] in zakazane or x == y:
        if x == y:
            x = random.randrange(0,liczba_miast-1)

        if permutacja[x] in zakazane:
            x = random.randrange(0,liczba_miast-1)
        elif permutacja[y] in zakazane:
            y = random.randrange(0,liczba_miast-1)

        if x != y and permutacja[x] not in zakazane and permutacja[y] not in zakazane:
            break
    return x,y

def dlugosc_sciezki(odl_miast,sciezka):
#prosta funkcjia która oblicza nam odległości pomiedzy miastami, w wygenerowannej ścieżce
    odl = 0
    start = sciezka[0]
    for i in range(len(sciezka) - 1):
        odl += odl_miast[start][sciezka[i+1]]
        start = sciezka[i+1]
    return round(odl,2)

def zachlannyTSP(liczba_miast,odl,zakaz):
    odl_zakazane = zakazane_odleglosci(odl,zakaz)
    sciezka = []
    x = random.randrange(0,liczba_miast-1)
    while x  in zakaz:
        x = random.randrange(0,liczba_miast-1)
    sciezka.append(x)
    najlepszy_dystans = 100000000
    aktualne_miasto = sciezka[0]
    for godzina in range(1, liczba_miast):
        min = 10000000
        nast = 0
        if godzina%3 == 0:
            for miasto in range(len(odl[aktualne_miasto])):
                if miasto in zakaz:
                    pass
                elif miasto not in sciezka and miasto != aktualne_miasto and odl_zakazane[aktualne_miasto][miasto] < min:
                    min = odl[aktualne_miasto][miasto]
                    nast = miasto
        else:
            for miasto in range(len(odl[aktualne_miasto])):
                if miasto not in sciezka and miasto != aktualne_miasto and odl[aktualne_miasto][miasto] < min:
                    min = odl[aktualne_miasto][miasto]
                    nast = miasto
        aktualne_miasto = nast
        sciezka.append(nast)
    sciezka.append(sciezka[0])
    najlepszy_dystans = dlugosc_sciezki(odl,sciezka)
    return sciezka,najlepszy_dystans

def tabuserchTSP(liczba_miast, odl_miast, domyslna_droga, zakazane):
    iteracje = 100000  # ilosc iteracji algorytmu TABU
    najlepsza_droga = list(domyslna_droga)
    najlepsza_odleglosc = dlugosc_sciezki(odl_miast, domyslna_droga)
    domyslna_droga.pop()
    drogi_TABU = []  # przechowuje dnajlepsze sciezki
    kandydat = stworz_permutacje(domyslna_droga, zakazane, liczba_miast)
    for losowa in range(15):
        nowy_kandydat = stworz_permutacje(domyslna_droga, zakazane, liczba_miast)
        if dlugosc_sciezki(odl_miast, kandydat) > dlugosc_sciezki(odl_miast, nowy_kandydat):
            kandydat = nowy_kandydat
    permutacja = list(kandydat)
    drogi_TABU.append(permutacja)
    for i in range(iteracje):
        wartosci = losowe_liczby(liczba_miast, permutacja,zakazane)
        g = wartosci[0]
        j = wartosci[1]
        permutacja[g], permutacja[j] = permutacja[j], permutacja[g]
        ost = int(len(permutacja)) - 1
        permutacja[ost] = permutacja[0]
        aktualna_odl = dlugosc_sciezki(odl_miast, permutacja)
        dodaj = list(permutacja)
        if aktualna_odl < dlugosc_sciezki(odl_miast, kandydat):
            kandydat = dodaj
        if dodaj not in drogi_TABU:
            if (len(drogi_TABU) < 5):
                drogi_TABU.append(dodaj)
            elif (len(drogi_TABU) == 5):
                drogi_TABU.pop(0)
                drogi_TABU.append(dodaj)
    if dlugosc_sciezki(odl_miast, kandydat) < najlepsza_odleglosc:
        najlepsza_droga = kandydat
        najlepsza_odleglosc = dlugosc_sciezki(odl_miast, kandydat)
    return najlepsza_droga, najlepsza_odleglosc

def main():
    liczba_miast = int(input("Podaj liczbe miast: "))
    for i in range(1):
        zakazane = []
       # zakazane = zakazane_miasta(liczba_miast)
        wsp_miast1 = generate_city_coordinates(liczba_miast)
    #    print(zakazane)
        wsp_miast = list(wsp_miast1)
        domyslna_droga = stworz_sciezke_z_ograniczeniem(liczba_miast,zakazane)
        odl_miast = oblicz_odleglosci(wsp_miast)  # wszystkie odleglosc
        for i in range(liczba_miast):
            print(odl_miast[i])
    #    print("domyslna:",dlugosc_sciezki(odl_miast,domyslna_droga))
    #    start = time.time()
    #    zachlanny = zachlannyTSP(liczba_miast,odl_miast,zakazane)
    #    koniec = time.time()
    #    print("scieżka zachlanna: ",zachlanny[0])
    #    print("sciezka dla zachlannego:",zachlanny[1])
    #    print("czas dla zachlannego: ",koniec - start)
    #    start1 = time.time()
    #    tabuTSP = tabuserchTSP(liczba_miast,odl_miast,domyslna_droga,zakazane)
    #    koniec1 = time.time()
    #    print("Najoptymalniejsza sciezka metodą Tabu Search: ", tabuTSP[0])
    #    print("Jej dlugosc wynosi:", tabuTSP[1])
    #    print("czas dla Tabu: ",koniec1 - start1)
    #    print("\n")
main()