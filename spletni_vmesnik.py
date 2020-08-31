import bottle, model, datetime, os

rokovniki = {}
for dat in os.listdir('shramba'):
    stevilo = ''
    for kandidat in dat:
        if kandidat.isdigit():
            stevilo += kandidat
    stevilo = int(stevilo)
    rokovniki[stevilo] = model.Rokovnik.nalozi_stanje(os.path.join('shramba', dat))

def rokovnik_uporabnika():
    st_uporabnika = bottle.request.get_cookie('st_uporabnika', secret='sikret')
    if st_uporabnika is None:
        st_uporabnika = len(rokovniki) + 1
        rokovniki[st_uporabnika] = model.Rokovnik(480)
        bottle.response.set_cookie('st_uporabnika', st_uporabnika, path='/', secret='sikret')
    return rokovniki[st_uporabnika]

def shrani_rokovnik():
    stevilo = bottle.request.get_cookie('st_uporabnika', secret='sikret')
    rokovnik = rokovniki[stevilo]
    rokovnik.shrani_stanje(os.path.join('shramba', f'Rokovnik_st_{stevilo}.json'))

@bottle.get('/')
def zacetna_stran():
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
    datum = datetime.datetime.strptime(datum, '%Y-%m-%d')
    dolzina_izpita = bottle.request.forms.getunicode('dolzina_izpita')
    tematika = bottle.request.forms.getunicode('tematika')
    kolicina_gradiva = bottle.request.forms.getunicode('kolicina_gradiva')
    predelano_gradivo = bottle.request.forms.getunicode('predelano_gradivo')
    predmet.dodaj_izpit(datum, int(dolzina_izpita), tematika, int(kolicina_gradiva), int(predelano_gradivo))
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/odstrani-predmet/')
def odstrani_predmet():
    rokovnik = rokovnik_uporabnika()
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    rokovnik.odstrani_predmet(predmet)
    shrani_rokovnik()
    bottle.redirect('/')

@bottle.post('/odstrani-izpit/')
def odstrani_izpit():
    rokovnik = rokovnik_uporabnika()
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    datum = datetime.datetime.strptime(bottle.request.forms.getunicode('izpit'), '%Y-%m-%d %H:%M:%S')
    izpit = predmet.najdi_izpit_glede_na_cas(datum)
    predmet.odstrani_izpit(izpit)
    shrani_rokovnik()
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)