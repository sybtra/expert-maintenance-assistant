from fastapi import UploadFile
from typing import Union, List
import io
import json
from bs4 import BeautifulSoup
import docx2txt
from PyPDF2 import PdfReader
import markdown

class DocumentExtractor:
    """A class to extract content from various uploaded document types."""
    
    SUPPORTED_EXTENSIONS = {'.md', '.txt', '.html', '.docx', '.doc', '.pdf', '.json'}
    
    @staticmethod
    async def extract_txt(file: UploadFile) -> str:
        """Extract content from .txt files."""
        content = await file.read()
        return content.decode('utf-8')
    
    @staticmethod
    async def extract_markdown(file: UploadFile) -> str:
        """Extract content from .md files and convert to text."""
        content = await file.read()
        md_content = content.decode('utf-8')
        html_content = markdown.markdown(md_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text()
    
    @staticmethod
    async def extract_html(file: UploadFile) -> str:
        """Extract content from .html files."""
        content = await file.read()
        soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
        return soup.get_text()
    
    @staticmethod
    async def extract_docx(file: UploadFile) -> str:
        """Extract content from .docx files."""
        content = await file.read()
        return docx2txt.process(io.BytesIO(content))
    
    @staticmethod
    async def extract_pdf(file: UploadFile) -> str:
        """Extract content from .pdf files."""
        content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(content))
        return ' '.join(page.extract_text() for page in pdf_reader.pages)
    
    @staticmethod
    async def extract_json(file: UploadFile) -> str:
        """Extract content from .json files."""
        content = await file.read()
        return json.dumps(json.loads(content.decode('utf-8')), ensure_ascii=False, indent=2)
    
    async def extract_content(self, files: Union[UploadFile, List[UploadFile]]) -> str:
        """
        Extract content from one or multiple uploaded files.
        
        Args:
            files: Single UploadFile or list of UploadFile objects
            
        Returns:
            Combined string of all contents
        
        Raises:
            ValueError: If file type is not supported
        """
        if isinstance(files, UploadFile):
            files = [files]
        
        contents = []
        content = ""
        
        for file in files:
            # Get file extension from filename
            ext = '.' + file.filename.split('.')[-1].lower()
            
            # Check if extension is supported
            if ext not in self.SUPPORTED_EXTENSIONS:
                raise ValueError(f"Unsupported file type: {ext}")
            
            # Extract content based on file type
            if ext in ['.txt']:
                content = await self.extract_txt(file)
            elif ext == '.md':
                content = await self.extract_markdown(file)
            elif ext == '.html':
                content = await self.extract_html(file)
            elif ext in ['.docx', '.doc']:
                content = await self.extract_docx(file)
            elif ext == '.pdf':
                content = await self.extract_pdf(file)
            elif ext == '.json':
                content = await self.extract_json(file)
                
            # Reset file position for potential reuse
            await file.seek(0)
            contents.append(content)
        
        return ' '.join(contents).strip()

