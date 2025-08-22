import os
import subprocess
import threading
import time
from datetime import datetime
from django.conf import settings

class StreamRecorder:
    def __init__(self):
        self.recording_process = None
        self.is_recording = False
        
    def record_stream(self, duration_minutes=60, output_filename=None):
        """Record CNBC stream for specified duration"""
        try:
            # Create output filename with timestamp
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"recording_{timestamp}.mp3"
                
            output_path = os.path.join(settings.MEDIA_ROOT, 'recordings', output_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # CNBC Live Stream URL (you may need to find a working one)
            # Example: CNBC Live YouTube stream
            stream_url = "https://www.youtube.com/live/your-cnbc-stream-id"  # Replace with actual URL
            
            # Use yt-dlp to record audio
            command = [
                'yt-dlp',
                '-x',  # Extract audio
                '--audio-format', 'mp3',
                '--audio-quality', '0',
                '--output', output_path,
                '--no-playlist',
                '--limit-rate', '1M',
                stream_url
            ]
            
            print(f"Starting recording: {output_path}")
            self.is_recording = True
            
            # Start recording process
            self.recording_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for specified duration or until process completes
            start_time = time.time()
            while time.time() - start_time < duration_minutes * 60 and self.is_recording:
                time.sleep(1)
                if self.recording_process.poll() is not None:
                    break
            
            # Stop recording
            self.stop_recording()
            
            print(f"Recording completed: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Recording error: {e}")
            self.stop_recording()
            return None
    
    def stop_recording(self):
        """Stop the current recording"""
        if self.recording_process and self.recording_process.poll() is None:
            self.recording_process.terminate()
            self.recording_process.wait()
        self.is_recording = False

# Global recorder instance
recorder = StreamRecorder()