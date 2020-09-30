
# PyGeneses

[![GitHub](https://img.shields.io/github/license/Project-DC/pygeneses)](https://github.com/Project-DC/pygeneses/blob/master/LICENSE)  ![GitHub stars](https://img.shields.io/github/stars/Project-DC/pygeneses?style=plastic)  ![GitHub contributors](https://img.shields.io/github/contributors/Project-DC/pygeneses)  ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)  ![GitHub last commit](https://img.shields.io/github/last-commit/Project-DC/pygeneses)

<p align="justify">PyGeneseses è un framework di Deep Reinforcement Learning basato su PyTorch che aiuta gli utenti a simulare agenti artificiali in ambienti bio-ispirati. Il framework fornisce algoritmi di Deep RL integrati e la visualizzazione dei risultati dell'addestramento in una dashboard interattiva. Gli ambienti sono un'astrazione semplificata del nostro mondo reale, gli agenti sono inseriti in questo mondo e possono interagire tra loro e con l'ambiente.</p>

La potenza di PyGeneseses è la sua API pulita e semplice che:
- Permette all'utente di eseguire la propria simulazione anche se non ha alcuna conoscenza di RL o DL.
- Permette ad un utente con esperienza in Deep RL di modificare il modello ed i parametri in modo estensivo.
<p align="justify">Cosa c'è di eccitante in PyGeneseses che chiedete, beh, PyGeneseses vi permette di creare una simulazione di lavoro scrivendo solo 2 righe senza alcuna conoscenza preliminare! PyGeneseses fornisce anche strumenti che vi aiuteranno a visualizzare i risultati con il minimo sforzo. Quindi cosa aspettate, installate PyGeneseses oggi stesso e diventate il dio della vostra creazione</p>

# Hacktoberfest 2020

L'Hacktoberfest 2020 è arrivato. I contributi sono ora benvenuti. Si prega di passare attraverso [CONTRIBUTING.md](../CONTRIBUTING.md) e le istruzioni in readme [Contribuisci](#contribute). Attendiamo con ansia i vostri contributi.

## Prima vita

<p align="justify">Prima vita è una specie di esseri simulati artificialmente creati come parte del Progetto DC. Questo repository contiene un ambiente di simulazione creato in pygame che deve essere utilizzato con algoritmi di Deep Reinforcement Learning per scoprire l'evoluzione di Prima Vita.</p>

## Installazione

PyGeneseses può essere installato utilizzando pip nel vostro sistema locale o in una piattaforma basata su cloud. I passi per l'installazione saranno gli stessi sia per il cloud che per l'installazione locale.

```bash
user@programmer~:$ pip install git+https://github.com/Project-DC/pygeneses
```

Poiché PyGeneseses non è ancora disponibile in pypi, per ora dovrete usare il link github repo link con pip per installarlo.

## Informazioni sui pacchetti   
<p align="justify">A partire dalla versione 0.1-beta, l'architettura di PyGeneseses è costruita intorno a 4 moduli principali. Ognuno di questi moduli fornisce una caratteristica o funzionalità unica al framework. Quindi, iniziamo con una breve introduzione a ciascuno di essi.</p>      

1. **pygeneses.envs**    
<p align="justify">Questo modulo permette di creare, configurare e modificare gli ambienti bio-ispirati all'interno. Per ora, questo fornisce solo un unico ambiente chiamato Prima Vita (First Life), ma presto ne arriveranno altri! Questo permette di impostare l'intero ambiente e la specie in poche righe di codice e fornisce sia API di alto livello che controllo di basso livello sull'ambiente. L'addestramento usando l'API include la registrazione di ogni azione di un agente in modo che possa essere studiata usando VitaBoard.</p>   

2. **pygeneses.models** 
<p align="justify">Il modulo "modelli" è ciò che ci permette di importare le reti neurali che la specie utilizza per imparare cosa fare. Per ora viene fornita solo l'implementazione del modello di default (REINFORCE), ma aggiungeremo il supporto per le reti innestabili personalizzate a partire dalla v0.2.</p>

3. **pygeneses.hypertune**    
<p align="justify">Il pacchetto 'HyperTune' ci permette di configurare e testare vari iperparametri che possiamo fornire per un ambiente e una specie (un elenco di iperparametri è fornito nella sezione Classi di questa documentazione). Questo contiene il test di un singolo iperparametro, la ricerca a griglia e la ricerca randomizzata. Questo ci permette di trovare il miglior set di iperparametri per visualizzare un tipo di comportamento. In questo modo si ottengono anche i log che possiamo studiare utilizzando Vitaboard.</p>

4. **pygeneses.vitaboard**   
<p align="justify">Vitaboard fornisce un cruscotto avanzato e interattivo per studiare gli agenti dopo la fase di formazione. Dopo la morte di ogni agente, le sue azioni vengono scritte in un file di registro. E vitaboard ci permette di visualizzare la vita dell'agente. Ci fornisce un visualizzatore di vita, statistiche di gruppo e un visualizzatore di storia genetica. Ci permette di identificare e comprendere i comportamenti mostrati da un agente mentre interagisce con l'ambiente o con altri agenti nell'ambiente.</p>

## Contribuire

Le seguenti risorse sono un buon posto per conoscere meglio PyGeneseses:-

1.  Introduzione a PyGeneseses  [Dev.to](https://dev.to/projectdc/introduction-to-pygeneses-26oc),  [Medium](https://medium.com/oss-build/introduction-to-pygeneses-1ed08a1a076c).
2.  Iniziare con PyGeneseses [Dev.to](https://dev.to/projectdc/getting-started-with-pygeneses-1co2),  [Medium](https://medium.com/oss-build/getting-started-with-pygeneses-839ff6b3023f).
3. Studiare i registri utilizzando VitaBoard [Dev.to](https://dev.to/projectdc/guidelines-about-vitaboard-2m36), [Medium](https://medium.com/oss-build/studying-logs-using-vitaboard-41e13e3197d7)

Oltre a questi post del blog, è anche possibile controllare il  [documenti ufficiali](https://project-dc.github.io/docs).

### Istruzioni per i contributori per la prima volta/contribuenti di primo livello per questioni relative alle domande durante l'HACKTOBERFEST

- Iniziate a lavorare sui problemi una volta che vi sono stati assegnati. Andate al problema e commentate che volete che vi venga assegnato. Una volta che il manutentore vi assegna il problema, iniziate a lavorarci. I problemi saranno assegnati in base al principio "primo arrivato, primo servito" (First Come First Serve (FCFS).
- Una volta assegnato il numero, avete una settimana (7 giorni) per presentare il PR. In caso contrario, il problema verrà riassegnato a qualcun altro. Poiché ogni numero relativo alle domande viene assegnato a un singolo collaboratore alla volta, speriamo sinceramente che collaboriate con noi.
- Se create una PR senza che il problema vi venga assegnato, la PR sarà contrassegnata come spam, poiché non state rispettando le regole.   
- Il link di google drive ai log da voi generati deve essere inserito nella directory dei log di localizzazione. Se non viene trovato nel posto giusto, i nostri manutentori scriveranno un commento alla PR come avvertimento e se la posizione corretta non viene ancora fornita al momento della ripresentazione, la PR sarà contrassegnata come spam per non aver aderito alle regole.

### Come lavorare sui problemi di generazione dei log?

1) Controllare quale iperparametro si deve sintonizzare, i valori per i quali si deve sintonizzare e il numero di stop_at nell'emissione.

2) Scrivete il codice in pygeneseses per questo (codice a 3 righe). Prendiamo un esempio in cui l'iperparametro da sintonizzare è **initial_population**, i valori per quello sono **[10, 20, 50, 90, 100]**, e il numero stop_at è **2000**, allora il codice avrà un aspetto simile a questo:-

```python
from pygeneses.hypertune import HyperTune

tuner = HyperTune(model_class='PrimaVita',
                  hyperparameters=['initial_population'],
                  values=[[10, 20, 50, 90, 100]],
                  stop_at=2000)

tuner.hypertuner()
```

3) Dopo l'addestramento ci sarà una cartella generata nella stessa posizione in cui avete addestrato gli agenti di Prima vita, il nome di questa cartella inizierà con Players_Data, questo è il registro di cui abbiamo bisogno. Potete zippare questo o caricare direttamente l'intera cartella su google drive.

4) Una volta che hai caricato i log in google drive condividi il link di quella cartella (o file zip) contenente i log in un file con il numero di emissione in formato txt (ad esempio, se stai facendo l'emissione 11 allora il nome del file dovrebbe essere 11.txt). Questo file deve essere messo nella directory dei log prima di creare la Pull Request. Una volta creata la PR attendere che un manutentore la unisca o chieda alcune modifiche.

Prima di proseguire si prega di consultare le regole in [CONTRIBUTING.md](../CONTRIBUTING.md).

## License

PyGeneses è rilasciato sotto licenza GNU GPL v3 [LICENZA](../LICENSE).

## La squadra

- [Siddhartha Dhar Choudhury](https://github.com/frankhart2018)
- [Pranshul Dobriyal](https://github.com/PranshulDobriyal)
- [Dhairya Jain](https://github.com/dhairyaj)
- [Farhad Bharucha](https://github.com/Farhad1234)
- [Aayush Agarwal](https://github.com/Aayush-99)
