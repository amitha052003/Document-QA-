from pypdf import PdfReader


def extract_pages(pdf_file):

    reader = PdfReader(pdf_file)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text and text.strip():

            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    return pages


def create_chunks(
    pages,
    chunk_size=1200,
    overlap=200
):

    chunks = []

    for page in pages:

        text = page["text"]
        page_number = page["page_number"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "text": chunk_text.strip(),
                    "page_number": page_number
                })

            start += chunk_size - overlap

    return chunks