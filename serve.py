from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

print(f"Loaded GROQ API Key: {groq_api_key}")

system_templates = "Translate the following into {language}"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_templates),
    ("user", "{text}"),
])

parser = StrOutputParser()

## Create chain
chain = prompt_template | model | parser


## App definition 
app = FastAPI(title="Langchain Server",
              version="1.0",
              description="A simple API server using Langchain runnable interfaces")

## Adding chain routes
print("Adding routes...")
add_routes(
    app,
    chain,
    path="/chain"
)
print("Routes added successfully")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)