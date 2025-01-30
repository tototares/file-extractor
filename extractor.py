from flask import Flask, request, jsonify
import pymupdf4llm
import pymupdf.pro
import fitz  # PyMuPDF
import io
app = Flask(__name__)
@app.route(‘/convert’, methods=[‘POST’])
def convert_to_markdown():
    # Unlock the pymupdf pro license
    pymupdf.pro.unlock(‘7z5cjGSb3UYwgQxgAxgXZPic’)
    # Get the uploaded file from the request
    uploaded_file = request.files[‘file’]
    # Read the file into memory
    file_bytes = uploaded_file.read()
    # Open the document using fitz (PyMuPDF) from a BytesIO stream
    doc = fitz.open(stream=io.BytesIO(file_bytes), filetype=“pdf”)
    # Convert the document to markdown using pymupdf4llm
    md_text = pymupdf4llm.to_markdown(doc)
    # Return the markdown as a JSON response
    return jsonify({“markdown”: md_text})
if __name__ == ‘__main__‘:
    app.run(host=‘0.0.0.0’, port=5001)