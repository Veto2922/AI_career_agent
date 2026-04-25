from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()


class LLMFactory:
    @staticmethod
    def create(provider: str):
        provider = provider.lower()

        if provider == "gemini":
            return init_chat_model(
                "google_genai:gemini-2.5-flash",
                api_key=os.getenv("GOOGLE_API_KEY"),
            )

        elif provider == "groq":
            return init_chat_model(
                "openai/gpt-oss-120b",
                model_provider="groq",
                api_key=os.getenv("GROQ_API_KEY"),
                timeout=60.0,
                max_retries=0,
            )

        elif provider == "openai":
            return init_chat_model("gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

        elif provider == "deepseek":
            return init_chat_model(
                "deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY")
            )

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
