import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None

REFUSAL_MESSAGE = (
    "Sorry, I can only help with Generative AI topics. "
    "Please ask me a question about GenAI, LLMs, "
    "prompt engineering, RAG, AI agents, or another "
    "GenAI topic."
)

MISSING_KEY_MESSAGE = (
    "The OpenAI API key is missing. Please add OPENAI_API_KEY "
    "to the .env file and restart the app."
)

API_ERROR_MESSAGE = (
    "I could not contact the OpenAI service right now. "
    "Please check your API key and internet connection, then try again."
)


def is_genai_question(user_input):
    if client is None:
        return False

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"""
Classify the following question.

Return ONLY YES or NO.

YES = the question is directly related to Generative AI,
LLMs, ChatGPT, OpenAI, prompt engineering, RAG, embeddings,
AI agents, fine-tuning, tokens, transformers used in GenAI,
multimodal GenAI, text/image/audio generation, or GenAI applications.

NO = anything unrelated to Generative AI.

Question:
{user_input}
"""
    )

    return response.output_text.strip().upper() == "YES"


def get_response(messages):
    if client is None:
        return MISSING_KEY_MESSAGE

    user_input = messages[-1]["content"]

    try:
        if not is_genai_question(user_input):
            return REFUSAL_MESSAGE

        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="""
You are a Generative AI tutor.

Only answer questions related to Generative AI.

Answer GenAI questions using simple language,
clear explanations, practical examples, and best practices.
""",
            input=messages,
            temperature=0.5,
        )

        return response.output_text
    except Exception:
        return API_ERROR_MESSAGE