from rest_framework import serializers
from .models import Instruments, Order


class InstrumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Instruments
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
