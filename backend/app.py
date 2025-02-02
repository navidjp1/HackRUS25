from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import time
import os

app = Flask(__name__)
CORS(app) 

@app.route('/generate', methods=['POST'])
def generate_wav():

    try:
        app.logger.info("Starting WAV generation...")
        time.sleep(10)  

        output_path = 'output.wav'
        if not os.path.exists(output_path):
            with open(output_path, 'wb') as f:
                f.write(b'\x00' * 1024 * 1024 * 25)  # 25 MB dummy file

        app.logger.info("WAV generation complete. Sending file...")

        return send_file(
            output_path,
            as_attachment=True,
            attachment_filename="output.wav",
            mimetype="audio/wav"
        )
    
    except Exception as e:
        app.logger.error("Error during WAV generation: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
