import streamlit as st
from openai import OpenAI
import requests
client=OpenAI()
# Function to generate code snippets using OpenAI
def generate_code(features, styles, components):
    # Construct prompt based on user requirements
    prompt = f"Generate a website with the following requirements:\nFeatures: {features}\nStyles: {styles}\nComponents: {components}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=400,
        messages=[
            {"role": "user", "content": prompt }
        ]
      
        
    )
    return response.choices[0].message.strip()

# Streamlit UI
def main():
    st.title("Custom Website Builder App")

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Generate Website"])

    if page == "Home":
        st.write("Welcome to the Custom Website Builder App!")
        st.write("Use the navigation on the left to get started.")

    elif page == "Generate Website":
        st.header("Generate Your Custom Website")

        # Get user requirements
        st.subheader("Specify Your Requirements")
        features = st.text_area("Features (e.g., contact form, image gallery)")
        styles = st.text_area("Styles (e.g., color scheme, fonts)")
        components = st.text_area("Components (e.g., header, footer)")

        if st.button("Generate Website"):
            # Generate website template using OpenAI
            website_template = generate_code(features, styles, components)

            # Display generated website template
            st.header("Generated Website Template")
            st.code(website_template, language="html")
