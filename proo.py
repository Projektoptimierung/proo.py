from sys import argv
import pylab as pl
import numpy as np
script, instanzdatei = argv		# Eingabe: Optimierung_DB.py [Instanzn.inst]
instanzen = open(instanzdatei)		# Instanzen einlesen...
rl=instanzen.readlines()

komprate=raw_input('Wieviele Werte sollen jeweils zusammengefasst werden? ')
lrl=int(komprate)	# Eingabe als Zahl auffassen

lepr={}		# leistungsprofil dictionairy {zugnummer:array(leistungswerte)}
spab={}		# spaeteste abfahrtszeit dictionairy {zugnummer:spaeteste abfahrtszeit}
mindesthaltezeit={}	# {zugnummer: [strecke, mindesthaltezeit]}
tm=0		# temporaere valiable speichert in der folgenden Schleife die Zeile vor der aktuellen
mz=0

for l in range(len(rl)):
    ls=rl[l].strip()	# Worte nach Leerzeichen teilen
    if tm=="PLANUNGSINTERVALL":	# Zahl in Zeile nach 'Planungsintervall' wird gemerkt
        pi=int(ls)
    if tm=="ANZAHL_ZUEGE":
        az=int(ls)	# analog Anzahl Zuege
    if tm=="ZUG_NR":
        zn=int(ls)	# Zugnummer wird glich in lepr mit dem jeweiligen Leistungsprofil eingetragen
    if tm=="SPAETESTE_ABFAHRT":
        spab.update({zn:int(ls)})	# spaeteste Abfahrtszeit fuer Zug in spab eingetragen
    if tm=="FAHRZEIT":
	fz=int(ls)*600
	fahrzeiten.update({zn:int(ls)})
    if tm=="STRECKEN_NR":		# streckennummer wird als strecke zwischengespeichert
	strecke=int(ls)
    if tm=="MINDESTHALTEZEIT":		# mindesthaltezeit wird als mz zwischengespeichert
	mz=int(ls)
	mindesthaltezeit.update({zn: [strecke, mz]}) 	#mindesthaltezeit wird in dic eingetragen
    if tm=="LEISTUNGSPROFIL":
        templist=np.zeros(fz+1)		# erstellt einen 0-Array mit so vielen Stellen, wie die Fahrt des Zuges dauert
        for zeile in range(fz+1):
            stripped=rl[l+zeile].strip()         # Leerzeichen
            angaben=stripped.split(',')		#Trennung der Zahlen nach Komma
            a=angaben[0]			#wird nicht verwendet, koennte vielleicht die Arbeit erleichtern?
            b=angaben[1]			#die Wertangabe in jeder Zeile
            templist[zeile]=float(b)		#Nullen werden im Array durch Werte ersetzt
        lepr.update({zn:np.array(templist)})	#Dictionairy wird ergaenzt mit Zugnummer und Leistungsarray
    tm=ls

def bound(zugnr):	# fasst Werte zusammen
  werte=lepr[zugnr]	# Leistungswerte des Zuges einlesen
  blist=[]
  for i,v in enumerate(werte):	#i=Index, v=Wert in der Werteliste
    nar=[]				
    if i%lrl==0 and i<fahrzeiten[zugnr]*600-lrl+1: 		# Indizes um komprate ueberspringen, aber Index darf nicht Dimension ueberschreiten
            nin=range(i,i+lrl)	# komprate-viele Zahlen
            nar+=[werte[nin]]	# im Wertearray
            arrlist=nar[0]	
            srl=sum(arrlist)	# summieren,
            bv=srl/lrl		# Durchschnitt der Zahlen
            blist.append(bv)	# in blist eintragen
  return blist			# und ausgeben

def wide(liste):		# zieht Leistungswerte wieder auf Originallaenge, zum Vergleich
  length=pi*600	
  widelist=[0]*length		# erstellt 0-Liste, so lang wie das Original Leistungsprofil
  for i,v in enumerate(liste):	
    for k in range(i*lrl,(i+1)*lrl):	# fuellt komprate-viele Stellen mit einem Wert aus den komprimierten Werten
      widelist[k]=v	
  return widelist
  
def widerf(zugnr):		# zieht Leistungswerte wieder auf Originallaenge, zum Vergleich
  length=maxdauer*600/lrl	
  widelist=[0]*length		# erstellt 0-Liste, so lang wie das Original Leistungsprofil
  for i,v in enumerate(erf(zugnr)):	
    for k in range(i*lrl,(i+1)*lrl):	# fuellt komprate-viele Stellen mit einem Wert aus den komprimierten Werten
      widelist[k]=v	
  return widelist
  
peaks=[]
for i in range(1,az+1):
  peaks.append(max(lepr[i]))
sw=max(peaks)/2
tal=-sw
print max(peaks)  

def erf(zugnr):		# Liste mit 1 fuer Werte ueber Schwelle, -1 fuer Taeler, 0 sonst
  werte=bound(zugnr)
  klist=[0]*len(werte)
  for i,v in enumerate(werte):
    if v>sw:		# Werte ueber Schwelle bekommen Wert 1
      klist[i]=1
    if v<tal:		# Taeler bekommen Wert -1
      klist[i]=-1
  return klist    

#print 'Werte ueber Schwelle:'	# Zeitpunkt und Leistung fuer Werte ueber Schwelle ausgeben
#for i,v in enumerate(erf(1)):
#  if v==1:
#    print 'Zeit in Zehntel-Sekunden:', i*lrl ,bound(1)[i]
#print '\n'	# Abstand
#print 'Taeler:'		# Dasselbe fuer Taeler
#for i,v in enumerate(erf(1)):
#  if v==-1:
#    print 'Zeit in Zehntel-Sekunden:', i*lrl ,bound(1)[i]
#print '\n'


dauer = []					# Liste mit Fahrzeit + Sp. abfahrtszeit
for n in range(1, az+1):
    dauer.append(spab[n]+fahrzeiten[n])
maxdauer =  max(dauer)				# Maximale dauer
      
print maxdauer
leertray = [0]*(maxdauer*600/lrl)
#print leertray
#print len(leertray)

def fill(liste):
  for i in range(len(liste)):
      leertray[i]+=liste[i]
  return leertray

def check(zugnr):
  tl=bound(zugnr)
  start=0
  sh=sw
  return move(sh,start,tl,zugnr)
	 
def move(schwelle,start, tl, zugnr):
    movelist=[0]*start+tl
    for i in range(len(movelist)):
      if movelist[i]+leertray[i]>schwelle*2:
	  if start<(spab[zugnr])*600/lrl:
	    start=start+600/lrl
	    return move(schwelle,start,tl,zugnr)
	  else:
	    sh1=schwelle+3000000
	    print 'error'
	    i= 0
    return start*lrl/600, fill(movelist), max(movelist)
	
  
	  
	
      
length=len(lepr[1])


#for nrs in lepr:
 # print check(nrs)


"""for plots in lepr:
  tempval=bound(plots)
  plist=wide(tempval)
  #print len(plist)
  #pl.plot(range(1,length+1),lepr[1],label='original',color='b')			# plottet vorgegebene Werte
  pl.plot(range(1,pi*600+1),plist,label='Zugnr. %s'%plots)	# plottet komprimierte Werte (auf gleiche Laenge gestreckt) 
"""
#for checks in range(1,az):
#  print checks, check(checks)[0]
#abf,plothelp=check(az)

#print az, abf,plothelp
  
#pl.plot(range(1,pi*600+1),wide(plothelp),label='binaer',color='k',linewidth=2)





abl=[]
for v in spab.values():
  if v not in abl:
    abl.append(v)

print abl
Zeiten = []

for v in sorted(abl):
  for i in range(1,az+1):
    if spab[i]==v:
      zeit,bina, maxpeak=check(i)
      print 'Zug:',i,'Sp.Ab.:',v,'Ab.zeit:',zeit, 'MaxPeak', maxpeak#Tray:',bina 
      Zeiten.append({i: zeit})
      #if zeit=='Error':
	#print i
	
	
print Zeiten

pl.plot(range(1,pi*600+1),wide(bina),label='binaer',color='k',linewidth=2)

pl.legend()	# Legt Legende an
pl.show()	# Zeigt Plot an
  
