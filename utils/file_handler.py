import os
import logging

logger = logging.getLogger(__name__)

def save_uploaded_file(uploaded_file, upload_folder):
    """
    Saves the uploaded file to the specified folder.
    
    Args:
        uploaded_file (FileStorage): The file object from Flask request.files.
        upload_folder (str): The directory to save the file.
        
    Returns:
        str: The full path to the saved file.
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Simple filename sanitization
    filename = uploaded_file.filename
    # Ensure we don't have directory traversal
    filename = os.path.basename(filename)
    
    file_path = os.path.join(upload_folder, filename)
    
    try:
        uploaded_file.save(file_path)
        return file_path
    except Exception as e:
        logger.error(f"Failed to save file {filename}: {e}")
        return None

def delete_file(file_path):
    """
    Deletes the specified file.
    
    Args:
        file_path (str): The path to the file to delete.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
             logger.error(f"Error deleting file {file_path}: {e}")
    else:
        logger.warning(f"File not found for deletion: {file_path}")
