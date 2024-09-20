from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip
from mutagen.mp3 import MP3
import os
from gtts import gTTS
import os
import shutil
# Text to convert to speech


def empty_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate over the files and directories in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # If it's a file, remove it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # If it's a directory, remove it and all its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        print(f"The folder {folder_path} does not exist.")


def save_audio(speech, out):
    # Language (optional, defaults to 'en')
    language = 'en'
    # Save as MP3 file
    # Create the gTTS object
    tts = gTTS(text=speech, lang=language)
    # Save the audio to a file
    tts.save(out)
    print(f"Audio saved ")


def get_audio_lengths(folder_path):
    """
    This function fetches the lengths of all audio files in a folder.

    Args:
        folder_path: The path to the folder containing the audio files.
`
    Returns:
        A list containing the lengths (in seconds) of all audio files in the folder.
    """
    audio_lengths = []
    c = 1
    for filename in os.listdir(folder_path):
        # Check if it's an MP3 file
        print(filename)
        if filename.endswith(f"audio{chr(c+64)}.mp3"):
            filepath = os.path.join(folder_path, filename)
            try:
                audio = MP3(filepath)
                # Get audio length in seconds
                length = audio.info.length
                audio_lengths.append(length)
            except (IOError, EOFError):
                print(f"Error processing file: {filename}")
        c = c+1
    return audio_lengths


# Specify the folder path (replace with your actual path)


# List of audio lengths in seconds
# Replace with your actual audio lengths
def generate_clips(image_folder, audio_folder, audio_lengths):

    # Get sorted list of image and audio files
    image_files = sorted([f for f in os.listdir(image_folder)
                          if f.lower().endswith(('png', 'jpg', 'jpeg'))])
    audio_files = sorted([f for f in os.listdir(audio_folder)
                          if f.lower().endswith(('mp3', 'wav'))])

    # Ensure the number of images and audio files match the length of audio_lengths
    assert len(image_files) == len(audio_files) == len(
        audio_lengths), "Mismatch in number of files or lengths"

    # Output folder for videos
    output_folder = 'ENTER YOUR DIRECTORY ADDRESS\output'
    os.makedirs(output_folder, exist_ok=True)

    # Process each image and audio file
    for i, (image_file, audio_file, duration) in enumerate(zip(image_files, audio_files, audio_lengths)):
        print("++\n"+image_file+audio_file+str(duration)+"\n++")
        # Create the image clip
        image_path = os.path.join(image_folder, image_file)
        image_clip = ImageClip(image_path, duration=duration)

        # Create the audio clip
        audio_path = os.path.join(audio_folder, audio_file)
        audio_clip = AudioFileClip(audio_path).set_duration(duration)

        # Set audio to the image clip
        video_clip = image_clip.set_audio(audio_clip)

        # Save the video
        output_path = os.path.join(output_folder, f'video_{i+1}.mp4')
        video_clip.write_videofile(output_path, codec='libx264', fps=24)

        # Close clips to free resources
        image_clip.close()
        audio_clip.close()
        video_clip.close()

        print("All videos have been created successfully.")


def merge_videos_in_folder(folder_path, output_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out video files (you can add more video formats if needed)
    video_files = [f for f in files if f.endswith(('.mp4'))]

    # Sort video files by name (optional, in case you want to merge in alphabetical order)
    video_files.sort()

    # Load video clips
    clips = []
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        clip = VideoFileClip(video_path)
        clips.append(clip)

    # Concatenate video clips
    final_clip = concatenate_videoclips(clips)

    # Write the result to a file
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')



