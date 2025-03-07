from django.shortcuts import render
from .forms import UploadFileForm
from .processFile import STT
from django.http import HttpResponse


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# Create your views here.
def Home(request):
    return render(request, "home/home.html")

def UploadFile(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        form = request.FILES['file']
        text = STT(request.FILES["file"]) # procesarConIA()
        return HttpResponse(text)
    else:
        form = UploadFileForm()
       
    return render(request, "home/home.html", {"form":form})