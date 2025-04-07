# Import necessary libraries     
import os  # For file operations 
import json  # For JSON operations
import numpy as np  # For numerical operations
import pickle  # For object serialization

class VoiceDatabase:
    def __init__(self, db_path="voice_db"):
        """
        Initialize the voice database
        
        Args:
            db_path: Directory to store user data
        """
        self.db_path = db_path
        
        # Create database directory if it doesn't exist
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            print(f"Created database directory at {db_path}")
    
    def save_user(self, username, embedding):
        """
        Save user data to database
        
        Args:
            username: User identifier
            embedding: Voice embedding vector
        """
        # Ensure username is valid
        username = self._sanitize_username(username)
        
        # Create user directory if it doesn't exist
        user_dir = os.path.join(self.db_path, username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Save embedding
        embedding_file = os.path.join(user_dir, "embedding.pkl")
        with open(embedding_file, 'wb') as f:
            pickle.dump(embedding, f)
        
        # Save metadata
        metadata = {
            "username": username,
            "created_at": str(np.datetime64('now')),
            "embedding_file": embedding_file
        }
        
        metadata_file = os.path.join(user_dir, "metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"User {username} saved to database")
        return True
    
    def get_user_embedding(self, username):
        """
        Get user embedding from database
        
        Args:
            username: User identifier
            
        Returns:
            embedding: Voice embedding vector or None if user not found
        """
        username = self._sanitize_username(username)
        embedding_file = os.path.join(self.db_path, username, "embedding.pkl")
        
        if not os.path.exists(embedding_file):
            print(f"User {username} not found in database")
            return None
        
        with open(embedding_file, 'rb') as f:
            embedding = pickle.load(f)
        
        return embedding
    
    def user_exists(self, username):
        """Check if user exists in database"""
        username = self._sanitize_username(username)
        return os.path.exists(os.path.join(self.db_path, username))
    
    def list_users(self):
        """List all users in the database"""
        if not os.path.exists(self.db_path):
            return []
            
        return [d for d in os.listdir(self.db_path) 
                if os.path.isdir(os.path.join(self.db_path, d))]
    
    def _sanitize_username(self, username):
        """Ensure username is safe for filesystem"""
        # Remove dangerous characters
        return "".join(c for c in username if c.isalnum() or c in ['-', '_']).lower()