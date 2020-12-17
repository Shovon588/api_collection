from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Trim, ClickInfo
from .serializers import TrimSerializer
from .utils import hashing, unhashing

# Create your views here.

BASE_URL = "http://127.0.0.1:8000/trim/"


class TrimLink(APIView):
    serializer_class = TrimSerializer

    def post(self, request):
        serializer = TrimSerializer(data=request.data)

        if serializer.is_valid():
            link = serializer.validated_data.get("link")
            alias = serializer.validated_data.get("alias")

            if alias:
                try:
                    link = Trim.objects.get(code=alias)
                    return Response({"status": "failed",
                                     "message": "Alias not available."},
                                    status=status.HTTP_204_NO_CONTENT)
                except:
                    link_obj = Trim.objects.create(link=link, code=alias)
                    return Response({"status": "success",
                                     "message": "Short link generated with alias.",
                                     "data": {
                                         "hash_code": alias,
                                         "short_link": BASE_URL + alias
                                     }
                                     },
                                    status=status.HTTP_200_OK)

            link_obj = Trim.objects.create(link=link)
            hash_code = hashing(link_obj.id)
            link_obj.code = hash_code
            link_obj.save()

            return Response({"status": "success",
                             "message": "Short link generated with hash code.",
                             "data": {
                                 "hash_code": hash_code,
                                 "short_link": BASE_URL + hash_code
                             }
                             },
                            status=status.HTTP_200_OK)

        return Response({"status": "failed",
                         "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class ClickInfoView(APIView):

    def get(self, request, hashed_code):
        try:
            link_obj = Trim.objects.get(code=hashed_code)
            short_link = BASE_URL + link_obj.code
        except:
            return Response({"status": "failed",
                             "message": "No url present with that code",
                             "code": hashed_code},
                            status=status.HTTP_400_BAD_REQUEST)

        created = link_obj.created_at
        noc = link_obj.noc

        links = ClickInfo.objects.filter(link=link_obj)

        time_band = {
            "0-4": 0,
            "4-8": 0,
            "8-12": 0,
            "12-16": 0,
            "16-20": 0,
            "20-0": 0
        }

        link = None
        for link in links:
            if 0 < link.created_at.hour <= 4:
                time_band["0-4"] += 1
            elif 4 < link.created_at.hour <= 8:
                time_band["4-8"] += 1
            elif 8 < link.created_at.hour <= 12:
                time_band["8-12"] += 1
            elif 12 < link.created_at.hour <= 16:
                time_band["12-16"] += 1
            elif 16 < link.created_at.hour <= 20:
                time_band["16-20"] += 1
            elif 20 < link.created_at.hour <= 24:
                time_band["20-0"] += 1

        frequency = time_band.values()
        if link:
            updated = link.created_at.date()
        else:
            updated = "--:--:--"

        return Response({"status": "success",
                         "message": "Response available for this code.",
                         "data": {
                             "short_link": short_link,
                             "time_band": frequency,
                             "created": created,
                             "updated": updated,
                             "no_of_clicks": noc,
                         }
                         },
                        status=status.HTTP_200_OK)


def handle_short_url(request, hashed_code):
    try:
        link = Trim.objects.get(code=hashed_code)
    except:
        return HttpResponse("<h1 style='text-align: center'>Hmm, That was an odd link.</h1>")

    original_link = link.link
    link.noc += 1
    link.save()

    ClickInfo.objects.create(link=link)

    return redirect(original_link)
