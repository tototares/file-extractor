from flask import Flask, request, jsonify
import pymupdf4llm
import pymupdf.pro
import fitz  # PyMuPDF
import io
import os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def convert_to_markdown():
    correctAuthToken = os.getenv("AUTH_TOKEN")
    providedAuthToken = request.headers.get('Authorization')
    if not correctAuthToken or not providedAuthToken or correctAuthToken != providedAuthToken:
        return jsonify({"error": "Auth token invalid"}), 403

    uploaded_file = request.files['file']
    if not uploaded_file:
        return jsonify({"error": "Missing File"}), 400

    # Unlock the pymupdf pro license
    license_key = os.getenv("PYMUPDF_LICENSE")
    if not license_key:
        return jsonify({"error": "Missing PyMuPDF Pro License"}), 500
    pymupdf.pro.unlock(license_key)

    file_bytes = uploaded_file.read()
    doc = fitz.open(stream=io.BytesIO(file_bytes), filetype="pdf")

    return jsonify({"markdown": pymupdf4llm.to_markdown(doc)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)