from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Trim
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
            link_obj = Trim.objects.create(link=link)
            hash_code = hashing(link_obj.id)
            link_obj.code = hash_code
            link_obj.save()

            return Response({"status": "success",
                             "message": "Hash code generated",
                             "data": {
                                 "hash_code": hash_code,
                                 "short_link": BASE_URL + hash_code
                             }
                             },
                            status=status.HTTP_200_OK)

        return Response({"status": "failed",
                         "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


def handle_short_url(request, hashed_code):
    obj_id = unhashing(hashed_code)
    link = Trim.objects.get(id=obj_id)
    original_link = link.link

    return redirect(original_link)
