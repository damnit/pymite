# Brainstorm

Darstellung Zeiteintrag Pattern:
    *   [3:00|3:55] <Projekt> <Leistung> <Kommentar>
    optional + Summe aller Zeiten


## Was braucht ein Commandline Tool für pymite?

- Alias für Projekte/Leitung zur schnelleren Eingabe
- Option (--raw <tsv, csv, json>) für alle Befehle
- Tracker


### Auflistung aller Projekte
> pymite projects [OPTIONS] <name> default: all active projects
Options:
  -a, --archived
  -i --id
  -s --sortby <project, id, customer>

Arguments:
    filter by name (case sensisitve)

    A = archiviert
    Ausgabe:
        A   [id] <Project> <customer_name>
        A   [id] <Project>
        A   [id] <Project>
        A   [id] <Project>
        A   [id] <Project>


### Auflistung aller Customer
> pymite customers [OPTIONS] <name> default: all active customer
Options:
  -a, --archived
  -i --id
  -s --sortby <id, customer>

Arguments:
    filter by name (case sensisitve)

    A = archiviert
    Ausgabe:
        A   [id] <customer_name> <note>
        A   [id] <customer_name> <note>
        A   [id] <customer_name> <note>
        A   [id] <customer_name> <note>
        A   [id] <customer_name> <note>


### Auflistung aller Services
> pymite services [OPTIONS] <name> default: all active services
Options:
  -a, --archived
  -i --id
  -s --sortby <id, customer>

Arguments:
    filter by name (case sensisitve)

    A = archiviert
    Ausgabe:
        A   [id] <name> <note>
        A   [id] <name> <note>
        A   [id] <name> <note>
        A   [id] <name> <note>
        A   [id] <name> <note>


### Zeiteinträge
* Rücksprache !!!!

> pymite time_entries [OPTIONS] <name> default: all time entries
Options:
  -c, --customer_id
  -p, --project_id
  -s, --service_id
  -u, --user_id

    From - To filter YYYY-MM-DD

    Ausgabe:
        nach UnitTest
        A   [id] <minutes ><date-at> <user_name> <custer_name> <project_name> <service_name>

> pymite add (time_entry) [OPTION] <note>
Options:
    -p, --project_id
    -s, --service_id
    -u, --user_id
    -d, --date_at
    -m, --minutes



### Wer bin ich
> pymite myself
    Ausgabe:
       <id type="integer">1</id>
       <name>Sebastian Munz</name>
       <email>sebastian@email.com</email>
       <note></note>
       <archived type="boolean">false</archived>
       <role>coworker</role>
       <language>de</language>
       <created-at type="datetime">2007-06-23T23:00:58+02:00</created-at>
       <updated-at type="datetime">2009-02-14T00:33:26+01:00</updated-at>

### Für wen arbeite ich
> pymite account
    Ausgabe:
       <id type="integer">123</id>
       <name>demo</name>
       <title>Demo GmbH</title>
       <currency>EUR</currency>
       <created-at type="datetime">2009-10-12T00:00:00+01:00</created-at>
       <updated-at type="datetime">2009-11-02T13:21:09+01:00</updated-at>

### Tracker
Start = grün
Stop = rot

> pymite tracker
    Ausgabe: 
        *   [3:00|3:55] <Projekt> <Leistung> <Kommentar>
        || no timer running!!

> pymite tracker <stop>
    Argument:
        stopping tracker | no tracker to stop
    Ausgabe:
        rot eingefärbt => stopped [3:00|3:55] <Projekt> <Leistung> <Kommentar>


> pymite tracker [id] <start|stop>
    Ausgabe: 
        *   [3:00|3:55] <Projekt> <Leistung> <Kommentar>
        || no timer running!!




## Welche Funktionen deckt pymite.cmd ab?

### config pymite realm speichern
> pymite configure [OPTIONS]
Options:
  -a, --apikey TEXT  Login to http://mite.yo.lk/api/index.htmland create your
                     API Key  [required]
  -r, --realm TEXT   realm is the part in the URL: https://<realm>.mite.yo.lk
                     [required]
  --help             Show this message and exit.


> $pymite daily [today|yesterday|Y-m-d] default: today
    * = laufender Task
    Ausgabe:
        *   [3:00|3:55] <Projekt> <Leistung> <Kommentar>
            [3:00|3:55] <Projekt> <Leistung>
            [3:00|3:55] <Projekt> <Leistung>
            [3:00|3:55] <Projekt> <Leistung>
            -----------------------------------------------
            Gesamt: Zeit
