#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 20:37:00 2023

@author: eliaselter
"""

#importerer vikitge bibliotek
import matplotlib.pyplot as plt
import requests
import json
#spør om ønsekde mengde dager
ant_dager = int(input("Hvor mange dager bak har du lyst til å gå? (50-1000): "))
#spør om hvilken aksje som skal vises
aksje = input("Skriv inn aksjenavn: ")
#henter api og oppdaterer den hver dag
url=f'https://api.twelvedata.com/time_series?start_date=2018-01-01&outputsize={ant_dager}&symbol={aksje}&interval=1day&apikey=9d09b5db90cd43cd95d44040ec89d644'

#gjør om data 
resultat = requests.get(url)    
data = resultat.json()
#data_formatert = json.dumps(data, indent=2)

#oppretter viktige lister som trengs for å plotte
dag = []
gjennomsnittsverdi = []

#henter verdiene fra api å legger de i listen gjennomsnittsverdi, samt at den regner ut gjennomsnittsverdien for dagen
verdier = data["values"]
for v in verdier:
  gdag = float(v["low"])+float(v["high"])/2
  gjennomsnittsverdi.append(round(gdag, 3))

#gjør det samme bare med datoene
for d in verdier:
  tid = d["datetime"]
  dag.append(tid)

#regner snitt de siste 10 og 50 dagene samt alle dagene oppgitt
def snittRegner(x):
  snitt = sum(gjennomsnittsverdi[:x]) 
  snitt = snitt / x
  snitt = round(snitt,2)
  return snitt

#kaller på funskjonen
totalsnitt = snittRegner(ant_dager)
snittFemti = snittRegner(50)
snittTi = snittRegner(10)


#setter navn på aksene og setter opp titel
plt.xlabel("Dato", fontsize=12)
plt.ylabel("Verdi (USD)", fontsize=12)
plt.title(f"Aksjekursen til {aksje} de siste {ant_dager} dagene (live)")

#gjør at intervallet totalt blit 20 x-Ticks og x-Dato uansett hvor mange dager som vises totalt
intervall = len(dag) // 20
#antall ticks og gjør at det totalt blit 20 stykk
xTicks = list(range(0, len(dag), intervall))
#gjør at de samsvarende 20 datoene blir vist
xDato = [dag[i] for i in xTicks]
#bruker de paramterene og setter de inn i grafen samt at de roterer for at grafen ikke skal overlappe
plt.xticks(xTicks, xDato, rotation=45)
# Juster tekststørrelsen for x-artikklene
plt.tick_params(axis='x', labelsize=10) 


#endrer fargene på snittene i grafen sånn at de viser om det er lurt eller ikke lurt å kjøpe aksjen
fargeFemti = "darkblue"
fargeTi = "blue"
if totalsnitt < snittTi and totalsnitt < snittFemti:
  fargeTi = "green"
  fargefemti = "darkgreen"
elif  totalsnitt > snittTi and totalsnitt > snittFemti: 
  fargeTi = "red"
  fargefemti = "darkred"
elif totalsnitt <snittFemti and snittFemti<snittTi:
  fargeTi = "gold"
  fargefemti = "green"
  

#inverterer aksen sånn at den blir riktig
plt.gca().invert_xaxis()

#plotter hovedgrafen
plt.plot(dag,gjennomsnittsverdi, label=f'gjennomsnittsverdi hver dag de siste {ant_dager} dagene')
#plotter totalsnitt
plt.plot(dag, [totalsnitt] * len(dag), linestyle='--', label=f'Totalt Gjennomsnitt: {totalsnitt}$', color = "gray")
#plotter snittFemti
plt.plot(dag, [snittFemti] * len(dag), linestyle='--', label=f'Snitt siste 50 dager: {snittFemti}$', color = f"{fargefemti}")
#plotter snittTi
plt.plot(dag, [snittTi] * len(dag), linestyle='--', label=f'Snitt siste 10 dager: {snittTi}$', color =f"{fargeTi}")
#den boksen i gjørne
plt.legend(fontsize=8)
plt.show()