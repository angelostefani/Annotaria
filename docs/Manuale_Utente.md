# Manuale Utente Annotaria

## 1. Scopo del documento
Questo manuale guida passo passo gli utilizzatori di Annotaria nella gestione delle attivita di raccolta dati, annotazione e amministrazione del sistema. Le informazioni sono organizzate per ruolo, cosi da rendere immediato trovare le istruzioni pertinenti.

## 2. Requisiti e accesso
- **Browser supportati**: versioni recenti di Chrome, Edge o Firefox con JavaScript attivo.
- **Avvio dell applicazione**: da terminale, posizionarsi nella cartella del progetto ed eseguire `uvicorn main:app --reload` (oppure il comando di deploy indicato nel README).
- **URL predefinito**: interfaccia utente su `http://localhost:9100/ui`, documentazione REST su `http://localhost:9100/docs`.
- **Credenziali**: la registrazione via `/ui/register` crea utenti con ruolo `Esperto`. La promozione a `Amministratore` richiede la modifica del campo `role` nella tabella `users` (via SQL o interfacce di amministrazione del database).

## 3. Ruoli e permessi
| Funzione | Esperto | Amministratore |
| --- | --- | --- |
| Login, cambio password | ✓ | ✓ |
| Selezione tipologie esperto | ✓ | ✓ |
| Visualizzazione immagini assegnate | ✓ | ✓ (vedi nota) |
| Compilazione questionario e annotazioni grafiche | ✓ | ✓ |
| Caricamento, modifica o cancellazione immagini | ✗ | ✓ |
| Import massivo da directory | ✗ | ✓ |
| Gestione tipologie di immagine ed esperto | ✗ | ✓ |
| Gestione domande, opzioni, etichette | ✗ | ✓ |
| Revisione risposte e annotazioni | ✗ | ✓ |

**Nota**: gli Esperti vedono solo immagini appartenenti alle tipologie associate alle loro competenze. Gli Amministratori visualizzano sempre l intero catalogo.

## 4. Navigazione generale dell interfaccia
- **Menu principale**: presente in alto in ogni pagina. Mostra i link contestuali al ruolo (Immagini per tutti, funzionalita amministrative solo per Amministratori).
- **Indicatore utente**: pillola con il nome utente in alto a destra, accompagnata dal link per il cambio password e dal pulsante Logout.
- **Notifiche**: salvataggi di risposte e importazioni mostrano un toast verde in alto a destra; gli errori compaiono in alert rossi o gialli.

## 5. Gestione account
### 5.1 Registrazione
1. Aprire `/ui/register`.
2. Compilare username e password.
3. Confermare: l utente viene creato con ruolo `Esperto`.

### 5.2 Login e logout
1. Accedere a `/ui/login`.
2. Inserire credenziali valide; in caso di errore compare un messaggio sul form.
3. Dopo l autenticazione si viene reindirizzati alla pagina `Images`.
4. Per terminare la sessione usare il pulsante **Logout** nel menu.

### 5.3 Cambio password
1. Dal menu scegliere **Cambia password**.
2. Inserire password corrente, nuova password (minimo 8 caratteri) e conferma.
3. Un messaggio conferma l esito; la password deve essere diversa dalla precedente.

## 6. Configurazione competenze (Esperti)
1. Aprire **Le mie tipologie** (link nel menu).
2. Selezionare una o piu tipologie di immagine coerenti con le proprie competenze.
3. Salvare: da questo momento la lista immagini mostra solo file collegati alle tipologie selezionate.
4. E possibile aggiornare la selezione in qualunque momento ripetendo la procedura.

## 7. Lavorare sulle immagini
### 7.1 Elenco immagini
- Raggiungibile dal menu **Images**.
- Ogni riga mostra ID, nome file, tipologia associata e metadati EXIF principali (data, coordinate, quota, marca e modello della camera).
- Azioni disponibili:
  - **View**: apre la scheda dettagliata con annotazioni e questionario.
  - **Edit** e **Delete**: visibili ma attive solo per Amministratori; un Esperto che prova a usarle riceve un messaggio di accesso negato.

### 7.2 Scheda immagine
La pagina di dettaglio contiene:
- **Navigazione sequenziale**: pulsanti Precedente/Successiva (attivi solo se esistono immagini adiacenti). Le frecce sinistra/destra della tastiera funzionano come scorciatoia.
- **Visualizzazione**: immagine principale con canvas sovrapposto per disegnare annotazioni.
- **Badge tipologia**: in alto sotto il titolo mostra il tipo assegnato oppure segnala che manca l associazione.
- **Questionario**: se presenti domande legate alla tipologia, il modulo compare sotto l immagine.

### 7.3 Annotazioni grafiche (poligoni)
1. Cliccare sull immagine per aggiungere vertici al poligono.
2. Eseguire un doppio click per chiudere la forma:
   - Se i vertici sono meno di tre, l annotazione viene azzerata automaticamente.
   - Altrimenti compare un prompt testo che elenca tutte le etichette disponibili (id: nome).
3. Inserire l ID numerico dell etichetta corretta e confermare.
4. L annotazione viene salvata tramite l endpoint REST `/annotations/` usando il token dell utente.
5. Le annotazioni esistenti sono disegnate in rosso con testo della label vicino al primo vertice.
6. Per eliminare o modificare un annotazione e necessario contattare un Amministratore, che puo intervenire dalla sezione **Annotations**.

### 7.4 Compilazione del questionario
1. Le domande sono caricate in sequenza; il contatore indica la posizione corrente.
2. Alcune domande possono comparire solo dopo specifiche risposte (logica di follow up).
3. Selezionare un opzione per ciascuna domanda; il pulsante **Successiva** diventa verde e cambia in **Completa** sull ultima domanda attiva.
4. Il pulsante **Salva risposte** rimane disattivo finche tutte le domande visibili non sono compilate.
5. Al salvataggio viene inviato un POST per ogni domanda a `/answers/`; un toast conferma l operazione.
6. Se la logica di follow up nasconde domande gia compilate, le relative risposte vengono automaticamente scartate prima del salvataggio.

## 8. Funzioni riservate agli amministratori
### 8.1 Gestione immagini
- **Upload singolo** (`/ui/images/upload`):
  1. Selezionare il file dal disco locale (la destinazione corrisponde alla cartella `image_data` configurata).
  2. Facoltativamente scegliere la tipologia da assegnare.
  3. Confermare per salvare su disco e registrare i metadati EXIF nel database.
- **Import massivo**:
  1. Indicare la directory da importare (relativa a `image_data`).
  2. Scegliere la tipologia comune e, se necessario, includere le sotto-cartelle.
  3. Avviare l import; il resoconto riporta file creati, aggiornati, ignorati e gli eventuali errori.
- **Modifica**: dalla tabella immagini e possibile rinominare il file (solo campo database) e cambiare tipologia.
- **Eliminazione**: rimuove sia il record che il file fisico dal percorso salvato.

### 8.2 Tipologie di immagine
- Elenco disponibile in `/ui/image-types`.
- Creare nuove tipologie, modificarne il nome o cancellarle.
- Le associazioni tra tipologie di immagine e tipologie di esperto sono gestite dalla sezione seguente.

### 8.3 Tipologie di esperto
- Accesso via `/ui/expert-types`.
- Ogni tipologia comprende un nome e un insieme di tipologie di immagine.
- Gli Esperti possono dichiarare di appartenere a una o piu tipologie; tale scelta determina quali immagini possono vedere.
- Eliminando una tipologia vengono rimossi anche i collegamenti con utenti e immagini.

### 8.4 Domande e opzioni
- Interfaccia principale in `/ui/questions`.
- Per ogni domanda e possibile:
  - Impostare il testo.
  - Collegare una o piu tipologie di immagine (la domanda sara mostrata solo per immagini di quei tipi).
  - Gestire le opzioni di risposta.
- **Logica condizionale**: all interno del form di un opzione si possono selezionare altre domande da mostrare quando quella risposta e scelta. Questo meccanismo consente percorsi diversi a seconda delle risposte degli esperti.

### 8.5 Etichette per annotazioni
- Sezione `/ui/labels`.
- Creare label descrittive (es. "Anomalia", "Vegetazione", "Danno struttura").
- Facoltativamente collegare ciascuna label alle tipologie di immagine pertinenti, cosi da guidare la scelta degli esperti (al momento il prompt in pagina elenca comunque tutte le label definite).
- Modificare o cancellare label gia esistenti in caso di consolidamento del catalogo.

### 8.6 Risposte e annotazioni archiviate
- Le viste `/ui/answers` e `/ui/annotations` permettono di controllare, modificare o cancellare manualmente i dati registrati dagli utenti. Sono strumenti utili per correggere errori o per esportare dati tramite copia incolla (in attesa di funzioni di export dedicate).

### 8.7 Manutenzione utenti
- Non e presente una pagina dedicata alla gestione degli utenti: le operazioni di cambio ruolo o cancellazione vanno eseguite direttamente sul database o tramite le API REST (`/users/`).
- Per revocare l accesso a un Esperto e consigliabile impostare una password temporanea e informare l utente o rimuovere il record dalla tabella `users`.

## 9. Integrazione via API
- Tutti i servizi REST sono esposti e documentati automaticamente da FastAPI in `/docs`.
- Ogni chiamata protetta richiede il token JWT ottenibile tramite `/token` (OAuth2 password flow).
- Le stesse risorse usate dall interfaccia web (immagini, domande, annotazioni, risposte, tipologie) sono disponibili via API; consultare i file in `docs/API_REST.md` e `docs/API_Examples.md` per esempi pratici.

## 10. Risoluzione dei problemi comuni
- **Immagine non visibile nella lista**: verificare che l Esperto abbia selezionato la tipologia corretta e che l immagine possieda quella tipologia.
- **Errore durante import massivo**: controllare che il percorso indicato sia interno a `image_data` e che i file abbiano estensioni supportate (`.jpg`, `.tif`, `.png`, `.raw`, `.nef`, `.cr2`, `.arw`).
- **Prompt label vuoto**: assicurarsi che esistano etichette nel sistema (sezione Labels). In assenza di label l annotazione non puo essere completata.
- **Token scaduto per chiamate API**: i token hanno durata predefinita di 30 minuti (`ACCESS_TOKEN_EXPIRE_MINUTES`); richiedere un nuovo token tramite `/token`.

## 11. Appendici
### A. Scorciatoie da tastiera
- `Freccia sinistra`: immagine precedente (se disponibile).
- `Freccia destra`: immagine successiva (se disponibile).

### B. Struttura dati rilevante
- Database relazionale gestito tramite SQLAlchemy; vedere `docs/Database_Structure.md` per il dettaglio delle tabelle.
- File immagini archiviati nella cartella `image_data` (configurabile via variabile d ambiente `IMAGE_DIR`).
- Dati storici (risposte e annotazioni) memorizzati nelle tabelle `answers` e `annotations`, collegati a immagini, domande, opzioni e utenti.

### C. Contatti e supporto
- In caso di malfunzionamenti applicativi raccogliere il file di log (`uvicorn.log` se si usa il comando di avvio suggerito nel README) e condividerlo.
