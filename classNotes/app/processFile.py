import buzz.transcriber
from openai import OpenAI
import subprocess
import os


def obtenerResumen(message):
    client = OpenAI(api_key='')

    print(message)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
        messages=[
        {"role":"developer","content":[{"type":"text","text":"Eres un experto informático y desarrollador de software, haz un resumen de la siguiente transcripción de una clase de informática:"}]},
        {"role": "user", "content": message}
    ]
    )
    return completion.choices[0].message.content

def STT(audio_file):
    my_env = os.environ.copy()
    my_env["QT_QPA_PLATFORM"] = "offscreen"

    route = "/home/xatou/projects/classNotes/src/Github/classNotes/classNotes/" + audio_file
    command = [
	"QT_QPA_PLATFORM=offscreen","/snap/bin/buzz", "add", 
        "-t", "transcribe", 
        "-l", "es", 
        "-m", "whisper", 
        "-s", "small", 
        "-p", "Transcribe este audio de una clase de informática, el nombre de la clase es métodos numéricos y es una clase introductoria",
        "--txt", 
        route
    ]

    # Set environment variables
    
    print("executing:", " ".join(command))
    # Execute the command
    result = subprocess.run(
        " ".join(command),
	shell=True,
	env=my_env,
	capture_output=True,
	
    )
    
    # Check if command was successful
    print(result)
    return result

