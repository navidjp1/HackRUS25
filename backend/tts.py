# 1️⃣ Install kokoro
# !pip install -q kokoro>=0.3.1 soundfile
# 2️⃣ Install espeak, used for English OOD fallback and some non-English languages
# !apt-get -qq -y install espeak-ng > /dev/null 2>&1
# 🇪🇸 'e' => Spanish es
# 🇫🇷 'f' => French fr-fr
# 🇮🇳 'h' => Hindi hi
# 🇮🇹 'i' => Italian it
# 🇧🇷 'p' => Brazilian Portuguese pt-br

# 3️⃣ Initalize a pipeline
import re
from kokoro import KPipeline
from IPython.display import display, Audio
import numpy as np
import soundfile as sf
# 🇺🇸 'a' => American English, 🇬🇧 'b' => British English
# 🇯🇵 'j' => Japanese: pip install misaki[ja]
# 🇨🇳 'z' => Mandarin Chinese: pip install misaki[zh]

def preprocess_text(text):
    """
    Replace single newline characters (those not adjacent to another newline)
    with a space. This preserves intentional paragraph breaks (i.e. double newlines).
    """
    return re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
 

pipeline = KPipeline(lang_code='a') # <= make sure lang_code matches voice

# This text is for demonstration purposes only, unseen during training
# text = '''A throng of bearded men, in sad-colored garments, and gray, steeple-crowned hats, intermixed with women, some wearing hoods and others bareheaded, was assembled in front of a wooden edifice, the door of which was heavily timbered with oak, and studded with iron spikes.'''


text = ""
with open('/Users/navidjery/Desktop/HackRUS25/backend/input1.txt', 'r') as file:
    text = file.read()

# text = preprocess_text(text)

# 4️⃣ Generate, display, and save audio files in a loop.
generator = pipeline(
    text, voice='af_heart', # <= change voice here
    speed=1, split_pattern=r'\n{2,}'
)

audio_segments = []
for i, (gs, ps, audio) in enumerate(generator):
    print(i)  # i => index
    print(gs) # gs => graphemes/text
    #print(ps) # ps => phonemes
    # display(Audio(data=audio, rate=24000, autoplay=i==0))
    audio_segments.append(audio)
    
full_audio = np.concatenate(audio_segments)
    
    
sf.write('full_text2.wav', full_audio, 24000) # save each audio file




