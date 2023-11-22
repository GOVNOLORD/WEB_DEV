from rest_framework import generics
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

from .models import Instruments, Order
from .serializers import InstrumentSerializers, OrderSerializers


class InstrumentListCreateView(generics.ListCreateAPIView):
    queryset = Instruments.objects.all()
    serializer_class = InstrumentSerializers

    @swagger_auto_schema(
        operation_description="Get the list of instruments",
        responses={200: InstrumentSerializers(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new instrument",
        request_body=InstrumentSerializers,
        responses={201: InstrumentSerializers()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    @swagger_auto_schema(
        operation_description="Get the list of orders",
        responses={200: OrderSerializers(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new orders",
        request_body=OrderSerializers,
        responses={201: OrderSerializers()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class InstrumentListView(APIView):
    def get(self, request):
        instruments = Instruments.objects.all()
        serializer = InstrumentSerializers(instruments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InstrumentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstrumentDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get details of a specific instrument",
        responses={200: InstrumentSerializers()},
    )
    def get(self, request, pk):
        instrument = generics.get_object_or_404(Instruments, pk=pk)
        serializer = InstrumentSerializers(instrument)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update details of a specific instrument",
        request_body=InstrumentSerializers,
        responses={200: InstrumentSerializers()},
    )
    def put(self, request, pk):
        instrument = generics.get_object_or_404(Instruments, pk=pk)
        serializer = InstrumentSerializers(instrument, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific instrument",
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        instrument = generics.get_object_or_404(Instruments, pk=pk)
        instrument.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializers(orders, many=True)
        return Response({'error: Order not found'}, serializer.data)

    def post(self, request):
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get details of a specific orders",
        responses={200: OrderSerializers()},
    )
    def get(self, request, pk):
        orders = generics.get_object_or_404(Order, pk=pk)
        serializer = OrderSerializers(orders)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update details of a specific orders",
        request_body=OrderSerializers,
        responses={200: OrderSerializers()},
    )
    def put(self, request, pk):
        orders = generics.get_object_or_404(Order, pk=pk)
        serializer = OrderSerializers(orders, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific orders",
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        orders = generics.get_object_or_404(Order, pk=pk)
        orders.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
