import os
import sys
import subprocess
import whisper
from pydub import AudioSegment
from pydub.silence import split_on_silence
import json
import re
from datetime import timedelta

class VideoToSRTConverterWhisper:
    def __init__(self, model_size="base"):
        """
        Initialize with Whisper model
        model_size options: "tiny", "base", "small", "medium", "large"
        """
        print(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        
    def mp4_to_mp3(self, input_video_path, output_audio_path=None):
        """
        Convert MP4 video to MP3 audio using ffmpeg
        """
        if output_audio_path is None:
            output_audio_path = input_video_path.replace('.mp4', '.mp3')
        
        try:
            # Check if ffmpeg is installed
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: ffmpeg is not installed. Please install ffmpeg first.")
            print("Download from: https://ffmpeg.org/download.html")
            return None
        
        try:
            # Convert MP4 to MP3
            cmd = [
                'ffmpeg', '-i', input_video_path,
                '-vn',  # No video
                '-acodec', 'mp3',
                '-ab', '192k',  # Bitrate
                '-ar', '16000',  # Sample rate (Whisper works best with 16kHz)
                '-y',  # Overwrite output file
                output_audio_path
            ]
            
            print(f"Converting {input_video_path} to MP3...")
            subprocess.run(cmd, check=True)
            print(f"Successfully converted to: {output_audio_path}")
            return output_audio_path
            
        except subprocess.CalledProcessError as e:
            print(f"Error converting video to audio: {e}")
            return None
    
    def transcribe_audio(self, audio_path):
        """
        Transcribe entire audio file using Whisper
        """
        print("Transcribing audio with Whisper...")
        
        try:
            # Transcribe with timestamps
            result = self.model.transcribe(
                audio_path,
                verbose=True,
                word_timestamps=True
            )
            
            return result
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def format_time(self, seconds):
        """
        Convert seconds to SRT time format (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        seconds = seconds % 3600
        minutes = int(seconds // 60)
        seconds = seconds % 60
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def generate_srt_from_whisper(self, transcription_result, output_path):
        """
        Generate SRT file from Whisper transcription result
        """
        print("Generating SRT file from Whisper transcription...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            subtitle_index = 1
            
            # Process segments from Whisper
            for segment in transcription_result['segments']:
                start_time = segment['start']
                end_time = segment['end']
                text = segment['text'].strip()
                
                if text:  # Only add subtitle if there's text
                    # Format timestamps
                    start_formatted = self.format_time(start_time)
                    end_formatted = self.format_time(end_time)
                    
                    # Write SRT format
                    f.write(f"{subtitle_index}\n")
                    f.write(f"{start_formatted} --> {end_formatted}\n")
                    f.write(f"{text}\n\n")
                    
                    subtitle_index += 1
        
        print(f"SRT file generated: {output_path}")
    
    def process_video(self, input_video_path, output_srt_path=None):
        """
        Main function to process video: MP4 -> MP3 -> SRT using Whisper
        """
        if not os.path.exists(input_video_path):
            print(f"Error: Video file '{input_video_path}' not found.")
            return False
        
        # Step 1: Convert MP4 to MP3
        mp3_path = self.mp4_to_mp3(input_video_path)
        if not mp3_path:
            return False
        
        # Step 2: Transcribe audio with Whisper
        transcription_result = self.transcribe_audio(mp3_path)
        if not transcription_result:
            print("Error: Could not transcribe audio.")
            return False
        
        # Step 3: Generate SRT file
        if output_srt_path is None:
            output_srt_path = input_video_path.replace('.mp4', '.srt')
        
        self.generate_srt_from_whisper(transcription_result, output_srt_path)
        
        # Clean up temporary MP3 file
        try:
            os.remove(mp3_path)
            print(f"Cleaned up temporary file: {mp3_path}")
        except:
            pass
        
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python video_to_srt_whisper.py <input_video.mp4> [output_srt.srt] [model_size]")
        print("\nModel sizes: tiny, base, small, medium, large")
        print("Example:")
        print("  python video_to_srt_whisper.py video.mp4")
        print("  python video_to_srt_whisper.py video.mp4 subtitles.srt")
        print("  python video_to_srt_whisper.py video.mp4 subtitles.srt medium")
        return
    
    input_video = sys.argv[1]
    output_srt = sys.argv[2] if len(sys.argv) > 2 else None
    model_size = sys.argv[3] if len(sys.argv) > 3 else "base"
    
    # Validate model size
    valid_models = ["tiny", "base", "small", "medium", "large"]
    if model_size not in valid_models:
        print(f"Invalid model size: {model_size}")
        print(f"Valid options: {', '.join(valid_models)}")
        return
    
    converter = VideoToSRTConverterWhisper(model_size)
    success = converter.process_video(input_video, output_srt)
    
    if success:
        print("\n✅ Processing completed successfully!")
    else:
        print("\n❌ Processing failed!")

if __name__ == "__main__":
    main()
