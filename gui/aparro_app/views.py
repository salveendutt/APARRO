from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .transcriber import Transcriber  # Import your Transcriber class

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        # Handle the audio file sent from the frontend
        audio_file = request.FILES.get('audio_data')

        # Use your Transcriber class to transcribe the audio
        transcriber = Transcriber(model_name="medium.en", device_type="cuda")
        transcription = transcriber._transcribe_audio(audio_file)
        

        return JsonResponse({'transcription': transcription})
    return render(request, 'transcribe.html')

def index(request):
    return render(request, 'index.html')

def ready_page(request):
    return render(request, 'ready_page.html')