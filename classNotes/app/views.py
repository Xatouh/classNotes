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
        print("Uploading files...")
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')  # Get all uploaded files
        model = request.POST['model']
        preprocess = request.POST['preprocess'] == 'on'
        language = request.POST['language']

        print("files:", files, "modelo:", model, "preprocesado:", preprocess, "lenguaje:", language)

        results = []
        for file in files:
            audio = AudioFile.objects.create(file=file, language=language, preprocess=preprocess, model=model)
            fileTitle = str(audio.file)
            filePreprocess = audio.preprocess
            fileLanguage = audio.language
            fileModel = audio.model

            print("Procesando archivo:", fileTitle)
            text = STT(fileTitle, preprocess=filePreprocess, model=fileModel, language=fileLanguage)
            folder = "output/" + file.name.split(".")[0] + "/"
            save(folder + "transcripcion.txt", text)
            print("Transcripción completada para:", fileTitle)

            summary = obtenerResumen(text)
            save(folder + "resumen.txt", summary)
            print("Resumen completado para:", fileTitle)

            results.append({"file": fileTitle, "transcription": text, "summary": summary})

        return HttpResponse(f"Resultados: {results}", content_type='text/plain; charset=utf-8')
    else:
        form = UploadFileForm()
    return render(request, "home/home.html", {"form": form})
