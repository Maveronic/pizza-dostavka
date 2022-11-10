from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import OrderCreationSerializer, OrderDetailSerializer, OrderStatusUpdateSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class OrderCreateListView(GenericAPIView):
    serializer_class = OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(operation_summary='List all pizza orders made')
    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary='Create a new pizza order')
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(GenericAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_summary='Retrieve a pizza order by id')
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary='Update an order by id')
    def put(self, request, order_id):
        data = request.data
        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(data=data, instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary='Remove/delete an order')
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateOrderStatusView(GenericAPIView):
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_summary='Update an order status')
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        data = request.data

        serializer = self.serializer_class(data=data, instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(GenericAPIView):
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(operation_summary='Get all orders for a user')
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        orders = Order.objects.all().filter(customer=user)

        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserOrderDetail(GenericAPIView):
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(operation_summary="Get a user's specific order")
    def get(self, request, user_id, order_id):
        user = User.objects.all().get(pk=user_id)
        order = Order.objects.all().filter(customer=user).get(pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
