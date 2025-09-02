from groq import Groq
from dotenv import load_dotenv
import os
import yt_dlp

load_dotenv()

GROQ_KEY_1 = os.getenv("GROQ_KEY_1")

client = Groq(api_key=GROQ_KEY_1)

def transcribe_audio(audio_path, client: Groq):

    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo"  # Groq Whisper
        )
    return transcript.text

def summarize_text_with_llm(text, client: Groq):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",   # Groq fast + cheap option
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes transcripts clearly. You are also a general assistant who can answer questions."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
    )
    return response.choices[0].message.content.strip()

def download_youtube_audio(url, output_path="yt_audio"):
    ydl_opts = {
        "format": "bestaudio/best",   # no video
        "outtmpl": output_path,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "64",  # lighter, faster
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path+".mp3"
