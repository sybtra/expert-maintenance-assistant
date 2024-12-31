import os
import loguru
import dotenv


class Config:
    _instance = None

    def __init__(self):
        self.NEEDED_VARS = [
            "APP_GROQ_MODEL",
            "GROQ_API_KEY",
            "SUPABASE_URL",
            "SUPABASE_KEY",
            "SUPABASE_PG_CONNECTION_STRING",
            "FASTAPI_URL",
            "APP_MODEL",
            "DB_NAME"
        ]
        self.APP_GROQ_MODEL = None
        self.GROQ_API_KEY = None

        self.SUPABASE_URL = None
        self.SUPABASE_KEY = None
        self.SUPABASE_PG_CONNECTION_STRING = None

        self.DEBUG = None
        self.FASTAPI_URL = None
        self.APP_MODEL = None
        self.DB_NAME = None

        self.llm = None
        self.supabase = None

    @classmethod
    def load(cls):
        if cls._instance is None:
            dotenv.load_dotenv()

            cls._instance = cls()
            cls._instance.APP_GROQ_MODEL = os.getenv("APP_GROQ_MODEL")
            cls._instance.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

            cls._instance.DEBUG = os.getenv("DEBUG")
            
            cls._instance.SUPABASE_URL = os.getenv("SUPABASE_URL")
            cls._instance.SUPABASE_KEY = os.getenv("SUPABASE_KEY")
            cls._instance.SUPABASE_PG_CONNECTION_STRING = os.getenv(
                "SUPABASE_PG_CONNECTION_STRING"
            )
            cls._instance.FASTAPI_URL = os.getenv("FASTAPI_URL")

            cls._instance.APP_MODEL = os.getenv("APP_MODEL")
            cls._instance.DB_NAME = os.getenv("DB_NAME")

            cls._instance.validate()
            # cls._instance.load_llm()
            # cls._instance.load_supabase()
        return cls._instance

    def validate(self):
        missing_vars = [var for var in self.NEEDED_VARS if not getattr(self, var)]
        if missing_vars:
            loguru.logger.error(f"Missing environment variables: {missing_vars}")
            exit(0)

    # def load_llm(self):
    #     self.llm = Groq(model=self.APP_GROQ_MODEL, api_key=self.GROQ_API_KEY)

    # def load_supabase(self):
    #     self.supabase = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

config = Config.load()

def get_config():
    return config
