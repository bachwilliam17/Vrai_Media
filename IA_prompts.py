from openai import OpenAI

client = OpenAI(api_key="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")

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