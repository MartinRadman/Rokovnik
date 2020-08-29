import bottle

#Začasna testna koda
import model, datetime

r = model.Rokovnik('Kr en', 480)

p1 = r.dodaj_predmet('Algebra', 8, 10)
p1.dodaj_izpit(datetime.datetime(2020, 8, 20, 15, 30), 120, 'Kr neki', 100, 20)
p1.dodaj_izpit(datetime.datetime(2020, 9, 20, 17, 30), 120, 'Kr neki', 100, 10)

p2 = r.dodaj_predmet('Analiza', 8, 10)
p2.dodaj_izpit(datetime.datetime(2020, 9, 20, 14, 00), 60, 'Še več kr neki', 120, 5)
p2.dodaj_izpit(datetime.datetime(2020, 9, 20, 18, 25), 120, 'Spet kr neki', 60, 8)
#Konec

@bottle.get('/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', rokovnik=r)

@bottle.get('/<ime>/')
def pozdravi(ime):
    return f'<h1>Pozdravljena {ime}!</h1>'

bottle.run(debug=True, reloader=True)