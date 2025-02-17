from flask import Flask, request, jsonify
import os
import io
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def convert_to_markdown():
    correctAuthToken = os.getenv("AUTH_TOKEN")
    providedAuthToken = request.headers.get('Authorization')
    if not correctAuthToken or not providedAuthToken or correctAuthToken != providedAuthToken:
        return jsonify({"error": "Auth token invalid"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "Missing File"}), 400

    uploaded_file = request.files['file']
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        file_bytes = uploaded_file.read()
        file_stream = DocumentStream(name=uploaded_file.name, stream=io.BytesIO(file_bytes))  # Direkter Stream statt Speicherung

        # Verwende DocumentConverter mit Memory-Stream
        converter = DocumentConverter()
        result = converter.convert(file_stream)

        if not result or not result.document:
            return jsonify({"error": "Failed to process document"}), 500

        markdown = result.document.export_to_markdown()

        if not markdown.strip():
            return jsonify({"error": "Extracted markdown is empty"}), 400

    except Exception as e:
        return jsonify({"error": "Failed to extract markdown", "details": str(e)}), 500

    return jsonify({"markdown": markdown})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)