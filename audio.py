import streamlit as st
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Function to generate audio using OpenAI's TTS model and save it to a file
def stream_to_file(text, file_path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    # Save the audio to the specified file path
    with open(file_path, "wb") as f:
        f.write(response.content)

# Define the Streamlit app
def main():
    st.title("OpenAI Text-to-Speech (TTS) Demo")

    # Input text box for user input
    input_text = st.text_input("Enter the text you want to convert to audio:")

    # Button to generate audio
    if st.button("Generate Audio"):
        if input_text:
            # Generate audio and save it to the file
            speech_file_path = Path("speech.mp3")  # Save the audio file in the current directory
            stream_to_file(input_text, speech_file_path)
            st.success("Audio generated successfully!")
        else:
            st.warning("Please enter some text to generate audio.")

    # Button to download the audio file
    if "speech_file_path" in locals():
        st.audio(speech_file_path.read_bytes(), format="audio/mp3", label="Download Audio", file_name="speech.mp3")

if __name__ == "__main__":
    main()
