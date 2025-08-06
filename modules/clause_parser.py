import fitz  # PyMuPDF
import docx
import re
import nltk
nltk.download('punkt')

def extract_text_from_pdf(uploaded_file):
    # Read directly from the uploaded stream
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def chunk_text_into_clauses(text):
    # Simple regex and sentence tokenization
    raw_clauses = re.split(r"\n\s*\d+\.\s*|\n\s*[A-Z][a-z]+:|\n\s*[A-Z\s]{5,}\n", text)
    clauses = []
    for chunk in raw_clauses:
        sentences = nltk.sent_tokenize(chunk)
        if len(sentences) > 0:
            clauses.append(" ".join(sentences))
    return [c.strip() for c in clauses if len(c.strip()) > 30]  # Filter noise

import re

def chunk_contract_text(contract_text):
    """
    Splits contract text into numbered or paragraph-based clauses.
    Returns a list of {'id': clause_id, 'text': clause_text}.
    """
    pattern = r"(?m)^(?P<clause_id>\d+(\.\d+)*).*?\n(?P<clause_text>.*?)(?=\n\d|\n\n|\Z)"
    matches = re.finditer(pattern, contract_text, re.DOTALL)

    chunks = []
    for i, match in enumerate(matches):
        clause_id = match.group("clause_id")
        clause_text = match.group("clause_text").strip()
        chunks.append({
            "id": f"Clause {clause_id}" if clause_id else f"Clause {i+1}",
            "text": clause_text
        })

    if not chunks:
        # Fallback: simple paragraph splitting
        chunks = [{"id": f"Clause {i+1}", "text": block.strip()}
                  for i, block in enumerate(contract_text.split("\n\n"))]
    return chunks