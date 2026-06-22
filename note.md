# Memoria

## Organizzazione

- Un gruppo di celle è una row (si legge tutta insieme)
- Un gruppo di row è una bank, ognuna ha il suo row buffer
- Un gruppo di bank è un rank
- Il memory controller si interfaccia con più rank


## Comandi
Una bank riceve comandi: 
- ACTIVATE (bank, row) che apre la row e la mette nel row buffer (equivalente
  a un refresh)
- READ/WRITE (bank) legge/scrive dal row buffer
- PRECHARGE (bank) azzera il row buffer, chiudendo la word line

Un refresh è effettuato con un ACTIVATE(bank, row) e poi un PRECHARGE(bank)
(apri e chiudi la row)

In DDR3, un refresh si effettua ogni 64ms.
Se abbiamo una bank da 8192 row (normale DDR3), il memory controller effettua
un refresh ogni 64ms/8192 = 7.8us


## Errori di Disturbo

Quando una row viene chiusa e aperta ripetutamente, alcune celle in row adiacenti perdono carica a una velocità maggiore del normale. Se non riescono a tenerla per 64ms, si effettua un errore di disturbo.

Le celle si dividono in 
- Celle rappresentano 0 con 0 e 1 con 1, un errore di disturbanza è 1 -> 0
- Anticelle rappresentano 0 con 1 e 1 con 0, un errore di disturbanza è 0 -> 1
A seconda del produttore, ram possono contenere principalmente celle,
anticelle, o un misto.


# Progetto
## Scaling down
Abbiamo effettuato uno scaling del refresh cycle, e del treshold per
gli errori di disturbo, di un fattore 200 rispetto a valori reali.
Questo ci serve per rendere il problema trattabile velocemente e fare una
dimostrazione visiva, e non dovrebbe in generale modificare la frequenza di
flip per refresh cycle. 

### Effetti su PARA
Questo scaling però urta PARA, la cui probabilità di flip va settata in
funzione solo del treshold per gli errori di disturbo. Visto che questo è 200
volte più piccolo, la probabilità dovrà essere notevolmente superiore, e
l'efficenza peggiore. Nella paper propongono un p = 0.001 che sembra essere
abbondantemente sicuro, per noi una p = 0.04 è il minimo per la sicurezza.
