import os
import time

import deepl
import argostranslate.package
import argostranslate.translate

from variables import TRANSLATE_TYPE

translate_type = TRANSLATE_TYPE


if translate_type == 'helsinki':
    from transformers import MarianMTModel, MarianTokenizer
    import torch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_name = "Helsinki-NLP/opus-mt-zh-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name).to(device)

    model.generate(**tokenizer("记得先交饭钱！好味情更久", return_tensors="pt", padding=True).to(device))
elif translate_type == 'argos':
    from_code = "zh"
    to_code = "en"

    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

    translatedText = argostranslate.translate.translate("馋馋你的嘴好味情更久, 相信没有谁的胃能拒绝它们的抚慰",
                                                        from_code, to_code)
    # Translate
    tic = time.perf_counter()

    translatedText = argostranslate.translate.translate("记得先交饭钱！好味情更久", from_code, to_code)
    toc = time.perf_counter()
    #print(f"Translated in {toc - tic:0.3f} s")
    #print(translatedText)
    # '¡Hola Mundo!'
elif translate_type == 'deepl':
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
print('translator started')

def translate(input_text):
    if translate_type == 'helsinki':
        return translate_helsinki(input_text)
    elif translate_type == 'argos':
        # need to set env ARGOS_DEVICE_TYPE=cuda
        return argostranslate.translate.translate(input_text, from_code, to_code)
    elif translate_type == 'deepl':
        return translate_deepl(input_text)
def translate_helsinki(input_text):
    tic = time.perf_counter()
    translated = model.generate(**tokenizer(input_text, return_tensors="pt", padding=True).to(device))
    #
    translated = ''.join([tokenizer.decode(t, skip_special_tokens=True) for t in translated])
    toc = time.perf_counter()
    #print(f"Translated in {toc - tic:0.3f} s")
    #print(translated)
    return translated


def translate_deepl(input_text):
    if len(input_text) > 30:
        return ""
    text = translator.translate_text(
        input_text, source_lang="ZH", target_lang="EN-US"
    ).text
    return text


