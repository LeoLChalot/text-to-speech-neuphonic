import os
import uuid
import logging
import soundfile as sf
from django.conf import settings
from neutts import NeuTTS2E, NeuTTS

logger = logging.getLogger(__name__)

_NEUTTS_2E_MODEL = None
_NEUTTS_GENERAL_MODELS = {}


def get_neutts_2e():
    """
    Lazy loader for local NeuTTS2E (emotional model).
    """
    global _NEUTTS_2E_MODEL
    if _NEUTTS_2E_MODEL is None:
        logger.info("Initializing local NeuTTS2E model...")
        _NEUTTS_2E_MODEL = NeuTTS2E()
    return _NEUTTS_2E_MODEL


def get_neutts_general(backbone_repo: str = "neuphonic/neutts-nano", backbone_device: str = "gpu", codec_repo: str = "neuphonic/neucodec", codec_device: str = "gpu"):
    """
    Lazy loader for local general NeuTTS model (voice cloning / multilingual).
    """
    global _NEUTTS_GENERAL_MODELS
    key = (backbone_repo, backbone_device, codec_repo, codec_device)
    if key not in _NEUTTS_GENERAL_MODELS:
        logger.info(f"Initializing local NeuTTS general model with backbone '{backbone_repo}'...")
        _NEUTTS_GENERAL_MODELS[key] = NeuTTS(
            backbone_repo=backbone_repo,
            backbone_device=backbone_device,
            codec_repo=codec_repo,
            codec_device=codec_device
        )
    return _NEUTTS_GENERAL_MODELS[key]


def generate_speech_emotional(text: str, speaker: str = "emily", emotion: str = "happy") -> tuple[str, str]:
    """
    Synthesize speech using NeuTTS2E (emotional control).
    Returns tuple: (file_path, filename)
    """
    tts = get_neutts_2e()
    wav = tts.infer(text, speaker=speaker, emotion=emotion)

    media_dir = getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media'))
    outputs_dir = os.path.join(media_dir, 'neutts_outputs')
    os.makedirs(outputs_dir, exist_ok=True)

    filename = f"neutts_2e_{uuid.uuid4().hex[:10]}.wav"
    filepath = os.path.join(outputs_dir, filename)
    sf.write(filepath, wav, 24000)
    return filepath, filename


def generate_speech_cloning(text: str, ref_audio_path: str, ref_text: str, backbone_repo: str = "neuphonic/neutts-nano") -> tuple[str, str]:
    """
    Synthesize speech locally using general NeuTTS with instant voice cloning.
    Returns tuple: (file_path, filename)
    """
    tts = get_neutts_general(backbone_repo=backbone_repo)
    ref_codes = tts.encode_reference(ref_audio_path)
    wav = tts.infer(text, ref_codes, ref_text)

    media_dir = getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media'))
    outputs_dir = os.path.join(media_dir, 'neutts_outputs')
    os.makedirs(outputs_dir, exist_ok=True)

    filename = f"neutts_clone_{uuid.uuid4().hex[:10]}.wav"
    filepath = os.path.join(outputs_dir, filename)
    sf.write(filepath, wav, 24000)
    return filepath, filename
