# Initiation à Djang & DjangoRestFramework

Projet visant à utiliser les modèle de synthèses volcales dévezloppés par **Neuphonic** 

- [Hugging Face - Neuphonic Home Page](https://huggingface.co/neuphonic)
- [Hugging Face - neutts-2e](https://huggingface.co/neuphonic/neutts-2e)
- [Hugging Face - neutts-nano](https://huggingface.co/neuphonic/neutts-nano)

> \[!NOTE] Le modèle *neutts-2e* est utilisé ici pour personnaliser la synthèse à un sentiment
> Tandis que le modèle *neutts-nano* est utilisé pour une synthyèse vocale basée sur un clonage de voix

## Configuratin de l'environnement

### Création de l'environnement virtuel

```bash
# ./
python -m venv .venv
source .venv/bin/activate
```

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Appliquer les migrations

```bash
python3 manage.py migrate
```

### Créer un super-utilisateur (Optionnel)

```bash
python3 manage.py createsuperuser
```

### Rassembler les fichiers statiques

```bash
python3 manage.py collectstatic
```

### Lancer le server de développement

```bash
python3 manage.py runserver
```
L'application sera accessible à l'adresse [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Architecture du dossier de projet