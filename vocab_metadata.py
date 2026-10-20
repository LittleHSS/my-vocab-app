# -*- coding: utf-8 -*-
"""
新概念英语第一册 智能词形变形、英文释义与经典例句知识库
包含：
1. 动词形态：第三人称单数 (3rd Singular)、一般过去时 (Past Simple)、过去分词 (Past Participle)、现在分词 (Present Participle / -ing)
2. 名词形态：复数形式 (Plural)
3. 形容词/副词形态：比较级 (Comparative) 与最高级 (Superlative)
4. 英文释义 (English Definition)
5. 经典实战例句 (Example Sentence & Translation)
"""

IRREGULAR_VERBS = {
    "be": {
        "s3": "is / are", "past": "was / were", "pp": "been", "ing": "being",
        "en": "to exist or live; used as a copular verb.",
        "eg": "He is a student at London University.",
        "cn": "他是伦敦大学的一名学生。"
    },
    "have": {
        "s3": "has", "past": "had", "pp": "had", "ing": "having",
        "en": "to possess, own, or hold; to eat or experience.",
        "eg": "I have a terrible cold today.",
        "cn": "我今天得了严重的感冒。"
    },
    "do": {
        "s3": "does", "past": "did", "pp": "done", "ing": "doing",
        "en": "to perform an action or activity.",
        "eg": "What are you doing now? — I am reading a book.",
        "cn": "你现在在做什么？— 我在看书。"
    },
    "go": {
        "s3": "goes", "past": "went", "pp": "gone / been", "ing": "going",
        "en": "to move or travel from one place to another.",
        "eg": "He usually goes to work by bus.",
        "cn": "他通常乘公交车去上班。"
    },
    "see": {
        "s3": "sees", "past": "saw", "pp": "seen", "ing": "seeing",
        "en": "to perceive with the eyes; to understand or meet.",
        "eg": "I saw him at the railway station yesterday.",
        "cn": "我昨天在火车站看见了他。"
    },
    "come": {
        "s3": "comes", "past": "came", "pp": "come", "ing": "coming",
        "en": "to move towards or arrive at a place.",
        "eg": "Where do you come from? — I come from France.",
        "cn": "你来自哪里？— 我来自法国。"
    },
    "take": {
        "s3": "takes", "past": "took", "pp": "taken", "ing": "taking",
        "en": "to get into one's hands; to carry or consume.",
        "eg": "Please take off your coat; it is very warm here.",
        "cn": "请脱下你的大衣，这里很暖和。"
    },
    "make": {
        "s3": "makes", "past": "made", "pp": "made", "ing": "making",
        "en": "to create, produce, or construct something.",
        "eg": "What make is your car? It is made in Germany.",
        "cn": "你的车是什么牌子的？它是德国制造的。"
    },
    "give": {
        "s3": "gives", "past": "gave", "pp": "given", "ing": "giving",
        "en": "to provide someone with something; to hand over.",
        "eg": "Give me that glass, please.",
        "cn": "请把那个玻璃杯递给我。"
    },
    "get": {
        "s3": "gets", "past": "got", "pp": "got / gotten", "ing": "getting",
        "en": "to receive, obtain, or become.",
        "eg": "He got up very early this morning.",
        "cn": "他今天早上起得很早。"
    },
    "find": {
        "s3": "finds", "past": "found", "pp": "found", "ing": "finding",
        "en": "to discover something by searching or by chance.",
        "eg": "I can't find my umbrella anywhere.",
        "cn": "我到处都找不到我的雨伞。"
    },
    "think": {
        "s3": "thinks", "past": "thought", "pp": "thought", "ing": "thinking",
        "en": "to have a particular opinion, belief, or idea.",
        "eg": "What do you think of this city?",
        "cn": "你觉得这座城市怎么样？"
    },
    "tell": {
        "s3": "tells", "past": "told", "pp": "told", "ing": "telling",
        "en": "to communicate information or a story in words.",
        "eg": "The doctor told him to stay in bed for three days.",
        "cn": "医生叫他卧床休息三天。"
    },
    "become": {
        "s3": "becomes", "past": "became", "pp": "become", "ing": "becoming",
        "en": "to begin to be; to turn into.",
        "eg": "He wants to become an engineer in the future.",
        "cn": "他将来想成为一名工程师。"
    },
    "leave": {
        "s3": "leaves", "past": "left", "pp": "left", "ing": "leaving",
        "en": "to go away from; to depart.",
        "eg": "The train leaves the platform at eight o'clock.",
        "cn": "火车将在八点整驶离站台。"
    },
    "feel": {
        "s3": "feels", "past": "felt", "pp": "felt", "ing": "feeling",
        "en": "to experience an emotion or physical sensation.",
        "eg": "Do you feel better today? — Yes, much better.",
        "cn": "你今天感觉好点了吗？— 是的，好多了。"
    },
    "put": {
        "s3": "puts", "past": "put", "pp": "put", "ing": "putting",
        "en": "to move something to a particular position.",
        "eg": "Put on your shoes and let's go out.",
        "cn": "穿上你的鞋子，我们出门吧。"
    },
    "bring": {
        "s3": "brings", "past": "brought", "pp": "brought", "ing": "bringing",
        "en": "to take or carry someone or something to a place.",
        "eg": "Can you bring me a cup of tea, please?",
        "cn": "请能给我倒杯茶来吗？"
    },
    "begin": {
        "s3": "begins", "past": "began", "pp": "begun", "ing": "beginning",
        "en": "to start doing something or happening.",
        "eg": "The concert began at eight o'clock yesterday evening.",
        "cn": "音乐会昨晚八点整开始了。"
    },
    "keep": {
        "s3": "keeps", "past": "kept", "pp": "kept", "ing": "keeping",
        "en": "to retain possession of; to stay in a specified state.",
        "eg": "Please keep the room clean and tidy.",
        "cn": "请保持房间干净整洁。"
    },
    "write": {
        "s3": "writes", "past": "wrote", "pp": "written", "ing": "writing",
        "en": "to mark letters, words, or symbols on a surface.",
        "eg": "She has written three letters this afternoon.",
        "cn": "她今天下午已经写了三封信。"
    },
    "stand": {
        "s3": "stands", "past": "stood", "pp": "stood", "ing": "standing",
        "en": "to be in an upright position on the feet.",
        "eg": "A tall man is standing behind the counter.",
        "cn": "一个身材高大的男人正站在柜台后面。"
    },
    "hear": {
        "s3": "hears", "past": "heard", "pp": "heard", "ing": "hearing",
        "en": "to perceive sound with the ear.",
        "eg": "I can hear the music from the next room.",
        "cn": "我能听到隔壁房间传来的音乐。"
    },
    "meet": {
        "s3": "meets", "past": "met", "pp": "met", "ing": "meeting",
        "en": "to come into the presence of someone; to get to know.",
        "eg": "Nice to meet you, Mr. Smith.",
        "cn": "很高兴认识你，史密斯先生。"
    },
    "run": {
        "s3": "runs", "past": "ran", "pp": "run", "ing": "running",
        "en": "to move rapidly on foot.",
        "eg": "The boy is running across the park.",
        "cn": "那个男孩正飞快地穿过公园。"
    },
    "pay": {
        "s3": "pays", "past": "paid", "pp": "paid", "ing": "paying",
        "en": "to give money for goods or services.",
        "eg": "How much did you pay for this suit?",
        "cn": "你买这套西装花了多少钱？"
    },
    "sit": {
        "s3": "sits", "past": "sat", "pp": "sat", "ing": "sitting",
        "en": "to rest with the body supported on buttocks.",
        "eg": "She is sitting in the comfortable armchair.",
        "cn": "她正坐在那把舒适的扶手椅里。"
    },
    "speak": {
        "s3": "speaks", "past": "spoke", "pp": "spoken", "ing": "speaking",
        "en": "to say words; to be able to talk in a language.",
        "eg": "Does he speak English or French?",
        "cn": "他说英语还是说法语？"
    },
    "read": {
        "s3": "reads", "past": "read [red]", "pp": "read [red]", "ing": "reading",
        "en": "to look at and comprehend the meaning of written words.",
        "eg": "My grandfather is reading a newspaper.",
        "cn": "我祖父正在看报纸。"
    },
    "grow": {
        "s3": "grows", "past": "grew", "pp": "grown", "ing": "growing",
        "en": "to increase in size; to cultivate plants.",
        "eg": "Beautiful roses grow in their garden.",
        "cn": "他们花园里种着美丽的玫瑰。"
    },
    "lose": {
        "s3": "loses", "past": "lost", "pp": "lost", "ing": "losing",
        "en": "to be deprived of or fail to keep.",
        "eg": "He has lost his key and cannot open the door.",
        "cn": "他弄丢了钥匙，打不开门。"
    },
    "fall": {
        "s3": "falls", "past": "fell", "pp": "fallen", "ing": "falling",
        "en": "to drop down from a higher level.",
        "eg": "He slipped and fell downstairs yesterday.",
        "cn": "他昨天滑倒滚下了楼梯。"
    },
    "send": {
        "s3": "sends", "past": "sent", "pp": "sent", "ing": "sending",
        "en": "to cause to go or be taken to a particular destination.",
        "eg": "I sent a postcard to my parents last week.",
        "cn": "我上周给我父母寄了一张明信片。"
    },
    "build": {
        "s3": "builds", "past": "built", "pp": "built", "ing": "building",
        "en": "to construct something by putting parts together.",
        "eg": "They built a new bridge over the river.",
        "cn": "他们在这条河上建了一座新桥。"
    },
    "understand": {
        "s3": "understands", "past": "understood", "pp": "understood", "ing": "understanding",
        "en": "to perceive the intended meaning of words or ideas.",
        "eg": "I can understand spoken English very well now.",
        "cn": "我现在能很好地听懂英语口语了。"
    },
    "break": {
        "s3": "breaks", "past": "broke", "pp": "broken", "ing": "breaking",
        "en": "to separate into pieces as a result of a blow or shock.",
        "eg": "Don't drop the vase; you will break it!",
        "cn": "别把花瓶摔了，你会把它打碎的！"
    },
    "spend": {
        "s3": "spends", "past": "spent", "pp": "spent", "ing": "spending",
        "en": "to pay out money or pass time.",
        "eg": "We spent our holiday in Greece last year.",
        "cn": "我们去年在希腊度过了假期。"
    },
    "cut": {
        "s3": "cuts", "past": "cut", "pp": "cut", "ing": "cutting",
        "en": "to divide or wound with a sharp-edged instrument.",
        "eg": "He cut the bread into thick slices.",
        "cn": "他把面包切成了厚厚的薄片。"
    },
    "rise": {
        "s3": "rises", "past": "rose", "pp": "risen", "ing": "rising",
        "en": "to move from a lower position to a higher one; sun coming up.",
        "eg": "The sun rises early in the summer morning.",
        "cn": "夏天早晨太阳升起得很早。"
    },
    "drive": {
        "s3": "drives", "past": "drove", "pp": "driven", "ing": "driving",
        "en": "to operate and control the direction of a vehicle.",
        "eg": "He is driving his new car to work today.",
        "cn": "他今天正开着他的新车去上班。"
    },
    "buy": {
        "s3": "buys", "past": "bought", "pp": "bought", "ing": "buying",
        "en": "to obtain in exchange for payment.",
        "eg": "She bought some meat and vegetables at the butcher's.",
        "cn": "她在肉铺买了一些肉和蔬菜。"
    },
    "wear": {
        "s3": "wears", "past": "wore", "pp": "worn", "ing": "wearing",
        "en": "to have on one's body as clothing or ornament.",
        "eg": "She is wearing a beautiful blue dress.",
        "cn": "她正穿着一件漂亮的蓝色连衣裙。"
    },
    "shut": {
        "s3": "shuts", "past": "shut", "pp": "shut", "ing": "shutting",
        "en": "to move into position so as to block an opening.",
        "eg": "Shut the window, please; it is cold outside.",
        "cn": "请关上窗户，外面很冷。"
    },
    "catch": {
        "s3": "catches", "past": "caught", "pp": "caught", "ing": "catching",
        "en": "to intercept and hold; to board a train or bus in time.",
        "eg": "Hurry up, or we won't catch the eight o'clock train.",
        "cn": "快点，否则我们就赶不上八点的火车了。"
    },
    "sleep": {
        "s3": "sleeps", "past": "slept", "pp": "slept", "ing": "sleeping",
        "en": "to be in a natural state of rest.",
        "eg": "The baby is sleeping peacefully in the bedroom.",
        "cn": "婴儿正在卧室里安静地熟睡。"
    },
    "swim": {
        "s3": "swims", "past": "swam", "pp": "swum", "ing": "swimming",
        "en": "to propel the body through water.",
        "eg": "The children are swimming across the river.",
        "cn": "孩子们正在游过这条河。"
    },
    "sing": {
        "s3": "sings", "past": "sang", "pp": "sung", "ing": "singing",
        "en": "to make musical sounds with the voice.",
        "eg": "She sang a lovely English song at the party.",
        "cn": "她在聚会上唱了一首好听的英文歌。"
    },
    "drink": {
        "s3": "drinks", "past": "drank", "pp": "drunk", "ing": "drinking",
        "en": "to swallow liquid.",
        "eg": "Would you like to drink some tea or coffee?",
        "cn": "你想喝点茶还是咖啡？"
    },
    "eat": {
        "s3": "eats", "past": "ate", "pp": "eaten", "ing": "eating",
        "en": "to consume food into the body.",
        "eg": "Have you eaten your lunch yet? — Yes, I have.",
        "cn": "你吃过午饭了吗？— 是的，吃过了。"
    },
    "fly": {
        "s3": "flies", "past": "flew", "pp": "flown", "ing": "flying",
        "en": "to move through the air using wings or an aircraft.",
        "eg": "The pilot has flown to Paris three times this week.",
        "cn": "这位飞行员本周已经飞往巴黎三次了。"
    },
    "forget": {
        "s3": "forgets", "past": "forgot", "pp": "forgotten", "ing": "forgetting",
        "en": "to fail to remember something.",
        "eg": "Don't forget to post the letter on your way to work.",
        "cn": "去上班的路上别忘了把信寄出去。"
    },
    "hurt": {
        "s3": "hurts", "past": "hurt", "pp": "hurt", "ing": "hurting",
        "en": "to cause physical pain or injury.",
        "eg": "He hurt his back when he lifted the heavy suitcase.",
        "cn": "他搬那个沉重的箱子时扭伤了背部。"
    },
    "ring": {
        "s3": "rings", "past": "rang", "pp": "rung", "ing": "ringing",
        "en": "to make a clear resonant or vibrating sound; to telephone.",
        "eg": "The telephone rang while I was having a bath.",
        "cn": "我正在洗澡时电话铃响了。"
    },
    "ride": {
        "s3": "rides", "past": "rode", "pp": "ridden", "ing": "riding",
        "en": "to sit on and control a horse, bicycle, or motorcycle.",
        "eg": "He rides his bicycle to school every morning.",
        "cn": "他每天早上骑自行车去上学。"
    },
    "sell": {
        "s3": "sells", "past": "sold", "pp": "sold", "ing": "selling",
        "en": "to give or hand over something in exchange for money.",
        "eg": "They sold their old car and bought a new one.",
        "cn": "他们卖掉了旧车，买了一辆新车。"
    },
    "shine": {
        "s3": "shines", "past": "shone", "pp": "shone", "ing": "shining",
        "en": "to give out or reflect light.",
        "eg": "The sun is shining brightly in the clear sky.",
        "cn": "太阳在晴朗的天空中灿烂地照耀着。"
    },
    "teach": {
        "s3": "teaches", "past": "taught", "pp": "taught", "ing": "teaching",
        "en": "to impart knowledge to or instruct someone.",
        "eg": "Mr. Sawyer teaches French and German at our school.",
        "cn": "索耶先生在我们学校教法语和德语。"
    },
    "throw": {
        "s3": "throws", "past": "threw", "pp": "thrown", "ing": "throwing",
        "en": "to propel something with force through the air.",
        "eg": "Don't throw paper on the floor.",
        "cn": "别把纸扔在地板上。"
    },
    "wake": {
        "s3": "wakes", "past": "woke", "pp": "woken", "ing": "waking",
        "en": "to emerge or cause to emerge from sleep.",
        "eg": "Please wake me up at seven o'clock tomorrow morning.",
        "cn": "明天早上七点请叫醒我。"
    },
    "win": {
        "s3": "wins", "past": "won", "pp": "won", "ing": "winning",
        "en": "to be successful or victorious in a contest or battle.",
        "eg": "Our football team won the match yesterday.",
        "cn": "我们足球队昨天赢得了比赛。"
    },
    "sweep": {
        "s3": "sweeps", "past": "swept", "pp": "swept", "ing": "sweeping",
        "en": "to clean an area by brushing away dirt with a broom.",
        "eg": "She swept the kitchen floor and dusted the furniture.",
        "cn": "她扫了厨房地板，并掸掉了家具上的灰尘。"
    },
    "cost": {
        "s3": "costs", "past": "cost", "pp": "cost", "ing": "costing",
        "en": "to require the payment of an amount of money.",
        "eg": "How much does this pair of shoes cost?",
        "cn": "这双鞋多少钱？"
    }
}

IRREGULAR_NOUNS = {
    "man": "men", "woman": "women", "child": "children", "tooth": "teeth",
    "foot": "feet", "mouse": "mice", "person": "people", "policeman": "policemen",
    "policewoman": "policewomen", "postman": "postmen", "milkman": "milkmen",
    "taximan": "taximen", "knife": "knives", "shelf": "shelves", "leaf": "leaves",
    "loaf": "loaves", "half": "halves", "thief": "thieves", "scarf": "scarves",
    "life": "lives", "wife": "wives"
}

ADJECTIVE_COMPARATIVES = {
    "good": ("better", "best"),
    "bad": ("worse", "worst"),
    "little": ("less", "least"),
    "much": ("more", "most"),
    "many": ("more", "most"),
    "far": ("farther / further", "farthest / furthest")
}

def derive_word_metadata(word_raw, meaning_raw):
    """
    智能推导单词的形态格式（第三人称单数、过去式、过去分词、现在分词、名词复数等）、英文释义与例句
    """
    word = word_raw.strip()
    w_lower = word.lower()
    meaning = meaning_raw.strip()

    is_verb = meaning.startswith("v.") or " v. " in meaning or "modal v." in meaning
    is_noun = meaning.startswith("n.") or " n. " in meaning
    is_adj = meaning.startswith("adj.") or " adj. " in meaning
    is_adv = meaning.startswith("adv.") or " adv. " in meaning

    meta = {
        "type": "other",
        "forms": {},
        "en": "",
        "eg": "",
        "cn": ""
    }

    # 1. 如果在不规则动词表中
    if w_lower in IRREGULAR_VERBS:
        v_data = IRREGULAR_VERBS[w_lower]
        meta["type"] = "verb"
        meta["forms"] = {
            "第三人称单数 (3rd Sg)": v_data["s3"],
            "一般过去时 (Past)": v_data["past"],
            "过去分词 (Past Participle)": v_data["pp"],
            "现在分词 (Present Participle / -ing)": v_data["ing"]
        }
        meta["en"] = v_data["en"]
        meta["eg"] = v_data["eg"]
        meta["cn"] = v_data["cn"]
        return meta

    # 2. 常规动词推导
    if is_verb and " " not in word:
        meta["type"] = "verb"
        # 3rd person singular
        if w_lower.endswith(("s", "sh", "ch", "x", "z", "o")):
            s3 = w_lower + "es"
        elif w_lower.endswith("y") and len(w_lower) > 1 and w_lower[-2] not in "aeiou":
            s3 = w_lower[:-1] + "ies"
        else:
            s3 = w_lower + "s"

        # past & pp
        if w_lower.endswith("e"):
            past = w_lower + "d"
        elif w_lower.endswith("y") and len(w_lower) > 1 and w_lower[-2] not in "aeiou":
            past = w_lower[:-1] + "ied"
        elif len(w_lower) >= 3 and w_lower[-1] not in "aeiouwxy" and w_lower[-2] in "aeiou" and w_lower[-3] not in "aeiou":
            past = w_lower + w_lower[-1] + "ed"
        else:
            past = w_lower + "ed"

        # ing
        if w_lower.endswith("ie"):
            ing = w_lower[:-2] + "ying"
        elif w_lower.endswith("e") and not w_lower.endswith(("ee", "oe", "ye")):
            ing = w_lower[:-1] + "ing"
        elif len(w_lower) >= 3 and w_lower[-1] not in "aeiouwxy" and w_lower[-2] in "aeiou" and w_lower[-3] not in "aeiou":
            ing = w_lower + w_lower[-1] + "ing"
        else:
            ing = w_lower + "ing"

        meta["forms"] = {
            "第三人称单数 (3rd Sg)": s3,
            "一般过去时 (Past)": past,
            "过去分词 (Past Participle)": past,
            "现在分词 (Present Participle / -ing)": ing
        }
        meta["en"] = f"to perform the action of {w_lower}; {meaning.split(' ')[-1]}"
        meta["eg"] = f"He always {s3} every morning."
        meta["cn"] = f"他每天早晨总是{meaning.split(' ')[-1]}。"
        return meta

    # 3. 名词形态推导 (复数形式)
    if is_noun and " " not in word:
        meta["type"] = "noun"
        if w_lower in IRREGULAR_NOUNS:
            pl = IRREGULAR_NOUNS[w_lower]
        elif "(不可数)" in meaning or "不可数" in meaning:
            pl = "[不可数名词 Uncountable]"
        elif w_lower.endswith(("s", "sh", "ch", "x", "z")):
            pl = w_lower + "es"
        elif w_lower.endswith("y") and len(w_lower) > 1 and w_lower[-2] not in "aeiou":
            pl = w_lower[:-1] + "ies"
        elif w_lower.endswith("o") and w_lower in ["potato", "tomato", "hero"]:
            pl = w_lower + "es"
        else:
            pl = w_lower + "s"

        meta["forms"] = {
            "单数形式 (Singular)": word,
            "复数形式 (Plural)": pl
        }
        clean_meaning = meaning.replace("n.", "").replace("(不可数)", "").strip().split("；")[0].split("，")[0]
        meta["en"] = f"a person, object, or concept: {clean_meaning}."
        meta["eg"] = f"There is a {w_lower} on the desk." if pl != "[不可数名词 Uncountable]" else f"There is some {w_lower} on the table."
        meta["cn"] = f"书桌上有一个/一些{clean_meaning}。"
        return meta

    # 4. 形容词形态推导 (比较级与最高级)
    if is_adj and " " not in word:
        meta["type"] = "adj"
        if w_lower in ADJECTIVE_COMPARATIVES:
            comp, sup = ADJECTIVE_COMPARATIVES[w_lower]
        elif len(w_lower) <= 5:
            if w_lower.endswith("e"):
                comp = w_lower + "r"
                sup = w_lower + "st"
            elif w_lower.endswith("y") and len(w_lower) > 1 and w_lower[-2] not in "aeiou":
                comp = w_lower[:-1] + "ier"
                sup = w_lower[:-1] + "iest"
            elif len(w_lower) >= 3 and w_lower[-1] not in "aeiouwxy" and w_lower[-2] in "aeiou" and w_lower[-3] not in "aeiou":
                comp = w_lower + w_lower[-1] + "er"
                sup = w_lower + w_lower[-1] + "est"
            else:
                comp = w_lower + "er"
                sup = w_lower + "est"
        else:
            comp = "more " + w_lower
            sup = "most " + w_lower

        meta["forms"] = {
            "原级 (Positive)": word,
            "比较级 (Comparative)": comp,
            "最高级 (Superlative)": sup
        }
        clean_meaning = meaning.replace("adj.", "").strip().split("；")[0].split("，")[0]
        meta["en"] = f"describing quality or state: {clean_meaning}."
        meta["eg"] = f"This coat is {w_lower}, but that one is {comp}."
        meta["cn"] = f"这件外套很{clean_meaning}，但那一件更{clean_meaning}。"
        return meta

    # 5. 动词短语 / 介词 / 副词 / 其他
    clean_meaning = meaning.split(" ")[-1]
    meta["type"] = "phrase"
    meta["forms"] = {
        "词组/搭配形式 (Structure)": word
    }
    meta["en"] = f"an English expression or modifier meaning {clean_meaning}."
    meta["eg"] = f"Please {w_lower} before you leave the room."
    meta["cn"] = f"在你离开房间之前，请{clean_meaning}。"
    return meta
