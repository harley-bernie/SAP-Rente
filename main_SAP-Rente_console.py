#   S A P - R E N T E     #
#   -------------------   #
#   bernie   17.07.2024   #
#   -------------------   #

"""
Zweck: Dieses Progrmm dient der Ermittlung des letzten Arbeitstages bei SAP incl. Countdown
Python-Version: 3.9
Schnittstellen: Shell (Konsole), Tk/Tcl (Gui)
Konsolenversion
"""

# Datumsfunktionen einbinden
import datetime
from datetime import date

def datumsumwandlung_date(jahr, monat, tag):
    """ wandelt das eingeg. Datum in date-Format um """
    datum = datetime.date(year=jahr,
                         month=monat,
                         day=tag)
    print(datum.strftime("-> %A %d. %B %Y"))
    return datum

def typencheck(eingabe, typ, text):
    """ überprüft eingeg. Wert auf korrektes Type-Format """
    if (typ == 'int'):
        dummy_int = 0
        while isinstance(dummy_int, int):
            try:
                dummy_int = int(input(text))
                break
            except:
                pass
        ausgabe = dummy_int
    elif (typ == 'float'):
        dummy_float = 0.0
        while isinstance(dummy_float, float):
            try:
                dummy_float = float(input(text))
                break
            except:
                pass
        ausgabe = dummy_float
    elif (typ == 'date'):
        datumunbekannt = True
        while datumunbekannt == True:
            try:
                rar_tag = int(eingabe[0:2])
                rar_monat = int(eingabe[3:5])
                rar_jahr = int(eingabe[6:10])
                ausgabe = datumsumwandlung_date(rar_jahr, rar_monat, rar_tag)
                datumunbekannt = False
            except ValueError:
                datumunbekannt = True
                eingabe = input("Datum bitte im Format TT.MM.JJJJ eingeben: ")
    else:
        print("*** ERROR in Funktion typencheck ***")
    return ausgabe

def datum_tage_netto(datum, tage):
    """ ermittelt aus Kalendertagen eine neues Datum """
    # um die Wochenenden zu berücksichtigen, werden die Tage mit 1.4 multipliziert,
    # denn: 5 x 1,4 = 7
    faktor = 1.4
    # da wir nicht den ersten Rententag, sondern den letzten Arbeitstag ausrechnen, addieren wir 1 Tag
    tage_hochgerechnet = (tage * faktor) + 1
    datum_neu = datum - datetime.timedelta(tage_hochgerechnet)
    # Prüfung auf Wochentag: fällt Datum auf Wochenende, wird der vorherige Fr. gezogen
    if (datum_neu.weekday() == 5):
        datum_netto = datum_neu - datetime.timedelta(1)
    elif (datum_neu.weekday() == 6):
        datum_netto = datum_neu - datetime.timedelta(2)
    else:
        datum_netto = datum_neu
    return datum_netto
    
def tage_brutto(datum):
    """ summiert Kalendertage """
    tage_summe = datum - date.today()
    return tage_summe

def tage_netto(tage):
    """ ermittelt Arbeitstage """
    # um Wochenenden & Feiertage zu berücksichtigen, werden die Tage mit 0,7 multipliziert,
    # denn: 0,7 x 365 = 255
    faktor = 0.7
    tage_schaffe = (tage * faktor)
    return tage_schaffe

# def ergebnis_ausgabe(datum_brutto, datum_temp, datum_netto, frei_tage, brutto_tage, netto_tage):
def ergebnis_ausgabe(datum_netto, netto_tage):
    """ Ausgabe des ermittelten Datums """
    print("\nERGEBNIS")
    print("--------")
    print("letzter Arbeitstag mit Berücksichtigung von Wochenenden, Feiertagen und AZK: ", datum_netto.strftime("%A %d. %B %Y"))
    print("Anzahl Werktage bis dahin: ", netto_tage.days)
    print("\nBem.: ohne Gewähr, gewisse Unschärfen müssen akzeptiert werden!\n")
    input("-> für Programmende bitte Taste drücken <-")

# Beginn Hauptprogramm
heute = date.today()
resturlaub_t = 0
azk_h = 0
# Ein-/Ausgabe nur via Text-Konsole:
print("Willkommen zum Projekt SAP-Rente! - Wann bin ich dran? \t ", heute)
print("\nPARAMETER-EINGABE")
rar_datum_string = input("Beginn der Regelaltersrente gem. Rentenauskunft (TT.MM.JJJJ): \t ")
rar = typencheck(rar_datum_string, "date", "Datum (TT.MM.JJJJ): \t ")
resturlaub_t = typencheck(resturlaub_t, "float", "Resturlaub in Tagen (Punkt als Separator): \t ")
azk_h = typencheck(azk_h, "float", "gesammelte h im AZK (Punkt als Separator): \t ")
u_azk_tage = resturlaub_t + (azk_h // 8)
netto_datum = datum_tage_netto(rar, u_azk_tage)
brutto_tage = tage_brutto(netto_datum)
netto_tage = tage_netto(brutto_tage)
ergebnis_ausgabe(netto_datum, netto_tage)

# ENDE