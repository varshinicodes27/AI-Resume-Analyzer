import pdfplumber


def extract_text_from_pdf(pdf_path: str):
    text = ""
    links = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            # Extract normal text
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

            # Extract clickable hyperlinks
            for annotation in page.annots or []:
                uri = annotation.get("uri")

                if uri:
                    links.append(uri)

    # Remove duplicate links while preserving order
    links = list(dict.fromkeys(links))

    # Add extracted URLs to the text sent to Gemini
    if links:
        text += "\n\n--- EXTRACTED HYPERLINKS ---\n"

        for link in links:
            text += link + "\n"

    return text