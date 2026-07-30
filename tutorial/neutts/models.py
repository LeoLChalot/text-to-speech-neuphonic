from django.db import models

class TTSGeneration(models.Model):
    MODE_CHOICES = [
        ('emotional', 'NeuTTS-2E (Emotional)'),
        ('cloning', 'NeuTTS Voice Cloning'),
    ]

    text = models.TextField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='emotional')
    speaker = models.CharField(max_length=50, blank=True, null=True)
    emotion = models.CharField(max_length=50, blank=True, null=True)
    backbone_model = models.CharField(max_length=100, default='neuphonic/neutts-nano')
    audio_file = models.FileField(upload_to='neutts_outputs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.mode}] {self.text[:30]}... ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
