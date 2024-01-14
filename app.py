from flask import Flask, request, render_template
import re
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_pii(text):
    pii_detected = []

    # Extract Aadhaar numbers
    aadhaar_matches = re.findall(r'\b\d{12}\b', text)
    for match in aadhaar_matches:
        pii_detected.append({"pii_type": "Aadhaar Number", "pii_value": match})

    # Extract Passport numbers
    passport_matches = re.findall(r'\b[Pp]\d{6}\b', text)
    for match in passport_matches:
        pii_detected.append({"pii_type": "Passport Number", "pii_value": match.upper()})

    # Extract mobile numbers
    mobile_matches = re.findall(r'\b\d{10}\b', text)
    for match in mobile_matches:
        pii_detected.append({"pii_type": "Mobile Number", "pii_value": match})

    # Extract email addresses
    email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    for match in email_matches:
        pii_detected.append({"pii_type": "Email Address", "pii_value": match})

    # Extract credit card numbers
    credit_card_matches = re.findall(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b', text)
    for match in credit_card_matches:
        pii_detected.append({"pii_type": "Credit Card Number", "pii_value": match})

    # Extract social security numbers
    ssn_matches = re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text)
    for match in ssn_matches:
        pii_detected.append({"pii_type": "Social Security Number", "pii_value": match})

    # Extract driver's license numbers
    dl_matches = re.findall(r'\b[DdLl]\d{10}\b', text)
    for match in dl_matches:
        pii_detected.append({"pii_type": "Driver's License Number", "pii_value": match.upper()})

    # Extract names using spaCy
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            pii_detected.append({"pii_type": "Name", "pii_value": ent.text})

    # Extract house addresses
    address_matches = re.findall(r'\b\d+\s[A-Za-z]+\b', text)
    for match in address_matches:
        pii_detected.append({"pii_type": "House Address", "pii_value": match})

    return pii_detected

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/detect_pii', methods=['POST'])
def detect_pii():
    try:
        paragraph = request.form.get('paragraph')
        pii_detected = extract_pii(paragraph)

        if not pii_detected:
            return render_template('index.html', result="No PII detected.")

        return render_template('index.html', result=pii_detected)

    except Exception as e:
        return render_template('index.html', result=None, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
