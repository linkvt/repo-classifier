# Repo Classifier
Repo Classifier is a web application realized with Django that uses Machine Learning algorithms to classify GitHub 
repositories into several categories. This project is developed by the team of the University of Stuttgart for the 
[informatiCup2017](https://github.com/InformatiCup/InformatiCup2017/).


## Requirements
- python 3.5+
- pip
- [yarn](https://yarnpkg.com/en/docs/install)

## Setup
- Create a virtual environment with `python -m venv .venv`
- Activate the venv with `source .venv/bin/activate` or install `autoenv` and create a `.env` file as described below
- Install the dependencies with `pip install -r requirements.txt`
- Setup the python SDK to `.venv/bin/python` to also access the dependencies in the venv
- Install web dependencies with `yarn`
- Copy the file `github.conf.template` to `github.conf` and set your GitHub token or credentials

### New Dependencies
- Install a dependency in the venv with `pip install DEPENDENCY`
- Save a snapshot of the dependencies with `pip freeze > requirements.txt`

### Configure autoenv
Simply create a file called `.env` in the root directory of the repository and paste this in it for Linux.
```
source .venv/bin/activate
echo "repo-classifier - NICE! (venv on)"
```

## Files for input
For classification we expect a file containing one line for each repository url.
```
https://github.com/briantemple/homeworkr
https://github.com/angular
...
```

For training we need a file which contains the label for a url.
We support two formatted inputs for training:

Separated with a simple space.
```
https://github.com/briantemple/homeworkr DEV
...
```

or separated with a comma and first line will be ignored (becaused we used the django export):
```
url,category
https://github.com/owncloud/documentation,DOCS
...
```

## Run the web application (Preferred)
- Run `python manage.py migrate` to setup the database.
- Execute `python manage.py runserver` to start the live reloading webserver on [localhost:8000](http://localhost:8000/).
- You can now run the classifier by uploading a file and pressing `Classify`.
- (Optional) You can train a model by uploading a file as described above and pressing `Train`.

## Run in CLI
After the complete setup described above open a terminal and `cd` into the root directory of the project.
Then just execute `python main.py` and a help output will guide you with the possible parameters.
For simple classification just run `python main.py -f "path/to/file" -c` which will run the classification (Attention: the model has to be available to run the classification).
If training is needed just replace the `-c` with `-t`: `python main.py -f "path/to/file" -t`

## FAQ

### Klassifikation funktioniert nicht. Konsole wirft Fehler mit nicht passenden Featurezahlen oder ähnliches.
Das schließt darauf hin, dass sich die Featurereihenfolge oder die Featureanzahl verändert hat und ein altes Classification model genutzt. Für den Fall muss man das Training neu starten und dadurch ein neues `model` generieren lassen, dass dann verwendet werden kann.

### Welche Daten werden persistent gespeichert?
Im root Verzeichnis befinden sich die `db` und ein `model`.
Die DB beinhaltet dabei gecachte Werte für Features und Repositories und erleichtert so neues Trainieren etc, da keine Request gesendet werden müssen.
Das Model ist das Klassifizierungsmodel und beinhaltet das Training, wodurch die Klassifizierung überhaupt erst ermöglicht wird.
Diese Dateien können auch kopiert und wiederverwendet werden, solange sich nichts an den Features selbst verändert.

## Reference
- autoenv: https://github.com/kennethreitz/autoenv
- packaging: https://packaging.python.org/installing/
- venv: https://docs.python.org/3/library/venv.html
