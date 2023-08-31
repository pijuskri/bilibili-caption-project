import os
import deepl

api_key = os.environ['deepl_token']

translator = deepl.Translator(api_key)

usage = translator.get_usage()
if usage.any_limit_reached:
    print('Translation limit reached.')
if usage.character.valid:
    print(
        f"Character usage: {usage.character.count} of {usage.character.limit}")
if usage.document.valid:
    print(f"Document usage: {usage.document.count} of {usage.document.limit}")

def translate(input):
    if len(input) > 30:
        return ""
    text = translator.translate_text(
        input, source_lang="ZH", target_lang="EN-US"
    ).text
    return text

