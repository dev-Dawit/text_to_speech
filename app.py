import boto3
import streamlit as st
from newspaper import Article
from newspaper.parsers import lxml_html_clean
import os

polly = boto3.client("polly")

def synthesize_speech(text, output_file):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna"  # Choose a voice (Joanna, Matthew, etc.)
    )
    with open(output_file, "wb") as file:
        file.write(response["AudioStream"].read())

def extract_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title, article.text

st.title("📰 News Reader Application with AI Text-to-Speech")
st.markdown(
    "Enter a valid news article URL below, and the app will convert the article's content to natural speech using Amazon Polly."
)

url_input = st.text_input("Enter the URL of a news article:")

if st.button("Generate Audio"):
    if url_input:
        try:
            st.info("Fetching article content, please wait...")
            title, article_text = extract_article(url_input)
            
            if len(article_text.strip()) == 0:
                st.error("The article has no content to process. Please try a different URL.")
            else:
                output_path = "output/news_audio.mp3"
                os.makedirs("output", exist_ok=True)
                st.info("Synthesizing speech, please wait...")
                synthesize_speech(article_text[:3000], output_path)
                st.audio(output_path, format="audio/mp3")
                st.success(f"Audio generated successfully! Article Title: {title}")
        except Exception as e:
            st.error(f"Failed to process the URL. Error: {e}")
    else:
        st.error("Please enter a valid news article URL.")
