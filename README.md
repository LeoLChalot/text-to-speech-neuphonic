# Initiation à Djang & DjangoRestFramework

Projet visant à utiliser les modèle de synthèses volcales dévezloppés par **Neuphonic** 

- [Hugging Face - Neuphonic Home Page](https://huggingface.co/neuphonic)
- [Hugging Face - neutts-2e](https://huggingface.co/neuphonic/neutts-2e)
- [Hugging Face - neutts-nano](https://huggingface.co/neuphonic/neutts-nano)

> \[!NOTE]
>
> Le modèle *neutts-2e* est utilisé ici pour personnaliser la synthèse à un sentiment
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

Le dossier de projet est organisé comme suit :

```plainText
text-to-speech-neuphonic/
├── .gitignore
├── README.md
├── manage.py                   # Script d'utilitaire de commande Django
├── requirements.txt            # Dépendances Python (django, neuphonic, etc.)
│
├── tutorial/                 # Dossier de configuration global (nommé selon l'init)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Configuration (incluant STATICFILES_DIRS, MEDIA_ROOT)
│   ├── urls.py                 # Routage global vers l'application
│   └── wsgi.py
│
└── neutts/                     # Application dédiée à la synthèse vocale
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py                # Contient le formulaire NeuttsForm
    ├── models.py               # Contient loe modèle TTSGeneration
    ├── services.py             # Logique d'appel IA (generate_speech_emotional, etc.)
    ├── urls.py                 # Routage local de l'application
    ├── views.py                # Vues web (neutts_view, serve_audio_view, api_generate_view)
    ├── migrations/             # Fichiers de migration de la base de données
    ├── templates/
    │   └── neutts/
    │       └── template.html   # Interface web utilisateur
    └── static/                 # Fichiers statiques gérés par collectstatic
        ├── css/
        │   └── neutts_style.css
        └── js/
            └── script.js
```

> \[!IMPORTANT]
> L'application *quickstart* a volontairement été omise pour ne pas surcharger la documentation
> Cette application est l'application du tutoriel proposé sur le site de [Django REST Framework](https://www.django-rest-framework.org/tutorial/quickstart/)