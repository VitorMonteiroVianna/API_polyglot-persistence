from enum import Enum

class AvailableModels(str, Enum):
    GEMINI_2_5_FLASH = "google/gemini-2.5-flash"
    GPT_4_1_MINI = "openai/gpt-4.1-mini"
    OPENAI_EMBEDDING_3_SMALL = "openai/text-embedding-3-small"
    OPENAI_EMBEDDING_3_LARGE = "openai/text-embedding-3-large"
    GEMINI_EMBEDDING_LARGE_2 = "google/gemini-embedding-001"
