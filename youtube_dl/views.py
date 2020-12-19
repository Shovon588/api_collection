from pytube import YouTube
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import YoutubeDLSerializer
from .utils import make_time, make_size


class YoutubeDL(APIView):
    serializer_class = YoutubeDLSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data.get("url")

            try:
                file = YouTube(url)
            except:
                return Response({
                    "status": "failed",
                    "message": "Invalid url",
                }, status=status.HTTP_404_NOT_FOUND)

            videos = file.streams

            thumbnail = file.thumbnail_url
            title = file.title
            duration = make_time(file.length)

            video_res = {
                "1080p": None,
                "720p": None,
                "480p": None,
                "360p": None,
                "240p": None,
                "144p": None
            }

            aud_size = 0
            audio = None
            for video in videos:
                if video.resolution in video_res and video_res[video.resolution] is None:
                    video_res[video.resolution] = {"resolution": video.resolution, "video_type": video.subtype,
                                                   "size": make_size(video.filesize),
                                                   "url": video.url}
                if video.type == "audio":
                    if video.filesize > aud_size:
                        audio = video
                        aud_size = video.filesize

            video_data = [value for key, value in video_res.items() if value is not None]

            audio_data = None
            if audio is not None:
                audio_type = audio.subtype
                size = make_size(audio.filesize)
                url = audio.url
                audio_data = {"audio_type": audio_type, "size": size, "url": url}

            return Response({
                "status": "success",
                "message": "Got some data.",
                "title": title,
                "duration": duration,
                "thumbnail": thumbnail,
                "video_data": video_data,
            }, status=status.HTTP_200_OK)

        return Response({"status": "failed",
                         "message": "Something went wrong.",
                         "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
