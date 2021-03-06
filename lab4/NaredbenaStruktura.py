from lab4 import config
from lab4 import PomocneFunkcije
from lab4 import Izrazi
from lab4 import Deklaracije_I_Definicije
from lab4.CvorStabla import CvorStabla
from lab4.CvorTablice import CvorTablice
from lab4.CvorTabliceUpgrade import CvorTabliceUpgrade


def slozena_naredba(cvor_stabla):
    #print("U slozena naredba metodi")

    kopija_dosega = CvorTablice(config.doseg.roditelj)
    kopija_dosega.lista_deklaracija = config.doseg.lista_deklaracija

    if config.doseg.je_u_petlji:
        kopija_dosega.je_u_petlji = True

    novi_doseg = CvorTablice(kopija_dosega)
    if cvor_stabla.je_u_petlji or config.doseg.je_u_petlji:
        novi_doseg.je_u_petlji = True
    config.doseg = novi_doseg

    if cvor_stabla.je_u_petlji:
        config.doseg.je_u_petlji = True

    for i in range(len(cvor_stabla.vrati_tipove(config.doseg))):
        novi_cvor = CvorStabla('<' + cvor_stabla.lista_imena[i], -1)

        novi_cvor.postavi_tip(cvor_stabla.vrati_tipove(config.doseg)[i])

        if cvor_stabla.je_u_petlji:
            novi_cvor.je_u_petlji = True

        novi_cvor.ime = cvor_stabla.lista_imena[i]
        #print(str(novi_cvor))
        config.doseg.lista_deklaracija.append(novi_cvor)

        offset = 4 * len(cvor_stabla.lista_imena)
        for ime in cvor_stabla.lista_imena:
            cvor_stabla.dodaj_kod("\tLOAD R0, (R7+" + str(offset) + ")\n")
            labela = "L" + str(config.brojac_labela)
            config.brojac_labela += 1
            cvor_stabla.dodaj_kod("\tSTORE R0, (" + labela + ")\n")
            PomocneFunkcije.vrati_vec_deklarirano(ime).labela = labela
            offset -= 4
            novi = CvorTabliceUpgrade(labela, None)
            novi.je_prazno = True
            config.tabela.append(novi)

    if len(cvor_stabla.lista_djece) == 3:
        lista_naredbi(cvor_stabla.lista_djece[1])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
    else:
        if cvor_stabla.je_u_petlji:
            cvor_stabla.lista_djece[1].je_u_petlji = True
        
        Deklaracije_I_Definicije.lista_deklaracija(cvor_stabla.lista_djece[1])
        if config.error:
            return

        lista_naredbi(cvor_stabla.lista_djece[2])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
    config.doseg = config.doseg.roditelj
    return


def lista_naredbi(cvor_stabla):
    #print("U lista naredbi metodi")
    if len(cvor_stabla.lista_djece) == 1:
       naredba(cvor_stabla.lista_djece[0])
       if config.error:
           return
       cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
    elif len(cvor_stabla.lista_djece) > 1:
        lista_naredbi(cvor_stabla.lista_djece[0])
        if config.error:
            return
        naredba(cvor_stabla.lista_djece[1])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
    return


def naredba(cvor_stabla):
    #print("U naredba metodi")

    desna_strana = cvor_stabla.lista_djece[0]
    if cvor_stabla.je_u_petlji:
        desna_strana.je_u_petlji = True

    podaci_desne_strane = desna_strana.podaci

    if podaci_desne_strane == '<slozena_naredba>':
        slozena_naredba(desna_strana)
    if podaci_desne_strane == '<izraz_naredba>':
        izraz_naredba(desna_strana)
    if podaci_desne_strane == '<naredba_grananja>':
        naredba_grananja(desna_strana)
    if podaci_desne_strane == '<naredba_petlje>':
        naredba_petlje(desna_strana)
    if podaci_desne_strane == '<naredba_skoka>':
        naredba_skoka(desna_strana)

    if config.error:
        return
    cvor_stabla.dodaj_kod(desna_strana.kod)

    return


def izraz_naredba(cvor_stabla):
    #print("U izraz naredba metodi")
    if len(cvor_stabla.lista_djece) == 1:
        cvor_stabla.postavi_tip("int")
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
    else:
        Izrazi.izraz(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.postavi_tip(cvor_stabla.lista_djece[0].vrati_tip(config.doseg))
        cvor_stabla.lista_tipova = cvor_stabla.lista_djece[0].vrati_tipove(config.doseg)
        cvor_stabla.ime = cvor_stabla.lista_djece[0].vrati_ime()
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)

    return


def naredba_grananja(cvor_stabla):
    #print("U naredba grananja metodi")

    Izrazi.izraz(cvor_stabla.lista_djece[2])
    if config.error:
        return

    if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), 'int') or cvor_stabla.lista_djece[2].je_funkcija():
        PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
        return

    naredba(cvor_stabla.lista_djece[4])
    if config.error:
        return

    if len(cvor_stabla.lista_djece) > 5:
        naredba(cvor_stabla.lista_djece[6])
        if config.error:
            return
    cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[2].kod)
    cvor_stabla.dodaj_kod("\tPOP R0\n")
    cvor_stabla.dodaj_kod("\tCMP R0, 0\n")
    cvor_stabla.dodaj_kod("\tJP_EQ " + "ELSE" + str(config.if_counter_label) + "\n")
    cvor_stabla.dodaj_kod("THEN" + str(config.if_counter_label) + "\n")
    cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[4].kod)
    cvor_stabla.dodaj_kod("\tJP " + "ENDIF" + str(config.if_counter_label) + "\n")
    cvor_stabla.dodaj_kod("\tJP_NE " + "ELSE" + str(config.if_counter_label) + "\n")
    cvor_stabla.dodaj_kod("ELSE" + str(config.if_counter_label) + "\n")

    if len(cvor_stabla.lista_djece) == 7:
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[6].kod)

    cvor_stabla.dodaj_kod("ENDIF" + str(config.if_counter_label) + "\n")
    config.if_counter_label += 1

    return


def naredba_petlje(cvor_stabla):
    #print("U naredba petlje metodi")

    if len(cvor_stabla.lista_djece) == 5:

        Izrazi.izraz(cvor_stabla.lista_djece[2])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[2].vrati_tip(config.doseg), 'int') or cvor_stabla.lista_djece[2].je_funkcija():
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.lista_djece[4].je_u_petlji = True

        naredba(cvor_stabla.lista_djece[4])
        if config.error:
            return

    if len(cvor_stabla.lista_djece) == 6:

        izraz_naredba(cvor_stabla.lista_djece[2])
        if config.error:
            return

        izraz_naredba(cvor_stabla.lista_djece[3])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[3].vrati_tip(config.doseg), 'int') or cvor_stabla.lista_djece[3].je_funkcija():
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        cvor_stabla.lista_djece[5].je_u_petlji = True

        naredba(cvor_stabla.lista_djece[5])
        if config.error:
            return

    if len(cvor_stabla.lista_djece) == 7:

        izraz_naredba(cvor_stabla.lista_djece[2])
        if config.error:
            return

        izraz_naredba(cvor_stabla.lista_djece[3])
        if config.error:
            return

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[3].vrati_tip(config.doseg), 'int') or cvor_stabla.lista_djece[3].je_funkcija():
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return

        Izrazi.izraz(cvor_stabla.lista_djece[4])
        if config.error:
            return

        cvor_stabla.lista_djece[6].je_u_petlji = True

        naredba(cvor_stabla.lista_djece[6])
        if config.error:
            return

    return


def naredba_skoka(cvor_stabla):
    #print("U naredba skoka metodi")

    if len(cvor_stabla.lista_djece) == 3:

        Izrazi.izraz(cvor_stabla.lista_djece[1])
        if config.error:
            return

        tip = PomocneFunkcije.vrati_tip_trenutne_funkcije()

        if not PomocneFunkcije.je_castable(cvor_stabla.lista_djece[1].vrati_tip(config.doseg), tip) or cvor_stabla.lista_djece[1].je_funkcija():
            PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
        cvor_stabla.dodaj_kod("\tPOP R6\n\tRET\n")

    else:
        if cvor_stabla.lista_djece[0].podaci.startswith('KR_RETURN'):
            if PomocneFunkcije.vrati_tip_trenutne_funkcije() != 'void':
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return
            cvor_stabla.dodaj_kod("\tRET\n")
        else:
            if not config.doseg.je_u_petlji:
                PomocneFunkcije.ispisi_error_poruku(cvor_stabla)
                return

    return


def prijevodna_jedinica(cvor_stabla):
    #print("U prijevodna jedinica metodi")
    if len(cvor_stabla.lista_djece) == 1:
        vanjska_deklaracija(cvor_stabla.lista_djece[0])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
    elif len(cvor_stabla.lista_djece) > 1:
        prijevodna_jedinica(cvor_stabla.lista_djece[0])
        if config.error:
            return
        vanjska_deklaracija(cvor_stabla.lista_djece[1])
        if config.error:
            return
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
        cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[1].kod)
    return


def vanjska_deklaracija(cvor_stabla):
    #print("U vanjska deklaracija metodi")
    if cvor_stabla.lista_djece[0].podaci == '<definicija_funkcije>':
        Deklaracije_I_Definicije.definicija_funkcije(cvor_stabla.lista_djece[0])
        if config.error:
            return
    else:
        Deklaracije_I_Definicije.deklaracija(cvor_stabla.lista_djece[0])
        if config.error:
            return
    cvor_stabla.dodaj_kod(cvor_stabla.lista_djece[0].kod)
    return
