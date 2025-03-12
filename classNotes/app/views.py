from django.shortcuts import render
from .forms import UploadFileForm
from .processFile import STT
from django.http import HttpResponse
from .models import AudioFile


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# Create your views here.
def Home(request):
    return render(request, "home/home.html")

def UploadFile(request):
    folder = "input/"
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        audio = AudioFile.objects.create(file=file)
	fileTitle = audio.file
        text = STT(str(folder + audio.file)) # procesarConIA()
        transcription = fileTitle + "_transcription"
	return HttpResponse(text['stderr'])
    else:
        form = UploadFileForm()
       
    return render(request, "home/home.html", {"form":form})
