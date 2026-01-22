import os
import streamlit as st

def save_uploaded_file(uploaded_file, upload_folder):
    """
    Saves the uploaded file to the specified folder.
    
    Args:
        uploaded_file (UploadedFile): The file uploaded via Streamlit.
        upload_folder (str): The directory to save the file.
        
    Returns:
        str: The full path to the saved file.
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    file_path = os.path.join(upload_folder, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return file_path

def delete_file(file_path):
    """
    Deletes the specified file.
    
    Args:
        file_path (str): The path to the file to delete.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        st.warning(f"File not found: {file_path}")
