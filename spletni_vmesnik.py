import bottle

#Začasna testna koda
import model, datetime

rokovnik = model.Rokovnik('Kr en', 480)

p1 = rokovnik.dodaj_predmet('Algebra', 8, 10)
p1.dodaj_izpit(datetime.datetime(2020, 8, 20, 15, 30), 120, 'Kr neki', 100, 20)
p1.dodaj_izpit(datetime.datetime(2020, 9, 20, 17, 30), 120, 'Kr neki', 100, 10)

p2 = rokovnik.dodaj_predmet('Analiza', 8, 10)
p2.dodaj_izpit(datetime.datetime(2020, 9, 20, 14, 00), 60, 'Še več kr neki', 120, 5)
p2.dodaj_izpit(datetime.datetime(2020, 9, 20, 18, 25), 120, 'Spet kr neki', 60, 8)
#Konec

@bottle.get('/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', rokovnik=rokovnik)

@bottle.post('/dodaj-predmet/')
def dodaj_predmet():
    ime = bottle.request.forms.getunicode('ime')
    pricakovana_ocena = bottle.request.forms.getunicode('pricakovana_ocena')
    tezavnost = bottle.request.forms.getunicode('tezavnost')
    rokovnik.dodaj_predmet(ime, pricakovana_ocena, tezavnost)
    bottle.redirect('/')

@bottle.post('/dodaj-izpit/')
def dodaj_izpit():
    predmet = rokovnik.poisci_predmet_glede_na_ime(bottle.request.forms.getunicode('predmet'))
    datum = bottle.request.forms.getunicode('datum')
    datum = datetime.datetime.strptime(datum, '%Y-%m-%d')
    dolzina_izpita = bottle.request.forms.getunicode('dolzina_izpita')
    tematika = bottle.request.forms.getunicode('tematika')
    kolicina_gradiva = bottle.request.forms.getunicode('kolicina_gradiva')
    predelano_gradivo = bottle.request.forms.getunicode('predelano_gradivo')
    predmet.dodaj_izpit(datum, dolzina_izpita, tematika, int(kolicina_gradiva), int(predelano_gradivo))
    bottle.redirect('/')


bottle.run(debug=True, reloader=True)