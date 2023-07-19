from django.shortcuts import render
from rest_framework import generics
from .models import Thing
from .serializers import Thingserializer
from .permissions import IsOwnerOrReadOnly

# ListAPIView
class Thing_list(generics.ListCreateAPIView):
    queryset = Thing.objects.all()
    serializer_class = Thingserializer

# RetrieveAPIView
class Thing_detail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Thing.objects.all()
    serializer_class = Thingserializer