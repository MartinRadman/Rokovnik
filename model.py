import datetime

class Rokovnik:
    def __init__(self, ime, delo_na_dan):
        self.ime = ime
        self.delo_na_dan = delo_na_dan
        self.predmeti = []
        self.izpiti = []
        self.izpiti_po_datumih = {}
        self.izpiti_po_pricakovanem_delu = {}
        self.izpiti_po_prioriteti = []

    def dodaj_predmet(self, ime, pricakovana_ocena, tezavnost):
        for predmet in self.predmeti:
            if ime.lower() == predmet.ime.lower():
                raise ValueError('Ta predmet že obstaja!')
        predmet = Predmet(ime, pricakovana_ocena, tezavnost, self)
        self.predmeti.append(predmet)
        self.predmeti.sort()
        return predmet

    def odstrani_predmet(self, predmet):
        self.predmeti.remove(predmet)

    def oceni_pricakovano_delo(self, izpit):
        kolicina_gradiva = izpit.kolicina_gradiva
        predelano_gradivo = izpit.predelano_gradivo
        preostanek = kolicina_gradiva - predelano_gradivo
        tezavnost = izpit.predmet.tezavnost
        minute = int((preostanek / (50 / tezavnost)) * 60)
        self.izpiti_po_pricakovanem_delu[izpit] = minute

    def kolicina_dela_na_dan(self, izpit):
        delo = self.izpiti_po_pricakovanem_delu[izpit]
        st_dni = izpit.datum.day - datetime.datetime.now().day
        return delo / st_dni

    def razvrsti_po_prioriteti(self, izpit):
        delo_na_dan = self.kolicina_dela_na_dan(izpit)
        pricakovana_ocena = izpit.predmet.pricakovana_ocena
        self.izpiti_po_prioriteti.append((izpit, int(delo_na_dan * pricakovana_ocena)))
        self.izpiti_po_prioriteti.sort(key=lambda x: x[1])

    def razporedi_delo(self, izpit, nacin):
        if nacin == 'čim prej':
            self.razporedi_delo_cim_prej(izpit)
        elif nacin == 'enakomerno':
            self.razporedi_delo_enakomerno(izpit)
        else:
            self.razporedi_delo_cim_kasneje(izpit)

    def razporedi_delo_cim_prej(self, izpit):
        pass

    def razporedi_delo_enakomerno(self, izpit):
        pass

    def razporedi_delo_cim_kasneje(self, izpit):
        pass


class Predmet:
    def __init__(self, ime, pricakovana_ocena, tezavnost, rokovnik):
        self.ime = ime
        self.pricakovana_ocena = pricakovana_ocena
        self.tezavnost = tezavnost
        self.izpiti = []
        self.izpiti_po_datumih = {}
        self.rokovnik = rokovnik

    def __str__(self):
        return self.ime

    def __gt__(self, other):
        return self.ime > other.ime

    def dodaj_izpit(self, datum, dolzina_izpita, tematika, kolicina_gradiva, predelano_gradivo):
        if not self.preveri_datum(datum, dolzina_izpita):
            raise ValueError('Ob tem času imate že zabeležen nek izpit!')
        izpit = Izpit(datum, dolzina_izpita, tematika, kolicina_gradiva, predelano_gradivo, self)
        self.izpiti.append(izpit)
        self.rokovnik.izpiti.append(izpit)
        self.razvrsti_izpite(izpit)

    def razvrsti_izpite(self, izpit):
        dan = izpit.datum.strftime("%x")
        self.izpiti_po_datumih[dan] = self.izpiti_po_datumih.get(dan, []) + [izpit]
        self.rokovnik.izpiti_po_datumih[dan] = self.rokovnik.izpiti_po_datumih.get(dan, []) + [izpit]
        self.rokovnik.oceni_pricakovano_delo(izpit)
        self.izpiti.sort()
        self.rokovnik.izpiti.sort()

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
    def __init__(self, datum, dolzina_izpita, tematika, kolicina_gradiva, predelano_gradivo, predmet):
        self.datum = datum
        self.dolzina_izpita = dolzina_izpita
        self.tematika = tematika
        self.kolicina_gradiva = kolicina_gradiva
        self.predelano_gradivo = predelano_gradivo
        self.predmet = predmet

    def __str__(self):
        return f'\033[92m{self.predmet}\033[0m {self.datum} {self.dolzina_izpita} minut: {self.tematika}'

    def __gt__(self, other):
        return self.datum > other.datum



    