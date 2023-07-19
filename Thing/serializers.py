from rest_framework import serializers
from .models import Thing

class Thingserializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = ('id','owner','desc','name','created_at','updated_at')