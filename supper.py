# prototype

from openai import OpenAI
import streamlit as st
import json
import google_scrap_auto
import prompts
import blog_posts
import tokens_count
import os 
import weather 
from langchain_core.prompts import ChatPromptTemplate
import tutor_audio as audio
import Crypto_function as crypt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain.chains.loading import RetrievalQAWithSourcesChain
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set page configuration 
st.set_page_config(page_title="ChatBrain Pro", page_icon='🚀', layout='centered')
client = OpenAI()

def log_to_file(log_message, filename="log.txt"):
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create or open the log file in append mode
    log_file_path = os.path.join(current_directory, filename)
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message + "\n")


# Define functions to interact with the JSON file
def load_settings():
    try:
        with open("settings.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(settings): # settings : The dictionary containing the settings.
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)


# Load settings or use default values if not found
settings = load_settings()

show_token_cost_default = settings.get("show_token_cost", False)
api_key_default = settings.get("api_key", "")
temperature_default = settings.get("temperature", 0.7)
top_p_default = settings.get("top_p", 1.0)
model_default = settings.get("model", "gpt-3.5-turbo")
    
# Add a button to the sidebar to clear messages
if st.sidebar.button("***Clear Messages***", key="clear_messages_button"):
    # Clear all messages
    st.session_state.messages = []
    # Rerun the app to reflect the changes
    st.rerun()

# Sidebar settings
st.sidebar.header("Settings")

show_token_cost = True  

api_key = st.sidebar.text_input("***API Key***",type="password",value=api_key_default)
temperature = st.sidebar.slider("***Temperature***", 0.1, 1.0, temperature_default)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, top_p_default)
model = st.sidebar.selectbox(
    "***Model***",
    ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k","dall-e-3"],
    index=0 if model_default == "gpt-3.5-turbo" else 1,
)

# Update settings with the new values
settings.update(
    {
        "show_token_cost": show_token_cost,
        "api_key": api_key,
        "temperature": temperature,
        "top_p": top_p,
        "model": model,
    }
)
save_settings(settings)


if "cumulative_tokens" not in st.session_state:
    st.session_state.cumulative_tokens = 0
if "cumulative_cost" not in st.session_state:
    st.session_state.cumulative_cost = 0


# Set the title with HTML and CSS
st.markdown("""<style>
.title {
    font-family: 'sans-serif',Verdana, Tahoma, Geneva, Verdana, sans-serif;
    font-size: 3em;
    font-weight: bold;
    color: #FAFAFA;
}
</style>
<i><h1 class="title">ChatBrain v2.0 </i>📊</h1></i>""", unsafe_allow_html=True)

# Set the API key if it's provided
if api_key:
    client.api_key = api_key
else:
    st.warning("***Please provide a valid OpenAI API Key.***")
    st.stop()

llm = ChatOpenAI(model=model,temperature=temperature)
output_parser = StrOutputParser()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Input field for user query
prompt = st.chat_input("What is up?")

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Display the input field and other chat components

if prompt:
    start_prompt_used = ""

    # Check for "reset" command from user
    if prompt.strip().lower() == "/reset":
        st.session_state.messages = []  # Clear the conversation
        st.session_state.cumulative_tokens = 0  # Reset cumulative tokens
        st.session_state.cumulative_cost = 0  # Reset cumulative cost
        st.sidebar.markdown(
            f"**Total Tokens Used This Session:** {st.session_state.cumulative_tokens}"
        )
        st.sidebar.markdown(
            f"**Total Cost This Session:** ${st.session_state.cumulative_cost:.2f}"
        )
        st.warning("Conversation and counters have been reset!")
        st.stop()  # Halts further execution for this run of the app


    
    if prompt.strip().lower().startswith("/summarize"):
        blog_url = prompt.split(" ", 1)[1].strip()
        # Display user's query
        with st.chat_message("user"):
          st.markdown(blog_url)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Summarizing: " + blog_url)
            blog_summary_prompt = blog_posts.get_blog_summary_prompt(blog_url)
            response_obj = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[{"role": "user", "content": blog_summary_prompt}]

            )
            blog_summary = ""
            
               
            if response_obj.choices[0].message.content is not None:
                    blog_summary += response_obj.choices[0].message.content
            blog_summary = output_parser.parse(blog_summary)
            message_placeholder.markdown(blog_summary + "▌")

            # update the whole prompt to update token count
            start_prompt_used = blog_summary_prompt + blog_summary

            message_placeholder.markdown(blog_summary)  # Display the summary in chat
            st.session_state.messages.append(
                {"role": "assistant", "content": blog_summary}
            )

    



    elif prompt.strip().lower().startswith("/audio"):
      # Extract the text from the command
      text_to_convert = prompt.strip()[len("/audio"):].strip()
      if not text_to_convert:
        st.warning("Please provide a question or text to generate audio.")
        st.stop()

      # Display user's query
      with st.chat_message("user"):
        st.markdown(text_to_convert)

      with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # Generate response text
        response_text = audio.generate_response(text_to_convert)

        # Generate audio
        message_placeholder.markdown("Generating response in the format of audio...")
        audio_content = audio.generate_audio(response_text)

        # Display response text
        st.session_state.messages.append({"role": "user", "content": text_to_convert})
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        # Display audio
        st.audio(audio_content, format="audio/mp3", start_time=0)
        st.success("Audio generated successfully!")

        start_prompt_used = text_to_convert + response_text



    elif prompt.strip().lower().startswith("/crypto"):
      crypto_symbol = prompt.split(" ", 1)[1].strip()
      price = crypt.get_crypto_price(crypto_symbol)
      if price  is not None:
       with st.chat_message("user"):
          st.markdown(crypto_symbol)
       with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(f"Analyzing the market for {crypto_symbol.upper()}...")

            # Include the adapted response message with the current price
          
            response_message = (
                f"The current price of {crypto_symbol.upper()} is ${price:.2f}. "
                "However, please note that cryptocurrency markets are highly "
                "volatile, and prices can fluctuate rapidly based on various factors. "
                "Therefore, it's essential to conduct thorough research and risk management "
                "before making investment decisions in the cryptocurrency space."
            )
            message_placeholder.markdown(f"Analyzing the market for {crypto_symbol.upper()}...")
            message_placeholder.markdown(response_message)
            st.session_state.messages.append({"role": "assistant", "content": response_message})

     


            
    elif prompt.strip().lower().startswith("/weather"):
      location = prompt.split(" ", 1)[1].strip()
      weather_data = weather.get_weather_data(location)
      if weather_data:
        with st.chat_message("user"):
          st.markdown("The weather in " + location)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(f"Retrieving weather data for {location}...")
            response_message = f"Weather in {location}:\n\n"
            for key, value in weather_data.items():
                response_message += f"- **{key}:** {value['value']} {value.get('unit', '')} *({value['info']})*\n"
            message_placeholder.markdown(response_message)
            st.session_state.messages.append({"role": "assistant", "content": response_message})
      else:
        with st.chat_message("assistant"):
            st.write("Failed to retrieve weather data.")    
      





    elif prompt.strip().lower().startswith("/rewrite"):
        input_text = prompt.split(" ", 1)[1].strip()
        with st.chat_message("user"):
          st.markdown(input_text)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Rewriting...")
            rewrite_prompt = prompts.rewrite_prompt.format(text=input_text)
            response_obj = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    
                    {"role": "user", "content": rewrite_prompt}
                ]          
            )
            new_written_text = ""
            
            if response_obj.choices[0].message.content is not None:
                    new_written_text += response_obj.choices[0].message.content
            new_written_text = output_parser.parse(new_written_text)
            message_placeholder.markdown(new_written_text + "▌")

            # update the whole prompt to update token count
            start_prompt_used = rewrite_prompt + new_written_text

            message_placeholder.markdown(new_written_text)
            st.session_state.messages.append(
                {"role": "assistant", "content": new_written_text}
            )
    




    elif prompt.strip().lower().startswith("/google"):
      input_query = prompt.split(" ", 1)[1].strip()
      with st.chat_message("user"):
        st.markdown(input_query)
      with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(
            "Searching Google For: " + input_query + "..."
        )
        search_results = google_scrap_auto.search_google_web_automation(input_query)
        urls = [result["url"] for result in search_results]  # Define urls
        docs = []
        for url in urls:
            loader = WebBaseLoader(url)
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '.', ','],
                chunk_size=1000
            )
            doc_chunks = text_splitter.split_documents(data)
            docs.extend(doc_chunks)

        # Create embeddings and save them to Chroma index
        embeddings = OpenAIEmbeddings()
        vectorstore_openai = Chroma.from_documents(docs, embeddings)
        if input_query and vectorstore_openai:
            retriever = vectorstore_openai.as_retriever()
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=retriever)
            result = chain.invoke({"question": input_query}, return_only_outputs=True)
            response = result["answer"]
            sources = result["sources"]

            message_placeholder.markdown(response)


            start_prompt_used =  response

            message_placeholder.markdown(start_prompt_used)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )




    
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are the best assistant in the world, providing detailed responses to any question."),
                ("user", "{input}")
            ]) 
            chain = prompt_template | llm | output_parser
            full_response = chain.invoke({"input": prompt})   
            message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            start_prompt_used = prompt + full_response

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )




    if show_token_cost:
        total_tokens_used = tokens_count.count_tokens(start_prompt_used, model)
        total_cost = tokens_count.estimate_input_cost_optimized(
            model, total_tokens_used
        )
        st.session_state.cumulative_tokens += total_tokens_used
        st.session_state.cumulative_cost += total_cost

        # Redisplay the updated cumulative tokens and cost in the left sidebar
        st.sidebar.markdown(
            f"**Total Tokens Used This Session:** {st.session_state.cumulative_tokens}"
        )
        st.sidebar.markdown(
            f"**Total Cost This Session:** ${st.session_state.cumulative_cost:.6f}"
        )

   

