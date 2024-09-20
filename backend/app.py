# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from stability_sdk.client import generation
from stability_sdk import client
from PIL import Image
from IPython.display import display
import warnings
import io
import getpass
from moviepy.editor import ImageClip, AudioFileClip
from mutagen.mp3 import MP3
import os
from gtts import gTTS
from edumat import save_audio, get_audio_lengths, generate_clips, merge_videos_in_folder, empty_folder
import os
import shutil

import requests
from pprint import pprint
import replicate
from collections import Counter
import google.generativeai as genai
app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests

# The stability SDK and other parts of the code remain the same


@app.route('/process_story', methods=['POST'])
def process_story():
    data = request.json
    my_story = data['story']  # This will be the story sent from Flutter
    folder_to_empty1 = r'C:\Users\ron61\Desktop\Edumate\edumate2\assets\videos'
    empty_folder(folder_to_empty1)
    folder_to_empty2 = r'C:\miniproject\output'
    empty_folder(folder_to_empty2)
    folder_to_empty3 = r'C:\miniproject\photos'
    empty_folder(folder_to_empty3)
    folder_to_empty4 = r'C:\miniproject\audios'
    empty_folder(folder_to_empty4)

    genai.configure(api_key="Enter your Api key Here")

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[{
        "role": "user",
        "parts": ["essay on ai"]
    },
        {
            "role": "model",
            "parts": ["## Artificial Intelligence: Reshaping Our World\n\nArtificial intelligence (AI) has transitioned from science fiction to a tangible reality, intricately woven into the fabric of our daily lives. From the algorithms curating our social media feeds to the voice assistants managing our schedules, AI's influence is undeniable and its potential, seemingly limitless. This essay explores the multifaceted landscape of AI, examining its applications, benefits, challenges, and the ethical considerations surrounding its development and deployment.\n\n**Applications Across Industries:**\n\nAI's versatility is evident in its wide range of applications across diverse sectors. In healthcare, AI algorithms analyze medical images with remarkable accuracy, aiding in early disease detection and diagnosis. The financial industry utilizes AI for fraud detection, algorithmic trading, and personalized financial advice. Manufacturing processes are becoming increasingly automated thanks to AI-powered robots and predictive maintenance systems. Even the creative industries are experiencing AI's impact, with AI tools assisting in music composition, graphic design, and content creation.\n\n**Benefits and Advancements:**\n\nThe integration of AI brings forth numerous benefits. Automation of repetitive tasks leads to increased efficiency and productivity, freeing up human workers to focus on more complex and creative endeavors. AI-powered systems can analyze vast datasets, identifying patterns and insights that would be impossible for humans to discern. This has led to breakthroughs in scientific research, weather prediction, and disaster response. Moreover, AI personalizes user experiences, tailoring products and services to individual preferences, ultimately enhancing customer satisfaction.\n\n**Challenges and Ethical Concerns:**\n\nDespite its transformative potential, AI presents significant challenges. Job displacement due to automation remains a concern, requiring proactive measures to reskill and upskill the workforce. Bias in AI algorithms, often stemming from biased training data, can lead to discriminatory outcomes and perpetuate societal inequalities. The issue of data privacy is also paramount, as AI systems often rely on vast amounts of personal data, raising concerns about its collection, storage, and use. \n\nThe development of autonomous weapons systems raises ethical questions about accountability and the potential for misuse. Ensuring the responsible development and deployment of AI is crucial, necessitating international cooperation and robust regulatory frameworks.\n\n**The Road Ahead:**\n\nAI is poised to revolutionize our world in ways we can only begin to imagine. As AI research progresses, we can expect even more sophisticated and capable systems. The key lies in harnessing the power of AI for the betterment of humanity while mitigating potential risks. Open dialogues, ethical guidelines, and continuous research are essential to ensure a future where AI complements and empowers human capabilities, leading to a more equitable and prosperous society."]
    },
        {
            "role": "user",
            "parts": ["stop"]
    },
        {
            "role": "model",
            "parts": ["Okay, I've stopped generating the essay."]
    },])

    convo.send_message(
        my_story+"\n give this story in simple english with less than 300 words")
    story = convo.last.text
    text1 = "generate scenes  or image description prompts for image generations for above story. Seperate each description with one End of line character. Dont include any headings for each description. JUst give me the descriptions as a set of 5 points and nothing else"
    text1_1 = "REMEMBER each prompt generates images independently.So doesn't lose context since each image is generated individually."
    text2 = "generate narration of one sentence for each scene based on story"
    convo.send_message(text1+text1_1)
    scripts = convo.last.text
    # convo.send_message(text2)
    dialoges = convo.last.text

    # dialoges =
    uw = ["Scene", "Narrator", "Description", "Dialogue for",
          "Images", "Panel", "Detailed", "Sentences"]
    up = ["*", ";", ":", "0", "1", "2", "3", "4", "5", "6",
          "7", "8", "9", "$", "#", "@", "-", "/", "(", ")", "."]

    def clean_text_img(text, unwanted_words, unwanted_punctuation):
       
        for word in unwanted_words:
            text = text.replace(word, "")
        for punc in unwanted_punctuation:
            text = text.replace(punc, "")
        return text.strip()  # Remove leading/trailing whitespace

    # Call for image prompts
    new_img_out = clean_text_img(scripts, uw, up)  # Clean the text
    new_img_lst = new_img_out.splitlines()  # Split into lines for list format

    # Print the list
    
    print(new_img_lst)

    def clean_text_nar(text, unwanted_words, unwanted_punctuation):
        """"Args:
            text: The original text string.
            unwanted_words: List of words to be excluded.
            unwanted_punctuation: List of punctuation characters to be removed.

        Returns:
            The cleaned text string.
        """
        for word in unwanted_words:
            text = text.replace(word, "")
        for punc in unwanted_punctuation:
            text = text.replace(punc, "")
        return text

    # call for narrartors dialogues
    new_nar_out = clean_text_nar(dialoges, uw, up)
    new_nar_list = new_nar_out.splitlines()
    print(new_nar_list)

    # NB: host url is not prepended with \"https\" nor does it have a trailing slash.
    STABILITY_HOST = 'grpc.stability.ai:443'

    # To get your API key, visit https://beta.dreamstudio.ai/membership

    stability_api = client.StabilityInference(
        host=STABILITY_HOST,
        key="Enter Your API key here",
        verbose=True,
    )
    c = 0
    for i in (new_img_lst):
        if len(i) > 15:
            c = c+1
            answers = stability_api.generate(
                prompt=i+",cartoonistic"+"colored",
                seed=121245125,  # if provided, specifying a random seed makes results deterministic
                steps=50,  # defaults to 30 if not specified
            )

            # iterating over the generator produces the api response
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                            "Your request activated the API's safety filters and could not be processed."
                            "Please modify the prompt and try again.")
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img = Image.open(io.BytesIO(artifact.binary))
                        display(img)
                        img.save(fr"ENTER YOUR DIRECTORY ADDRESS\photos\{chr(c+64)}.jpg")
    n = 0
    for i, j in enumerate(new_nar_list):
        #    if i != 0:
        if len(j) > 15:
            n = n+1
            save_audio(j, fr"ENTER YOUR DIRECTORY ADDRESS\audio{chr(n+64)}.mp3")

    folder_path = r"ENTER YOUR DIRECTORY ADDRESS\audios"

    # Get the audio lengths
    audio_lengths = get_audio_lengths(folder_path)
    print(audio_lengths)
    if audio_lengths:
        print("Audio Lengths (in seconds):")
        for i, length in enumerate(audio_lengths):
            # Format to 2 decimal places
            print(f"  - audio{i+1}.mp3: {length:.2f}")
    else:
        print("No audio files found in the folder.")

    # Define paths to image and audio folders
    image_folder = r'ENTER YOUR DIRECTORY ADDRESS\photos'
    audio_folder = r'ENTER YOUR DIRECTORY ADDRESS\audios'

    generate_clips(image_folder, audio_folder, audio_lengths)
    folder_path = r'ENTER YOUR DIRECTORY ADDRESS\output'
    # Replace with your desired output path
    output_path = r'ENTER YOUR DIRECTORY ADDRESS\assets\videos\Output.mp4'
    merge_videos_in_folder(folder_path, output_path)
    # my_story = data['story']  # This will be the story sent from Flutter

    # Rest of your story processing code, generating images and audio

    response = {
        "status": "success",
        "message": "Story processed successfully."
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
