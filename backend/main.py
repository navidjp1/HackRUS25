from obtain import extract_text_from_url
from split import split_text
from kokoro import KPipeline
from IPython.display import display, Audio
import numpy as np
import soundfile as sf



url1 = "https://www.gutenberg.org/cache/epub/25344/pg25344.txt"
url2 = "https://www.gutenberg.org/cache/epub/98/pg98.txt"
url3 = "https://www.gutenberg.org/cache/epub/1184/pg1184.txt" # very long
url4 = "https://www.gutenberg.org/cache/epub/43/pg43.txt" # short

url = url4

book_id = url.split('/')[-2]

text = extract_text_from_url(url)
parts = split_text(text)


pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice


for i, part in enumerate(parts):

    generator = pipeline(
        part, voice='af_heart', # <= change voice here
        speed=1, split_pattern=r'\n{2,}'
    )

    audio_segments = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(i)  # i => index
        print(gs[1:250] + '\n') # gs => graphemes/text
        audio_segments.append(audio)
        
    full_audio = np.concatenate(audio_segments)
    sf.write(f'part{i}.wav', full_audio, 24000) # save each audio file

