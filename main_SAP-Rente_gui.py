#   S A P - R E N T E     #
#   -------------------   #
#   bernie   25.07.2021   #
#   -------------------   #

"""
Zweck: Dieses Progrmm dient der Ermittlung des letzten Arbeitstages bei SAP
Python-Version: 3.9
Schnittstellen: Shell (Konsole), Tk/Tcl (Gui)
Gui-Version
"""

# Datumsfunktionen einbinden
import datetime
from datetime import date

# GUI-Toolkit TK einbinden
import tkinter as tk
from tkinter import *

def datumsumwandlung_date(jahr, monat, tag):
    """ wandelt das eingeg. Datum in date-Format um """
    datum = datetime.date(year=jahr,
                         month=monat,
                         day=tag)
    datum_label.config(text=(datum.strftime("-> %A %d. %B %Y")))
    return datum

def typencheck(eingabe, typ, text):
    """ überprüft eingeg. Wert auf korrektes Type-Format """
    if (typ == 'int'):
        intunbekannt = True
        while intunbekannt == True:
            try:
                dummy_int = int(eingabe)
                intunbekannt = False
            except ValueError:
                intunbekannt = False
                feier_label.config(text=("*** bitte Tage ganzzahlig ohne Trennzeichen eingeben! ***"))
            try:
                ausgabe = dummy_int
            except NameError:
                ausgabe = ""
    elif (typ == 'float-t'):
        urlaubunbekannt = True
        while urlaubunbekannt == True:
            try:
                dummy_float = float(eingabe)
                urlaubunbekannt = False
            except ValueError:
                urlaubunbekannt = False
                urlaub_label.config(text=("*** bitte Tage als Zahl mit Punkt als Trennzeichen eingeben! ***"))
            try:
                ausgabe = dummy_float
            except NameError:
                ausgabe = ""
    elif (typ == 'float-h'):
        azkunbekannt = True
        while azkunbekannt == True:
            try:
                dummy_float = float(eingabe)
                azkunbekannt = False
            except ValueError:
                azkunbekannt = False
                azk_label.config(text=("*** bitte Stunden als Zahl mit Punkt als Trennzeichen eingeben! ***"))
            try:
                ausgabe = dummy_float
            except NameError:
                ausgabe = ""
    elif (typ == 'date'):
        datumunbekannt = True
        while datumunbekannt == True:
            try:
                rar_tag = int(eingabe[0:2])
                rar_monat = int(eingabe[3:5])
                rar_jahr = int(eingabe[6:10])
                datumunbekannt = False
            except ValueError:
                datumunbekannt = False
                datum_label.config(text=("*** bitte Datum im Format TT.MM.JJJJ eingeben! ***"))
            try:
                ausgabe = datumsumwandlung_date(rar_jahr, rar_monat, rar_tag)
            except NameError:
                ausgabe = ""
    return ausgabe

def datum_tage_netto(datum_alt, tage, firedays):
    """ ermittelt aus Tagen eine neues Datum """
    # um die Wochenenden zu berücksichtigen, werden die Tage mit 1.4 multipliziert,
    # denn: 5 x 1,4 = 7
    faktor = 1.4
    # da wir nicht den ersten Rententag, sondern den letzten Arbeitstag ausrechnen, addieren wir 1 Tag
    tage_hochgerechnet = (tage * faktor) + firedays + 1
    datum_neu = datum_alt - datetime.timedelta(tage_hochgerechnet)
    # Prüfung auf Wochentag: fällt Datum auf Wochenende, wird der vorherige Fr. gezogen
    if (datum_neu.weekday() == 5):
        datum_netto = datum_neu - datetime.timedelta(1)
    elif (datum_neu.weekday() == 6):
        datum_netto = datum_neu - datetime.timedelta(2)
    else:
        datum_netto = datum_neu
    return datum_netto

def button_action1():
    datum_text = eingabe_datum.get()
    if (datum_text == ""):
        datum_label.config(text="*** bitte Datum (TT.MM.JJJJ) eingeben! ***")
    else:
        global rar
        rar_datum_string = datum_text
        datum_text = "Datum: " + datum_text
        rar = typencheck(rar_datum_string, "date", "Datum (TT.MM.JJJJ):")

def button_action2():
    urlaub_text = eingabe_urlaub.get()
    if (urlaub_text == ""):
        urlaub_label.config(text="*** bitte Resturlaub (Tage) eingeben! ***")
    else:
        global resturlaub_t
        urlaub_string = urlaub_text
        urlaub_text = "-> Resturlaub: " + urlaub_text + " Arbeitstage"
        urlaub_label.config(text=urlaub_text)
        resturlaub_t = typencheck(urlaub_string, "float-t", "Resturlaub in Tagen:")

def button_action3():
    azk_text = eingabe_azk.get()
    if (azk_text == ""):
        azk_label.config(text="*** bitte gesammelte AZK-Stunden eingeben! ***")
    else:
        global azk_h
        azk_string = azk_text
        azk_text = "-> AZK: " + azk_text + " Stunden"
        azk_label.config(text=azk_text)
        azk_h = typencheck(azk_string, "float-h", "gesammelte h im AZK:")

def button_action4():
    feier_text = eingabe_feier.get()
    if (feier_text == ""):
        feier_label.config(text="*** bitte zu berücksichtigende Feiertage eingeben! ***")
    else:
        global feiertage
        feier_string = feier_text
        feier_text = "-> Feiertage: " + feier_text + " Tage"
        feier_label.config(text=feier_text)
        feiertage = typencheck(feier_string, "int", "Zahl zu berücksichtigender Feiertage:")

def button_action5():
    tage = resturlaub_t + (azk_h // 8)
    netto_datum = datum_tage_netto(rar, tage, feiertage)
    ergebnis_string = netto_datum.strftime("%A %d. %B %Y")
    ergebnis_label.config(text=ergebnis_string, font=('Arial', 18))
    text1_string = "ERGEBNIS: letzter Arbeitstag mit Berücksichtigung von WE und eingeg. Feiertagen:"
    text1_label.config(text=text1_string, font=('Arial', 16))
    text2_string = "Bem.: ohne Gewähr, gewisse Unschärfen müssen akzeptiert werden!"
    text2_label.config(text=text2_string, font=('Arial', 16))

# Beginn Hauptprogramm
heute = date.today()

# globale Steuervariablen
rar = 0
resturlaub_t = 0
azk_h = 0
feiertage = 0

# Fenster-Kram
fenster = Tk()
fenster.geometry('1024x768')
fenster.title("Willkommen zum Projekt SAP-Rentner! - wann bin ich dran?")

# Anweisungs-Label
datum_label = Label(fenster, text="Beginn der Regelaltersrente gem. Rentenauskunft (TT.MM.JJJJ):", font=('Arial', 14))
urlaub_label = Label(fenster, text="Resturlaub in Tagen (Punkt als Separator):", font=('Arial', 14))
azk_label = Label(fenster, text="gesammelte h im AZK (Punkt als Separator):", font=('Arial', 14))
feier_label = Label(fenster, text="evtl. Anzahl zu berücksichtigender Feiertage:", font=('Arial', 14))
text1_label = Label(fenster)
text2_label = Label(fenster)
ergebnis_label = Label(fenster)

# Benutzer-Eingabenn
eingabe_datum = Entry(fenster, bd=5, width=13, font=('Arial', 14))
eingabe_urlaub = Entry(fenster, bd=5, width=10, font=('Arial', 14))
eingabe_azk = Entry(fenster, bd=5, width=10, font=('Arial', 14))
eingabe_feier = Entry(fenster, bd=5, width=10, font=('Arial', 14))

ok_button1 = Button(fenster, text="OK 1", font=('Arial', 16), command=button_action1)
ok_button2 = Button(fenster, text="OK 2", font=('Arial', 16), command=button_action2)
ok_button3 = Button(fenster, text="OK 3", font=('Arial', 16), command=button_action3)
ok_button4 = Button(fenster, text="OK 4", font=('Arial', 16), command=button_action4)
ergebnis_button = Button(fenster, text="Berechnen", font=('Arial', 18), command=button_action5)
exit_button = Button(fenster, text="EXIT", font=('Arial', 18), command=fenster.quit)

datum_label.place(x=0, y=0)
urlaub_label.place(x=0, y=35)
azk_label.place(x=0, y=70)
feier_label.place(x=0, y=105)
text1_label.place(x=50, y=250)
ergebnis_label.place(x=140, y=280)
text2_label.place(x=50, y=310)

eingabe_datum.place(x=430, y=0)
eingabe_urlaub.place(x=440, y=35)
eingabe_azk.place(x=440, y=70)
eingabe_feier.place(x=440, y=105)

ok_button1.place(x=560, y=0)
ok_button2.place(x=560, y=35)
ok_button3.place(x=560, y=70)
ok_button4.place(x=560, y=105)
ergebnis_button.place(x=530, y=150)
exit_button.place(x=550, y=190)

fenster.mainloop()

# ENDE