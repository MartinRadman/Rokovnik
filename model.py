import datetime, math, json

class Rokovnik:
    def __init__(self, delo_na_dan):
        self.delo_na_dan = delo_na_dan
        self.predmeti = []
        self.izpiti = []
        self.izpiti_po_datumih = {}
        self.izpiti_po_pricakovanem_delu = {}
        self.izpiti_po_prioriteti = []
        self.razporeditev_dela = {}

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

    def poisci_predmet_glede_na_ime(self, ime_predmeta):
        for predmet in self.predmeti:
            if predmet.ime == ime_predmeta:
                return predmet
        return ValueError('Predmet s tem imenom ne obstaja!')

    def oceni_pricakovano_delo(self, izpit):
        kolicina_gradiva = izpit.kolicina_gradiva
        predelano_gradivo = izpit.predelano_gradivo
        preostanek = int(kolicina_gradiva - predelano_gradivo)
        tezavnost = int(izpit.predmet.tezavnost)
        minute = int((preostanek / (50 / tezavnost)) * 60)
        self.izpiti_po_pricakovanem_delu[izpit] = minute

    def kolicina_dela_na_dan(self, izpit):
        delo = self.izpiti_po_pricakovanem_delu[izpit]
        st_dni = self.stevilo_dni_do_izpita(izpit)
        try:
            return delo / st_dni
        except:
            return -1

    def stevilo_dni_do_izpita(self, izpit):
        razlika = izpit.datum - datetime.datetime.now()
        return razlika.days

    def razvrsti_po_prioriteti(self, izpit):
        delo_na_dan = self.kolicina_dela_na_dan(izpit)
        pricakovana_ocena = int(izpit.predmet.pricakovana_ocena)
        self.izpiti_po_prioriteti.append((izpit, int(delo_na_dan * pricakovana_ocena)))
        self.izpiti_po_prioriteti.sort(key=lambda x: x[1])

    def razporedi_delo_enakomerno(self):
        self.razporeditev_dela = {}
        ostanek_dela = {}
        for izpit, _ in self.izpiti_po_prioriteti:
            celotno_delo1 = self.enakomerna_razporeditev(izpit, self.kolicina_dela_na_dan(izpit), self.izpiti_po_pricakovanem_delu[izpit])
            celotno_delo2 = self.izpiti_po_pricakovanem_delu[izpit]
            while celotno_delo1 != celotno_delo2:
                celotno_delo2 = celotno_delo1
                celotno_delo1 = self.enakomerna_razporeditev(izpit, celotno_delo1 / self.stevilo_dni_do_izpita(izpit), celotno_delo1)
            if celotno_delo1 > 0:
                ostanek_dela[izpit] = celotno_delo1
        return ostanek_dela

    def enakomerna_razporeditev(self, izpit, delo_na_dan, celotno_delo):
        for razpolozljivi_dan in self.razpolozljivi_dnevi(izpit):
                if celotno_delo <= 0:
                    break
                dan = self.dan_v_datumu(razpolozljivi_dan)
                zasedeno = self.preveri_koliko_je_dela_na_dan(dan)
                na_razpolagi = self.delo_na_dan - zasedeno
                dodeljeno_delo = math.ceil(min(na_razpolagi, delo_na_dan))
                if izpit in self.razporeditev_dela.get(dan, {}):
                    self.razporeditev_dela[dan][izpit] += dodeljeno_delo
                else: 
                    self.razporeditev_dela[dan] = {**self.razporeditev_dela.get(dan, {}), **{izpit: dodeljeno_delo}}
                celotno_delo -= dodeljeno_delo
        return celotno_delo

    @staticmethod
    def dan_v_datumu(datum):
        dan, _ = str(datum).split(' ')
        return dan

    @staticmethod
    def razpolozljivi_dnevi(izpit):
        razpolozljivi_dnevi = []
        razlika = izpit.datum - datetime.datetime.now()
        st_dni = razlika.days - 1
        for i in range(1, st_dni + 1):
                datum = datetime.datetime.now() + datetime.timedelta(days=i)
                razpolozljivi_dnevi.append(datum)
        return razpolozljivi_dnevi

    def preveri_koliko_je_dela_na_dan(self, dan):
        try:
            delo_po_predmetih = self.razporeditev_dela[dan]
            delo = sum(delo_po_predmetih.values())
            return delo
        except:
            return 0

    def slovar_s_stanjem(self):
        return {
            'delo_na_dan': self.delo_na_dan,
            'predmeti': [{
                'ime': predmet.ime,
                'pricakovana_ocena': predmet.pricakovana_ocena,
                'tezavnost': predmet.tezavnost
            } for predmet in self.predmeti],
            'izpiti': [{
                'datum': str(izpit.datum),
                'dolzina_izpita': izpit.dolzina_izpita,
                'tematika': izpit.tematika,
                'kolicina_gradiva': izpit.kolicina_gradiva,
                'predelano_gradivo': izpit.predelano_gradivo,
                'predmet': str(izpit.predmet)
            } for izpit in self.izpiti],
        }

    @staticmethod
    def nalozi_iz_slovarja(slovar_s_stanjem):
        rokovnik = Rokovnik(slovar_s_stanjem['delo_na_dan'])
        for predmet in slovar_s_stanjem['predmeti']:
            predmet_obj = rokovnik.dodaj_predmet(
                predmet['ime'],
                predmet['pricakovana_ocena'],
                predmet['tezavnost'],
                )
            for izpit in slovar_s_stanjem['izpiti']:
                if predmet['ime'] == izpit['predmet']:
                    predmet_obj.dodaj_izpit(
                        datetime.datetime.strptime(izpit['datum'], '%Y-%m-%d %H:%M:%S'),
                        izpit['dolzina_izpita'],
                        izpit['tematika'],
                        izpit['kolicina_gradiva'],
                        izpit['predelano_gradivo']
                        )
        return rokovnik
    
    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w', encoding='UTF-8') as datoteka:
            json.dump(self.slovar_s_stanjem(), datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, datoteka):
        with open(datoteka, encoding='UTF-8') as dat:
            slovar_s_stanjem = json.load(dat)
        return cls.nalozi_iz_slovarja(slovar_s_stanjem)

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
        dan = self.rokovnik.dan_v_datumu(izpit.datum)
        self.izpiti_po_datumih[dan] = self.izpiti_po_datumih.get(dan, []) + [izpit]
        self.rokovnik.izpiti_po_datumih[dan] = self.rokovnik.izpiti_po_datumih.get(dan, []) + [izpit]
        self.rokovnik.oceni_pricakovano_delo(izpit)
        self.izpiti.sort()
        self.rokovnik.izpiti.sort()
        self.rokovnik.razvrsti_po_prioriteti(izpit)
        self.rokovnik.oceni_pricakovano_delo(izpit)

    def odstrani_izpit(self, izpit):
        dan = self.rokovnik.dan_v_datumu(izpit.datum)
        self.izpiti_po_datumih[dan].remove(izpit)
        self.izpiti.remove(izpit)
        self.rokovnik.izpiti_po_datumih[dan].remove(izpit)
        self.rokovnik.izpiti.remove(izpit)

    def preveri_datum(self, datum, dolzina_izpita):
        dan = self.rokovnik.dan_v_datumu(datum)    
        if dan in self.izpiti_po_datumih:
            for izpit in self.izpiti_po_datumih[dan]:
                dolzina_izpita2 = izpit.dolzina_izpita
                if datum < izpit.datum and izpit.datum - datum < datetime.timedelta(minutes=dolzina_izpita):
                    return False
                elif izpit.datum < datum and datum - izpit.datum < datetime.timedelta(minutes=dolzina_izpita2):
                    return False
        return True

    def najdi_izpit_glede_na_cas(self, datum):
        for izpit in self.izpiti:
            if izpit.datum == datum:
                return izpit
        return ValueError('Izpit ob tem času ne obstaja!')

class Izpit:
    def __init__(self, datum, dolzina_izpita, tematika, kolicina_gradiva, predelano_gradivo, predmet):
        self.datum = datum
        self.dolzina_izpita = dolzina_izpita
        self.tematika = tematika
        self.kolicina_gradiva = kolicina_gradiva
        self.predelano_gradivo = predelano_gradivo
        self.predmet = predmet
        self.ime = f'Izpit pri predmetu {self.predmet}, ki bo izveden {self.datum}'

    def __str__(self):
        return f'\033[92m{self.predmet}\033[0m Izpit bo izveden {self.datum} in bo trajal {self.dolzina_izpita} minut. Opis: {self.tematika}'

    def __gt__(self, other):
        return self.datum > other.datum


class Racun:
    def __init__(self, ime, geslo, rokovnik):
        self.ime = ime
        self.geslo = geslo
        self.rokovnik = rokovnik
    
    def avtentikacija_gesla(self, geslo):
        if self.geslo != geslo:
            raise ValueError('Vnešeno geslo je napačno!')
    
    def shrani_stanje(self, dat):
        stanje = {
            'ime': self.ime,
            'geslo': self.geslo,
            'rokovnik': self.rokovnik.slovar_s_stanjem(),
        }
        with open(dat, 'w', encoding='UTF-8') as d:
            json.dump(stanje, d, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, dat):
        with open(dat, encoding='UTF-8') as d:
            stanje = json.load(d)
        ime = stanje['ime']
        geslo = stanje['geslo']
        rokovnik = Rokovnik.nalozi_iz_slovarja(stanje['rokovnik'])
        return cls(ime, geslo, rokovnik)
    