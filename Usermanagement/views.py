from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Usermanagement import serializers as user_management_serializer
from lib.constant import STATUS, MESSAGE, DATA


class UserCreateApi(APIView):
    serializer_class = user_management_serializer.UserSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                MESSAGE: "success",
                DATA: {},
                STATUS: status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)
        return Response({
            MESSAGE: serializer.errors,
            DATA: {},
            STATUS: status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)