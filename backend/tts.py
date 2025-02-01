from transformers import pipeline
import numpy as np
from scipy.io.wavfile import write

# Initialize the text-to-speech pipeline with the Kokoro model.
# The pipeline will download the model automatically from Hugging Face.
tts_pipeline = pipeline("text-to-speech", model="hexgrad/Kokoro-82M", framework="pt")

# Define your sample text.
sample_text = (
    "Hello, this is a sample text-to-speech conversion using the Kokoro model from Hugging Face. "
    "This lightweight model is perfect for general speech synthesis."
)

# Run the TTS pipeline.
# The output is a dictionary containing the waveform and its sampling rate.
output = tts_pipeline(sample_text)

# Extract the waveform (a list or numpy array) and the sampling rate.
audio_array = output["array"]
sampling_rate = output["sampling_rate"]

# Save the audio as a WAV file.
output_filename = "kokoro_output.wav"
write(output_filename, sampling_rate, np.array(audio_array))

print(f"Audio file saved as {output_filename}")
