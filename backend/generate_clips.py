from moviepy.editor import AudioFileClip, ImageClip


import os


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
    output_folder = 'C:\miniproject\output'
    os.makedirs(output_folder, exist_ok=True)

    # Process each image and audio file
    for i, (image_file, audio_file, duration) in enumerate(zip(image_files, audio_files, audio_lengths)):
        print("++\n"+image_file+audio_file+duration+"\n++")
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
