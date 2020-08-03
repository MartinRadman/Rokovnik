import datetime

class Rokovnik:
    def __init__(self):
        self.predmeti = []

    def dodaj_predmet(self, ime, pricakovana_ocena, tezavnost):
        for predmet in self.predmeti:
            if ime.lower() == predmet.ime.lower():
                raise ValueError('Ta predmet že obstaja!')
        predmet = Predmet(ime, pricakovana_ocena, tezavnost)
        self.predmeti.append(predmet)
        return predmet

    def odstrani_predmet(self, predmet):
        self.predmeti.remove(predmet)


class Predmet:
    def __init__(self, ime, pricakovana_ocena, tezavnost):
        self.ime = ime
        self.pricakovana_ocena = pricakovana_ocena
        self.tezavnost = tezavnost
        self.izpiti = []
        self.izpiti_po_datumih = {}

    def dodaj_izpit(self, datum, dolzina_izpita, tematika, kolicina_gradiva):
        if not self.preveri_datum(datum, dolzina_izpita):
            raise ValueError('Ob tem času imate že zabeležen nek izpit!')
        izpit = Izpit(datum, dolzina_izpita, tematika, kolicina_gradiva)
        self.izpiti.append(izpit)
        dan = izpit.datum.strftime("%x")
        self.izpiti_po_datumih[dan] = self.izpiti_po_datumih.get(dan, []) + [izpit]

    def odstrani_izpit(self, izpit):
        dan = izpit.datum.strftime("%x")
        self.izpiti_po_datumih[dan].remove(izpit)
        self.izpiti.remove(izpit)

    def preveri_datum(self, datum, dolzina_izpita):
        dan = datum.strftime("%x")    
        if dan in self.izpiti_po_datumih:
            for izpit in self.izpiti_po_datumih[dan]:
                dolzina_izpita2 = izpit.dolzina_izpita
                if datum < izpit.datum and izpit.datum - datum < datetime.timedelta(minutes=dolzina_izpita):
                    return False
                elif izpit.datum < datum and datum - izpit.datum < datetime.timedelta(minutes=dolzina_izpita2):
                    return False
        return True

class Izpit:
    def __init__(self, datum, dolzina_izpita, tematika, kolicina_gradiva):
        self.datum = datum
        self.dolzina_izpita = dolzina_izpita
        self.tematika = tematika
        self.kolicina_gradiva = kolicina_gradiva