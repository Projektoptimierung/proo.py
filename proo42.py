import sys
sys.setrecursionlimit(50000)	# funktionen darf sich 500000 mal selbst aufrufen
from sys import argv
import pylab as pl
import numpy as np
import operator
script, instanzdatei = argv	# Eingabe: Optimierung_DB.py [Instanzn.inst]
instanzen = open(instanzdatei)	# Instanzen einlesen...
rl=instanzen.readlines()

#komprate=raw_input('Wieviele Werte sollen jeweils zusammengefasst werden? ')
#lrl=int(komprate)	# Eingabe als Zahl auffassen
lrl=20
#kompschwelle=raw_input('Um wie viel soll die Schwelle erhoeht werden? (In 1/x) ')
#schwellekomp=int(kompschwelle)
schwellekomp=4

#Schneller bei mehrfachem Ausprobieren

fahrzeiten={}	# fahrzeiten dictionairy, einfacher beim Zugriff
lepr={}	# leistungsprofil dictionairy {zugnummer:array(leistungswerte)}
frab={}	# frueheste abfahrtszeit dictionary {zugnunner: frueheste abfahrt}
spab={}	# spaeteste abfahrtszeit dictionairy {zugnummer:spaeteste abfahrtszeit}
mindesthaltezeit={}	# {zugnummer: [strecke, mindesthaltezeit]}
tm=0	# temporaere valiable speichert in der folgenden Schleife die Zeile vor der aktuellen
mz=0

for l in range(len(rl)):
    ls=rl[l].strip()	# Worte nach Leerzeichen teilen
    if tm=="PLANUNGSINTERVALL":	# Zahl in Zeile nach 'Planungsintervall' wird gemerkt
        pi=int(ls)
    if tm=="ANZAHL_ZUEGE":
        az=int(ls)	# analog Anzahl Zuege
    if tm=="ZUG_NR":
        zn=int(ls)	# Zugnummer wird glich in lepr mit dem jeweiligen Leistungsprofil eingetragen
    if tm=="FRUEHESTE_ABFAHRT":
	frab.update({zn:int(ls)})
    if tm=="SPAETESTE_ABFAHRT":
        spab.update({zn:int(ls)})	# spaeteste Abfahrtszeit fuer Zug in spab eingetragen
    if tm=="FAHRZEIT":
	fz=int(ls)*600
	fahrzeiten.update({zn:int(ls)})
    if tm=="STRECKEN_NR":	# streckennummer wird als strecke zwischengespeichert
	strecke=int(ls)
    if tm=="MINDESTHALTEZEIT":	# mindesthaltezeit wird als mz zwischengespeichert
	mz=int(ls)
	mindesthaltezeit.update({zn: [strecke, mz]}) #mindesthaltezeit wird in dic eingetragen
    if tm=="LEISTUNGSPROFIL":
        templist=np.zeros(fz+1)	# erstellt einen 0-Array mit so vielen Stellen, wie die Fahrt des Zuges dauert
        for zeile in range(fz+1):
            stripped=rl[l+zeile].strip() # Leerzeichen
            angaben=stripped.split(',')	#Trennung der Zahlen nach Komma
            a=angaben[0]	#wird nicht verwendet, koennte vielleicht die Arbeit erleichtern?
            b=angaben[1]	#die Wertangabe in jeder Zeile
            templist[zeile]=float(b)	#Nullen werden im Array durch Werte ersetzt
        lepr.update({zn:np.array(templist)})	#Dictionairy wird ergaenzt mit Zugnummer und Leistungsarray
    tm=ls

def bound(zugnr):	# fasst Werte zusammen
  werte=lepr[zugnr]	# Leistungswerte des Zuges einlesen
  blist=[]
  for i,v in enumerate(werte):	#i=Index, v=Wert in der Werteliste
    nar=[]	
    if i%lrl==0 and i<fahrzeiten[zugnr]*600-lrl+1: # Indizes um komprate ueberspringen, aber Index darf nicht Dimension ueberschreiten
            nin=range(i,i+lrl)	# komprate-viele Zahlen
            nar+=[werte[nin]]	# im Wertearray
            arrlist=nar[0]	
            srl=sum(arrlist)	# summieren,
            bv=srl/lrl	# Durchschnitt der Zahlen
            blist.append(bv)	# in blist eintragen
  return blist	# und ausgeben

def wide(liste):	# zieht Leistungswerte wieder auf Originallaenge, zum Vergleich
  length=pi*600	
  widelist=[0]*length	# erstellt 0-Liste, so lang wie das Original Leistungsprofil
  for i,v in enumerate(liste):	
    for k in range(i*lrl,(i+1)*lrl):	# fuellt komprate-viele Stellen mit einem Wert aus den komprimierten Werten
      widelist[k]=v	
  return widelist
  
def widerf(zugnr):	# zieht Leistungswerte wieder auf Originallaenge, zum Vergleich
  length=maxdauer*600/lrl	
  widelist=[0]*length	# erstellt 0-Liste, so lang wie das Original Leistungsprofil
  for i,v in enumerate(erf(zugnr)):	
    for k in range(i*lrl,(i+1)*lrl):	# fuellt komprate-viele Stellen mit einem Wert aus den komprimierten Werten
      widelist[k]=v	
  return widelist
  
peaks=[]
for i in range(1,az+1):
  peaks.append(max(lepr[i]))
sw = max(peaks)/az
tal=-sw
peaks_sortiert=sorted(peaks)

def erf(zugnr):	# Liste mit 1 fuer Werte ueber Schwelle, -1 fuer Taeler, 0 sonst
  werte=bound(zugnr)
  klist=[0]*len(werte)
  for i,v in enumerate(werte):
    if v>sw:	# Werte ueber Schwelle bekommen Wert 1
      klist[i]=1
    if v<tal:	# Taeler bekommen Wert -1
      klist[i]=-1
  return klist

#print 'Werte ueber Schwelle:' # Zeitpunkt und Leistung fuer Werte ueber Schwelle ausgeben
#for i,v in enumerate(erf(1)):
# if v==1:
# print 'Zeit in Zehntel-Sekunden:', i*lrl ,bound(1)[i]
#print '\n' # Abstand
#print 'Taeler:' # Dasselbe fuer Taeler
#for i,v in enumerate(erf(1)):
# if v==-1:
# print 'Zeit in Zehntel-Sekunden:', i*lrl ,bound(1)[i]
#print '\n'


dauer = []	# Liste mit Fahrzeit + Sp. abfahrtszeit
for n in range(1, az+1):
    dauer.append(spab[n]+fahrzeiten[n])
maxdauer = max(dauer)	# Maximale dauer
      
#print maxdauer
leertray = [0]*(maxdauer*600/lrl)
#print leertray
#print len(leertray)

def fill(liste):
  for i in range(len(liste)):
      leertray[i]+=liste[i]
  return leertray

  
def check(zugnr):
  tl=bound(zugnr)
  frueheste=int(frab[zugnr])*600/lrl
  start=(int(frab[zugnr]))*600/lrl
  schwelle=sw
  return move(schwelle,start,tl,zugnr, frueheste)

def move(schwelle,start, tl, zugnr, frueheste):
    movelist=[0]*start+tl
    for i in range(len(movelist)):
      if movelist[i]+leertray[i]>schwelle:
	if start<(spab[zugnr])*600/lrl:
	  start=start+600/lrl
	  return move(schwelle,start,tl,zugnr, frueheste)
	else:
	  return move(schwelle+schwelle*1/schwellekomp, frueheste , tl, zugnr, frueheste)
    return start*lrl/600, fill(movelist), max(leertray)

  


      
length=len(lepr[1])


#for nrs in lepr:
 # print check(nrs)


"""for plots in lepr:
tempval=bound(plots)
plist=wide(tempval)
#print len(plist)
#pl.plot(range(1,length+1),lepr[1],label='original',color='b') # plottet vorgegebene Werte
pl.plot(range(1,pi*600+1),plist,label='Zugnr. %s'%plots) # plottet komprimierte Werte (auf gleiche Laenge gestreckt)
"""
#for checks in range(1,az):
# print checks, check(checks)[0]
#abf,plothelp=check(az)

#print az, abf,plothelp
  
#pl.plot(range(1,pi*600+1),wide(plothelp),label='binaer',color='k',linewidth=2)





abl=[]
for v in spab.values():
  if v not in abl:
    abl.append(v)
    

#print abl
Zeiten = {}


# sortierung: peaks: nach peaks sortiert
# abl: nach abfahrtszeit sortiert
# zum aendern peaks durch abl und max(lepr[i]) durch spab[i] ersetzen
# oder umgekehrt
for v in sorted(abl):
  for i in range(1,az+1):
    if spab[i]==v:
      zeit,bina, maxpeak=check(i)
      print 'Zug:',i,'Sp.Ab.:',v, ' Fr. Ab.:', frab[i], 'Ab.zeit:',zeit, 'MaxPeak', maxpeak#Tray:',bina
      Zeiten.update({i: zeit})
      #if zeit=='Error':
#print i


print Zeiten, maxpeak

def findepeak(twl):
  for i,v in enumerate(twl):
    if v==max(twl):
      return i	#i istIndex fuer den Peak, i*lrl ist Zeit in Zehntelsekunden
      

      
def findezuege(twl):
  pew=[]		# Peak erzeugende Werte (Zug, Wert beim Peak)
  st=findepeak(twl)
  for zug,abfahrt in Zeiten.iteritems():
      ab=abfahrt*600/lrl
      an=(abfahrt+fahrzeiten[zug])*600/lrl
      if st > ab and st < an:		# Wenn Peakstelle zwischen Abfahrt und Ankunft liegt
	pew.append((zug,lepr[zug][st-ab]))
  if pew==[]:
    return st,  pl.plot(range(1,pi*600+1),wide(twl),label='binaer',color='r',linewidth=1) 
  else:
    return pvz(pew,twl)
	








  

def schub(zug,werteliste):
  cl=[]
  vergleich=[]
  ab=Zeiten[zug]
  sa=spab[zug]
  #if sa==ab:
    #return werteliste
  for s in range(sa-ab+1):
    newbin=[]    
    for i in range(pi*600/lrl):
      vm=(ab*600/lrl*[0]+list(lepr[zug]))[i]
      vp=((ab+s)*600/lrl*[0]+list(lepr[zug]))[i]
      newbin.append(werteliste[i]-vm+vp)
    vergleich.append((newbin,s))
    cl.append((max(newbin),s))
  (gw,vz)=min(cl)
  #print gw, vz
  return vergleich[vz][0],vz
  
def pvz(pzl,twl):
  verschiebungszeiten=[]
  for (z,w) in sorted(pzl, key=operator.itemgetter(1), reverse=True):	#Liste der Peak erzeugenden Zuege, nach Leistungswerten an der Stelle absteigend sortiert \m/
      zl=max(twl)
      twl,zeve=schub(z,twl) #aktuell Werteliste, Zeitverschiebung
      print zeve
      Zeiten.update({z:Zeiten[z]+zeve})
      verschiebungszeiten.append(zeve)
      if zl<max(twl):
	print 'ALERT!',max(twl)
	break
  print verschiebungszeiten
  if max(verschiebungszeiten)==0:
	return max(twl), pl.plot(range(1,pi*600+1),wide(twl),label='binaer',color='r',linewidth=1)
  else:
        return findezuege(twl)
      



print findezuege(bina)

#print max(bina), max(schub(6,bina))
      
pl.plot(range(1,pi*600+1),wide(bina),label='binaer',color='k',linewidth=1)

pl.legend()	# Legt Legende an
pl.show()	# Zeigt Plot an

