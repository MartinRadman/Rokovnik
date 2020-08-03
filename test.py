import model, datetime

r = model.Rokovnik()
p = r.dodaj_predmet('Algebra', 8, 10)
i1 = p.dodaj_izpit(datetime.datetime(2020, 8, 4, 15, 30), 120, 'Kr neki', 100)

i2 = p.dodaj_izpit(datetime.datetime(2020, 8, 4, 16, 30), 120, 'Kr neki', 100)