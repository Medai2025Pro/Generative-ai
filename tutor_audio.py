import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()


# Function to generate response
def generate_response(text):
 response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": text},
  ]
)
 res=response.choices[0].message.content
 return res

# Function to generate audio using OpenAI's TTS model
def generate_audio(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy", # 'nova','shimmer','echo','onyx','fable','alloy'
        input=text
    )
    return response.content

# Main Streamlit app
def main():
    st.title("Tutor_TTC Voice🔉")

    # Text input
    input_text = st.text_input("***Enter your question***")

    # Generate audio
    if st.button("Generate response"):
        answewr=generate_response(input_text)
        audio_file = generate_audio(answewr)
        st.audio(audio_file, format="audio/mp3", start_time=0)
        st.success("Audio generated successfully!")
# Run the Streamlit app
if __name__ == "__main__":
    main()
