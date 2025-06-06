from openai import OpenAI
import sys

def obtenerResumen(message):
    client = OpenAI(api_key='')

    print(message)

    completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
        messages=[
        {"role":"developer","content":[{"type":"text","text":"Eres un profesional del mundo de la informática con un alto nivel de conocimiento. Haz un resumen de la siguiente transcripción de una clase, destaca los puntos mas importantes y desarrollalos haciendo un resumen extenso. Incluye citas de lo que se dice en la reunión. No te limites en cantidad de palabras y detalles, que no se te escapen ningúno de ellos. Asegurate de que si, se nombre alguna tarea que se deba realizar o encargo general que de el profesor, indicarlo en el resumen. No inventes cosas de las cuáles no se encuentran en la transcripción. Utiliza Markdown"}]},
        {"role": "user", "content": message}
    ]
    )

    results = completion.choices[0].message.content
    return results

        
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Uso: python resumir.py <archivo_de_audio>")
#         sys.exit(1)
#     else:
#         message = open(sys.argv[1], "r", encoding="utf-8").read()
#         resumen = obtenerResumen(message)
#         print(resumen)