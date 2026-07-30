import os
import urllib.parse
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, FileResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import NeuttsForm
from .models import TTSGeneration
from .services import generate_speech_emotional, generate_speech_cloning


def serve_audio_view(request, filename=None):
    if not filename:
        filepath = request.GET.get('filepath')
        if filepath and os.path.exists(filepath):
            filename = os.path.basename(filepath)
    
    if not filename:
        raise Http404("Fichier audio non spécifié.")

    media_dir = getattr(settings, 'MEDIA_ROOT', os.path.join(settings.BASE_DIR, 'media'))
    audio_path = os.path.join(media_dir, 'neutts_outputs', filename)

    if not os.path.exists(audio_path) or not os.path.isfile(audio_path):
        filepath = request.GET.get('filepath')
        if filepath and os.path.exists(filepath) and os.path.isfile(filepath):
            audio_path = filepath
        else:
            raise Http404("Le fichier audio demandé est introuvable.")

    return FileResponse(open(audio_path, 'rb'), content_type='audio/wav', filename=os.path.basename(audio_path))


def neutts_view(request):
    """
    Web application view for local NeuTTS speech synthesis.
    """
    form = NeuttsForm()
    recent_generations = []
    try:
        recent_generations = TTSGeneration.objects.order_by('-created_at')[:5]
    except Exception:
        pass

    context = {
        'form': form,
        'error': None,
        'success': False,
        'recent_generations': recent_generations
    }

    if request.method == 'POST':
        form = NeuttsForm(request.POST, request.FILES)
        context['form'] = form

        if form.is_valid():
            mode = form.cleaned_data['mode']
            gen_text = form.cleaned_data['gen_text']

            try:
                if mode == 'emotional':
                    speaker = form.cleaned_data.get('speaker') or 'emily'
                    emotion = form.cleaned_data.get('emotion') or 'happy'
                    filepath, filename = generate_speech_emotional(
                        text=gen_text,
                        speaker=speaker,
                        emotion=emotion
                    )
                    try:
                        TTSGeneration.objects.create(
                            text=gen_text,
                            mode='emotional',
                            speaker=speaker,
                            emotion=emotion,
                            audio_file=f"neutts_outputs/{filename}"
                        )
                    except Exception:
                        pass
                else:
                    # Voice Cloning Mode
                    backbone_repo = form.cleaned_data.get('backbone_repo') or 'neuphonic/neutts-nano'
                    ref_audio = request.FILES.get('ref_audio_file')
                    ref_text = form.cleaned_data.get('ref_text')

                    if not ref_audio or not ref_text:
                        raise ValueError("Le mode clonage de voix requiert un fichier audio (.wav) et son texte de référence.")

                    ref_dir = os.path.join(settings.MEDIA_ROOT, 'neutts_refs')
                    os.makedirs(ref_dir, exist_ok=True)
                    ref_path = os.path.join(ref_dir, ref_audio.name)
                    with open(ref_path, 'wb+') as destination:
                        for chunk in ref_audio.chunks():
                            destination.write(chunk)

                    filepath, filename = generate_speech_cloning(
                        text=gen_text,
                        ref_audio_path=ref_path,
                        ref_text=ref_text,
                        backbone_repo=backbone_repo
                    )
                    try:
                        TTSGeneration.objects.create(
                            text=gen_text,
                            mode='cloning',
                            backbone_model=backbone_repo,
                            audio_file=f"neutts_outputs/{filename}"
                        )
                    except Exception:
                        pass

                audio_url = reverse('serve_audio_filename', kwargs={'filename': filename})
                context['audio_result_url'] = audio_url
                context['filename'] = filename
                context['success'] = True
                try:
                    context['recent_generations'] = TTSGeneration.objects.order_by('-created_at')[:5]
                except Exception:
                    pass

            except Exception as e:
                context['error'] = f"Erreur lors de la génération local NeuTTS : {str(e)}"
        else:
            context['error'] = "Veuillez vérifier les champs du formulaire."

    return render(request, 'neutts/template.html', context)


@csrf_exempt
def api_generate_view(request):
    """
    REST API endpoint for generating audio locally via NeuTTS.
    POST /tts/api/generate/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    mode = request.POST.get('mode', 'emotional')
    text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'error': 'Missing required parameter: text'}, status=400)

    try:
        if mode == 'emotional':
            speaker = request.POST.get('speaker', 'emily')
            emotion = request.POST.get('emotion', 'happy')
            filepath, filename = generate_speech_emotional(text=text, speaker=speaker, emotion=emotion)
        else:
            backbone_repo = request.POST.get('backbone_repo', 'neuphonic/neutts-nano')
            ref_text = request.POST.get('ref_text', '')
            ref_audio = request.FILES.get('ref_audio')
            if not ref_audio or not ref_text:
                return JsonResponse({'error': 'Cloning mode requires ref_audio file and ref_text string.'}, status=400)

            ref_dir = os.path.join(settings.MEDIA_ROOT, 'neutts_refs')
            os.makedirs(ref_dir, exist_ok=True)
            ref_path = os.path.join(ref_dir, ref_audio.name)
            with open(ref_path, 'wb+') as destination:
                for chunk in ref_audio.chunks():
                    destination.write(chunk)

            filepath, filename = generate_speech_cloning(
                text=text,
                ref_audio_path=ref_path,
                ref_text=ref_text,
                backbone_repo=backbone_repo
            )

        audio_url = request.build_absolute_uri(reverse('serve_audio_filename', kwargs={'filename': filename}))
        return JsonResponse({
            'status': 'success',
            'mode': mode,
            'text': text,
            'filename': filename,
            'audio_url': audio_url
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)