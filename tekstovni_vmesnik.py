import model

#Začasna testna koda
import model, datetime

r = model.Rokovnik()
p = r.dodaj_predmet('Algebra', 8, 10)
i1 = p.dodaj_izpit(datetime.datetime(2020, 8, 4, 15, 30), 120, 'Kr neki', 100)

i2 = p.dodaj_izpit(datetime.datetime(2020, 8, 4, 17, 30), 120, 'Kr neki', 100)
#Konec

def meni():
    rokovnik = r
    while True:
        print(uvodni_tekst(rokovnik))
        vnos = input('> ')
        dejanje(vnos, rokovnik)

def uvodni_tekst(rokovnik):
    if rokovnik.predmeti:
        return '''
        Izberite možnost:
        1) Dodaj predmet
        2) Odstrani predmet
        3) Dodaj izpit
        4) Odstrani izpit
        X) Izhod iz programa'''
    else:
        return '''Izberite možnost:
        1) Dodaj predmet
        X) Izhod is programa'''

def dejanje(vnos, rokovnik):
    if vnos == '1':
        dodaj_predmet(rokovnik)
    elif vnos == '2':
        odstrani_predmet(rokovnik)
    elif vnos == '3':
        dodaj_izpit()
    elif vnos == '4':
        odstrani_izpit()
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
            niz = input('Prosimo, vnesite številko! >')

def odstrani_predmet(rokovnik):
    print('Kateri predmet želite odstraniti?')
    i = 1
    for predmet in rokovnik.predmeti:
        print(f'{i}) {predmet}')
    vnos = input('> ')
    rokovnik.odstrani_predmet(rokovnik.predmeti[v_stevilko(vnos) - 1])




meni()