import bottle, model, datetime, os, hashlib


racuni = {}

if not os.path.isdir('shramba'):
    os.mkdir('shramba')

for datoteka in os.listdir('shramba'):
    racun = model.Racun.nalozi_stanje(os.path.join('shramba', datoteka))
    racuni[racun.ime] = racun

def racun_uporabnika():
    ime = bottle.request.get_cookie('ime', secret='sikret')
    if ime is None:
        bottle.redirect('/prijava/')
    return racuni[ime]

def rokovnik_uporabnika():
    return racun_uporabnika().rokovnik

def shrani_rokovnik():  
    racun = racun_uporabnika()
    racun.shrani_stanje(os.path.join('shramba', f'{racun.ime}.json'))


@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava_v_racun.html')



@bottle.post('/prijava/')
def prijava_post():
    ime = bottle.request.forms.getunicode('ime')
    geslo = bottle.request.forms.getunicode('geslo')
    sifra = hashlib.sha512()
    sifra.update(geslo.encode(encoding='UTF-8'))
    boljse_geslo = sifra.hexdigest()
    racun = racuni[ime]
    racun.avtentikacija_gesla(boljse_geslo)
    bottle.response.set_cookie('ime', racun.ime, path='/', secret='sikret')
    bottle.redirect('/')


@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('ime', path='/')
    bottle.redirect('/')

@bottle.get('/registracija/')
def registracija_get():
    return bottle.template('registracija.html')

@bottle.post('/registracija/')
def registracija_post():
    ime = bottle.request.forms.getunicode('ime')
    geslo = bottle.request.forms.getunicode('geslo')
    delo_na_dan = int(bottle.request.forms.getunicode('delo_na_dan'))
    sifra = hashlib.sha512()
    sifra.update(geslo.encode(encoding='UTF-8'))
    boljse_geslo = sifra.hexdigest()
    racun = model.Racun(ime, boljse_geslo, model.Rokovnik(delo_na_dan))
    racuni[ime] = racun
    bottle.response.set_cookie('ime', racun.ime, path='/', secret='sikret')
    bottle.redirect('/')



@bottle.get('/')
def zacetna_stran():
    shrani_rokovnik()
    rokovnik = rokovnik_uporabnika()
    return bottle.template('zacetna_stran.html', rokovnik=rokovnik)

@bottle.post('/dodaj-predmet/')
def dodaj_predmet():
    rokovnik = rokovnik_uporabnika()
    ime = bottle.request.forms.getunicode('ime')
    pricakovana_ocena = int(bottle.request.forms.getunicode('pricakovana_ocena'))
    tezavnost = int(bottle.request.forms.getunicode('tezavnost'))
    rokovnik.dodaj_predmet(ime, pricakovana_ocena, tezavnost)
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/dodaj-izpit/')
def dodaj_izpit():
    rokovnik = rokovnik_uporabnika()
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    datum = bottle.request.forms.getunicode('datum')
    ura = int(bottle.request.forms.getunicode('ura'))
    minuta = int(bottle.request.forms.getunicode('minuta'))
    datum = datetime.datetime.strptime(datum + f' {ura}:{minuta}', '%Y-%m-%d %H:%M')
    dolzina_izpita = bottle.request.forms.getunicode('dolzina_izpita')
    tematika = bottle.request.forms.getunicode('tematika')
    kolicina_gradiva = bottle.request.forms.getunicode('kolicina_gradiva')
    predelano_gradivo = bottle.request.forms.getunicode('predelano_gradivo')
    predmet.dodaj_izpit(datum, int(dolzina_izpita), tematika, int(kolicina_gradiva), int(predelano_gradivo))
    rokovnik.razporedi_delo_enakomerno()
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/odstrani-predmet/')
def odstrani_predmet():
    rokovnik = rokovnik_uporabnika()
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    rokovnik.odstrani_predmet(predmet)
    rokovnik.razporedi_delo_enakomerno()
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/uredi-predmet/')
def dodaj_predmet():
    rokovnik = rokovnik_uporabnika()
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    ime = bottle.request.forms.getunicode('ime')
    pricakovana_ocena = int(bottle.request.forms.getunicode('pricakovana_ocena'))
    tezavnost = int(bottle.request.forms.getunicode('tezavnost'))
    predmet.ime = ime
    predmet.pricakovana_ocena = pricakovana_ocena
    predmet.tezavnost = tezavnost
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/odstrani-izpit/')
def odstrani_izpit():
    rokovnik = rokovnik_uporabnika()
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    datum = datetime.datetime.strptime(bottle.request.forms.getunicode('izpit'), '%Y-%m-%d %H:%M:%S')
    izpit = predmet.najdi_izpit_glede_na_cas(datum)
    predmet.odstrani_izpit(izpit)
    rokovnik.razporedi_delo_enakomerno()
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/uredi-izpit/')
def uredi_izpit():
    rokovnik = rokovnik_uporabnika()
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    izpit = predmet.izpiti[int(bottle.request.forms.getunicode('index'))]
    datum = bottle.request.forms.getunicode('datum')
    ura = int(bottle.request.forms.getunicode('ura'))
    minuta = int(bottle.request.forms.getunicode('minuta'))
    datum = datetime.datetime.strptime(datum + f' {ura}:{minuta}', '%Y-%m-%d %H:%M')
    dolzina_izpita = int(bottle.request.forms.getunicode('dolzina_izpita'))
    tematika = bottle.request.forms.getunicode('tematika')
    kolicina_gradiva = int(bottle.request.forms.getunicode('kolicina_gradiva'))
    predelano_gradivo = int(bottle.request.forms.getunicode('predelano_gradivo'))
    izpit.datum = datum
    izpit.dolzina_izpita = dolzina_izpita
    izpit.tematika = tematika
    izpit.kolicina_gradiva = kolicina_gradiva
    izpit.predelano_gradivo = predelano_gradivo
    izpit.predmet = predmet
    rokovnik.razporedi_delo_enakomerno()
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/uredi-rokovnik/')
def uredi_rokovnik():
    rokovnik = rokovnik_uporabnika()
    delo_na_dan = int(bottle.request.forms.getunicode('delo_na_dan'))
    rokovnik.delo_na_dan = delo_na_dan
    shrani_rokovnik()
    bottle.redirect('/')



@bottle.get('/napoved/')
def napoved():
    rokovnik = rokovnik_uporabnika()
    rokovnik.razporedi_delo_enakomerno()
    shrani_rokovnik()
    return bottle.template('napoved.html', rokovnik=rokovnik)

bottle.run(debug=True, reloader=True)