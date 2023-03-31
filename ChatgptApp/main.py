import openai  # pip install openai
import typer  # pip install "typer[all]"
from rich import print  # pip install rich
from rich.table import Table
import config
import docx

"""
Webs de interés:
- Módulo OpenAI: https://github.com/openai/openai-python
- Documentación API ChatGPT: https://platform.openai.com/docs/api-reference/chat
- Typer: https://typer.tiangolo.com
- Rich: https://rich.readthedocs.io/en/stable/
"""

def main():

    openai.api_key = config.api_key

    print("💬 [bold green]ChatGPT API en Python[/bold green]")

    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("new", "Crear una nueva conversación")

    print(table)

    # Contexto del asistente
    context = {"role": "system",
               "content": "Eres un escritor de ensayos acerca de obras literarias muy útil."}
    messages = [context]

    request = 1

    while True:

        content = __prompt()

        if content == "new":
            print("🆕 Nueva conversación creada")
            messages = [context]
            content = __prompt()

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})

        #print(f"[bold green]> [/bold green] [green]{response_content}[/green]")
        
        doc = docx.Document()
        
        doc.add_paragraph(response_content)

        doc.save(str(content)+str(request)+'.docx')

        print("✅ ¡Ensayo guardado!")

        print(request)

        request += 1

def __prompt() -> str:
    prompt = typer.prompt("\n¿Qué obra literaria requieres? ")

    if prompt == "exit":
        exit = typer.confirm("✋ ¿Estás seguro?")
        if exit:
            print("👋 ¡Hasta luego!")
            raise typer.Abort()
        
        return __prompt()

    return prompt


if __name__ == "__main__":
    typer.run(main)