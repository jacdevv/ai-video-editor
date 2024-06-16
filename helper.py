from moviepy.editor import *

class VideoEditor:
    def __init__(self, file_path):
        self.video = VideoFileClip(file_path)
        self.edited_video = self.video

    def trim(self, start_time, end_time):
        self.video = self.video.subclip(start_time, end_time)
        return self

    def remove_segment(self, start_time, end_time):
        clip1 = self.video.subclip(0, start_time)
        clip2 = self.video.subclip(end_time, self.video.duration)
        self.video = concatenate_videoclips([clip1, clip2])
        return self

    def add_text(self, text, font_size=50, color='white', duration=None, position=('center', 'bottom')):
        txt_clip = TextClip(text, fontsize=font_size, color=color, bg_color='transparent')
        txt_clip = txt_clip.set_position(position).set_duration(duration or self.video.duration)
        self.video = CompositeVideoClip([self.video or self.video, txt_clip])
        return self

    def resize(self, width=None, height=None):
        self.video = self.video or self.video
        self.video = self.video.resize(width=width, height=height)
        return self

    def add_audio(self, audio_file):
        audio = AudioFileClip(audio_file)
        self.video = self.video or self.video
        self.video = self.video.set_audio(audio)
        return self

    def fade_in_out(self, fade_in_duration=1, fade_out_duration=1):
        self.video = self.video or self.video
        self.video = self.video.fadein(fade_in_duration).fadeout(fade_out_duration)
        return self

    def rotate(self, angle):
        self.video = self.video or self.video
        self.video = self.video.rotate(angle)
        return self

    def merge_videos(self, video_files):
        clips = [VideoFileClip(file) for file in video_files]
        self.video = concatenate_videoclips([self.video or self.video] + clips)
        return self

    def extract_audio(self, output):
        audio = self.video.audio if self.video else self.video.audio
        audio.write_audiofile(output)
        return self

    def change_speed(self, speed_factor):
        self.video = self.video or self.video
        self.video = self.video.fx(vfx.speedx, speed_factor)
        return self

    def adjust_brightness(self, brightness_factor):
        self.video = self.video or self.video
        self.video = self.video.fx(vfx.colorx, brightness_factor)
        return self

    def adjust_contrast(self, contrast_factor):
        self.video = self.video or self.video
        self.video = self.video.fx(vfx.lum_contrast, contrast_factor)
        return self

    # def apply_filter(self, filter_name):
    #     Implement later
    def add_transition(self, type, duration):
        # This is a placeholder implementation, real implementation depends on transition type
        self.video = self.video or self.video
        transition_clip = self.video.crossfadein(duration)
        self.video = concatenate_videoclips([transition_clip, self.video])
        return self

    def add_overlay(self, overlay_file, position=('center', 'top')):
        overlay_clip = VideoFileClip(overlay_file).set_position(position)
        self.video = CompositeVideoClip([self.video or self.video, overlay_clip])
        return self

    def crop(self, x, y, width, height):
        self.video = self.video or self.video
        self.video = self.video.crop(x1=x, y1=y, x2=x+width, y2=y+height)
        return self

    def adjust_volume(self, volume_level):
        self.video = self.video or self.video
        self.video = self.video.volumex(volume_level)
        return self

    # def add_subtitle(self, subtitle_file):
    #     # Use whisper here, implement later

    def reverse(self):
        self.video = self.video or self.video
        self.video = self.video.fx(vfx.time_mirror)
        return self

    def write(self, output_path):
        self.video = self.video or self.video
        self.video.write_videofile(output_path)