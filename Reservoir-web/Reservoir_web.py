import sqlite3
from sqlite3 import Error
import PySimpleGUIWeb as sg
from datetime import date
import pandas as pd

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=10)
        return conn
    except Error as e:
        print(e)
    return conn

def executeSQLcommand(db, SQLcommand):
    c = db.cursor()
    c.execute(SQLcommand)
    rows = c.fetchall()
    return rows

def executeSQLrez(db, SQLcommand):
    c = db.cursor()
    com = '''INSERT INTO Rezerwacja(Pokoj_hotelowyId_pokoju, UzytkownikId_uzytkownika, Termin_rozpoczecia, Termin_zakonczenia) 
VALUES (?, ?, ?, ?)'''
    c.execute(com, SQLcommand)
    return c.lastrowid     

def executeSQLwyp(db, SQLcommand):
    c = db.cursor()
    com = '''INSERT INTO Wyposazenie_Rezerwacja(WyposazenieId_wyposazenia, RezerwacjaId_rezerwacji) 
VALUES (?, ?)'''
    c.execute(com, SQLcommand)
    return

def executeSQLwyz(db, SQLcommand):
    c = db.cursor()
    com = '''INSERT INTO Wyzywienie_Rezerwacja(WyzywienieId_pakietu, RezerwacjaId_rezerwacji) 
VALUES (?, ?)'''
    c.execute(com, SQLcommand)
    return   

def executeSQLuzyt(db, SQLcommand):
    c = db.cursor()
    com = '''INSERT INTO Uzytkownik(RolaId_roli, Login, Haslo, Imie, Nazwisko, Nr_telefonu, Email, KlientCzyPracownik) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    c.execute(com, SQLcommand)
    return c.lastrowid

def executeSQLadres(db, SQLcommand):
    c = db.cursor()
    com = '''INSERT INTO Adres(Miasto, Ulica, Kod_pocztowy, Nr_budynku, Nr_mieszkania, KontoId_konta) 
VALUES (?, ?, ?, ?, ?, ?)'''
    c.execute(com, SQLcommand)
    return c.lastrowid

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

database = r'F:/Desktop/IV semestr/Inżynieria oprogramowania/Reservoir/database/reservoir.db'
db = create_connection(database)

#####################################################################################
logowanie = [ [sg.Text('Witaj w Reservoir!')],
                [sg.Text('Wprowadź swój login oraz hasło')],
                [sg.Text('Login:   '), sg.InputText(key='login')],
                [sg.Text('Hasło:   '), sg.InputText(key='haslo')],
                [sg.Button('Zaloguj się'), sg.Button('Załóż konto')]]
window = sg.Window('Reservoir').Layout(logowanie)

while True:
    event, values = window.read()

    if event == 'Zaloguj się':
        com = 'SELECT Login, Haslo, RolaId_roli FROM Uzytkownik WHERE (Login="{}" AND Haslo="{}");'.format(values['login'],values['haslo'])
        login = values['login']
        konto = executeSQLcommand(db, com)
        if len(konto) == 0:
            sg.Popup('Nieprawidłowe dane!')
        else:
            if konto[0][2] == 1:
                m_klient = [ [sg.Text('Witaj w Reservoir - module obsługi klientów!')],
                [sg.Button('Dokonaj rezerwacji')],
                [sg.Button('Wyloguj się')]
                ]
                klient = sg.Window('Moduł klienta').Layout(m_klient)
                while True:
                    event, values = klient.read()
                    if event == 'Dokonaj rezerwacji':
                        terminy = [[sg.Text('Data rezerwacji:   '), sg.InputText(key='data')],
                  [sg.Text("Czas trwania pobytu (w dniach):   "), sg.InputText(key='dni')],
                  [sg.Button('Sprawdź wolne terminy'), sg.Button('Anuluj')]]
                        termin = sg.Window('Wybór terminu').Layout(terminy)
                        while True:
                            event, values = termin.read()
                            if event == sg.WIN_CLOSED:
                                break
                            if event == 'Anuluj':
                                termin.close()
                                break
                            if event == 'Sprawdź wolne terminy':
                                if len(values['dni']) < 1 or len(values['data']) < 1:
                                    sg.Popup('Wprowadź poprawne dane!')
                                    values['dni'] = 0
                                today = date.today().strftime("%Y-%m-%d")
                                today = pd.to_datetime(today)
                                check = str(pd.to_datetime(values['data']) - today)[0]
                                if int(values['dni']) < 1:
                                    sg.Popup('Wprowadź poprawną liczbę dni!')
                                elif check == '-':
                                    sg.Popup('Wprowadź poprawną datę!')
                                else:
                                    com = '''SELECT Pokoj_hotelowy.Id_pokoju FROM Pokoj_hotelowy, Rezerwacja 
    WHERE Pokoj_hotelowy.Id_pokoju NOT IN (SELECT Pokoj_hotelowyId_pokoju FROM Rezerwacja WHERE date('{}', '+{} day') BETWEEN Termin_rozpoczecia and Termin_zakonczenia)
    ORDER BY Pokoj_hotelowy.Nr_pokoju ASC'''
                                    pokoje = []
                                    for i in range(0, int(values['dni'])):
                                        pokoje.append(executeSQLcommand(db, com.format(str(values['data']), i)))
                                    for i in range(1, len(pokoje)):
                                        pokoje[0] = intersection(pokoje[0],pokoje[i])
                                    pok = []
                                    for x in pokoje[0]:
                                        if x not in pok:
                                            pok.append(x)
                                    wolne = []
                                    for i in range(0, len(pok)):
                                        wolne.append(pok[i][0])
                                    wolne = tuple(wolne)
                                    com = """SELECT Pokoj_hotelowy.Nr_pokoju, Typ_pokoju.Nazwa_typu, Pietro.Nr_pietra, Pietro.Obiekt_hotelowyId_obiektu FROM Pokoj_hotelowy, Pietro, Typ_pokoju
                    WHERE Pokoj_hotelowy.Id_pokoju IN {}
                    AND Pokoj_hotelowy.PietroId_pietra=Pietro.Id_pietra AND Pokoj_hotelowy.Typ_pokojuId_typu=Typ_pokoju.Id_typu
                    ORDER BY Pokoj_hotelowy.Nr_pokoju ASC""".format(wolne)
                                    pokoje = executeSQLcommand(db, com)

                                    rezerwacja = ([[sg.Text('Data rezerwacji:   '), sg.Text(values['data'])],
                 [sg.Text("Czas trwania pobytu (w dniach):   "), sg.Text(values['dni'])],
                 [sg.Text('Wolne pokoje (nr.pok - typ - piętro - budynek):   '),sg.InputCombo(pokoje,key='pokoj')],
                 [sg.Text('Dodatkowe wyposażenie:   ')],
                 [sg.Checkbox('Szlafrok', key='szlafrok'), sg.Checkbox('Bamboszki', key='bamboszki')],
                 [sg.Text('Pakiety wyżywieniowe:   ')],
                 [sg.Checkbox('Śniadania', key='sniadania'), sg.Checkbox('Obiady', key='obiady')],
                 [sg.Checkbox('Obiadokolacje', key='obiadokolacje'), sg.Checkbox('Kolacje',key='kolacje')],
                 [sg.Button('Zarezerwuj'), sg.Button('Anuluj')]])
                                    dni = int(values['dni'])
                                    data = values['data']
                                    rez = sg.Window('Dokonaj rezerwacji').Layout(rezerwacja)
                                    for i in range(0,len(pokoje)):
                                        pokoje[i] = str(pokoje[i])
                                    while True:
                                        event, values = rez.read()
                                        if event == sg.WIN_CLOSED:
                                            break
                                        if event == 'Anuluj':
                                            rez.close()
                                            break
                                        if event == 'Zarezerwuj':
                                            kwota = 0
                                            uzyt = executeSQLcommand(db,'SELECT Id_uzytkownika FROM Uzytkownik WHERE Login="{}"'.format(login))
                                            uzyt = int(uzyt[0][0])
                                            num = int(dni) - 1
                                            num = executeSQLcommand(db, 'SELECT date("{}", "+{} days")'.format(data, num))[0][0]
                                            index = pokoje.index(values['pokoj'])
                                            r = (wolne[index],uzyt, data, num)
                                            with db:
                                                idr = executeSQLrez(db, r)
                                                if values['szlafrok'] == True:
                                                    executeSQLwyp(db, (1, idr))
                                                if values['bamboszki'] == True:
                                                    executeSQLwyp(db, (2, idr))
                                                if values['sniadania'] == True:
                                                    executeSQLwyz(db, (1, idr))
                                                if values['obiady'] == True:
                                                    executeSQLwyz(db, (2, idr))
                                                if values['kolacje'] == True:
                                                    executeSQLwyz(db, (3, idr))
                                                if values['obiadokolacje'] == True:
                                                    executeSQLwyz(db, (4, idr))
                                            kwota += executeSQLcommand(db, '''SELECT (Typ_pokoju.Cena*{}) FROM Typ_pokoju, Rezerwacja, Pokoj_hotelowy
    WHERE Typ_pokoju.Id_typu=Pokoj_hotelowy.Typ_pokojuId_typu AND Pokoj_hotelowy.Id_pokoju=Rezerwacja.Pokoj_hotelowyId_pokoju
    AND Rezerwacja.Id_rezerwacji={};'''.format(dni,idr))[0][0]
                                            kwota += executeSQLcommand(db, '''SELECT (sum(Wyzywienie.Cena)*{}) FROM Wyzywienie, Rezerwacja, Wyzywienie_Rezerwacja
    WHERE Wyzywienie.Id_pakietu=Wyzywienie_Rezerwacja.WyzywienieId_pakietu AND Wyzywienie_Rezerwacja.RezerwacjaId_rezerwacji=Rezerwacja.Id_rezerwacji
    AND Rezerwacja.Id_rezerwacji={};'''.format(dni,idr))[0][0]
                                            kwota += executeSQLcommand(db, '''SELECT sum(Wyposazenie.Cena) FROM Wyposazenie, Rezerwacja, Wyposazenie_Rezerwacja
    WHERE Wyposazenie.Id_wyposazenia=Wyposazenie_Rezerwacja.WyposazenieId_wyposazenia AND Wyposazenie_Rezerwacja.RezerwacjaId_rezerwacji=Rezerwacja.Id_rezerwacji
    AND Rezerwacja.Id_rezerwacji={};'''.format(idr))[0][0]
                                            sg.PopupGetText('Podsumowanie','''Dodano rezerwację!
Dane do wykonania przelewu:
	Odbiorca: Hotel Testowy
	Nr. konta: 11 2222 3333 4444 5555 6666 7777
	Tytuł przelewu: REZERWACJA_{}
	Kwota do zapłaty: {} PLN'''.format(idr, kwota),size=(40,8))
                                            rez.close()
                                            break
                                termin.close()
                                break

                    if event == sg.WIN_CLOSED:
                        break
                    if event == 'Wyloguj się':
                        klient.close()
                        break
    if event == 'Załóż konto':
        k_klienta = [[sg.Text('Imie:   '), sg.InputText(key='imie')],
                     [sg.Text('Nazwisko:   '), sg.InputText(key='nazwisko')],
                     [sg.Text('Miasto:   '), sg.InputText(key='miasto')],
                     [sg.Text('Ulica:   '), sg.InputText(key='ulica')],
                     [sg.Text('Kod pocztowy:   '), sg.InputText(key='kod_p')],
                     [sg.Text('Nr. budynku:   '), sg.InputText(key='nr_b')],
                     [sg.Text('Nr. mieszkania:   '), sg.InputText(key='nr_m')],
                     [sg.Text('Nr. telefonu:   '), sg.InputText(key='tel')],
                     [sg.Text('Adres E-mail:   '), sg.InputText(key='email')],
                     [sg.Text('Login:   '), sg.InputText(key='login')],
                     [sg.Text('Hasło:   '), sg.InputText(key='haslo')],
                     [sg.Text('Powtórz hasło:   '), sg.InputText(key='p_haslo')],
                     [sg.Button('Utwórz konto'), sg.Button('Anuluj')]]
        k_k = sg.Window('Tworzenie konta klienta').Layout(k_klienta)
        while True:
            event, values = k_k.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'Anuluj':
                k_k.close()
                break
            if event == 'Utwórz konto':
                if values['haslo'] != values['p_haslo']:
                    sg.Popup('Hasła nie są zgodne!')
                if len(executeSQLcommand(db,'SELECT Login, Email FROM Uzytkownik WHERE (Login="{}" AND Email="{}");'.format(values['login'],values['email']))) != 0:
                    sg.Popup('Użytkownik już istnieje!')
                else:
                    temp = (1, values['login'], values['haslo'], values['imie'], values['nazwisko'], values['tel'], values['email'], 0)
                    with db:
                        idu = executeSQLuzyt(db, temp)
                        ad = (values['miasto'], values['ulica'], values['kod_p'], int(values['nr_b']), int(values['nr_m']), idu)
                        ida = executeSQLadres(db,ad)
                    if idu > 0 and ida > 0:
                        sg.Popup('Użytkownik został utworzony!')
                    else:
                        sg.Popup('Użytkownik nie został utworzony!')
                    k_k.close()
                    break
    if event == sg.WIN_CLOSED:
        break

window.close()

