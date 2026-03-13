import re
import pdfplumber
import html

# ===============================
# PDF TEXT EXTRACTION
# ===============================
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print("PDF Extraction Error:", e)
    return text


# ===============================
# CLEAN TEXT
# ===============================
def clean_text(text):
    try:
        # Decode unicode escapes like \u003C
        text = text.encode().decode("unicode_escape")
    except Exception:
        pass

    # Decode HTML entities
    text = html.unescape(text)

    # Fix common broken chars
    text = text.replace("â", "–")
    text = text.replace("<br>", "\n")
    text = text.replace("<br/>", "\n")
    text = text.replace("<br />", "\n")

    return text


# ===============================
# HEADING CHECK
# ===============================
def is_heading(line, keywords):
    line_clean = line.strip().lower()
    if len(line_clean.split()) > 6:
        return False
    for word in keywords:
        if word in line_clean:
            return True
    return False


# ===============================
# FORMAT TEXT WITH LINE BREAKS
# ===============================
def format_text_with_breaks(text):
    if text == "Not mentioned":
        return text
    formatted = re.sub(r'([.,])\s+', r'\1<br>', text)
    return formatted


# ===============================
# PARSE RESUME SECTIONS
# ===============================
def parse_resume(text):
    text = clean_text(text)
    lines = text.split("\n")

    sections = {
        "summary": [],
        "experience": [],
        "education": [],
        "skills": []
    }

    current_section = None

    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue

        # Detect headings
        if is_heading(line_strip, [
            "summary", "professional summary", "objective",
            "about", "about me", "profile"
        ]):
            current_section = "summary"
            continue
        elif is_heading(line_strip, [
            "experience", "work experience", "professional experience",
            "employment history"
        ]):
            current_section = "experience"
            continue
        elif is_heading(line_strip, [
            "education", "academic background", "qualification"
        ]):
            current_section = "education"
            continue
        elif is_heading(line_strip, [
            "skills", "technical skills", "core skills", "competencies"
        ]):
            current_section = "skills"
            continue

        if current_section:
            sections[current_section].append(line_strip)

    # Convert list → paragraph text
    for key in sections:
        combined = " ".join(sections[key]).strip()

        if key == "summary":
            combined = re.sub(r'\S+@\S+', '', combined)
            combined = re.sub(r'\+?\d[\d\s\-]{7,}', '', combined)

        combined = format_text_with_breaks(combined)
        sections[key] = combined if combined else "Not mentioned"

    return sections
