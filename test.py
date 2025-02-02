import spacy
from spacy.matcher import Matcher
import re
import pdfplumber

# step 1 - load spacy model
nlp = spacy.load("en_core_web_sm")

# step 2 - extracting text from resume
with pdfplumber.open("jakes-resume.pdf") as pdf:
    resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

print(resume_text[:500]) # displays first 500 characters in resume

# step 3 - Named Entity Recognition
doc = nlp(resume_text)

for ent in doc.ents:
    print(f"{ent.label_}: {ent.text}")

# STEP 4 - Custom pattern matching
# Regex pattern for phone numbers
phone_regex = r'(\+\d{1,2}\s)?(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})'
phones = re.findall(phone_regex, resume_text)

# Regex pattern for LinkedIn URLs
linkedin_regex = r'linkedin\.com/(in|pub)/[A-Za-z0-9-_/]+'
linkedins = re.findall(linkedin_regex, resume_text)

# Extract emails using SpaCy Matcher
matcher = Matcher(nlp.vocab)
email_pattern = [
    {"TEXT": {"REGEX": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"}}
]
matcher.add("EMAIL", [email_pattern])

matches = matcher(doc)

emails = []
for match_id, start, end in matches:
    span = doc[start:end]
    emails.append(span.text)

print(f"Extracted Phones: {[phone[1] for phone in phones]}")
print(f"Extracted Emails: {emails}")
print(f"Extracted LinkedIn URLs: {[f'https://linkedin.com/{linkedin}' for linkedin in linkedins]}")

# STEP 5 - Extract the person's name
name = ""
for ent in doc.ents:
    if ent.label_ == "PERSON":
        name = ent.text
        break

print(f"Extracted Name: {name}")

# STEP 6 - Extracting other entities
# Example for extracting organizations
organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
print(f"Extracted Organizations: {organizations}")

# STEP 7 - Combining extracted information into organized structure
parsed_resume = {
    "Name": name,
    "Phone": phones[0][1],
    "Email": emails[0],
    "LinkedIn": f'https://linkedin.com/{linkedins[0]}'
}

for match_id, start, end in matches:
    span = doc[start:end]
    match_label = nlp.vocab.strings[match_id]
    if match_label == "EMAIL":
        parsed_resume["Email"] = span.text

print(parsed_resume)