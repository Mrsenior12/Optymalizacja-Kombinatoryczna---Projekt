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
        x = random.randrange(0, len(mozliwosci))
        while x-1 in zakazane:
            x = random.randrange(0, len(mozliwosci))
        zakazane.append(mozliwosci[x])
        mozliwosci.pop(x)
    return zakazane

def generate_city_coordinates(liczba_miast):
# tworzenie miast na podstawie ich współrzędznych X i Y
    lista = []
    for i in range(liczba_miast):
        a,x, y = input().split()
        x1 = int(x)
        y1 = int(y)
        lista.append((x1, y1))
    #axis_range = range(liczba_miast*1)
    #return tuple(zip(sample(axis_range, liczba_miast), sample(axis_range, liczba_miast)))
    return lista

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

def sciezka_bez(liczba_miast):
    sciezka = []
    for i in range(liczba_miast):
        sciezka.append(i)
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

def odleglosci(x1, y1, x2, y2):  # odleglosci miedzy miastem A i miastem B
    old = ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    return round(math.sqrt(old), 2)

def stworz_permutacje(domyslna_droga,zakazane,liczba_miast):
#tworzymy permutacje równą ilości miast
#najpierw usuwamy z listy lementy zakazane
#następnie losujemy liczby z podanego zaresu, dla 0 są to liczby z listy bez zakazanych
#dla podzielnych przez 3 z listy zakazanych
#dla reszyt z listy bez zakazanych
#na koniec dodajemy pierwszy element aby komiwojażer wrócił do miasta z którego wyruszył
    permutacja = []
    lista = copy.deepcopy(domyslna_droga)
    zakazane = copy.deepcopy(zakazane)
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
   # print(sciezka)
    for i in range(len(sciezka) - 1):
        odl += odl_miast[start][sciezka[i+1]]
        start = sciezka[i+1]
    return round(odl,2)

def zachlannyTSP(liczba_miast,odl,zakaz):
    wszystki = []
    najlepszy_dystans = 100000000
    for a in range(liczba_miast):
        sciezka = []
        if a not in zakaz:
            sciezka.append(a)
            aktualne_miasto = sciezka[0]
            for i in range(1,liczba_miast):
                min = 10000000
                nast = 0
                for j in range(len(odl[aktualne_miasto])):
                    if i%3 == 0 and j in zakaz:
                        pass
                    elif j not in sciezka and j != aktualne_miasto and odl[aktualne_miasto][j] < min:
                        min = odl[aktualne_miasto][j]
                        nast = j
                aktualne_miasto = nast
                sciezka.append(nast)
            sciezka.append(sciezka[0])
            x = dlugosc_sciezki(odl,sciezka)
            if x < najlepszy_dystans:
                wszystki = sciezka
                najlepszy_dystans = x
    return wszystki,najlepszy_dystans

def tabuserchTSP(liczba_miast,odl_miast,domyslna_droga,zakazane):
        iteracje = 100000  # ilosc iteracji algorytmu TABU
        najlepsza_droga = domyslna_droga.copy()
        najlepsza_odleglosc = dlugosc_sciezki(odl_miast, domyslna_droga)
        domyslna_droga.pop()
        drogi_TABU = []  # przechowuje dnajlepsze sciezki
        wartosci_TABU = []
        permutacja = stworz_permutacje(domyslna_droga, zakazane, liczba_miast)
        for losowa in range(15):
            nowy_kandydat = stworz_permutacje(domyslna_droga,zakazane,liczba_miast)
            if dlugosc_sciezki(odl_miast, permutacja) > dlugosc_sciezki(odl_miast, nowy_kandydat):
                permutacja = nowy_kandydat
        if dlugosc_sciezki(odl_miast, permutacja) < najlepsza_odleglosc:
            drogi_TABU.append(permutacja)
            wartosci_TABU.append(dlugosc_sciezki(odl_miast, permutacja))
        for i in range(iteracje):
            wartosci = losowe_liczby(liczba_miast,permutacja,zakazane) # pętla ma na celu zmianę wartości zmiennej J gdyby zmienna J była równa zmiennej G
            g = wartosci[0]
            j = wartosci[1]
            permutacja[g], permutacja[j] = permutacja[j], permutacja[g]
            ost = int(len(permutacja)) - 1
            permutacja[ost] = permutacja[0] # dodanie do końcca listy nową liste ze zmienionymi 2 elementami
            aktualna_odl = dlugosc_sciezki(odl_miast, permutacja)
            if (len(drogi_TABU) < 5):
                drogi_TABU.append(permutacja)                    # dodanie do tablicy tabu kombinacji przejść między miastami
                wartosci_TABU.append(aktualna_odl)                           # dodanie do tablicy Tabu otrzymanej długości ścieżki
            elif (len(drogi_TABU) == 5 and aktualna_odl < max(wartosci_TABU)):     # żeby ułatwić analize ograniczamy tablicę tabu i tabuval do 5 elementów,
                if permutacja in drogi_TABU:# if się wykona wtedy i tylko wtedy gdy tabu jest == 5 oraz wartość ścieżki jest mniejsza od maxa w obecnej tablicy wartości tabu,
                    pass                                    # gdy nowowygenerowana tablica ze ściężką jest już w tablicy tabu przeskakujemy do nowej generacji
                else:                                       # w przeciwnym wypadku sprawdzamy jaki indeks ma największa wartość w tablicy wartości, a następnie zamieniamy wartości
                    poz = wartosci_TABU.index(max(wartosci_TABU))
                    drogi_TABU[poz] = permutacja
                    wartosci_TABU[poz] = aktualna_odl
        optpoz = wartosci_TABU.index(min(wartosci_TABU))
        najlepsza_odleglosc = wartosci_TABU[optpoz]
        najlepsza_droga = drogi_TABU[optpoz]
  #      wyniki.append((drogi_TABU[optpoz], wartosci_TABU[optpoz]))
 #   for i in range(len(wyniki)):
 #       if wyniki[i][1] < najlepsza_odleglosc:
 #           najlepsza_droga = wyniki[i][0]
 #           najlepsza_odleglosc = wyniki[i][1]
        return najlepsza_droga,najlepsza_odleglosc

def main():
        liczba_miast = int(input("Podaj liczbe miast: "))
        caly = time.time()
        zakazane = []
        #zakazane = zakazane_miasta(liczba_miast)
        print(len(zakazane))
        #zakazane = [
        wsp_miast1 = generate_city_coordinates(liczba_miast)
        print(zakazane)
    #for i in range(1):
        wsp_miast = copy.deepcopy(wsp_miast1)
        domyslna_droga = stworz_sciezke_z_ograniczeniem(liczba_miast,zakazane)
        # domyslna_droga = sciezka_bez(liczba_miast)
        odl_miast = oblicz_odleglosci(wsp_miast)  # wszystkie odleglosc
        # for i in range(liczba_miast):
        #     print(wsp_miast[i])
        print(dlugosc_sciezki(odl_miast,domyslna_droga))
        start = time.time()
        zachlanny = zachlannyTSP(liczba_miast,odl_miast,zakazane)
        koniec = time.time()
        print(zachlanny[0],zachlanny[1])
        print("czas dla zachlannego: ",koniec - start)
        start1 = time.time()
        tabuTSP = tabuserchTSP(liczba_miast,odl_miast,domyslna_droga,zakazane)
        koniec1 = time.time()
        print("Najoptymalniejsza sciezka metodą Tabu Search: ", tabuTSP[0])
        print("Jej dlugosc wynosi:", tabuTSP[1])
        print("czas dla Tabu: ",koniec1 - start1)
        print("\n")
        cccc=time.time()
        print("proigram dzialal przez: ",cccc-caly)

main()