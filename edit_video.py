from helper import *
from openai import OpenAI
import whisper_timestamped as whisper
import streamlit as st

def callOpenAI(prompt, transcription):
    client = OpenAI(api_key="sk-x")
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a video editor. You only use scripting to edit videos using moviepy."},
        {"role": "user", "content": f"""
            VideoEditor Class Description
            The VideoEditor class allows you to edit videos using various methods. You can chain these methods to apply multiple edits sequentially. 
            
            Methods:
            trim(start_time, end_time)
            Trims the video to the specified start and end times.
            start_time (float): Start time in seconds.
            end_time (float): End time in seconds.
            
            remove_segment(start_time, end_time)
            Removes a segment of the video between the specified start and end times.
            start_time (float): Start time of the segment to remove (in seconds).
            end_time (float): End time of the segment to remove (in seconds).
            
            add_text(text, font_size=50, color='white', duration=None, position=('center', 'bottom'))
            Adds text to the video at the specified position.
            text (str): The text to add.
            font_size (int, optional): Font size of the text. Defaults to 50.
            color (str, optional): Color of the text. Defaults to 'white'.
            duration (float, optional): Duration of the text in seconds. Defaults to the video duration.
            position (tuple, optional): Position of the text as (horizontal, vertical) alignment. Defaults to ('center', 'bottom').
            
            resize(width=None, height=None)
            Resizes the video to the specified width and height.
            width (int, optional): Width of the resized video. Defaults to None (no resize).
            height (int, optional): Height of the resized video. Defaults to None (no resize).
           
            add_audio(audio_file)
            Adds an audio file to the video.
            audio_file (str): Path to the audio file.
            
            fade_in_out(fade_in_duration=1, fade_out_duration=1)
            Fades in and out the video with the specified durations.
            fade_in_duration (float, optional): Duration of the fade-in in seconds. Defaults to 1.
            fade_out_duration (float, optional): Duration of the fade-out in seconds. Defaults to 1.
            
            rotate(angle)
            Rotates the video by the specified angle.
            angle (int): Rotation angle in degrees.
            
            merge_videos(video_files)
            Merges multiple video files into one.
            video_files (list): List of video file paths to merge.
            
            extract_audio(output)
            Extracts the audio from the video and saves it to the specified output file.
            output (str): Path to the output audio file.
            
            change_speed(speed_factor)
            Changes the playback speed of the video.
            speed_factor (float): Factor by which to change the speed.
            
            adjust_brightness(brightness_factor)
            Adjusts the brightness of the video.
            brightness_factor (float): Factor by which to adjust the brightness.
            
            adjust_contrast(contrast_factor)
            Adjusts the contrast of the video.
            contrast_factor (float): Factor by which to adjust the contrast.
            
            apply_filter(filter_name)
            Applies a visual filter to the video.
            filter_name (str): Name of the filter to apply.
            
            add_transition(type, duration)
            Adds a transition between video segments.
            type (str): Type of transition.
            duration (float): Duration of the transition in seconds.
            
            add_overlay(overlay_file, position=('center', 'top'))
            Adds an image or video overlay.
            overlay_file (str): Path to the overlay file.
            position (tuple, optional): Position of the overlay. Defaults to ('center', 'top').
            
            crop(x, y, width, height)
            Crops the video to the specified region.
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
            width (int): Width of the crop region.
            height (int): Height of the crop region.
            
            adjust_volume(volume_level)
            Adjusts the audio volume.
            volume_level (float): Factor by which to adjust the volume.
            
            add_subtitle(subtitle_file)
            Adds subtitles to the video.
            subtitle_file (str): Path to the subtitle file.
            
            reverse()
            Reverses the playback of the video.
            
            write(output_path)
            Writes the edited video to the specified output path.
            output_path (str): Path to the output video file.
        
        This is the transcription of the video:
        {transcription}
        
        Now, please give code that would execute this prompt (python) using the class described: {prompt}. Only give me the code that ONLY execute what is needed for this prompt. 
        Don't format it. Return everything in 1 line. Chain directly, don't make any variable.
        Only use functions that I described, DO NOT execute any other code that does not relate to the prompt or edit the video.
        Example:
        VideoEditor("input.mp4").remove_segment(0, 5).add_text("Hello, World!", position=('center', 'bottom')).write("output.mp4")
        """},
    ]
    )
    return response.choices[0].message.content

def transcribe():
    video = VideoFileClip("input.mp4")
    audio = video.audio
    audio.write_audiofile("audio.mp3")

    audio = whisper.load_audio("audio.mp3")
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, language="en")

    words_with_timestamps = []
    for segment in result['segments']:
        for word in segment['words']:
            words_with_timestamps.append([
                word['text'],
                word['start'],
                word['end']
            ])
    return words_with_timestamps

st.title("AI Video Editor")
st.info("Edit your video using prompts.")
video = st.file_uploader("Upload your video", type=["mp4"])
if video is not None:
    with open("input.mp4", "wb") as f:
        f.write(video.getbuffer())
    st.video("input.mp4")
    
prompt = st.text_input(label="Your prompt")

if st.button("Edit Video"):
    transcription = transcribe()
    st.text(transcription)
    code = callOpenAI(prompt, transcription)
    st.text(code)
    eval(code)
    st.video("output.mp4")


