Webová stránka pro filmový festival na GEKOMu pro rok 2024 (festival se koná v prosinci, stránka neni ani trochu hotová)

# Poznámky
- server ukládá do variable app.room všechny místnosti, ve kterých se něco děje (podle jednotlivých dní). to je důležitý pro zobrazování programu. tahle variable se ale musí updatovat před každým requestem, protože když běží wsgi na víc workerech tak ta promenna se nesyncuje a tim padem když se něco updatne v programu tak je to potom out of sync