import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel

SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def query_word(category: str, model: str, generation_config: dict):
    model = GenerativeModel(model)
    responses = model.generate_content(
        f"Name a single existing {category}.",
        generation_config=generation_config,
        safety_settings=SAFETY_SETTINGS,
    )

    word = responses.candidates[0].content.parts[0].text
    return word.lower()


def query_hint(word: str, model: str, generation_config: dict):
    model = GenerativeModel(model)
    responses = model.generate_content(
        f'Describe the word "{word}" without mentioning it.',
        generation_config=generation_config,
        safety_settings=SAFETY_SETTINGS,
    )

    hint = responses.candidates[0].content.parts[0].text
    hint = hint.replace(word, "***")
    return hint
