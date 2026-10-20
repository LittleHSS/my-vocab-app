# -*- coding: utf-8 -*-
"""
新概念英语第一册 纯正权威离线词典直接内嵌模块
无需读取外部 JSON，完全杜绝云端丢失文件、路径不对导致触发兜底模板的问题！
"""
from special_dict_part1 import SPECIAL_DICT

def derive_word_metadata(word_raw, meaning_raw):
    word = word_raw.strip()
    w_lower = word.lower()
    
    # 1. 优先精准匹配权威词典
    if w_lower in SPECIAL_DICT:
        d = SPECIAL_DICT[w_lower]
        return {
            "type": "authoritative",
            "forms": d.get("forms", {}),
            "en": d.get("en", ""),
            "eg": d.get("eg", ""),
            "cn": d.get("cn", "")
        }
    
    # 2. 如果单词不在词典中，根据词性生成语法严密的高级例句，绝不用死板的 The teacher asked us about...
    clean_m = meaning_raw.replace("v.", "").replace("n.", "").replace("adj.", "").replace("adv.", "").replace("prep.", "").strip().split("；")[0].split("，")[0].split(" (")[0]
    
    if meaning_raw.startswith("v.") or " v. " in meaning_raw:
        return {
            "type": "generated",
            "forms": {"原形 (Base)": word, "基本词性": "动词 (Verb)"},
            "en": f"to perform or experience the action: {clean_m}.",
            "eg": f"We decided to {word} together yesterday.",
            "cn": f"我们昨天决定一起去{clean_m}。"
        }
    elif meaning_raw.startswith("n.") or "n." in meaning_raw:
        article = "an" if word[0].lower() in "aeiou" else "a"
        return {
            "type": "generated",
            "forms": {"单数 (Singular)": word, "基本词性": "名词 (Noun)"},
            "en": f"a person, thing, or concept: {clean_m}.",
            "eg": f"I saw {article} {word} near the station this morning.",
            "cn": f"今天早晨我在车站附近见到了一个/一位{clean_m}。"
        }
    elif meaning_raw.startswith("adj.") or "adj." in meaning_raw:
        return {
            "type": "generated",
            "forms": {"原级 (Positive)": word, "基本词性": "形容词 (Adjective)"},
            "en": f"describing a quality or state: {clean_m}.",
            "eg": f"The story he told us was very {word}.",
            "cn": f"他给我们讲的故事非常{clean_m}。"
        }
    elif meaning_raw.startswith("adv.") or "adv." in meaning_raw:
        return {
            "type": "generated",
            "forms": {"词性 (Part of Speech)": "副词 (Adverb)"},
            "en": f"in a particular manner: {clean_m}.",
            "eg": f"She answered the question very {word}.",
            "cn": f"她非常{clean_m}地回答了这个问题。"
        }
    else:
        return {
            "type": "generated",
            "forms": {"短语/表达": word},
            "en": f"a common expression meaning: {clean_m}.",
            "eg": f"He used the expression '{word}' in his speech.",
            "cn": f"他在演讲中使用了'{clean_m}'这个表达。"
        }
