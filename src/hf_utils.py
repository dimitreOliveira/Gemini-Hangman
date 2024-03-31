import logging
import re
import string

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

GEMMA_WORD_PATTERNS = [
    "(?<=\*)(.*?)(?=\*)",
    '(?<=")(.*?)(?=")',
]


def query_hf(
    query: str,
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    generation_config: dict,
    device: str,
) -> str:
    """Queries an LLM model using the Vertex AI API.

    Args:
        query (str): Query sent to the Vertex API
        model (str): Model target by Vertex
        generation_config (dict): Configurations used by the model

    Returns:
        str: Vertex AI text response
    """
    generation_config = GenerationConfig(
        do_sample=True,
        max_new_tokens=generation_config["max_output_tokens"],
        top_k=generation_config["top_k"],
        top_p=generation_config["top_p"],
        temperature=generation_config["temperature"],
    )

    input_ids = tokenizer(query, return_tensors="pt").to(device)
    outputs = model.generate(**input_ids, generation_config=generation_config)
    outputs = tokenizer.decode(outputs[0], skip_special_tokens=True)
    outputs = outputs.replace(query, "")
    return outputs


def query_word(
    category: str,
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    generation_config: dict,
    device: str,
) -> str:
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

    matched_word = ""
    while not matched_word:
        word = query_hf(query, model, tokenizer, generation_config, device)

        # Extract word of interest from Gemma's output
        for pattern in GEMMA_WORD_PATTERNS:
            matched_words = re.findall(rf"{pattern}", word)
            matched_words = [x for x in matched_words if x != ""]
            if matched_words:
                matched_word = matched_words[-1]

    matched_word = matched_word.translate(str.maketrans("", "", string.punctuation))
    matched_word = matched_word.lower()

    logger.info("Word queried successful")
    return matched_word


def query_hint(
    word: str,
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    generation_config: dict,
    device: str,
) -> str:
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
    hint = query_hf(query, model, tokenizer, generation_config, device)
    hint = re.sub(re.escape(word), "***", hint, flags=re.IGNORECASE)
    logger.info("Hint queried successful")
    return hint


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)
