import pandas as pd
import io
import PyPDF2
import docx
from io import StringIO
import base64

def get_file_text(uploaded_file):
    """
    Extract text from various file formats
    
    Args:
        uploaded_file: The uploaded file object
        
    Returns:
        str: Extracted text from the file
    """
    file_name = uploaded_file.name.lower()
    
    if file_name.endswith('.txt'):
        # For txt files
        return uploaded_file.getvalue().decode('utf-8')
    
    elif file_name.endswith('.pdf'):
        # For PDF files
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")
    
    elif file_name.endswith('.docx'):
        # For DOCX files
        try:
            doc = docx.Document(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {e}")
    
    else:
        raise Exception("Unsupported file format. Please upload a .txt, .pdf, or .docx file.")
