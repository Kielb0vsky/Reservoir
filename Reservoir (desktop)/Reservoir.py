from functools import partial
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msb
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    # create a database connection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=10)
        return conn
    except Error as e:
        print(e)
    return conn

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

class GUI:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        master.title("Reservoir")

        self.tekst = tk.Label(master, text='''Witaj w systemie obsługi hoteli "RESERVOIR" !
        Wprowadź swój login oraz hasło''',height = 3)

        self.login = tk.Entry(master)
        self.login_tekst = tk.Label(master, text="Login:   ")

        self.haslo = tk.Entry(master)
        self.haslo_text = tk.Label(master, text = "Hasło:   ")

        self.log = partial(self.logowanie, master, db)
        self.zaloguj_sie = tk.Button(master, text="Zaloguj się", command=self.log)

        self.zamknij = tk.Button(master, text="Wyjdź", command=master.destroy)

        self.tekst.grid(column=1, row = 0)
        self.login_tekst.grid(column=0, row = 1, sticky=tk.E)
        self.login.grid(column=1, row=1)
        self.haslo_text.grid(column=0, row=2,sticky=tk.E)
        self.haslo.grid(column=1, row=2)
        self.zaloguj_sie.grid(column = 1, row = 3, padx=5, pady=5)
        self.zamknij.grid(column=1, row = 4, padx=5, pady=5)

    def logowanie(self, master, db):
        l = self.login.get()
        h = self.haslo.get()
        self.login.delete(0, tk.END)
        self.haslo.delete(0, tk.END)

        com = 'SELECT Login, Haslo, RolaId_roli FROM Uzytkownik WHERE (Login="{}" AND Haslo="{}");'.format(l,h)
        konto = self.executeSQLcommand(db, com)
        if len(konto) == 0:
            self.tekst.destroy()
            self.tekst = tk.Label(master, text='''Witaj w systemie obsługi hoteli "RESERVOIR" !
        Niepoprawne dane!''',height = 3)
            self.tekst.grid(column=1, row = 0)
        elif len(konto) == 1:
            if konto[0][2] == 4:
                self.master.destroy()
                root = tk.Tk()
                self.admin(root, self.db)
                root.mainloop()
            elif konto[0][2] == 2:
                self.master.destroy()
                root = tk.Tk()
                self.pracownik(root, self.db)
                root.mainloop()

    def executeSQLcommand(self, db, SQLcommand):
        c = db.cursor()
        c.execute(SQLcommand)
        rows = c.fetchall()
        return rows

    class admin:
        def __init__(self, master, db):
            self.master = master
            self.db = db
            master.title("Moduł administratora")

            self.dodanie = tk.Button(master, text="Dodaj nowy budynek", command=self.dodawanieO, width = 30, height = 5)

            self.edycja =tk.Button(master,text="Dodaj nowe pokoje", command=self.dodawanieP, width = 30, height = 5)

            self.zamknij = tk.Button(master, text="Wyjdź", command=master.destroy, width = 30, height = 5)

            self.dodanie.grid(row = 0, padx = 5, pady = 5)
            self.edycja.grid(row = 1, padx = 5, pady = 5)
            self.zamknij.grid(row=2, padx = 5, pady = 5)
    
        def dodawanieO(self):
            root = tk.Tk()
            self.d(root, self.db)
            root.mainloop()

        def dodawanieP(self):
            root = tk.Tk()
            self.p(root, self.db)
            root.mainloop()

        class d:
            def __init__(self, master, db):
                self.master = master
                self.db = db
                master.title("Dodawanie obiektu")

                hotele = self.executeSQLcommand(self.db, "SELECT Nazwa_hotelu FROM Hotel;")
                h = []
                for i in range(0, len(hotele)):
                    h.append(hotele[i][0])
                self.hotelL = tk.Label(master, text="Hotel:   ")
                self.h_value = tk.StringVar()
                self.hotel = ttk.Combobox(master, textvariable = self.h_value)
                self.hotel['values'] = h
                self.hotel.current(0)

                self.miastoL = tk.Label(master,text="Miasto:   ")
                self.miasto = tk.Entry(master)

                self.ulicaL = tk.Label(master, text="Ulica:   ")
                self.ulica = tk.Entry(master)
                
                self. kodpocztowyL = tk.Label(master, text="Kod pocztowy:   ")
                self.kodpocztowy = tk.Entry(master)

                self.nrbudynkuL = tk.Label(master, text="Nr. budynku:   ")
                self.nrbudynku = tk.Entry(master)

                self.telefonL = tk.Label(master, text="Nr. kontaktowy:   ")
                self.telefon = tk.Entry(master)

                self.pietraL = tk.Label(master, text="Liczba pięter:   ")
                self.pietra = tk.Entry(master)

                self.zatwierdz = tk.Button(master, text="Zatwierdź", command=self.dodawanie, width = 15, height = 3)
                self.anuluj = tk.Button(master, text="Anuluj", command=master.destroy, width = 15, height = 3)

                self.hotelL.grid(row=0, column = 0, padx=3, pady=3, sticky=tk.W)
                self.hotel.grid(row=0, column = 1, padx=3, pady=3)
                self.miastoL.grid(row=1, column = 0, padx=3, pady=3, sticky=tk.W)
                self.miasto.grid(row=1, column = 1, padx=3, pady=3)
                self.ulicaL.grid(row=2, column = 0, padx=3, pady=3, sticky=tk.W)
                self.ulica.grid(row=2, column = 1, padx=3, pady=3)
                self.kodpocztowyL.grid(row=3, column = 0, padx=3, pady=3, sticky=tk.W)
                self.kodpocztowy.grid(row=3, column = 1, padx=3, pady=3)
                self.nrbudynkuL.grid(row=4, column = 0, padx=3, pady=3, sticky=tk.W)
                self.nrbudynku.grid(row=4, column = 1, padx=3, pady=3)
                self.telefonL.grid(row=5, column = 0, padx=3, pady=3, sticky=tk.W)
                self.telefon.grid(row=5, column = 1, padx=3, pady=3)
                self.pietraL.grid(row=6, column=0, padx=3, pady=3, sticky=tk.W)
                self.pietra.grid(row=6, column = 1, padx=3, pady=3)
                self.zatwierdz.grid(row=7, column = 0, padx=3, pady=3)
                self.anuluj.grid(row=7, column = 1, padx=3, pady=3)

            def executeSQLcommand(self, db, SQLcommand):
                c = db.cursor()
                c.execute(SQLcommand)
                rows = c.fetchall()
                return rows

            def executeSQLadres(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Adres(Miasto, Ulica, Kod_pocztowy, Nr_budynku) 
VALUES (?, ?, ?, ?)'''
                c.execute(com, SQLcommand)
                return c.lastrowid

            def executeSQLobiekt(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Obiekt_hotelowy(AdresId_adres, HotelId_hotelu, Nr_kontaktowy) 
                VALUES (?,?,?)'''
                c.execute(com, SQLcommand)
                return c.lastrowid

            def executeSQLpietro(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Pietro(Nr_pietra, Obiekt_hotelowyId_obiektu) 
                VALUES (?,?)'''
                c.execute(com, SQLcommand)
                return c.lastrowid

            def dodawanie(self):
                p = self.pietra.get()
                if len(p) == 0:
                    return
                p = int(p)
                h = self.hotel.get()
                m = self.miasto.get()
                u = self.ulica.get()
                k = self.kodpocztowy.get()
                n = self.nrbudynku.get()
                kon = self.telefon.get()
                
                with self.db:
                    adres = (m,u,k,n)
                    ida = self.executeSQLadres(adres)
                    hot = str('SELECT Id_hotelu FROM Hotel WHERE Nazwa_hotelu="{}";'.format(h))
                    idh = self.executeSQLcommand(self.db, hot)
                    idh = idh[0][0]
                    obiekt = (ida,idh,kon)
                    ido = self.executeSQLobiekt(obiekt)
                    for i in range(0,p):
                        pietro = (i+1,ido)
                        idp = self.executeSQLpietro(pietro)
                self.master.destroy()

        class p:
            def __init__(self, master, db):
                self.master = master
                self.db = db
                master.title("Dodawanie pokoi")

                self.nrL = tk.Label(self.master, text="Numer pokoju:   ")
                self.pietroL = tk.Label(self.master, text="Piętro-Budynek:   ")
                self.typL = tk.Label(self.master, text="Typ pokoju:   ")

                self.nr = tk.Entry(self.master)

                pietra = self.executeSQLcommand("SELECT Nr_pietra, Obiekt_hotelowyId_obiektu FROM Pietro;")
                pi = []
                for i in range(0, len(pietra)):
                    pi.append((pietra[i][0], pietra[i][1]))
                self.pi_value = tk.StringVar()
                self.pietro = ttk.Combobox(self.master, textvariable = self.pi_value)
                self.pietro['values'] = pi
                self.pietro.current(0)

                typy = self.executeSQLcommand("SELECT Nazwa_typu FROM Typ_pokoju;")
                t = []
                for i in range(0, len(typy)):
                    t.append(typy[i][0])
                self.t_value = tk.StringVar()
                self.typ = ttk.Combobox(self.master, textvariable = self.t_value)
                self.typ['values'] = t
                self.typ.current(0)

                self.info1 = tk.Label(self.master, text="Dodano pokój:")
                self.info2 = tk.Label(self.master, text="--  ->  --  ->  --")

                self.dodaj = tk.Button(self.master, text="Dodaj pokój",command = self.dodaj, width = 10, height = 3)
                self.zamknij = tk.Button(self.master, text="Zakończ", command=self.master.destroy, width = 10, height = 3)

                self.nrL.grid(row=0, column=0, padx=3, pady=3, sticky=tk.W)
                self.nr.grid(row=0, column=1, padx=3, pady=3)
                self.pietroL.grid(row=1, column=0, padx=3, pady=3, sticky=tk.W)
                self.pietro.grid(row=1, column=1, padx=3, pady=3)
                self.typL.grid(row=2, column=0, padx=3, pady=3, sticky=tk.W)
                self.typ.grid(row=2, column=1, padx=3, pady=3)
                self.info1.grid(row=3, column=0, padx=3, pady=3, sticky=tk.W)
                self.info2.grid(row=3, column=1, padx=3, pady=3)
                self.dodaj.grid(row=4, column=0, padx=3, pady=3)
                self.zamknij.grid(row=4, column=1, padx=3, pady=3)

            def dodaj(self):
                n = self.nr.get()
                p = self.pietro.get()
                b = int(p[2])
                p = int(p[0])
                t = self.typ.get()
                
                idp = self.executeSQLcommand("SELECT Id_pietra FROM Pietro WHERE (Nr_pietra={} AND Obiekt_hotelowyId_obiektu={});".format(p,b))
                idp = idp[0][0]
                idt = self.executeSQLcommand('SELECT Id_typu FROM Typ_pokoju WHERE Nazwa_typu="{}";'.format(t))
                idt = idt[0][0]
                with self.db:
                    pokoj = (n,idp, idt)
                    id = self.executeSQLpokoj(pokoj)
                    self.nr.delete(0, tk.END)
                    self.info1 = tk.Label(self.master, text="Dodano pokój:")
                    self.info2 = tk.Label(self.master, text="{} -> {};{} -> {}".format(n,p,b,t))
                    self.info1.grid(row=3, column=0, padx=3, pady=3, sticky=tk.W)
                    self.info2.grid(row=3, column=1, padx=3, pady=3)


            def executeSQLcommand(self, SQLcommand):
                c = self.db.cursor()
                c.execute(SQLcommand)
                rows = c.fetchall()
                return rows

            def executeSQLpokoj(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Pokoj_hotelowy(Nr_pokoju, PietroId_pietra, Typ_pokojuId_typu) 
                VALUES (?,?,?)'''
                c.execute(com, SQLcommand)
                return c.lastrowid

    class pracownik:
        def __init__(self, master, db):
            self.master = master
            self.db = db
            master.title("Moduł pracownika")

            self.dodanie = tk.Button(master, text="Dodaj rezerwację", command=self.rezerwacja, width = 30, height = 5)
            self.zamknij = tk.Button(master, text="Wyjdź", command=master.destroy, width = 30, height = 5)

            self.dodanie.grid(row = 0, padx = 5, pady = 5)
            self.zamknij.grid(row=1, padx = 5, pady = 5)

        def rezerwacja(self):
            self.pytanie = tk.Label(self.master, text="Czy klient posiada konto?")
            self.tak = tk.Button(self.master, text="TAK", command=self.rez, width = 15, height = 3 )
            self.nie = tk.Button(self.master, text="NIE", command=self.uz, width = 15, height = 3)

            self.pytanie.grid(row = 2, padx = 5, pady = 5)
            self.tak.grid(row=3, padx = 5, pady = 5)
            self.nie.grid(row=4, padx = 5, pady = 5)

        def rez(self):
            self.pytanie.destroy()
            self.tak.destroy()
            self.nie.destroy()
            root = tk.Tk()
            self.r(root, self.db)
            root.mainloop()

        def uz(self):
            self.pytanie.destroy()
            self.tak.destroy()
            self.nie.destroy()
            root = tk.Tk()
            self.u(root, self.db)
            root.mainloop()

        class r:
            def __init__(self, master, db):
                self.master = master
                self.db = db
                master.title("Tworzenie rezerwacji")
                self.kwota = 0

                self.dataL = tk.Label(self.master, text="Data rezerwacji (YYYY-MM-DD):")
                self.data = tk.Entry(self.master)

                self.dniL = tk.Label(self.master, text="Czas trwania pobytu (w dniach):")
                self.dni = tk.Entry(self.master)

                self.terminy = tk.Button(self.master, text="Sprawdź wolne pokoje", command = self.pokoje, width = 20, height = 3)

                self.dataL.grid(row=0, column = 0, padx=3,pady=3, sticky=tk.W)
                self.data.grid(row=0, column = 1, padx=3,pady=3)
                self.dniL.grid(row=1, column = 0, padx=3,pady=3, sticky=tk.W)
                self.dni.grid(row=1, column = 1, padx=3,pady=3)
                self.terminy.grid(row=2, column = 1, padx=3,pady=3)

            def executeSQLcommand(self, SQLcommand):
                c = self.db.cursor()
                c.execute(SQLcommand)
                rows = c.fetchall()
                return rows

            def executeSQLrez(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Rezerwacja(Pokoj_hotelowyId_pokoju, UzytkownikId_uzytkownika, Termin_rozpoczecia, Termin_zakonczenia) 
VALUES (?, ?, ?, ?)'''
                c.execute(com, SQLcommand)
                return c.lastrowid     

            def executeSQLwyp(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Wyposazenie_Rezerwacja(WyposazenieId_wyposazenia, RezerwacjaId_rezerwacji) 
VALUES (?, ?)'''
                c.execute(com, SQLcommand)
                return

            def executeSQLwyz(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Wyzywienie_Rezerwacja(WyzywienieId_pakietu, RezerwacjaId_rezerwacji) 
VALUES (?, ?)'''
                c.execute(com, SQLcommand)
                return   

            def pokoje(self):
                com = '''SELECT Pokoj_hotelowy.Id_pokoju FROM Pokoj_hotelowy, Rezerwacja 
    WHERE Pokoj_hotelowy.Id_pokoju NOT IN (SELECT Pokoj_hotelowyId_pokoju FROM Rezerwacja WHERE date('{}', '+{} day') BETWEEN Termin_rozpoczecia and Termin_zakonczenia)
    ORDER BY Pokoj_hotelowy.Nr_pokoju ASC'''
                days = self.dni.get()
                start = self.data.get()
                if len(days) == 0 or len(start) == 0:
                    return
                pokoje = []
                for i in range(0, int(days)):
                    pokoje.append(self.executeSQLcommand(com.format(start, i)))
                for i in range(1, len(pokoje)):
                    pokoje[0] = intersection(pokoje[0],pokoje[i])
                wolne = []
                for i in range(0, len(pokoje[0])):
                    wolne.append(pokoje[0][i][0])
                self.wolne = tuple(wolne)
                com = """SELECT Pokoj_hotelowy.Nr_pokoju, Typ_pokoju.Nazwa_typu, Pietro.Nr_pietra, Pietro.Obiekt_hotelowyId_obiektu FROM Pokoj_hotelowy, Pietro, Typ_pokoju
WHERE Pokoj_hotelowy.Id_pokoju IN {}
AND Pokoj_hotelowy.PietroId_pietra=Pietro.Id_pietra AND Pokoj_hotelowy.Typ_pokojuId_typu=Typ_pokoju.Id_typu
ORDER BY Pokoj_hotelowy.Nr_pokoju ASC""".format(self.wolne)
                pokoje = self.executeSQLcommand(com)

                self.terminy.destroy()

                self.pokojeL = tk.Label(self.master, text="Wolne pokoje:")
                self.opis = tk.Label(self.master, text="(nr.pok - typ - piętro - budynek)")
                self.p_value = tk.StringVar()
                self.pokoj = ttk.Combobox(self.master, textvariable = self.p_value)
                self.pokoj['values'] = pokoje
                self.pokoj.current(0)

                self.loginL = tk.Label(self.master, text="Login klienta:")
                self.login = tk.Entry(self.master)

                self.wyposazenieL = tk.Label(self.master, text="Dodatkowe wyposażenie:")
                self.wyposazenie1 = ttk.Checkbutton(self.master, text="Szlafrok")
                self.wyposazenie2 = ttk.Checkbutton(self.master, text="Bamboszki")
                self.wyposazenie1.state(['!alternate'])
                self.wyposazenie2.state(['!alternate'])

                self.wyzywienie = tk.Label(self.master, text="Pakiety wyżywieniowe:")
                self.wyzywienie1 = ttk.Checkbutton(self.master, text= "Śniadania")
                self.wyzywienie2 = ttk.Checkbutton(self.master, text= "Obiady")
                self.wyzywienie3 = ttk.Checkbutton(self.master, text= "Kolacje")
                self.wyzywienie4 = ttk.Checkbutton(self.master, text= "Obiadokolacje")
                self.wyzywienie1.state(['!alternate'])
                self.wyzywienie2.state(['!alternate'])
                self.wyzywienie3.state(['!alternate'])
                self.wyzywienie4.state(['!alternate'])

                self.zakoncz = tk.Button(self.master, text="Dodaj rezerwację", command = self.zarezerwuj, width=15, height=3)
                self.anuluj = tk.Button(self.master, text="Anuluj", command = self.master.destroy, width=15, height=3)

                self.pokojeL.grid(row=3, column = 0, padx=3,pady=3, sticky=tk.W)
                self.opis.grid(row=3, column = 1, padx=3,pady=3, sticky=tk.W)
                self.pokoj.grid(row=4, column = 1, padx=3,pady=3, sticky=tk.W)
                self.loginL.grid(row=5, column = 0, padx=3,pady=3, sticky=tk.W)
                self.login.grid(row=5, column = 1, padx=3,pady=3, sticky=tk.W)
                self.wyposazenieL.grid(row=6, column=0, padx=3, pady=3, sticky=tk.W)
                self.wyposazenie1.grid(row=6, column=1, padx=3, pady=3, sticky=tk.W)
                self.wyposazenie2.grid(row=7, column=1, padx=3, pady=3, sticky=tk.W)
                self.wyzywienie.grid(row=8, column=0, padx=3, pady=3, sticky=tk.W)
                self.wyzywienie1.grid(row=8, column=1, padx=3, pady=3, sticky=tk.W)
                self.wyzywienie2.grid(row=9, column=1, padx=3, pady=3, sticky=tk.W)
                self.wyzywienie3.grid(row=10, column=1, padx=3, pady=3, sticky=tk.W)
                self.wyzywienie4.grid(row=11, column=1, padx=3, pady=3, sticky=tk.W)
                self.zakoncz.grid(row=12, column=0, padx=3, pady=3)
                self.anuluj.grid(row=12, column=1, padx=3, pady=3)

            def zarezerwuj(self):
                p = self.wolne[self.pokoj.current()]
                u = self.login.get()
                uzyt = self.executeSQLcommand('SELECT Id_uzytkownika FROM Uzytkownik WHERE Login="{}"'.format(u))
                uzyt = int(uzyt[0][0])
                t = self.data.get()
                n = self.dni.get()
                num = self.dni.get()
                num = int(num) - 1
                num = self.executeSQLcommand('SELECT date("{}", "+{} days")'.format(t,num))
                num = num[0][0]
                rezerwacja = (p,uzyt,t,num)
                with self.db:
                    idr = self.executeSQLrez(rezerwacja)
                    if self.wyposazenie1.instate(['selected']):
                        self.executeSQLwyp((1, idr))
                    if self.wyposazenie2.instate(['selected']):
                        self.executeSQLwyp((2, idr))
                    if self.wyzywienie1.instate(['selected']):
                        self.executeSQLwyz((1, idr))
                    if self.wyzywienie2.instate(['selected']):
                        self.executeSQLwyz((2, idr))
                    if self.wyzywienie3.instate(['selected']):
                        self.executeSQLwyz((3, idr))
                    if self.wyzywienie4.instate(['selected']):
                        self.executeSQLwyz((4, idr))
                self.kwota += self.executeSQLcommand('''SELECT (Typ_pokoju.Cena*{}) FROM Typ_pokoju, Rezerwacja, Pokoj_hotelowy
WHERE Typ_pokoju.Id_typu=Pokoj_hotelowy.Typ_pokojuId_typu AND Pokoj_hotelowy.Id_pokoju=Rezerwacja.Pokoj_hotelowyId_pokoju
AND Rezerwacja.Id_rezerwacji={};'''.format(n,idr))[0][0]
                self.kwota += self.executeSQLcommand('''SELECT (sum(Wyzywienie.Cena)*{}) FROM Wyzywienie, Rezerwacja, Wyzywienie_Rezerwacja
WHERE Wyzywienie.Id_pakietu=Wyzywienie_Rezerwacja.WyzywienieId_pakietu AND Wyzywienie_Rezerwacja.RezerwacjaId_rezerwacji=Rezerwacja.Id_rezerwacji
AND Rezerwacja.Id_rezerwacji={};'''.format(n,idr))[0][0]
                self.kwota += self.executeSQLcommand('''SELECT sum(Wyposazenie.Cena) FROM Wyposazenie, Rezerwacja, Wyposazenie_Rezerwacja
WHERE Wyposazenie.Id_wyposazenia=Wyposazenie_Rezerwacja.WyposazenieId_wyposazenia AND Wyposazenie_Rezerwacja.RezerwacjaId_rezerwacji=Rezerwacja.Id_rezerwacji
AND Rezerwacja.Id_rezerwacji={};'''.format(idr))[0][0]
                self.master.destroy()
                msb.showinfo("Podsumowanie", '''Dodano rezerwację!
Kwota do zapłaty wynosi {} PLN'''.format(self.kwota))
                
                


        class u:
            def __init__(self, master, db):
                self.master = master
                self.db = db
                master.title("Tworzenie konta klienta")

                self.imieL = tk.Label(self.master, text="Imię:")
                self.imie = tk.Entry(self.master)
                self.nazwiskoL = tk.Label(self.master, text="Nazwisko:")
                self.nazwisko = tk.Entry(self.master)
                self.miastoL = tk.Label(self.master,text="Miasto:   ")
                self.miasto = tk.Entry(self.master)
                self.ulicaL = tk.Label(self.master, text="Ulica:   ")
                self.ulica = tk.Entry(self.master)       
                self. kodpocztowyL = tk.Label(self.master, text="Kod pocztowy:   ")
                self.kodpocztowy = tk.Entry(self.master)
                self.nrbudynkuL = tk.Label(self.master, text="Nr. budynku:   ")
                self.nrbudynku = tk.Entry(self.master)
                self.nrmieszkaniaL = tk.Label(self.master, text="Nr. mieszkania:")
                self.nrmieszkania = tk.Entry(self.master)
                self.nrL = tk.Label(self.master, text="Nr. telefonu:")
                self.nr = tk.Entry(self.master)
                self.emailL = tk.Label(self.master, text="E-mail:")
                self.email = tk.Entry(self.master)
                self.loginL = tk.Label(self.master, text="Login:")
                self.login = tk.Entry(self.master)
                self.hasloL = tk.Label(self.master, text="Hasło:")
                self.haslo = tk.Entry(self.master)


                self.dalej = tk.Button(self.master, text="Dalej", command=self.rezerwacja, width = 15, height = 3)
                self.anuluj = tk.Button(self.master, text="Anuluj", command=self.master.destroy, width = 15, height = 3)

                self.imieL.grid(row=0, column = 0, padx=3, pady=3, sticky=tk.W)
                self.imie.grid(row=0, column = 1, padx=3, pady=3)
                self.nazwiskoL.grid(row=1, column = 0, padx=3, pady=3, sticky=tk.W)
                self.nazwisko.grid(row=1, column = 1, padx=3, pady=3)
                self.miastoL.grid(row=2, column = 0, padx=3, pady=3, sticky=tk.W)
                self.miasto.grid(row=2, column = 1, padx=3, pady=3)
                self.ulicaL.grid(row=3, column = 0, padx=3, pady=3, sticky=tk.W)
                self.ulica.grid(row=3, column = 1, padx=3, pady=3)
                self.kodpocztowyL.grid(row=4, column = 0, padx=3, pady=3, sticky=tk.W)
                self.kodpocztowy.grid(row=4, column = 1, padx=3, pady=3)
                self.nrbudynkuL.grid(row=5, column = 0, padx=3, pady=3, sticky=tk.W)
                self.nrbudynku.grid(row=5, column = 1, padx=3, pady=3)
                self.nrmieszkaniaL.grid(row=6, column = 0, padx=3, pady=3, sticky=tk.W)
                self.nrmieszkania.grid(row=6, column = 1, padx=3, pady=3)
                self.nrL.grid(row=7, column = 0, padx=3, pady=3, sticky=tk.W)
                self.nr.grid(row=7, column = 1, padx=3, pady=3)
                self.emailL.grid(row=8, column = 0, padx=3, pady=3, sticky=tk.W)
                self.email.grid(row=8, column = 1, padx=3, pady=3)
                self.loginL.grid(row=9, column = 0, padx=3, pady=3, sticky=tk.W)
                self.login.grid(row=9, column = 1, padx=3, pady=3)
                self.hasloL.grid(row=10, column = 0, padx=3, pady=3, sticky=tk.W)
                self.haslo.grid(row=10, column = 1, padx=3, pady=3)
                self.dalej.grid(row=11, column = 0, padx=3, pady=3)
                self.anuluj.grid(row=11, column = 1, padx=3, pady=3)

            class r:
                def __init__(self, master, db, uzytkownik = str):
                    self.master = master
                    self.db = db
                    self.log = uzytkownik
                    master.title("Tworzenie rezerwacji")
                    self.kwota = 0

                    self.dataL = tk.Label(self.master, text="Data rezerwacji (YYYY-MM-DD):")
                    self.data = tk.Entry(self.master)

                    self.dniL = tk.Label(self.master, text="Czas trwania pobytu (w dniach):")
                    self.dni = tk.Entry(self.master)

                    self.terminy = tk.Button(self.master, text="Sprawdź wolne pokoje", command = self.pokoje, width = 20, height = 3)

                    self.dataL.grid(row=0, column = 0, padx=3,pady=3, sticky=tk.W)
                    self.data.grid(row=0, column = 1, padx=3,pady=3)
                    self.dniL.grid(row=1, column = 0, padx=3,pady=3, sticky=tk.W)
                    self.dni.grid(row=1, column = 1, padx=3,pady=3)
                    self.terminy.grid(row=2, column = 1, padx=3,pady=3)

                def executeSQLcommand(self, SQLcommand):
                    c = self.db.cursor()
                    c.execute(SQLcommand)
                    rows = c.fetchall()
                    return rows

                def executeSQLrez(self, SQLcommand):
                    c = self.db.cursor()
                    com = '''INSERT INTO Rezerwacja(Pokoj_hotelowyId_pokoju, UzytkownikId_uzytkownika, Termin_rozpoczecia, Termin_zakonczenia) 
    VALUES (?, ?, ?, ?)'''
                    c.execute(com, SQLcommand)
                    return c.lastrowid     

                def executeSQLwyp(self, SQLcommand):
                    c = self.db.cursor()
                    com = '''INSERT INTO Wyposazenie_Rezerwacja(WyposazenieId_wyposazenia, RezerwacjaId_rezerwacji) 
    VALUES (?, ?)'''
                    c.execute(com, SQLcommand)
                    return

                def executeSQLwyz(self, SQLcommand):
                    c = self.db.cursor()
                    com = '''INSERT INTO Wyzywienie_Rezerwacja(WyzywienieId_pakietu, RezerwacjaId_rezerwacji) 
    VALUES (?, ?)'''
                    c.execute(com, SQLcommand)
                    return   

                def pokoje(self):
                    com = '''SELECT Pokoj_hotelowy.Id_pokoju FROM Pokoj_hotelowy, Rezerwacja 
    WHERE Pokoj_hotelowy.Id_pokoju NOT IN (SELECT Pokoj_hotelowyId_pokoju FROM Rezerwacja WHERE date('{}', '+{} day') BETWEEN Termin_rozpoczecia and Termin_zakonczenia)
    ORDER BY Pokoj_hotelowy.Nr_pokoju ASC'''
                    days = self.dni.get()
                    start = self.data.get()
                    if len(days) == 0 or len(start) == 0:
                        return
                    pokoje = []
                    for i in range(0, int(days)):
                        pokoje.append(self.executeSQLcommand(com.format(start, i)))
                    for i in range(1, len(pokoje)):
                        pokoje[0] = intersection(pokoje[0],pokoje[i])
                    wolne = []
                    for i in range(0, len(pokoje[0])):
                        wolne.append(pokoje[0][i][0])
                    self.wolne = tuple(wolne)
                    com = """SELECT Pokoj_hotelowy.Nr_pokoju, Typ_pokoju.Nazwa_typu, Pietro.Nr_pietra, Pietro.Obiekt_hotelowyId_obiektu FROM Pokoj_hotelowy, Pietro, Typ_pokoju
    WHERE Pokoj_hotelowy.Id_pokoju IN {}
    AND Pokoj_hotelowy.PietroId_pietra=Pietro.Id_pietra AND Pokoj_hotelowy.Typ_pokojuId_typu=Typ_pokoju.Id_typu
    ORDER BY Pokoj_hotelowy.Nr_pokoju ASC""".format(self.wolne)
                    pokoje = self.executeSQLcommand(com)

                    self.terminy.destroy()

                    self.pokojeL = tk.Label(self.master, text="Wolne pokoje:")
                    self.opis = tk.Label(self.master, text="(nr.pok - typ - piętro - budynek)")
                    self.p_value = tk.StringVar()
                    self.pokoj = ttk.Combobox(self.master, textvariable = self.p_value)
                    self.pokoj['values'] = pokoje
                    self.pokoj.current(0)

                    self.loginL = tk.Label(self.master, text="Login klienta:")
                    self.login = tk.Label(self.master, text="{}".format(self.log))

                    self.wyposazenieL = tk.Label(self.master, text="Dodatkowe wyposażenie:")
                    self.wyposazenie1 = ttk.Checkbutton(self.master, text="Szlafrok")
                    self.wyposazenie2 = ttk.Checkbutton(self.master, text="Bamboszki")
                    self.wyposazenie1.state(['!alternate'])
                    self.wyposazenie2.state(['!alternate'])

                    self.wyzywienie = tk.Label(self.master, text="Pakiety wyżywieniowe:")
                    self.wyzywienie1 = ttk.Checkbutton(self.master, text= "Śniadania")
                    self.wyzywienie2 = ttk.Checkbutton(self.master, text= "Obiady")
                    self.wyzywienie3 = ttk.Checkbutton(self.master, text= "Kolacje")
                    self.wyzywienie4 = ttk.Checkbutton(self.master, text= "Obiadokolacje")
                    self.wyzywienie1.state(['!alternate'])
                    self.wyzywienie2.state(['!alternate'])
                    self.wyzywienie3.state(['!alternate'])
                    self.wyzywienie4.state(['!alternate'])

                    self.zakoncz = tk.Button(self.master, text="Dodaj rezerwację", command = self.zarezerwuj, width=15, height=3)
                    self.anuluj = tk.Button(self.master, text="Anuluj", command = self.master.destroy, width=15, height=3)

                    self.pokojeL.grid(row=3, column = 0, padx=3,pady=3, sticky=tk.W)
                    self.opis.grid(row=3, column = 1, padx=3,pady=3, sticky=tk.W)
                    self.pokoj.grid(row=4, column = 1, padx=3,pady=3, sticky=tk.W)
                    self.loginL.grid(row=5, column = 0, padx=3,pady=3, sticky=tk.W)
                    self.login.grid(row=5, column = 1, padx=3,pady=3, sticky=tk.W)
                    self.wyposazenieL.grid(row=6, column=0, padx=3, pady=3, sticky=tk.W)
                    self.wyposazenie1.grid(row=6, column=1, padx=3, pady=3, sticky=tk.W)
                    self.wyposazenie2.grid(row=7, column=1, padx=3, pady=3, sticky=tk.W)
                    self.wyzywienie.grid(row=8, column=0, padx=3, pady=3, sticky=tk.W)
                    self.wyzywienie1.grid(row=8, column=1, padx=3, pady=3, sticky=tk.W)
                    self.wyzywienie2.grid(row=9, column=1, padx=3, pady=3, sticky=tk.W)
                    self.wyzywienie3.grid(row=10, column=1, padx=3, pady=3, sticky=tk.W)
                    self.wyzywienie4.grid(row=11, column=1, padx=3, pady=3, sticky=tk.W)
                    self.zakoncz.grid(row=12, column=0, padx=3, pady=3)
                    self.anuluj.grid(row=12, column=1, padx=3, pady=3)

                def zarezerwuj(self):
                    p = self.wolne[self.pokoj.current()]
                    u = self.log
                    uzyt = self.executeSQLcommand('SELECT Id_uzytkownika FROM Uzytkownik WHERE Login="{}"'.format(u))
                    uzyt = int(uzyt[0][0])
                    t = self.data.get()
                    n = self.dni.get()
                    num = self.dni.get()
                    num = int(num) - 1
                    num = self.executeSQLcommand('SELECT date("{}", "+{} days")'.format(t,num))
                    num = num[0][0]
                    rezerwacja = (p,uzyt,t,num)
                    with self.db:
                        idr = self.executeSQLrez(rezerwacja)
                        if self.wyposazenie1.instate(['selected']):
                            self.executeSQLwyp((1, idr))
                        if self.wyposazenie2.instate(['selected']):
                            self.executeSQLwyp((2, idr))
                        if self.wyzywienie1.instate(['selected']):
                            self.executeSQLwyz((1, idr))
                        if self.wyzywienie2.instate(['selected']):
                            self.executeSQLwyz((2, idr))
                        if self.wyzywienie3.instate(['selected']):
                            self.executeSQLwyz((3, idr))
                        if self.wyzywienie4.instate(['selected']):
                            self.executeSQLwyz((4, idr))
                    self.kwota += self.executeSQLcommand('''SELECT (Typ_pokoju.Cena*{}) FROM Typ_pokoju, Rezerwacja, Pokoj_hotelowy
    WHERE Typ_pokoju.Id_typu=Pokoj_hotelowy.Typ_pokojuId_typu AND Pokoj_hotelowy.Id_pokoju=Rezerwacja.Pokoj_hotelowyId_pokoju
    AND Rezerwacja.Id_rezerwacji={};'''.format(n,idr))[0][0]
                    self.kwota += self.executeSQLcommand('''SELECT (sum(Wyzywienie.Cena)*{}) FROM Wyzywienie, Rezerwacja, Wyzywienie_Rezerwacja
    WHERE Wyzywienie.Id_pakietu=Wyzywienie_Rezerwacja.WyzywienieId_pakietu AND Wyzywienie_Rezerwacja.RezerwacjaId_rezerwacji=Rezerwacja.Id_rezerwacji
    AND Rezerwacja.Id_rezerwacji={};'''.format(n,idr))[0][0]
                    self.kwota += self.executeSQLcommand('''SELECT sum(Wyposazenie.Cena) FROM Wyposazenie, Rezerwacja, Wyposazenie_Rezerwacja
    WHERE Wyposazenie.Id_wyposazenia=Wyposazenie_Rezerwacja.WyposazenieId_wyposazenia AND Wyposazenie_Rezerwacja.RezerwacjaId_rezerwacji=Rezerwacja.Id_rezerwacji
    AND Rezerwacja.Id_rezerwacji={};'''.format(idr))[0][0]
                    self.master.destroy()
                    msb.showinfo("Podsumowanie", '''Dodano rezerwację!
Kwota do zapłaty wynosi {} PLN'''.format(self.kwota))

            def executeSQLuzyt(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Uzytkownik(RolaId_roli, Login, Haslo, Imie, Nazwisko, Nr_telefonu, Email, KlientCzyPracownik) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
                c.execute(com, SQLcommand)
                return c.lastrowid

            def executeSQLadres(self, SQLcommand):
                c = self.db.cursor()
                com = '''INSERT INTO Adres(Miasto, Ulica, Kod_pocztowy, Nr_budynku, Nr_mieszkania, KontoId_konta) 
VALUES (?, ?, ?, ?, ?, ?)'''
                c.execute(com, SQLcommand)
                return c.lastrowid

            def rezerwacja(self):
                i = self.imie.get()
                n = self.nazwisko.get()
                num = self.nr.get()
                e = self.email.get()
                l = self.login.get()
                h = self.haslo.get()

                with self.db:
                    uzyt = (1, l, h, i, n, num, e, 0)
                    idu = self.executeSQLuzyt(uzyt)
                    mia = self.miasto.get()
                    uli = self.ulica.get()
                    kod = self.kodpocztowy.get()
                    nrbud = self.nrbudynku.get()
                    nrmiesz = self.nrmieszkania.get()
                    adres = (mia, uli, kod, nrbud, nrmiesz, idu)
                    ida = self.executeSQLadres(adres)

                self.master.destroy()
                root = tk.Tk()
                self.r(root, self.db, l)
                root.mainloop()

database = r'database/reservoir.db'
conn = create_connection(database)

root = tk.Tk()
my_gui = GUI(root, conn)
root.mainloop()
