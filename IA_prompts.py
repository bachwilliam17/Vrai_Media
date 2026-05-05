from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Entrer un prompt et recuperer son output
def prompt_IA(system_prompt, user_prompt):
    print("\nEnvoi de la requete au LLM ..")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": f"{system_prompt}" },
            { "role": "user",   "content": f"{user_prompt}"   }
        ]
    )

    print("\nPrompt traite par le LLM.")
    return response.choices[0].message.content