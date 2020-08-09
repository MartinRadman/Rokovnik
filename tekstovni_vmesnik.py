import model, datetime

#Začasna testna koda
import model, datetime

r = model.Rokovnik()
p = r.dodaj_predmet('Algebra', 8, 10)
p.dodaj_izpit(datetime.datetime(2020, 8, 4, 15, 30), 120, 'Kr neki', 100)

p.dodaj_izpit(datetime.datetime(2020, 8, 4, 17, 30), 120, 'Kr neki', 100)
#Konec

def meni():
    rokovnik = r
    while True:
        print(uvodni_tekst(rokovnik))
        vnos = input('> ')
        dejanje(vnos, rokovnik)

def uvodni_tekst(rokovnik):
    if rokovnik.predmeti:
        if preveri_prisotnost_izpitov(rokovnik):
            return '''
            Izberite možnost:
            1) Dodaj predmet
            2) Odstrani predmet
            3) Dodaj izpit
            4) Odstrani izpit
            X) Izhod iz programa'''
        else:
            return '''
            Izberite možnost:
            1) Dodaj predmet
            2) Odstrani predmet
            3) Dodaj izpit
            X) Izhod iz programa'''
    else:
        return '''Izberite možnost:
        1) Dodaj predmet
        X) Izhod is programa'''

def preveri_prisotnost_izpitov(rokovnik):
    for predmet in rokovnik.predmeti:
        if predmet.izpiti:
            return True
    return False

def dejanje(vnos, rokovnik):
    if vnos == '1':
        dodaj_predmet(rokovnik)
    elif vnos == '2':
        odstrani_predmet(rokovnik)
    elif vnos == '3':
        dodaj_izpit(rokovnik)
    elif vnos == '4':
        odstrani_izpit(rokovnik)
    elif vnos.lower() == 'x':
        raise SystemExit
    else:
        print('Prosimo, vnesite ustrezno številko!')

def dodaj_predmet(rokovnik):
    ime = input('Kako je ime predmetu? > ')
    pricakovana_ocena = input('Kolikšna je pričakovana ocena predmeta? > ')
    tezavnost = input('Kako bi ocenili težavnost predmeta na lestvici od 1 (najlažje) do 10 (najtežje)? > ')
    rokovnik.dodaj_predmet(ime, v_stevilko(pricakovana_ocena), v_stevilko(tezavnost))

def v_stevilko(niz):
    while True:
        try:
            return int(niz)
        except:
            niz = input('Prosimo, vnesite številko! > ')

def prikaz_predmetov(rokovnik):
    i = 1
    for predmet in rokovnik.predmeti:
        print(f'{i}) {predmet}')
        i += 1

def odstrani_predmet(rokovnik):
    predmet = izbira_predmeta(rokovnik)
    rokovnik.odstrani_predmet(predmet)

def dodaj_izpit(rokovnik):
    predmet = izbira_predmeta(rokovnik)
    predmet.dodaj_izpit(*podatki_za_predmet(predmet))

def izbira_predmeta(rokovnik):
    print('Izberite predmet:')
    prikaz_predmetov(rokovnik)
    vnos = input('> ')
    predmet = rokovnik.predmeti[v_stevilko(vnos) - 1]
    return predmet

def podatki_za_predmet(predmet):
    datum = vnos_datuma(predmet)
    dolzina_izpita = input('Koliko minut bo trajal izpit? > ') 
    tematika = input('Dodajte kratek opis izpita. > ')
    kolicina_gradiva = input('Koliko strani gradiva morate predelati za izpit? > ')
    return datum, v_stevilko(dolzina_izpita), tematika, v_stevilko(kolicina_gradiva)

def vnos_datuma(predmet):
    leto = input('Katerega leta bo izpit? > ')
    mesec = input('Katerega meseca bo izpit? (vnesite zaporedno številko meseca) > ')
    dan = input('Katerega dne bo izpit? > ')
    ura = input('Ob kateri uri bo izpit? (uro in minuto ločite s piko, npr. 15.30) > ')
    ura = ura.split('.')
    datum = datetime.datetime(v_stevilko(leto), v_stevilko(mesec), v_stevilko(dan), v_stevilko(ura[0]), v_stevilko(ura[1]))
    return datum

def odstrani_izpit(rokovnik):
    predmet = izbira_predmeta(rokovnik)
    izpit = izbira_izpita(predmet)
    predmet.odstrani_izpit(izpit)

def prikaz_izpitov(predmet):
    i = 1
    for izpit in predmet.izpiti:
        print(f'{i}) {izpit}')
        i += 1

def izbira_izpita(predmet):
    print('Izberite izpit:')
    prikaz_izpitov(predmet)
    vnos = input('> ')
    izpit = predmet.izpiti[v_stevilko(vnos) - 1]
    return izpit

meni()