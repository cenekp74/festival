Webová stránka pro filmový festival na GEKOMu pro rok 2024 (festival se koná v prosinci, stránka neni ani trochu hotová)

# Poznámky
- server ukládá do variable app.room všechny místnosti, ve kterých se něco děje (podle jednotlivých dní). to je důležitý pro zobrazování programu. tahle variable se ale musí updatovat před každým requestem, protože když běží wsgi na víc workerech tak ta promenna se nesyncuje a tim padem když se něco updatne v programu tak je to potom out of sync. podobnej problem je u fotogalerie (variable app.albums_dict)
- muj program se interne jmenuje "favorite", protoze jsem debil a ted se mi to uz nechce predelavat. mozna se i nekde na strance jmenuje "oblibene", ale je to proste muj program
- system meho programu je udelany pres cookies. client posle request na server, server posle zpatky updatovanou cookie. slo by to udelat i tak, ze by se cookie menila rovnou u clienta javascriptem. takhle se mi to zda hezci, jednodussi a taky to usnadnuje implementaci pripadnyho verejnyho login systemu (jakoze by se lidi prihlasovali a jejich progam by se neukladal jenom do cookiesky, ale i nekam do databaze)
- kvuli browser cache se css a js soubory versionujou. kdyz chci neco zmenit v css nebo js souboru tak to zmenim napr. v main.css, pak udelam kopii main.css s version cislem (napr. main-007.css) a zmenim vsechny odkazy na ten soubor (pokud je to jenom mala zmena ktera nemusi platit hned, upravim jenom main.css a pak to zkopiruju do posledni verze)
- vsechny routs v api.py maji dany url prefix /api (definovane v `__init__.py`)
- komentare a nazvy veci jsou tak napul cesky a napul anglicky, nektery veci se proste lip pisou v anglictine nez to krkolome prekladat
- kdyz naclonuju repo z githubu a chci to spustit, musim nejdriv spustit create_db.py a vytvorit dir static/upload, static/fotogalerie a soubor static/fotogalerie/albums.json (do nej staci dat prazdny dict {})
- obrazky k hostum a workshopum se ukladaji do stejny slozky jako soubory z upload
- v lokalnich funkcich se casto pouziva variable name id - vim, ze je to spatne podle PEP protoze existuje builtin fce id, ale jsem linej to vsude menit a mam pocit ze v local scopu to moc neva
- context-menu (cm) = item-details, omylem jsem to nekde nazval jinak a nechce se mi to menit
- program_day a favorite_day jsou hodne podobny. cast s vytvarenim context menu je uplne stejna. program se lisi v malych detailech
### WIP mod
Work in progress mode - kdyz je zapnuty, tak se requesty na program, workshopy a hosty presmeruji na /wip (pokud neni user prihlaseny).
Lze obejit tim, ze do url pridam ?force-display (kvuli testovani s ostatnima abych nemusel delat loginy)
Nastavuje se v `__init__.py`. V `decorators.py` je definovany dekorator wip_disabled. Ten je u vsech fci v routs.py, ktery maji byt zakazany v wip modu.
### Kavarna a cajovna (shop)
Blueprint shop (`shop.py`) obsahuje fce k systemu kavarny a cajovny. Vsechno se uklada do stejny db jako program atd. V budoucnu by se sem mohl pridat i merch nebo jiny veci na prodej. 