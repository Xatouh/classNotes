import buzz.transcriber
from openai import OpenAI
import subprocess
import os
import time

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

def run_buzz_command(audio_file):
    # Command exactly as you would type it in the terminal
    
    command_str = f"QT_QPA_PLATFORM=offscreen python -m buzz add -t transcribe -l es -m whisper -s large-v3-turbo -p \"Transcribe este audio de una clase de informática, el nombre de la clase es métodos numéricos y es una clase introductoria\" --txt {audio_file}"
    print("Executing command:", command_str)
    # Execute directly as you would in terminal, with shell=True
    process = subprocess.Popen(
        command_str,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=os.setsid  # Use a new process group
    )
    
    try:
        # Wait for the command to complete
        stdout, stderr = process.communicate(timeout=1800)  # 20 minutes timeout
        
        # Check if there's an output file that was created
        # You might need to add logic here to find and read the output file
        
        return {
            "returncode": process.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "success": process.returncode == 0
        }
    except subprocess.TimeoutExpired:
        # Kill the process group if it times out
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": "Process timed out",
            "success": False
        }

def STT(audio_file):
    print("Starting transcription of", audio_file)
    start_time = time.time()
    
    result = run_buzz_command(audio_file)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"Process took {elapsed:.2f} seconds")
    
    if result["success"]:
        print("Command executed successfully")
        if result["stdout"]:
            print("Output:", result["stdout"])
        else:
            print("No stdout output, check for output files")
    else:
        print("Command failed")
        print("Error:", result["stderr"])
    
    return result
