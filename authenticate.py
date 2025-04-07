# Import necessary libraries     
import os  # For file operations
import argparse  # For command-line argument parsing
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For plotting
from utils import record_audio, extract_voice_embedding, compare_embeddings  # For audio recording, embedding extraction, and comparison
from database import VoiceDatabase  # For database operations

DEFAULT_THRESHOLD = 0.8 # Minimum threshold for authentication, if the similarity score is greater than or equal to the threshold, the user is authenticated

def authenticate_user(username, passphrase=None, threshold=DEFAULT_THRESHOLD, visualize=False):
    """
    Authenticate a user by comparing their voice to a stored embedding
    
    Args:
        username: User identifier
        passphrase: Optional passphrase to display
        threshold: Similarity threshold for authentication (0-1)
        visualize: Whether to display a visualization of similarity
        
    Returns:
        authenticated: True if authenticated, False otherwise
    """
    db = VoiceDatabase()
    
    # Check if user exists
    if not db.user_exists(username):
        print(f"User {username} not found. Please register first.")
        return False
    
    # Get stored embedding
    stored_embedding = db.get_user_embedding(username)
    
    # Display instructions
    print("\n=== Voice Authentication ===")
    print(f"Hello {username}! Please authenticate with your voice.")
    
    if passphrase:
        print(f"\nPlease say: \"{passphrase}\"")
    else:
        print("\nPlease say your passphrase clearly.")
    
    input("Press Enter when ready to record...")
    
    # Record audio
    temp_file = os.path.join("temp", f"{username}_auth.wav")
    os.makedirs("temp", exist_ok=True)
    
    record_audio(temp_file)
    
    # Extract embedding
    print("Processing voice...")
    new_embedding = extract_voice_embedding(temp_file)
    
    # Compare embeddings
    similarity = compare_embeddings(stored_embedding, new_embedding)
    
    # Authentication result
    authenticated = similarity >= threshold
    
    print(f"\nSimilarity score: {similarity:.4f}")
    print(f"Threshold: {threshold:.4f}")
    
    if authenticated:
        print(f"Authentication successful! Welcome, {username}.")
    else:
        print(f"Authentication failed! Voice does not match stored profile.")
    
    # Visualization
    if visualize:
        visualize_authentication(similarity, threshold)
        
    return authenticated

def visualize_authentication(similarity, threshold):
    """Display a visualization of authentication result"""
    plt.figure(figsize=(10, 5))
    
    # Create a gauge-like visualization
    plt.axvspan(0, threshold, alpha=0.2, color='red')
    plt.axvspan(threshold, 1, alpha=0.2, color='green')
    
    plt.plot([similarity, similarity], [0, 1], 'b-', linewidth=2)
    plt.scatter([similarity], [0.5], color='blue', s=150, zorder=5)
    
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title('Voice Authentication Result')
    plt.xlabel('Similarity Score')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks([])
    
    plt.annotate(f'Score: {similarity:.4f}', 
                 xy=(similarity, 0.5),
                 xytext=(similarity, 0.7),
                 arrowprops=dict(arrowstyle='->'),
                 ha='center')
    
    plt.annotate(f'Threshold: {threshold:.4f}', 
                 xy=(threshold, 0.5),
                 xytext=(threshold, 0.3),
                 arrowprops=dict(arrowstyle='->'),
                 ha='center')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voice Authentication - Login")
    parser.add_argument("username", help="Username to authenticate")
    parser.add_argument("--passphrase", "-p", help="Suggest the passphrase for the user to speak")
    parser.add_argument("--threshold", "-t", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Similarity threshold for authentication (0-1), default: {DEFAULT_THRESHOLD}")
    parser.add_argument("--visualize", "-v", action='store_true',
                        help="Display a visualization of the authentication result")
    
    args = parser.parse_args()
    authenticate_user(args.username, args.passphrase, args.threshold, args.visualize) 