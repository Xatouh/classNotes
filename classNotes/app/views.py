from django.shortcuts import render
from .forms import UploadFileForm
from .transcribe_file import STT
from .resumir import obtenerResumen
from .utils import save
from django.http import HttpResponse
from .models import AudioFile


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file

# Create your views here.
def Home(request):
    return render(request, "home/home.html")

def UploadFile(request):
    
    if request.method == "POST":
        print("Uploading file...")
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']

        folder = "output/"+file.name.split(".")[0] + "/"

        audio = AudioFile.objects.create(file=file)
        fileTitle = str(audio.file)
        text = STT(fileTitle) # procesarConIA()
        save(folder + "transcripcion.txt", text)
        print("Transcripción completada.")
        summary = obtenerResumen(text)
        save(folder + "resumen.txt", summary)
        print("Resumen completado.")
        return HttpResponse(f"Transcripción: {text}\nResumen: {summary}", content_type='text/plain; charset=utf-8')
    else:
        form = UploadFileForm()
    return render(request, "home/home.html", {"form":form})
