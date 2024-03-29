import logging

import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel

SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def query_vertex_ai(query: str, model: str, generation_config: dict) -> str:
    """Queries an LLM model using the Vertex AI API.

    Args:
        query (str): Query sent to the Vertex API
        model (str): Model target by Vertex
        generation_config (dict): Configurations used by the model

    Returns:
        str: Vertex AI text response
    """
    model = GenerativeModel(model)
    responses = model.generate_content(
        query,
        generation_config=generation_config,
        safety_settings=SAFETY_SETTINGS,
    )
    return responses.candidates[0].content.parts[0].text


def query_word(category: str, model: str, generation_config: dict) -> str:
    """Queries a word to be used for the hangman game.

    Args:
        category (str): Category used as source sample a word
        model (str): Model target by Vertex
        generation_config (dict): Configurations used by the model

    Returns:
        str: Queried word
    """
    logger.info(f"Quering word for category: '{category}'...")
    query = f"Name a single existing {category}."
    word = query_vertex_ai(query, model, generation_config)
    logger.info("Word queried successful")
    return word.lower()


def query_hint(word: str, model: str, generation_config: dict) -> str:
    """Queries a hint for the hangman game.

    Args:
        word (str): Word used as source to create the hint
        model (str): Model target by Vertex
        generation_config (dict): Configurations used by the model

    Returns:
        str: Queried hint
    """
    logger.info(f"Quering hint for word: '{word}'...")
    query = f"Describe the word '{word}' without mentioning it."
    hint = query_vertex_ai(query, model, generation_config)
    hint = hint.replace(word, "***")
    logger.info("Hint queried successful")
    return hint


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)
