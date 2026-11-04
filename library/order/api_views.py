from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser
from authentication.permissions import IsLibrarian
from .models import Order
from .serializer import OrderSerializer, UserOrderSerializer


class OrderAPIView(APIView):
    permission_classes = [IsLibrarian]

    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserOrderAPIView(APIView):
    permission_classes = [IsLibrarian]

    def get(self, request, user_id, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk, user_id=user_id)
            serializer = UserOrderSerializer(order)
        else:
            orders = Order.objects.filter(user_id=user_id)
            serializer = UserOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, pk=None):
        user = get_object_or_404(CustomUser, pk=user_id)
        serializer = UserOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id, pk=None):
        order = get_object_or_404(Order, pk=pk, user_id=user_id)
        serializer = UserOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id, pk=None):
        order = get_object_or_404(Order, pk=pk, user_id=user_id)
        serializer = UserOrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, pk=None):
        order = get_object_or_404(Order, pk=pk, user_id=user_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
