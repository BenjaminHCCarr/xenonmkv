import os

from xenonmkv.utils.process_handler import ProcessHandler


class FFMpeg():
    video_path = audio_path = video_fps = video_pixel_ar = ""

    args = log = None

    def __init__(self, video_path, audio_path, video_fps,
                 video_pixel_ar, args, log):
        self.video_path = video_path
        self.audio_path = audio_path
        self.video_fps = str(video_fps)
        self.video_pixel_ar = video_pixel_ar
        self.args = args
        self.log = log

    def package(self):
        prev_dir = os.getcwd()
        os.chdir(self.args.scratch_dir)

        # Make sure there is no 'output.mp4' in the scratch directory
        # FFMpeg has a tendency to add tracks
        output_file = os.path.join(os.getcwd(), self.args.name + ".mp4")
        if os.path.isfile(output_file):
            os.unlink(output_file)

        cmd = [self.args.tool_paths["mp4box"], "output.mp4",
               # Always create new file with mp4box/GPAC
               "-add", self.video_path, "-fps", self.video_fps,
               "-par", "1=" + self.video_pixel_ar,
               "-add", self.audio_path, "-tmp", self.args.scratch_dir,
               "-new",
               "-itags", "name=" + self.args.name]

        ph = ProcessHandler(self.args, self.log)
        process = ph.start_output(cmd)

        if process != 0:
            # Destroy temporary file
            # so it does not have multiple tracks imported
            os.unlink(output_file)
            self.log.warning("An error occurred while creating "
                             "an MP4 file with FFMpeg")
            # Continue retrying to create the file

        self.log.debug("FFMpeg process complete")

        # When complete, change back to original directory
        os.chdir(prev_dir)
