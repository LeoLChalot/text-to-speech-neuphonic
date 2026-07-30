from django import forms

class NeuttsForm(forms.Form):
    MODE_CHOICES = [
        ('emotional', 'NeuTTS-2E (Émotionnel)'),
        ('cloning', 'NeuTTS (Clonage de voix local)'),
    ]

    mode = forms.ChoiceField(
        label="Mode de Synthèse",
        choices=MODE_CHOICES,
        initial='emotional',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_mode'})
    )

    gen_text = forms.CharField(
        label="Texte à générer",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Entrez le texte à convertir en parole...', 'class': 'form-control'}),
        max_length=1000,
        required=True,
        initial="Saisissez votre texte ici pour générer la piste audio !"
    )

    # NeuTTS-2E Fields
    speaker = forms.ChoiceField(
        label="Voix (Speaker)",
        choices=[('emily', 'Emily (F)'), ('paul', 'Paul (M)'), ('sophie', 'Sophie (F)'), ('steven', 'Steven (M)')],
        required=False,
        initial='emily',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    emotion = forms.ChoiceField(
        label="Émotion",
        choices=[
            ('neutral', 'Neutre'),
            ('happy', 'Heureux'),
            ('sad', 'Triste'),
            ('angry', 'En colère'),
            ('disgusted', 'Dégoûté'),
            ('fearful', 'Peur'),
            ('surprised', 'Surpris')
        ],
        required=False,
        initial='happy',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Voice Cloning / Backbone Fields
    backbone_repo = forms.ChoiceField(
        label="Modèle Backbone",
        choices=[
            ('neuphonic/neutts-nano', 'NeuTTS-Nano (English)'),
            ('neuphonic/neutts-air', 'NeuTTS-Air (English - Faster)'),
            ('neuphonic/neutts-nano-french', 'NeuTTS-Nano-French'),
            ('neuphonic/neutts-nano-german', 'NeuTTS-Nano-German'),
            ('neuphonic/neutts-nano-spanish', 'NeuTTS-Nano-Spanish'),
        ],
        required=False,
        initial='neuphonic/neutts-nano',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ref_audio_file = forms.FileField(
        label="Fichier Audio Référence (.wav)",
        required=False,
        widget=forms.FileInput(attrs={'accept': '.wav', 'class': 'form-control'})
    )

    ref_text = forms.CharField(
        label="Texte de Référence Audio",
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Transcription exacte de l\'audio de référence...', 'class': 'form-control'}),
        required=False
    )
