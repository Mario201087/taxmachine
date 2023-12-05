from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Set the Tesseract path if it's not in your PATH environment variable
# pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        try:
            # Save the uploaded file
            file_path = 'uploads/' + file.filename
            file.save(file_path)

            # Use Tesseract to extract text from the image
            text = pytesseract.image_to_string(Image.open(file_path))

            # Convert text to XML
            xml_data = create_xml(text)

            # Save the XML data to a file
            xml_file_path = 'uploads/' + file.filename.replace('.png', '.xml')
            with open(xml_file_path, 'w') as xml_file:
                xml_file.write(xml_data)

            # Return the XML file path
            return jsonify({'xml_file_path': xml_file_path})

        except Exception as e:
            return jsonify({'error': str(e)})

def create_xml(text):
    # Create a simple XML structure
    root = ET.Element("root")
    element = ET.SubElement(root, "text")
    element.text = text

    # Convert ElementTree to string
    xml_data = ET.tostring(root).decode()

    return xml_data

if __name__ == '__main__':
    app.run(debug=True)
