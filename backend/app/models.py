from django.db import models

class Keyword(models.Model):
    word = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word

class RecordingSchedule(models.Model):
    TIME_CHOICES = [
        ('09:00', '9:00 AM'),
        ('12:00', '12:00 PM'),
    ]
    
    time_slot = models.CharField(max_length=5, choices=TIME_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording at {self.get_time_slot_display()}"

class DetectedClip(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='clips/')
    transcript = models.TextField(blank=True)

    def __str__(self):
        return f"Clip: {self.keyword.word} at {self.timestamp}"