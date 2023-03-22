from django.shortcuts import render
from .models import vaction

# Create your views here.
def index(request):

    table = vaction.objects.all()

    return render(request, 'table/index.html',{"tables": table})

