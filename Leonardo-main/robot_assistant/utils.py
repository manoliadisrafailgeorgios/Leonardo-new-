# -*- coding: utf-8 -*-
def extract_place(text):
    words = ["πήγαινε", "με", "στο", "στη", "στον", "σε", "στην"]

    for w in words:
        text = text.replace(w, "")

    return text.strip()
