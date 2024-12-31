import magic
from langchain.document_loaders.parsers import BS4HTMLParser, PDFMinerParser
from langchain.document_loaders.parsers.generic import MimeTypeBasedParser
from langchain.document_loaders.parsers.txt import TextParser
from langchain.document_loaders.parsers.msword import MsWordParser
from langchain_community.document_loaders import Blob
from fastapi import UploadFile
from typing import Union, List
import tempfile
import os

async def get_mime_type(filename: str, content: bytes) -> str:
    """
    Déterminer le type MIME d'un fichier en utilisant l'extension et le contenu.
    """
    # Types MIME connus par extension
    MIME_TYPES = {
        '.txt': 'text/plain',
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.json': 'application/json'
    }
    
    # Vérifier d'abord l'extension
    ext = os.path.splitext(filename.lower())[1]
    if ext in MIME_TYPES:
        return MIME_TYPES[ext]
    
    # Si pas trouvé par extension, utiliser python-magic
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(content)
    
    # Si on obtient application/octet-stream, on se replie sur l'extension
    if mime_type == 'application/octet-stream' and ext in MIME_TYPES:
        return MIME_TYPES[ext]
        
    return mime_type

async def parse_data(file: UploadFile):
    """
    Parse un fichier uploadé en utilisant le parser approprié selon son type MIME.
    
    Args:
        file (UploadFile): Le fichier à parser
        
    Returns:
        List: Liste des documents parsés
    """
    HANDLERS = {
        "application/pdf": PDFMinerParser(),
        "text/plain": TextParser(),
        "text/html": BS4HTMLParser(),
        "application/msword": MsWordParser(),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": MsWordParser(),
        "application/json": TextParser()  # JSON peut être géré par le TextParser
    }

    try:
        # Lire le contenu du fichier
        content = await file.read()
        
        # Obtenir le type MIME avec notre fonction améliorée
        mime_type = await get_mime_type(file.filename, content)
        
        if mime_type not in HANDLERS:
            raise ValueError(f"Type de fichier non supporté: {mime_type}")
        
        # Créer le blob avec les bytes
        blob = Blob.from_data(
            data=content,
            mime_type=mime_type,
        )
        
        # Parser le document
        parser = HANDLERS[mime_type]
        documents = parser.parse(blob=blob)
        documents[0].metadata["source"] = file.filename
        
        return documents
        
    except Exception as e:
        raise Exception(f"Erreur lors du parsing du document: {str(e)}")
    
    finally:
        # Réinitialiser le fichier pour une utilisation ultérieure
        await file.seek(0)
        # Fermer le fichier
        await file.close()