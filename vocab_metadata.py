# -*- coding: utf-8 -*-
import json
import os

DICT_FILE = os.path.join(os.path.dirname(__file__), "full_dictionary.json")

def load_dict():
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

_DICTIONARY_CACHE = load_dict()

def derive_word_metadata(word_raw, meaning_raw):
    word = word_raw.strip()
    w_lower = word.lower()
    
    if w_lower in _DICTIONARY_CACHE:
        d = _DICTIONARY_CACHE[w_lower]
        return {
            "type": "authoritative",
            "forms": d.get("forms", {}),
            "en": d.get("en", ""),
            "eg": d.get("eg", ""),
            "cn": d.get("cn", "")
        }
    
    # 极简兜底
    return {
        "type": "fallback",
        "forms": {"词汇": word},
        "en": f"Definition: {meaning_raw}",
        "eg": f"The teacher asked us about '{word}'.",
        "cn": f"老师向我们询问了关于'{word}'的意思。"
    }
