import magic
from langchain.document_loaders.parsers import BS4HTMLParser, PDFMinerParser
from langchain.document_loaders.parsers.generic import MimeTypeBasedParser
from langchain.document_loaders.parsers.txt import TextParser
from langchain.document_loaders.parsers.msword import MsWordParser
from langchain_community.document_loaders import Blob

def parse_data(data):
    # Configure the parsers that you want to use per mime-type!
    HANDLERS = {
        # "application/pdf": PDFMinerParser(),
        "text/plain": TextParser(),
        # "text/html": BS4HTMLParser(),
        # "ms/word": MsWordParser(),
    }

    # Instantiate a mimetype based parser with the given parsers
    MIMETYPE_BASED_PARSER = MimeTypeBasedParser(
        handlers=HANDLERS,
        fallback_parser=None,
    )

    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(data)

    # A blob represents binary data by either reference (path on file system)
    # or value (bytes in memory).
    blob = Blob.from_data(
        data=data,
        mime_type=mime_type,
    )

    parser = HANDLERS[mime_type]
    documents = parser.parse(blob=blob)
    documents[0].metadata['source'] = "App"
    return documents

