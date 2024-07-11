Webová stránka pro filmový festival na GEKOMu pro rok 2024 (festival se koná v prosinci, stránka neni ani trochu hotová)

# Poznámky
- server ukládá do variable app.room všechny místnosti, ve kterých se něco děje (podle jednotlivých dní). to je důležitý pro zobrazování programu. tahle variable se ale musí updatovat před každým requestem, protože když běží wsgi na víc workerech tak ta promenna se nesyncuje a tim padem když se něco updatne v programu tak je to potom out of sync
- muj program se interne jmenuje "favorite", protoze jsem debil a ted se mi to uz nechce predelavat. mozna se i nekde na strance jmenuje "oblibene", ale je to proste muj program
- kvuli browser cache se css a js soubory versionujou. kdyz chci neco zmenit v css nebo js souboru tak to zmenim napr. v main.css, pak udelam kopii main.css s version cislem (napr. main-007.css) a zmenim vsechny odkazy na ten soubor
### WIP mod
Work in progress mode - kdyz je zapnuty, tak se requesty na program, workshopy a hosty presmeruji na /wip (pokud neni user prihlaseny).
Nastavuje se v `__init__.py`. V `decorators.py` je definovany dekorator wip_disabled. Ten je u vsech fci v routs.py, ktery maji byt zakazany v wip modu.    