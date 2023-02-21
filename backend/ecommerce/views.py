from django.shortcuts import render
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Item,Order
from .serializers import ItemSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from json import JSONDecodeError
from django.http import JsonResponse
from django.contrib.auth.models import User
# Create your views here.

class ItemViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_class = (IsAuthenticatedOrReadOnly)
    
    
class OrderViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin, 
        GenericViewSet
        ):
    """
    A simple ViewSet for listing, retrieving and creating orders.
    """
    permission_classes = ()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        print(self.request)
        user = self.request.user
        return Order.objects.filter(user=user.id)
    
    def create(self,request):
        try:
            user = User.objects.first()
            data = self.request.data
            print(data)
            serializer = OrderSerializer(data = data)
            if serializer.is_valid():
                item = Item.objects.get(pk=data["item"])
                order = item.place_order(user,data["quantity"])
                return Response(OrderSerializer(order).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)