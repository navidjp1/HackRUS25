from deep_translator import GoogleTranslator


def translate_text(text, target_language='english'):

    lang_codes = {
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "hindi": "hi",
        "portuguese": "pt"
    }

    target_lang_code = lang_codes.get(target_language.lower(), "en")

    chunks = []
    max_chunk_size = 4000
    if len(text) > max_chunk_size:
        chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    else:
        chunks = [text]

    translator = GoogleTranslator(source='auto', target=target_lang_code)
    
    translated_chunks = []
    for chunk in chunks:
        translated_chunk = translator.translate(chunk)
        translated_chunks.append(translated_chunk)
    
    return "".join(translated_chunks)



