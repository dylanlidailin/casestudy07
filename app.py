from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Service is running"
    }), 200

@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    """File upload endpoint"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided",
                "status": "error"
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "error": "No file selected",
                "status": "error"
            }), 400
        
        # Save file temporarily
        filename = file.filename
        file.save(filename)
        
        # Get file info
        file_size = os.path.getsize(filename)
        
        return jsonify({
            "status": "success",
            "filename": filename,
            "size": file_size,
            "message": "File uploaded successfully",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to the API",
        "endpoints": {
            "health": "/api/v1/health",
            "upload": "/api/v1/upload"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
