import av
import cv2
import numpy as np
from wutil import Size


def video_writer(out_p: str, fps: float, vid_width: int, vid_height: int) -> cv2.VideoWriter:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    return cv2.VideoWriter(out_p, fourcc, fps, (vid_width, vid_height))


def video_writer_from_cap(cap: cv2.VideoCapture, out_p: str) -> cv2.VideoWriter:
    fps = cap.get(cv2.CAP_PROP_FPS)

    vid_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return video_writer(out_p, fps, vid_width, vid_height)


class AvVideoWriter:
    '''
    PyAV videowriter based on sample https://pyav.org/docs/develop/cookbook/numpy.html#generating-video

    Encodes video with h264 codec, follows interface similar to OpenCV VideoWriter.
    '''

    def __init__(
        self,
        out_p: str,
        size: Size,
        fps: float
    ):
        self.container = av.open(out_p, mode='w')

        self.stream = self.container.add_stream('h264', rate=fps)
        self.stream.width = size.w
        self.stream.height = size.h
        self.stream.pix_fmt = 'yuv420p'
        self.container.streams.video[0].thread_type = 'AUTO'

    def write(self, img: np.ndarray):
        frame = av.VideoFrame.from_ndarray(img, format='rgb24')
        for packet in self.stream.encode(frame):
            self.container.mux(packet)

    def release(self):
        # Flush stream
        for packet in self.stream.encode():
            self.container.mux(packet)

        # Close the file
        self.container.close()
