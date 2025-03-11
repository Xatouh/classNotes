from django.shortcuts import render
from .forms import UploadFileForm
from .processFile import run_buzz_command as STT
from django.http import HttpResponse
from .models import AudioFile


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# Create your views here.
def Home(request):
    return render(request, "home/home.html")

def UploadFile(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        audio = AudioFile.objects.create(file=file)
        text = STT(str(audio.file)) # procesarConIA()
        return HttpResponse(text)
    else:
        form = UploadFileForm()
       
    return render(request, "home/home.html", {"form":form})
