from django.shortcuts import render
from django.http.response import JsonResponse
from .serializers import CountriesSerializers
from .models import Countries
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET','POST'])
def countrieslist(request):
    if request.method == 'GET':
        countries=Countries.objects.all()
        name=request.GET.get('name',None)
        if name is not None:
            countries=countries.filter(name__icontains=name)
        countries_serilalizers=CountriesSerializers(countries,many=True)
        return JsonResponse(countries_serilalizers.data,safe=False)
        
    elif request.method == 'POST':
        countries_data=JSONParser().parse(request)
        countries_serilalizers=CountriesSerializers(data=countries_data)
        if countries_serilalizers.is_valid():
            countries_serilalizers.save()
            return JsonResponse(countries_serilalizers.data,status=status.HTTP_201_CREATED)
        return JsonResponse(countries_serilalizers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def countries_details(request,pk):
    try:
        countries=Countries.objects.get(pk=pk)
    except Countries.DoesNotEXist:
        return JsonResponse({'message':'the counries does not exist'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        countries_serializers=CountriesSerializers(countries)
        return JsonResponse(countries_serializers.data)

    elif request.method == 'PUT':
         countries_data=JSONParser().parse(request)
         countries_serializers=CountriesSerializers(countries,countries_data)
         if countries_serializers.is_valid():
             countries_serializers.save()
             return JsonResponse(countries_serializers.data)
         return JsonResponse(countries_serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        countries.delete()
        return JsonResponse({'message':'you have successfully deleted the data'},status=status.HTTP_204_NO_CONTENT)