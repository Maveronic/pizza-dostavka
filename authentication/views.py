from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . import serializers
from drf_yasg.utils import swagger_auto_schema


class UserCreateView(GenericAPIView):
    serializer_class = serializers.UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create a user account")
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
