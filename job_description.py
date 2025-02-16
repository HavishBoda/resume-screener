import re
import sys
import pdfplumber
from collections import defaultdict

# matches with expr,
def matchSub(expr, text):
    matches = re.findall(expr, text)
    cleaned = re.sub(expr, "", text)
    # return the first match if it exists along with the cleaned text
    return matches[0] if len(matches) else "", cleaned
    


def get_gpa(text):
    expr = r"[1-4](?:\.[0-9]{1,2})\/4"
    return matchSub(expr, text)

def get_phone(text):
    expr = r'(?:\+\d{1,2}\s)?(?:\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})'
    return matchSub(expr, text)
# TODO: add other regex

def get_lines(name):
    with pdfplumber.open(name) as pdf:
        return pdf.pages[0].extract_text_lines()
    
SECTION_TITLES = [
    "company",
    "location",
    "department",
    "employment type",
    "job summary",
    "responsibilities",
    "qualifications",
    "skills", 
    "required skills",
    "work environment",
    "about",
    "how",
    "benefits",
    "description"
]

# TODO: implement this
# should give back the section title we're in now
# if this isn't a section, return ""
def section_title(line):
    for word in line['text'].lower().split():
        if word in SECTION_TITLES:
            return word
    return ""

def get_sections(lines):
    sectionData = defaultdict(list)


    section = ""
    for line in lines:
        if not len(line):
            continue
        res = section_title(line)
        if res:
            section = res
        elif len(section):
            sectionData[section].append(line["text"])
    
    return sectionData

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("give resume path")
        exit(1)
    name = sys.argv[1]
    with pdfplumber.open(name) as pdf:
        text = pdf.pages[0].extract_text()
        gpa, text = get_gpa(text)
        phone, text = get_phone(text)

        lines = get_lines(name)

        print(gpa)
        print(phone)

        data = get_sections(lines)
        for key in data:
            print(key)
            for line in data[key]:
                print(line)
            print()
