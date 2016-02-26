# vilperg-senti
(c) Caroline Berg, Simon Will
    Februar 2016
    berg@cl.uni-heidelberg.de
    will@cl.uni-heidelberg.de

## Mitgelieferte Programme und so

## Abhängigkeiten

Für die Ausführung der Programme werden Interpreter/Compiler für die folgenden
Programmiersprachen und die aufgelisteten Pakete benötigt.

  * python3
    - urllib
    - lxml
    - Beautifulsoup (bs4)
  * Java SE7
    - Weka (3.6.1 oder neuer)
  * Perl 5
    - Set::Scalar
  * Bash
    - Den [Tree-Tagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)
    - Tagging-Scripts für den Tree-Tagger
  * AWK

Für die Kompilierung der LaTeX-Dateien werden folgende Pakete benötigt:
  * babel
  * inputenc
  * fontenc
  * lmodern
  * biblatex (und biber)

Außerdem ist eine Datei nötig, die Wortformen „Sentiment-Scores“ zuordnet.
Wir empfehlen
[SentiWS](http://asv.informatik.uni-leipzig.de/download/sentiws.html),
aber jede gleich formatierte Datei funktioniert genauso.

## Überblick

Die Programme in diesem Projekt ermöglichen, Amazon-Reviews zu bestimmten
Produktklassen herunterzuladen, sie (mit dem TreeTagger und den zugehörigen
Skripten) zu tokenisieren und mit POS-Tags zu versehen. Weiterhin können aus
den Texten mithilfe von SentiWS Features extrahiert und in Dateien geschrieben
werden, die dann ins ARFF-Format umgewandelt werden können. Die Dateien im
ARFF-Format können in WEKA verarbeitet werden. Das kann man entweder selbst
mit in der graphischen Oberfläche von WEKA oder automatisiert mit einem der
Programme tun.

## Einzelne Programme

### Amazon-Scraper

Das Programm `write_amazon_reviews.py` kann mit einer Überblicksseite über
Amazon-Produkte (z. B. `http://www.amazon.de/s/ref=sr_nr_n_14?fst=as:off&rh=n:360487031,k:enten&keywords=enten&ie=UTF8&qid=1456479070&rnid=1703609031`)
und einem Namen für ein anzulegendes Verzeichnis aufgerufen werden und lädt
dann einige Produktdaten und zugehörige Reviews herunter und speichert sie in
einer Verzeichnisstruktur unter dem angegebenen Verzeichnis.

  `write_amazon_reviews.py start_url out_dir`

### Preprocessing

Das Programm `preprocess.sh` kann aufgerufen werden mit dem Namen des
Verzeichnisses, in dem die Reviews liegen (z. B. `out_dir`, das beim
Amazon-Scraper angegeben wurde), und dem Namen der Dateien, die den
Review-Text enthalten (`content` im Normalfall).

In den Programmen `preprocess.sh` und `my_tree_tagger.sh` müssen einige
Variablen, die Pfade zu Tagger-Skripten enthalten, richtig eingestellt werden,
nämlich die folgenden:

  * In `preprocess.sh`:
    - `MY_TREE_TAGGER`
  * In `my_tree_tagger.sh`:
    - `BIN`
    - `CMD`
    - `LIB`

  `preprocess.sh out_dir content`

### Chunking

### Feature-Extraktion

Die Feature-Extraktion kann mit dem Python-Programm `write_features.py`
ausgeführt werden. Alternativ kann das Wrapper-Shell-Skript
`write_features.sh` verwendet werden. Der Aufruf für das Shell-Skript benötigt
mindestens drei Argumente:

  1. den Ausführmodus, der angibt, was mit bereits extrahierten
    Feature-Dateien geschieht
    * `append`, um an bestehende Feature-Dateien anzuhängen
    * `overwrite`, um bestehende Feature-Dateien zu überschreiben
    * `updatè`, um nur die in `write_features.sh` angegebenen Features in den
      bestehenden Feature-Dateien zu ändern.
  2. eine SentiWS-Datei
  3. das Verzeichnis, in dem die Reviews liegen.
  4. Es können noch zusätzliche Verzeichnisse angegeben werden.

  `write_features.sh overwrite /path/to/sentiws out_dir additional_out_dir`

Mit dem Skript `stars_to_features.sh` müssen nun die Sterne aus der
`info`-Datei in die Feature-Datei geschrieben werden. Das Skript
`normalize_features.sh` wird verwendet, um die Sentiment-Features zu
normalisieren und das Skript `add_binary_judgement.sh` fügt das Feature
`binary_judgement` ein. All diese Skripte müssen für jedes Review einzeln
angewandt werden, wozu sich der UNIX-Befehl `find` anbietet.
Eine automatisierte Anwendung dieser drei Skripte bietet das Skript
`add_additional_features.sh` an.

TODO: `add_additional_features` schreiben und beschreiben!

Um die Feature-Dateien in ARFF-Format umzuwandeln, wird das Programm
`arff_data.py` aufgerufen. Es werden folgende Argumente übergeben:
  
  1. das Verzeichnis, in dem die Feature-Dateien liegen
  2. den Namen der ARFF-Datei, die erstellt werden soll
  3. die Namen der Features, die in die ARFF-Datei übernommen werden sollen.
    Es ist zu empfehlen, als letztes Argument das Klassen-Feature anzugeben.

  `arff_data.py out_dir outfile.arff overall_sentiment token_number stars`

### Experimente


