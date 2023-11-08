from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from .models import Opportunity
from .forms import OpportunityForm
from .serializers import OpportunitySerializer 
from rest_framework import viewsets, status
from rest_framework.views import APIView
import requests

API_BASE_URL = 'http://localhost:8000/api/'
# Create your views here.

def opportunity_create_view(request):
    opportunity = None

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        
        if form.is_valid():
            if 'submit' in request.POST:
                create_opportunity(form.cleaned_data)
                print("called submit")
                form = OpportunityForm()
            elif 'rewrite' in request.POST:
                opportunity=form.instance
                opportunity.description=opportunity.rewrite_me()
                opportunity.tags=opportunity.get_tags()
                opportunity.save()
                print(opportunity)
                form = OpportunityForm(instance=opportunity)
    else:
        form = OpportunityForm()

    return render(request, 'opportunity_create.html', {'form': form, 'opportunity': opportunity})

#helper functions for api views
def create_opportunity(data):
    url=API_BASE_URL+'opportunity/'
    response = requests.post(url,data)

#api views
class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

class apiOpportunityCreateView(APIView):
    def post(self,request):
        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OpportunityRewriteView(APIView):
    def post(self,request,pk):
        opportunity = Opportunity.objects.get(pk=pk)
        opportunity.description=opportunity.rewrite_me()  
        opportunity.save()
        serializer = OpportunitySerializer(opportunity)
        return Response(serializer.data,status=status.HTTP_200_OK)