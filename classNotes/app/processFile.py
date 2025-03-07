import buzz.transcriber
from openai import OpenAI
import subprocess



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
    result = subprocess.run(["python","--version"], capture_output=True)
    print(result)

    command = [
        "python", "-m", "buzz", "add", 
        "-t", "transcribe", 
        "-l", "es", 
        "-m", "whisper", 
        "-s", "small", 
        "-p", "Transcribe este audio de una clase de informática, el nombre de la clase es métodos numéricos y es una clase introductoria",
        "--txt", 
        audio_file
    ]

    # Set environment variables
    env = {"QT_QPA_PLATFORM": "offscreen"}

    # Execute the command
    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True
    )

    # Check if command was successful
    if result.returncode == 0:
        print("Command executed successfully")
        print("Output:", result.stdout)
    else:
        print("Command failed")
        print("Error:", result.stderr)

    return result

