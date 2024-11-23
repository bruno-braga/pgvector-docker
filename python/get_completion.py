import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_completion(prompt, system_prompt, model="gpt-4o-mini", json_format=False):
    """
    Obtém uma resposta do modelo de linguagem usando a API OpenAI.

    Args:
        prompt (str): O prompt principal a ser enviado ao modelo
        system_prompt (str): O prompt de sistema que define o comportamento do modelo
        model (str, optional): Nome do modelo a ser usado. Padrão é "gpt-4o-mini"
        json_format (bool, optional): Se True, força a resposta em formato JSON. Padrão é False

    Returns:
        str: A resposta gerada pelo modelo
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
        max_tokens=500,
        response_format={"type": "json_object"} if json_format else None
    )
    
    return response.choices[0].message.content