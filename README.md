vilperg-senti
=============
© Caroline Berg, Simon Will;
  Februar 2016;
  berg@cl.uni-heidelberg.de, will@cl.uni-heidelberg.de

Mitgelieferte Programme und so
------------------------------

Folgende Programme und Dokumente sind relevant:

    vilperg-senti/
    ├── abschlussbericht
    │   ├── abschlussbericht.pdf
    │   └── abschlussbericht.tex
    ├── experimenting
    │   └── MyClassifier
    │       ├── AttributeSelectionClassify.class
    │       ├── AttributeSelectionClassify.java
    │       ├── ClassifierType.class
    │       └── ClassifierType.java
    ├── feature_extraction
    │   ├── add_additional_features.pl
    │   ├── add_binary_judgement.sh
    │   ├── arff_data.py
    │   ├── feature_getter.py
    │   ├── normalize_features.sh
    │   ├── SentiWS_handler.py
    │   ├── stars_to_features.sh
    │   ├── write_features.py
    │   └── write_features.sh
    ├── get_amazon_reviews
    │   ├── vilperg_amazonreview.py
    │   └── write_amazon_reviews.py
    ├── preprocess_extractfeatures_makearff.pl
    ├── preprocessing
    │   ├── my_tree_tagger.sh
    │   └── preprocess.sh
    ├── presentation
    │   ├── beamerthemeheidelberg.sty
    │   ├── presentation.pdf
    │   └── presentation.tex
    ├── README.md
    ├── review_chunking
    │   ├── make_chunks.pl
    │   └── make_chunks.sh
    └── statusbericht
        ├── statusbericht.pdf
        └── statusbericht.tex

Abhängigkeiten
--------------

Für die Ausführung der Programme werden Interpreter/Compiler für die
folgenden Programmiersprachen und die aufgelisteten Pakete benötigt.

  * Python 3
    - `urllib`
    - `enum`
    - `lxml`
    - `Beautifulsoup` (`bs4`)
  * Java (getestet mit SE 7)
    - Weka (getestet mit 3.6.1)
  * Perl 5
    - `Set::Scalar`
  * Bash
    - Den [Tree-Tagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)
    - Tagging-Scripts für den Tree-Tagger
  * AWK

Für die Kompilierung der LaTeX-Dateien werden das Programm `biber` sowie
folgende Pakete benötigt:

  * `adjustbox`
  * `babel`
  * `beamer`
  * `biblatex`
  * `booktabs`
  * `color`
  * `floatflt`
  * `fontenc`
  * `graphicx`
  * `hyperref`
  * `inputenc`
  * `listings`
  * `lmodern`
  * `siunitx`

Außerdem ist eine Datei nötig, die Wortformen „Sentiment-Scores“ zuordnet.
Wir empfehlen
[SentiWS](http://asv.informatik.uni-leipzig.de/download/sentiws.html),
aber jede gleich formatierte Datei funktioniert genauso.

Überblick
---------

Die Programme in diesem Projekt ermöglichen, Amazon-Reviews zu bestimmten
Produktklassen herunterzuladen, sie (mit dem TreeTagger und den zugehörigen
Skripten) zu tokenisieren und mit POS-Tags zu versehen. Weiterhin können aus
den Texten mithilfe von SentiWS Features extrahiert und in Dateien geschrieben
werden, die dann ins ARFF-Format umgewandelt werden können. Die Dateien im
ARFF-Format können in WEKA verarbeitet werden. Das kann man entweder selbst
mit in der graphischen Oberfläche von WEKA oder automatisiert mit einem der
Programme tun.

Einzelne Programme
------------------

### Amazon-Scraper

Das Programm `write_amazon_reviews.py` kann mit einer Überblicksseite über
Amazon-Produkte (z. B. `http://www.amazon.de/s/ref=sr_nr_n_14?fst=as:off&rh=n:360487031,k:enten&keywords=enten&ie=UTF8&qid=1456479070&rnid=1703609031`)
und einem Namen für ein anzulegendes Verzeichnis aufgerufen werden und lädt
dann einige Produktdaten und zugehörige Reviews herunter und speichert sie in
einer Verzeichnisstruktur unter dem angegebenen Verzeichnis.

Beispielaufruf:

    python3 write_amazon_reviews.py start_url reviews_top_dir/

### Preprocessing

Das Programm `preprocess.sh` kann aufgerufen werden mit dem Namen des
Verzeichnisses, in dem die Reviews liegen (z. B. `out_dir`, das beim
Amazon-Scraper angegeben wurde), und dem Namen der Dateien, die den
Review-Text enthalten (im Normalfall `'content'`).

In den Programmen `preprocess.sh` und `my_tree_tagger.sh` müssen einige
Variablen, die Pfade zu Tagger-Skripten enthalten, richtig eingestellt werden,
nämlich die folgenden:

  * In `preprocess.sh`:
    - `MY_TREE_TAGGER`
  * In `my_tree_tagger.sh`:
    - `BIN`
    - `CMD`
    - `LIB`

Beispielaufruf:

    > bash preprocess.sh reviews_top_dir/ content

### Chunking

Das Perl-Skript `make_chunks.pl` kann dazu benutzt werden, eine Struktur aus
symbolischen Links zu schaffen, wobei die Links auf bereits vorhandene
Review-Verzeichnisse verweisen. Die Links werden so in Unterverzeichnissen
(„Chunks“) angeordnet, dass sich in jedem Chunk von jeder Sternzahl gleich
viele Reviews befinden. Außerdem werden die Links zufällig auf die Chunks
verteilt.

Für eine detaillierte Auflistung der Optionen des Skripts, kann der folgende
Befehl ausgeführt werden:

    perl make_chunks.pl --help

Das Skript verlangt mindestens zwei Argumente:

  1. das Verzeichnis, in dem die Reviews leben.
  2. den Namen des Verzeichnisses, unter dem die Symlink-Struktur entstehen
    soll.

Ein typischer Aufruf sollte allerdings auch durch `--housing-dir reviews` den
Namen der Review-Verzeichnisse spezifizieren, mit dem Schalter `--balance` die
Balancierung aktivieren und mit `--chunk-size N` die Anzahl der Dateien pro
Chunk angeben. (`N` sollte dabei am besten durch 5 teilbar sein.)

Beispielaufruf:

    perl make_chunks.pl --housing-dir reviews/\
    --chunk-size 50\
    --balance\
    reviews_top_dir/ reviews_chunks/

### Feature-Extraktion

Die Feature-Extraktion kann mit dem Python-Programm `write_features.py`
ausgeführt werden. Für eine detaillierte Auflistung der Optionen dieses
Programms, kann folgender Befehl ausgeführt werden:

    > python3 write_features.py --help

Alternativ zum Python-Programm kann das Wrapper-Shell-Skript
`write_features.sh` verwendet werden. Die Features werden dann für jedes
Review in einer Datei 'features' gespeichert. Der Aufruf für das Shell-Skript
benötigt mindestens drei Argumente:

  1. den Ausführmodus, der angibt, was mit bereits extrahierten
    Feature-Dateien geschieht
    * `append`, um an bestehende Feature-Dateien anzuhängen
    * `overwrite`, um bestehende Feature-Dateien zu überschreiben
    * `updatè`, um nur die in `write_features.sh` angegebenen Features in den
      bestehenden Feature-Dateien zu ändern.
  2. eine SentiWS-Datei
  3. das Verzeichnis, in dem die Reviews leben.
  4. Es können noch zusätzliche Verzeichnisse angegeben werden.

Beispielaufruf:

    > bash write_features.sh overwrite /path/to/sentiws_file\
    reviews_top_dir/ additional_reviews_top_dir/

Mit dem Skript `stars_to_features.sh` müssen nun die Sterne aus der
`info`-Datei in die Feature-Datei geschrieben werden. Das Skript
`normalize_features.sh` wird verwendet, um die Sentiment-Features zu
normalisieren und das Skript `add_binary_judgement.sh` fügt das Feature
`binary_judgement` ein. All diese Skripte müssen für jedes Review einzeln
angewandt werden, wozu sich der UNIX-Befehl `find` anbietet.
Eine automatisierte Anwendung dieser drei Skripte bietet das Skript
`add_additional_features.pl` an.

`add_additional_features.pl` benötigt als sein einziges Argument das
Verzeichnis, das die Reviews enthält, zu deren 'features'-Dateien Features
hinzugefügt werden sollen.

Beispielaufruf:

    > perl add_additional_features.pl reviews_top_dir/

Um die Feature-Dateien in ARFF-Format umzuwandeln, wird das Programm
`arff_data.py` aufgerufen. Es werden folgende Argumente übergeben:
  
  1. das Verzeichnis, in dem die Feature-Dateien liegen
  2. den Namen der ARFF-Datei, die erstellt werden soll
  3. die Namen der Features, die in die ARFF-Datei übernommen werden sollen.
    Es ist zu empfehlen, als letztes Argument das Klassen-Feature anzugeben.

Beispielaufruf:

    > python3 arff_data.py reviews_top_dir/ outfile.arff\
    overall_sentiment token_number stars

### Experimente


