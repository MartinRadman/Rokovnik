import model, datetime

#Začasna testna koda
import model, datetime

r = model.Rokovnik('Kr en', 480)

p1 = r.dodaj_predmet('Algebra', 8, 10)
p1.dodaj_izpit(datetime.datetime(2020, 9, 1, 15, 30), 120, 'Kr neki', 100, 20)
p1.dodaj_izpit(datetime.datetime(2020, 9, 1, 17, 30), 120, 'Kr neki', 100, 10)

p2 = r.dodaj_predmet('Analiza', 8, 10)
p2.dodaj_izpit(datetime.datetime(2020, 9, 1, 14, 00), 60, 'Še več kr neki', 120, 5)
p2.dodaj_izpit(datetime.datetime(2020, 9, 1, 18, 25), 120, 'Spet kr neki', 60, 8)
#Konec

def modro(niz):
    return f'\033[1;94m{niz}\033[0m'

def rdece(niz):
    return f'\033[1;91m{niz}\033[0m'

def uspeh():
    print(modro('Uspešno opravljeno!'))

def meni():
    rokovnik = r
    while True:
        uvodni_tekst(rokovnik)
        print('\tX) Izhod iz programa')
        vnos = input('> ')
        vnos = preveri_veljavnost_vnosa(vnos, rokovnik)
        dejanje(vnos, rokovnik)

def uvodni_tekst(rokovnik):
    print('\n\tIzberite možnost:')
    s = stanje(rokovnik)
    if s[0]:
        if s[1]:
            prikaz_seznama(['Dodaj predmet', 'Odstrani predmet', 'Dodaj izpit', 'Odstrani izpit', 'Prikaži prihajajoče izpite', 'Prikaži učni načrt'])
        else:
            prikaz_seznama(['Dodaj predmet', 'Odstrani predmet', 'Dodaj izpit'])
    else:
        prikaz_seznama(['Dodaj predmet'])

def stanje(rokovnik):
    return [rokovnik.predmeti, preveri_prisotnost_izpitov(rokovnik)]
   
def preveri_prisotnost_izpitov(rokovnik):
    for predmet in rokovnik.predmeti:
        if predmet.izpiti:
            return True
    return False

def preveri_veljavnost_vnosa(vnos, rokovnik):
    if vnos.lower() == 'x':
        return 'X'
    vnos = v_stevilko(vnos)
    s = stanje(rokovnik)
    if s[0]:
        if s[1]:
            vnos = preveri_mejo(vnos, [1, 6])
        else:
            vnos = preveri_mejo(vnos, [1, 3])
    else:
        vnos = preveri_mejo(vnos, [1, 1])
    return str(vnos)

def dejanje(vnos, rokovnik):
    if vnos == '1':
        dodaj_predmet(rokovnik)
    elif vnos == '2':
        odstrani_predmet(rokovnik)
    elif vnos == '3':
        dodaj_izpit(rokovnik)
    elif vnos == '4':
        odstrani_izpit(rokovnik)
    elif vnos == '5':
        prikazi_prihajajoce_izpite(rokovnik)
    elif vnos == '6':
        prikazi_ucni_nacrt(rokovnik)
    elif vnos.lower() == 'x':
        raise SystemExit

def dodaj_predmet(rokovnik):
    ime = input('Kako je ime predmetu? > ')
    pricakovana_ocena = preveri_mejo(v_stevilko(input('Kolikšna je pričakovana ocena predmeta? > ')), [5, 10])
    tezavnost = preveri_mejo(v_stevilko(input('Kako bi ocenili težavnost predmeta na lestvici od 1 (najlažje) do 10 (najtežje)? > ')), [1, 10])
    while True:
        try:
            rokovnik.dodaj_predmet(ime, pricakovana_ocena, tezavnost)
            break
        except:
            ime = input(rdece('Predmet s tem imenom že obstaja. Prosimo, vnesite novo ime! > '))
    uspeh()

def v_stevilko(niz):
    if type(niz) == int:
        return niz
    while True:
        if niz.isdigit():
            return int(niz)
        else:
            niz = input('Prosimo vnesite število! > ')


def preveri_mejo(stevilo, meja):
    while not znotraj_meje(stevilo, meja):
        if tip_meje(meja) == 'spodnja':
            stevilo = input(rdece(f'Prosimo, vnesite številko večje ali enako od {meja[0]}! > '))
        elif tip_meje(meja) == 'obojestranska':
            stevilo = input(rdece(f'Prosimo, vnesite številko med {meja[0]} in {meja[1]}! > '))
        elif tip_meje(meja) == 'zgornja':
            stevilo = input(rdece(f'Prosimo, vnesite številko manjše ali enako od {meja[0]}! > '))
        else:
            stevilo = input(rdece(f'Prosimo, vnesite ustrezno številko! > '))
    return stevilo

def tip_meje(meja):
    if meja[0] == None:
        if meja[1] == None:
            return 'brez'
        else:
            return 'zgornja'
    elif meja[0] == meja[1]:
        return 'trivialna'
    else:
        if meja[1] == None:
            return 'spodnja'
    return 'obojestranska'

def znotraj_meje(stevilo, meja):
    stevilo = v_stevilko(stevilo)
    tip = tip_meje(meja)
    if tip == 'spodnja':
        if stevilo < meja[0]:
            return False
    elif tip == 'zgornja':
        if stevilo > meja[1]:
            return False
    elif tip == 'brez':
        return True
    elif stevilo not in range(meja[0], meja[1] + 1):
        return False
    return True

def prikaz_seznama(sez):
    i = 1
    for vrednost in sez:
        print(f'\t{i}) {vrednost}')
        i += 1

def odstrani_predmet(rokovnik):
    predmet = izbira_predmeta(rokovnik)
    rokovnik.odstrani_predmet(predmet)
    uspeh()

def dodaj_izpit(rokovnik):
    predmet = izbira_predmeta(rokovnik)
    predmet.dodaj_izpit(*podatki_za_predmet(predmet), predmet)
    uspeh()

def izbira_predmeta(rokovnik):
    print('\tIzberite predmet:')
    prikaz_seznama(rokovnik.predmeti)
    vnos = input('> ')
    predmet = rokovnik.predmeti[preveri_mejo(v_stevilko(vnos), [1, len(rokovnik.predmeti)]) - 1]
    return predmet

def podatki_za_predmet(predmet):
    datum = vnos_datuma(predmet)
    dolzina_izpita = preveri_mejo(v_stevilko(input('Koliko minut bo trajal izpit? > ')), [0, None])
    tematika = input('Dodajte kratek opis izpita. > ')
    kolicina_gradiva = preveri_mejo(v_stevilko(input('Koliko strani gradiva morate predelati za izpit? > ')), [0, None])
    return datum, dolzina_izpita, tematika, kolicina_gradiva

def vnos_datuma(predmet):
    leto = preveri_mejo(v_stevilko(input('Katerega leta bo izpit? > ')), [None, None])
    mesec = preveri_mejo(v_stevilko(input('Katerega meseca bo izpit? (vnesite zaporedno številko meseca) > ')), [1, 12])
    dan = preveri_mejo(v_stevilko(input('Katerega dne bo izpit? > ')), [1, 31])
    ura = input('Ob kateri uri bo izpit? (uro in minuto ločite s piko, npr. 15.30) > ')
    while True:
        try:
            ura = ura.split('.')
            datum = datetime.datetime(leto, mesec, dan, preveri_mejo(v_stevilko(ura[0]), [None, None]), preveri_mejo(v_stevilko(ura[1]), [None, None]))
            break
        except:
            ura = input(rdece('Prosimo pravilno vnesite uro! (uro in minuto ločite s piko, npr. 15.30) > '))
    return datum

def odstrani_izpit(rokovnik):
    predmet = izbira_predmeta(rokovnik)
    izpit = izbira_izpita(predmet)
    predmet.odstrani_izpit(izpit)
    uspeh()

def izbira_izpita(predmet):
    print('\tIzberite izpit:')
    prikaz_seznama(predmet.izpiti)
    vnos = input('> ')
    izpit = predmet.izpiti[preveri_mejo(v_stevilko(vnos), [1, len(predmet.izpiti)]) - 1]
    return izpit

def prikazi_prihajajoce_izpite(rokovnik):
    for predmet in rokovnik.predmeti:
        print('\n')
        for izpit in predmet.izpiti:
            print(izpit)

def prikazi_ucni_nacrt(rokovnik):
    kaj_prikazano = False
    dolzina = do_kdaj_hoces_podatke()
    ostanek = rokovnik.razporedi_delo_enakomerno()
    for datum in rokovnik.razporeditev_dela:
        if (datetime.datetime.strptime(datum, '%m/%d/%y') - datetime.datetime.now()).days > dolzina:
            continue
        kaj_prikazano = True
        print(datum)
        for izpit in rokovnik.razporeditev_dela[datum]:
            cas = rokovnik.razporeditev_dela[datum][izpit]
            if cas != 0:
                print(izpit)
                print(f'Predvidenih je {cas} minut dela.\n')
    preveri_ostanek(ostanek)
    if not kaj_prikazano:
        print(modro(f'\nZa ta čas nimate razporejenega nič dela. :D'))

def preveri_ostanek(ostanek):
    if ostanek:
        for izpit in ostanek:
            print(f'Žal vam za izpit {izpit} zmanjka {ostanek[izpit]} minut dela.')

def do_kdaj_hoces_podatke():
    dolzina = input('Za koliko dni vnaprej hočete videti učni načrt? > ')
    return v_stevilko(dolzina)

r.razporedi_delo_enakomerno()
meni()