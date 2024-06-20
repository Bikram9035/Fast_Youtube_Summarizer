import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import time
from groq import Groq
from openai import OpenAI



load_dotenv(".env")



# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
# os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

groqllm=Groq()
# gpt=OpenAI()



prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 1000 words. Please provide the summary of the text given here:  """

def yt_transcript(yt_video_url):

    try:
        video_id=yt_video_url.split("v=")[-1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id,languages=["en","en-IN","hi"])

        transcript=""
        for i in transcript_text:
            transcript+= " "+i["text"]

        return transcript

    except Exception as e:
        raise e

# #-------------- use any one of the api services depending on video length and how fast u want it to process

#uncomment below code if your video length greater than 30 min-google_gemini

# def gemini(transcript_text,prompt):

#     model=genai.GenerativeModel("models/gemini-1.5-pro-latest")              #models/gemini-1.5-flash,models/gemini-1.5-pro-latest
#     response=model.generate_content(prompt+transcript_text, stream=True)
    
#     for chunk in response:
#        yield chunk.text

#---------------------------------------------------------------------------------

#the fastest one , use it if your video length is less than 30min(groq api)
def llm(transcript_text,prompt):
    response = groqllm.chat.completions.create(
        messages=[
             {
            "role": "system",
            "content": prompt,
             },
             { 
            "role": "user",
            "content": transcript_text,
             }
        ],
        model="llama3-8b-8192", 
        # model="llama3-70b-8192",
        # model="mixtral-8x7b-32768",
        stream=True,
        max_tokens=800,
        
    )

    for chunk in response:
        yield chunk.choices[0].delta.content

#----------------------------------------------------------------------------
#this is second fastest but same video length i.e less than 30min
# def gptllm(transcript_text,prompt):
#     response=gpt.chat.completions.create(
#             messages=[
#                         { 
                        
#                         "role":"system",
#                         "content":prompt,

#                         },
#                         {
#                          "role":"user",
#                          "content":transcript_text,     


#                         }

#                      ],
#             model="gpt-4o",
#             stream=True,
#             max_tokens=500,
#     )

    # for chunk in response:
    #     yield chunk.choices[0].delta.content

#------------------------------------------------------------------------------------
st.title("YouTube AI Summarizer")
youtube_link=st.text_input("Paste the YouTube Video Link")

if youtube_link:                             
    video_id = youtube_link.split("v=")[-1]
    
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True) 
start=time.time()
if st.button("SUBMIT"):  
    transcription_text=yt_transcript(youtube_link)

    if transcription_text:
       st.markdown("Summary of the Video")
       summary=llm(transcription_text,prompt)
       st.write_stream(summary)
print(time.time()-start)





