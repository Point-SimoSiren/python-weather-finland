import sqlite3
import requests #### Requests kirjastolla http pyynnöt on näppärämpiä Tee pip install requests -komento!
from datetime import datetime

# Funktio joka kirjoittaa lokia
def kirjoita_lokia(parametri):
    aikaleima = datetime.now().strftime('%d.%m.%Y klo %H.%M:%S')
   
    tiedosto = open("lampo_loki.txt", "a")
    rivi = str(aikaleima) + " " + parametri
   
    tiedosto.write(rivi + "\r")
    tiedosto.close()

paikkakunta = ""

print("Säähakusovellus käynnistyy...")
print()
print('Haluatko vaihtaa haettavia paikkakuntia?')
syöte = input("Vastaa antamalla K tai X.")

if syöte.upper() == "K":
    
    conn = sqlite3.connect('Kunnat.db')
    print()
    print("Kunnat tietokantaan yhdistetty.")
    sql2 = """DROP TABLE IF EXISTS Paikkakunnat"""
    kursori = conn.cursor()
    kursori.execute(sql2)
    sql = """CREATE TABLE IF NOT EXISTS Paikkakunnat(
        paikkakunta text)"""
    print()    
    print("Lisätään uusi Paikkakunnat taulu tietokantaan.")    
    kursori = conn.cursor()
    kursori.execute(sql)
    print()
    print("Taulu lisätty tietokantaan.")
    print()

    while paikkakunta != "X":
        paikkakunta = input("Anna paikkakunta: ")
        if paikkakunta != "X": 
            sql = f'INSERT INTO Paikkakunnat VALUES ("{paikkakunta}")'
            kursori.execute(sql)
            conn.commit()
            print("Paikkakunta tallennettu.")
            print()

        else:
            continue
            
elif syöte.upper() == "X":
    print("Seuraava kysymys.")
    print()
else:
    print("Annoit väärän vastauksen.")

print("Haluatko hakea lämpötilatiedon ilmatieteenlaitokselta? K tai X")
syöte2 = input("Mikä on vastauksesi? ")
print()

if syöte2.upper() == "K":
    conn = sqlite3.connect('Kunnat.db')
    kursori = conn.cursor()
    print("Tässä tulokset paikkakuntien lämpötiloista!")
    sql = "SELECT paikkakunta FROM Paikkakunnat"
    for rivi in kursori.execute(sql):
        
        paikkakuntaStr = str(rivi)

        paikkakunta = paikkakuntaStr[2:-3]      
        url = f"https://www.ilmatieteenlaitos.fi/saa/{paikkakunta}"
               
        vastaus = requests.get(url, params={"encoding": "utf-8"})
        vastauksen_status = vastaus.status_code
        laskuri = 0
        if vastauksen_status == 200:
            html = str(vastaus.text)
            indeksi = html.index('Temperature') # Tämä teksti etsitään html sisällöstä
            alku = indeksi + 11 # Tämän verran Temperature sanan alusta niin alkaa lukema
            loppu = alku + 5 # Tässä lukema päättyy
            html2 = html[alku:loppu]
            print(f"Lämpötila {paikkakunta} on {html2}")
            laskuri += 1
            kirjoita_lokia(f"Löydettiin {laskuri} tulosta.")

        elif vastauksen_status == 500:
            kirjoita_lokia(f"{paikkakunta} Hakuvirhe")
        else:
            print("Odottamaton virhe. Ohjelman suoritus päättyy.")
               
        print("Valmis!")
        

elif syöte2.upper() == "X":
    print("Kiitos ja näkemiin!")
    
else:
    print("Vastausmuoto oli virheellinen.")
    
print()
conn.close()
print("Tack och adjö")

