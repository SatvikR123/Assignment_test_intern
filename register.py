# Import necessary libraries      
import os  # For file operations
import argparse  # For command-line argument parsing
from utils import record_audio, extract_voice_embedding  # For audio recording and embedding extraction
from database import VoiceDatabase  # For database operations

# Register a new user by recording their voice and extracting an embedding  
def register_user(username, passphrase=None):
    """
    Register a new user by recording their voice and extracting an embedding
    
    Args:
        username: User identifier
        passphrase: Optional passphrase to display
    """
    db = VoiceDatabase()
    
    # Check if user already exists
    if db.user_exists(username):
        print(f"User {username} already exists. Use a different username or delete the existing user.")
        return False
    
    # Display instructions
    print("\n=== Voice Registration ===")
    print(f"Hello {username}! You'll need to record your voice for authentication.")
    
    if passphrase:
        print(f"\nPlease say: \"{passphrase}\"")
    else:
        print("\nPlease say your chosen passphrase clearly.")
    
    input("Press Enter when ready to record...")
    
    # Record audio
    temp_file = os.path.join("temp", f"{username}_register.wav")
    os.makedirs("temp", exist_ok=True)
    
    record_audio(temp_file)
    
    # Extract embedding
    print("Processing voice...")
    embedding = extract_voice_embedding(temp_file)
    
    # Save to database
    db.save_user(username, embedding)
    
    print(f"\nRegistration successful! User {username} can now authenticate.")
    return True

if __name__ == "__main__":
    # Command-line interface for user registration  
    parser = argparse.ArgumentParser(description="Voice Authentication - Registration")
    parser.add_argument("username", help="Username to register")
    parser.add_argument("--passphrase", "-p", help="Suggest a passphrase for the user to speak")
    
    args = parser.parse_args()
    register_user(args.username, args.passphrase) 