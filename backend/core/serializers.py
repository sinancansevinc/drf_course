from . import models
from rest_framework import serializers
from rest_framework import fields

class ContactSerializer(serializers.ModelSerializer):
    name = fields.CharField(source="title",required=True)
    message = fields.CharField(source="description",required=True)
    email = fields.EmailField(required=True)
    
    class Meta:
        model = models.Contact
        fields=['name','email','message']