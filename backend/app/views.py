from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Keyword, RecordingSchedule, DetectedClip
from .forms import KeywordForm
from .utils.recorder import recorder

def home(request):
    """Simple home page showing detected clips"""
    clips = DetectedClip.objects.all().order_by('-timestamp')[:10]
    keywords = Keyword.objects.filter(is_active=True)
    schedules = RecordingSchedule.objects.filter(is_active=True)
    
    return render(request, 'home.html', {
        'clips': clips,
        'keywords': keywords,
        'schedules': schedules,
        'is_recording': recorder.is_recording
    })

def add_keyword(request):
    """Add a new keyword to monitor"""
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = KeywordForm()
    
    return render(request, 'add_keyword.html', {'form': form})

def start_recording(request):
    """Start recording manually"""
    if request.method == 'POST':
        duration = int(request.POST.get('duration', 5))  # Default 5 minutes for testing
        result = recorder.record_stream(duration_minutes=duration)
        
        if result:
            return JsonResponse({'status': 'success', 'file': result})
        else:
            return JsonResponse({'status': 'error', 'message': 'Recording failed'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def stop_recording(request):
    """Stop recording manually"""
    recorder.stop_recording()
    return JsonResponse({'status': 'success', 'message': 'Recording stopped'})

def recording_status(request):
    """Get current recording status"""
    return JsonResponse({
        'is_recording': recorder.is_recording,
        'status': 'recording' if recorder.is_recording else 'idle'
    })