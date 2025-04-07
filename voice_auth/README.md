# Offline Voice Authentication System

A simple voice authentication system that works completely offline. This system allows users to register their voice and then authenticate using future voice inputs.

## How It Works

1. **Voice Registration**:
   - Users record a short audio clip speaking a custom passphrase
   - The system extracts a voiceprint (speaker embedding) using the resemblyzer library
   - This voiceprint is stored in a local file-based database

2. **Voice Authentication**:
   - When authenticating, users record themselves saying the same passphrase
   - The system extracts a new voiceprint and compares it to the stored one
   - Using cosine similarity, the system determines if the voices match
   - If the similarity exceeds a threshold (default: 0.75), authentication succeeds

3. **Offline Capability**:
   - All processing happens locally without internet connection
   - Uses lightweight pre-trained models for voice embedding

## Installation

1. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Note: PyAudio installation may require additional system dependencies:
   - Windows: No additional steps needed
   - macOS: `brew install portaudio`
   - Linux: `sudo apt-get install python3-pyaudio`

## Usage

### 1. Register a user

```bash
python register.py username --passphrase "my secure passphrase"
```

Example:
```bash
python register.py john --passphrase "voice is my password"
```

### 2. Authenticate a user

```bash
python authenticate.py username --passphrase "my secure passphrase" --visualize
```

Example:
```bash
python authenticate.py john --passphrase "voice is my password" --visualize
```

## Performance Observations

- **Voice Consistency**: The system works best when users maintain consistent tone, speed, and pronunciation
- **Background Noise**: A quiet environment leads to better authentication accuracy
- **Passphrase Length**: Longer passphrases (3-5 seconds) provide better accuracy than very short ones
- **Threshold Setting**: The default threshold of 0.75 balances security and usability; adjust as needed

## Advanced Features

1. **Multiple Users**: The system supports an unlimited number of users
2. **Visualization**: Use the `--visualize` flag to see a graphical representation of similarity scores
3. **Adjustable Threshold**: Set custom thresholds with the `--threshold` flag (0-1 range)

## Limitations and Future Improvements

- **Noise Robustness**: Future versions could implement better noise filtering
- **Liveness Detection**: Currently vulnerable to replay attacks; could add measures to detect recorded voices
- **Pronunciation Analysis**: Could implement stricter passphrase checking

## Directory Structure

- `register.py`: Handles user registration
- `authenticate.py`: Handles authentication
- `utils.py`: Shared utilities and functions
- `database.py`: Database management functions
- `voice_db/`: Directory storing user voice embeddings
- `temp/`: Temporary audio files 