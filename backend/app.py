from translate import translate_text
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import time
import os
from obtain import extract_text_from_url
from split import split_text
from kokoro import KPipeline
from IPython.display import display, Audio
import numpy as np
import soundfile as sf
from io import BytesIO



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# pipeline = KPipeline(lang_code='a')

lang_codes = {
    "english": "a",
    "spanish": "e",
    "french": "f",
    "hindi": "h",
    "portuguese": "p"
}

voice_types = {
    "english": {
        "Female Voice": "af_heart",
        "Male Voice": "am_michael"
    },
    "spanish": {
        "Female Voice": "ef_dora",
        "Male Voice": "em_alex"
    },
    "french": {
        "Female Voice": "ff_siwis",
        "Male Voice": "am_michael"
    },
    "hindi": {
        "Female Voice": "hf_alpha",
        "Male Voice": "hm_omega"
    },
    "portuguese": {
        "Female Voice": "pf_dora",
        "Male Voice": "pm_alex"
    },
}


@app.route('/generate', methods=['POST'])
def generate_wav():
    try:
        data = request.get_json()
        part_number = data.get('part', 1)
        url = data.get('url', '')
        voiceType = data.get('voice', 'Female Voice')
        language = data.get('language', 'Translate?')
        book_id = url.split('/')[-2]

        text = extract_text_from_url(url)
        parts = split_text(text)

        if part_number > len(parts):
            return jsonify({"error": "No more parts available"}), 404
        
        app.logger.info(f"Starting WAV generation for part {part_number}...")

        # Translate the text if needed
        translated_text = parts[part_number-1]
        if language != 'Translate?':
            translated_text = translate_text(translated_text, language)
            if translated_text is None:
                return jsonify({"error": "Translation failed"}), 500
            
        code = lang_codes.get(language.lower(), "a")
        pipeline = KPipeline(lang_code=code)

        voiceTypeRegion = voice_types.get(language.lower(), {"Female Voice": "af_heart", "Male Voice": "am_michael"})
        voiceType = voiceTypeRegion.get(voiceType, "af_heart")

        generator = pipeline(
            translated_text, voice=voiceType,
            speed=1, split_pattern=r'\n{2,}'
        )

        audio_segments = []
        for i, (gs, ps, audio) in enumerate(generator):
            print(i)  # i => index
            print(gs + '\n') # gs => graphemes/text
            audio_segments.append(audio)
            
        full_audio = np.concatenate(audio_segments)
        
        audio_buffer = BytesIO()
        sf.write(audio_buffer, full_audio, 24000, format='wav')
        audio_buffer.seek(0)  # Reset buffer position to beginning

        app.logger.info(f"WAV generation complete for part {part_number}. Sending file...")

        return send_file(
            audio_buffer,
            mimetype="audio/wav",
            as_attachment=True,
            download_name=f'book_{book_id}_part_{part_number}.wav'
        )
    

    except Exception as e:
        app.logger.error(f"Error during WAV generation for part {part_number}: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True)
