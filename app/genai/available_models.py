from enum import Enum

class AvailableModels(str, Enum):
    GEMINI_2_5_FLASH = "google/gemini-2.5-flash"
    GPT_4_1_MINI = "openai/gpt-4.1-mini"