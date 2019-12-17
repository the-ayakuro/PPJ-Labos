import config
import PomocneFunkcije
import Izrazi
import NaredbenaStruktura
from CvorStabla import CvorStabla
from CvorTablice import CvorTablice

definirane_funkcije = []
deklarirane_funkcije = []

#Nisam sig za ove postavi_tipove i to, provjeriti

def definicija_funkcije(cvor_stabla):
    global definirane_funkcije
    global deklarirane_funkcije
    Izrazi.ime_tipa(cvor_stabla.lista_djece[0])
    if cvor_stabla.lista_djece[0].je_konstanta:
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    if PomocneFunkcije.funkcija_vec_postoji(config.doseg,cvor_stabla.lista_djece[0].ime):
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    if cvor_stabla.lista_djece[3].podaci.startswith("KR_VOID"):
        if PomocneFunkcije.konfliktna_deklaracija(config.doseg,cvor_stabla.lista_djece[0].ime,cvor_stabla.lista_djece[0].vrati_tip(config.doseg)):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.je_definiran = True
        cvor_stabla.ime = cvor_stabla.lista_djece[1].ime
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.postavi_tip("void")
        if cvor_stabla.ime == "main" and cvor_stabla.vrati_tip(config.doseg) == "int":
            config.nema_main = False
        config.doseg.dodaj_dijete(cvor_stabla)
        definirane_funkcije.append(cvor_stabla.ime)
        NaredbenaStruktura.slozena_naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return
    else:
        lista_parametara(cvor_stabla.lista_djece[3])
        if config.error:
            return
        if PomocneFunkcije.konfliktna_deklaracija(config.doseg,cvor_stabla.ime,cvor_stabla.vrati_tip(config.doseg)):
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.je_definiran = True
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[1].ime
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[3].vrati_tipove(config.doseg)
        cvor_stabla.lista_imena = cvor_stabla.lista_djece[3].vrati_imena()
        definirane_funkcije.append(cvor_stabla.ime)
        config.doseg.dodaj_dijete(cvor_stabla)
        NaredbenaStruktura.slozena_naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return
    return

def deklaracija_parametara(cvor_stabla):
    Izrazi.ime_tipa(cvor_stabla.lista_djece[0])
    if config.error:
        return
    if cvor_stabla.lista_djece[0].vrati_tip(config.doseg) == "void":
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    if len(cvor_stabla.lista_djece) == 2:
        cvor_stabla.tip = cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
    else:
        cvor_stabla.tip = "niz" + cvor_stabla.lista_djece[0].vrati_tip(config.doseg)
    cvor_stabla.ime = cvor_stabla.lista_djece[1].vrati_ime()
    config.doseg.dodaj_dijete(cvor_stabla)
    return

def lista_parametara(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        deklaracija_parametara(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.dodaj_ime(cvor_stabla.lista_djece[0].vrati_ime())
    lista_parametara(cvor_stabla.lista_djece[0])
    if config.error:
        return
    deklaracija_parametara(cvor_stabla.lista_djece[2])
    if config.error:
        return
    if cvor_stabla.lista_djece[2].ime in cvor_stabla.lista_djece[0].lista_imena:
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return
    cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
    cvor_stabla.postavi_tip(cvor_stabla.lista_djece[2].vrati_tip(config.doseg))
    cvor_stabla.lista_imena = cvor_stabla.lista_djece[0].vrati_imena()
    cvor_stabla.dodaj_ime(cvor_stabla.lista_djece[2].vrati_ime())
    return


def lista_deklaracija(cvor_stabla):
    if len(cvor_stabla.lista_djece) == 1:
        deklaracija(cvor_stabla.lista_djece[0])
    else:
        lista_deklaracija(cvor_stabla.lista_djece[0])
        deklaracija(cvor_stabla.lista_djece[1])
    return


def deklaracija(cvor_stabla):
    Izrazi.ime_tipa(cvor_stabla.lista_djece[0])
    if config.errror:
        return
    cvor_stabla.lista_djece[1].postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
    lista_init_deklaratora(cvor_stabla.lista_djece[1])
    return


def lista_init_deklaratora(cvor_stabla):
    return


def init_deklarator(cvor_stabla):
    return


def izravni_deklarator(cvor_stabla):
    return


def inicijalizator(cvor_stabla):
    return


def lista_izraza_pridruzivanja(cvor_stabla):
    return