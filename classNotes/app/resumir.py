import os
from openai import OpenAI
import sys

msg1 = "Eres un profesional del mundo de la informática con un alto nivel de conocimiento, donde luego de un gran recorrido profesional, decides ser un docente que hace clases individuales a alumnos. Haz un resumen de la siguiente transcripción de una clase, destaca los puntos mas importantes, desarrollalos haciendo un resumen extenso e incluye información relevante adicional que contribuyan a comprender mejor cada uno de los temas tratados en la transcripción. Incluye citas de lo que se dice en la clase. No te limites en cantidad de palabras y detalles, que no se te escapen ningúno de ellos. Asegurate de que si, se nombre alguna tarea que se deba realizar o encargo general que de el profesor, indicarlo en el resumen. No inventes cosas de las cuáles no se encuentran en la transcripción. Utiliza Markdown"
msg2 = "Eres un profesional del área informática con experiencia en metodologías ágiles y en la docencia individual. A partir de la siguiente transcripción de una reunión, elabora una minuta breve y precisa. Resume lo conversado usando viñetas claras y concisas.Usa expresiones como: Se acordó..., Se decidió..., Se conversó acerca de..., entre otras similares. Si hay frases relevantes en la reunión, inclúyelas entre comillas como citas. Si se asignan tareas o responsabilidades, enuméralas al final bajo un subtítulo 'Tareas asignadas'. No inventes información que no aparezca explícitamente en la transcripción. El resultado debe estar en formato Markdown, claro y directo."

def obtenerResumen(message):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
        "role": "user",
        "content": [
            {
            "type": "input_text",
            "text": message
            }
        ]
        },
        {
        "role": "system",
        "content": [
            {
            "type": "input_text",
            "text": msg1
            }
        ]
        },
        
    ],
    text={
        "format": {
        "type": "text"
        }
    },
    reasoning={},
    tools=[
        {
        "type": "web_search_preview",
        "user_location": {
            "type": "approximate",
            "country": "CL",
            "region": "Metropolitana",
            "city": "Santiago de Chile"
        },
        "search_context_size": "low"
        }
    ],
    tool_choice="auto",
    temperature=1,
    max_output_tokens=10405,
    top_p=1,
    store=True
    )


    results = procesar_respuesta(response)
    return results

def procesar_respuesta(response):
        # Buscar el primer mensaje de tipo 'message' con contenido
    for item in response.output:
        if item.type == 'message' and hasattr(item, 'content'):
            for content_piece in item.content:
                if hasattr(content_piece, 'text'):
                    texto = content_piece.text
                    
                    # Opcional: si deseas añadir los enlaces por separado al final
                    enlaces = []
                    if hasattr(content_piece, 'annotations'):
                        for annotation in content_piece.annotations:
                            if annotation.type == 'url_citation':
                                enlaces.append(f"- [{annotation.title}]({annotation.url})")

                    markdown = f"""\
                        ## 📄 Resumen de la respuesta

                        {texto}

                        ---

                        ### 🔗 Enlaces citados:
                        {chr(10).join(enlaces)}
                        """
                    return markdown

    return "⚠️ No se encontró contenido en la respuesta."



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python resumir.py <archivo_de_audio>")
        sys.exit(1)
    else:
        message = open(sys.argv[1], "r", encoding="utf-8").read()
        resumen = obtenerResumen(message)
        print(resumen)

