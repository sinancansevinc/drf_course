from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ContactSerializer
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from .models import Contact
# Create your views here.


class ContactApiView(views.APIView):
    """Simple Api view for Contact entiries
    """
    serializer_class = ContactSerializer

    # Returns a dictionary containing any extra context that should be supplied to the serializer.
    # Defaults to including request , format , view

    # def get_serializer_context(self):
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }

    # #returns serializer instance
    # def get_serializer(self,*args,**kwargs):
    #     kwargs['context'] = self.get_serializer_context()
    #     return self.serializer_class(*args, **kwargs)
    
    def get(self, request, format=None):
        print(Contact.objects.count())
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        try:
            data = request.data
            serializer = ContactSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status = status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)
