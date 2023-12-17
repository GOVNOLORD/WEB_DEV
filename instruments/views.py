from django.contrib.auth import authenticate
from django.views import View
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from .models import Instruments, Order
from .serializers import InstrumentSerializers, OrderSerializers, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer
from .permissions import IsAdmin


class LoginView(APIView):
    def post(self, reqest, *args, **kwargs):
        username = reqest.data.get('username')
        password = reqest.data.get('password')
        user = authenticate(reqest, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InstrumentListCreateView(generics.ListCreateAPIView):
    queryset = Instruments.objects.all()
    serializer_class = InstrumentSerializers
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get the list of instruments",
        responses={200: InstrumentSerializers(many=True).data},
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
        responses={200: OrderSerializers(many=True).data},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create new orders",
        request_body=OrderSerializers,
        responses={201: OrderSerializers()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class InstrumentListView(APIView):
    @swagger_auto_schema(
        operation_description="Get the list of instruments",
        responses={200: InstrumentSerializers(many=True).data},
    )
    def get(self, request):
        instruments = Instruments.objects.all()
        serializer = InstrumentSerializers(instruments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new instrument",
        request_body=InstrumentSerializers,
        responses={201: InstrumentSerializers()},
    )
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
        instrument = get_object_or_404(Instruments, pk=pk)
        serializer = InstrumentSerializers(instrument)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update details of a specific instrument",
        request_body=InstrumentSerializers,
        responses={200: InstrumentSerializers()},
    )
    def put(self, request, pk):
        instrument = get_object_or_404(Instruments, pk=pk)
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
        instrument = get_object_or_404(Instruments, pk=pk)
        instrument.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListView(APIView):
    @swagger_auto_schema(
        operation_description="Get the list of orders",
        responses={200: OrderSerializers(many=True).data},
    )
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializers(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new order",
        request_body=OrderSerializers,
        responses={201: OrderSerializers()},
    )
    def post(self, request):
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get details of a specific order",
        responses={200: OrderSerializers()},
    )
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializers(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update details of a specific order",
        request_body=OrderSerializers,
        responses={200: OrderSerializers()},
    )
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializers(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific order",
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomAuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        if request.user.is_stuff:
            return Response({'message': 'This is admin view'})
        else:
            return Response({'massage': 'Permission denied '}, status=403)
