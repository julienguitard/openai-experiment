from openai import OpenAI
from apis.constants import DEEPSEEK_API_KEY

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

role_config = {
    "role": 'data engineer',
    "speciality":'domain modelling with Postregsql'
}

content_config = {
    "output":'Postgresql database schema',
    "theme":'',
    "extra_context":"Do not hesitate to create enum type or small tables to avoid unguarded VARCHAR types and populate your tables",
    "negative_guideline":" Do not give examples of queries"
}

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a {role} specializing {speciality}".format(**role_config)},
        {"role": "user", "content": "Give an example of {output} for {theme}.{extra_context}.{negative_guideline}".format(**content_config )},
    ],
    max_tokens=8100,
    stream=False
)

print(response.choices[0].message.content)