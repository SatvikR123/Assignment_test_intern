# Import necessary libraries
import os  # For file operations
import wave  # For reading and writing WAV files    
import pyaudio  # For audio input/output
import librosa  # For audio processing
from scipy.spatial.distance import cosine  # For cosine similarity
from resemblyzer import VoiceEncoder  # For voice embedding extraction

# Audio recording parameters 
RATE = 16000 # Sample rate (Hz)
CHANNELS = 1 # Mono means the audio is recorded in one channel
FORMAT = pyaudio.paInt16 # Audio format (16-bit PCM) also called sample width
CHUNK = 1024 # Buffer size for audio frames or frames per buffer
RECORD_SECONDS = 5 # Recording duration in seconds

# Utility functions
def record_audio(filename, duration=RECORD_SECONDS):
    """
    Record audio from microphone and save to file
    
    Args:
        filename: Output filename (.wav)
        duration: Recording duration in seconds
    """
    print(f"Recording for {duration} seconds...")
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save to WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved to {filename}")
    return filename

def extract_voice_embedding(audio_file):
    """
    Extract voice embedding using resemblyzer
    
    Args:
        audio_file: Path to WAV file
        
    Returns:
        embedding: Voice embedding vector
    """
    # Load audio file
    audio, _ = librosa.load(audio_file, sr=RATE, mono=True)
    
    # Initialize the voice encoder
    encoder = VoiceEncoder()
    
    # Get embedding
    embedding = encoder.embed_utterance(audio)
    
    return embedding # Returns a 256-dimensional embedding for the input audio

def compare_embeddings(embedding1, embedding2):
    """
    Compare two voice embeddings using cosine similarity
    
    Args:
        embedding1: First voice embedding
        embedding2: Second voice embedding
        
    Returns:
        similarity: Similarity score (0-1)
    """
    # Calculate cosine similarity (1 - cosine distance)
    similarity = 1 - cosine(embedding1, embedding2)
    return similarity 