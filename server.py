from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
from langchain.output_parsers import BooleanOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

_ = load_dotenv()

set_llm_cache(SQLiteCache())


class CustomBooleanParser(BooleanOutputParser):
    def parse(self, output: str) -> bool:
        try:
            output = output.strip()
            output = output.strip(",.")
            return super().parse(output)
        except ValueError:
            return None


prompt = PromptTemplate.from_template('''You are answering a boolean question.
Is `{dish_name}` suitable for vegetarian?
Respond with only `Y` or `N`: ''')

chatgpt = ChatOpenAI(model="gpt-3.5-turbo-0125", max_tokens=1)

boolean_output_parser = CustomBooleanParser(true_val="Y", false_val="N")

chain = prompt | chatgpt | boolean_output_parser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/classify_dishes")
async def classify_dishes(dish_names: list[str]):
    response = await chain.abatch([{"dish_name": dish_name} for dish_name in dish_names])
    return [
        {
            "dish_name": dish_name,
            "is_vegetarian": is_vegetarian
        }
        for dish_name, is_vegetarian in zip(dish_names, response)
        if is_vegetarian is True
    ]
