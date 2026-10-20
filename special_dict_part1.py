# -*- coding: utf-8 -*-
import json
import os
import csv

# 专业权威的新概念英语第一册精品例句、地道英文释义与语法形态库
SPECIAL_DICT = {
    "above": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "基本用法": "在...上方 (不接触表面)"},
        "en": "at a higher level or position than something else, without touching it.",
        "eg": "The aeroplane is flying above the clouds.",
        "cn": "飞机正在云层上方飞行。"
    },
    "abroad": {
        "forms": {"词性 (Part of Speech)": "副词 (Adverb)", "基本用法": "修饰动词 (如 go/live/travel abroad)"},
        "en": "in or to a foreign country.",
        "eg": "He has lived abroad for more than five years.",
        "cn": "他在国外已经生活了五年多。"
    },
    "accident": {
        "forms": {"单数 (Singular)": "accident", "复数 (Plural)": "accidents"},
        "en": "an unfortunate event resulting in damage or injury.",
        "eg": "There was a bad accident on the road yesterday.",
        "cn": "昨天这条马路上发生了一起严重的事故。"
    },
    "across": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "基本用法": "横过、穿过 (从表面的一边到另一边)"},
        "en": "from one side to the other of something with clear limits.",
        "eg": "The boy is running across the street.",
        "cn": "那个男孩正飞快地穿过街道。"
    },
    "actor": {
        "forms": {"单数 (Singular)": "actor", "复数 (Plural)": "actors", "阴性形式": "actress"},
        "en": "a person whose profession is acting on stage or in films.",
        "eg": "He is a famous actor in London.",
        "cn": "他是伦敦一位著名的男演员。"
    },
    "actress": {
        "forms": {"单数 (Singular)": "actress", "复数 (Plural)": "actresses"},
        "en": "a female actor on stage, in films, or on television.",
        "eg": "She will appear on stage as a leading actress.",
        "cn": "她将作为主角女演员登台表演。"
    },
    "address": {
        "forms": {"单数 (Singular)": "address", "复数 (Plural)": "addresses"},
        "en": "the particulars of the place where someone lives or an organization is situated.",
        "eg": "Can you write down your address on this envelope?",
        "cn": "你能在这个信封上写下你的地址吗？"
    },
    "aeroplane": {
        "forms": {"单数 (Singular)": "aeroplane", "复数 (Plural)": "aeroplanes"},
        "en": "a powered flying vehicle with fixed wings.",
        "eg": "The aeroplane took off from London airport on time.",
        "cn": "飞机准时从伦敦机场起飞。"
    },
    "afford": {
        "forms": {"第三人称单数": "affords", "一般过去时": "afforded", "过去分词": "afforded", "现在分词": "affording"},
        "en": "to have enough money or time to be able to buy or do something.",
        "eg": "We cannot afford to buy a new car this year.",
        "cn": "我们今年买不起一辆新车。"
    },
    "afraid": {
        "forms": {"词性 (Part of Speech)": "形容词 (Adjective)", "常用搭配": "be afraid of (害怕...)"},
        "en": "feeling fear, worry, or anxiety about something.",
        "eg": "Don't be afraid; the dog is very friendly.",
        "cn": "别害怕，这只狗非常友好。"
    },
    "after": {
        "forms": {"词性 (Part of Speech)": "介词/连词 (Prep. / Conj.)", "基本用法": "在...之后"},
        "en": "in the time following an event or period.",
        "eg": "Let's go for a walk in the park after dinner.",
        "cn": "晚饭后我们去公园散步吧。"
    },
    "afternoon": {
        "forms": {"单数 (Singular)": "afternoon", "复数 (Plural)": "afternoons", "固定短语": "in the afternoon"},
        "en": "the time from noon or lunchtime to evening.",
        "eg": "He usually plays tennis on Sunday afternoon.",
        "cn": "他通常在周日下午打网球。"
    },
    "again": {
        "forms": {"词性 (Part of Speech)": "副词 (Adverb)", "基本用法": "再一次，又一次"},
        "en": "another time; once more.",
        "eg": "Please say that again; I didn't hear clearly.",
        "cn": "请再说一遍，我刚才没听清楚。"
    },
    "ago": {
        "forms": {"词性 (Part of Speech)": "副词 (Adverb)", "基本用法": "...以前 (常与一般过去时连用)"},
        "en": "before the present time in the past.",
        "eg": "I saw him at the railway station two days ago.",
        "cn": "两天前我在火车站见到了他。"
    },
    "agree": {
        "forms": {"第三人称单数": "agrees", "一般过去时": "agreed", "过去分词": "agreed", "现在分词": "agreeing"},
        "en": "to have the same opinion as someone else.",
        "eg": "I completely agree with what you said.",
        "cn": "我完全同意你说的话。"
    },
    "air hostess": {
        "forms": {"单数 (Singular)": "air hostess", "复数 (Plural)": "air hostesses"},
        "en": "a woman whose job is to serve passengers on an aircraft.",
        "eg": "She works as an air hostess for an international airline.",
        "cn": "她在一家国际航空公司担任空姐。"
    },
    "airport": {
        "forms": {"单数 (Singular)": "airport", "复数 (Plural)": "airports"},
        "en": "a complex of runways and buildings for the take-off, landing, and maintenance of aircraft.",
        "eg": "We arrived at the airport two hours before the flight.",
        "cn": "我们在航班起飞前两小时到达了机场。"
    },
    "all": {
        "forms": {"词性 (Part of Speech)": "限定词/代词 (Det. / Pron.)", "基本用法": "全部的，所有的"},
        "en": "the whole quantity or extent of something.",
        "eg": "All the students are listening carefully to the teacher.",
        "cn": "所有的学生都在认真听老师讲课。"
    },
    "almost": {
        "forms": {"词性 (Part of Speech)": "副词 (Adverb)", "基本用法": "几乎，差不多"},
        "en": "not quite; very nearly.",
        "eg": "Dinner is almost ready; please wash your hands.",
        "cn": "晚饭差不多做好了，请去洗手。"
    },
    "along": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "基本用法": "沿着，顺着"},
        "en": "moving in a constant direction on a road, river, or path.",
        "eg": "They are walking along the river bank together.",
        "cn": "他们正一起沿着河岸散步。"
    },
    "already": {
        "forms": {"词性 (Part of Speech)": "副词 (Adverb)", "基本用法": "已经 (常用于肯定句)"},
        "en": "before or by now or a specified time.",
        "eg": "I have already finished my homework.",
        "cn": "我已经做完家庭作业了。"
    },
    "also": {
        "forms": {"词性 (Part of Speech)": "副词 (Adverb)", "基本用法": "也，同样 (放句中)"},
        "en": "in addition; too.",
        "eg": "He speaks French and he also knows some German.",
        "cn": "他说法语，而且也懂一些德语。"
    },
    "always": {
        "forms": {"词性 (Part of Speech)": "频度副词 (Frequency Adverb)", "基本用法": "总是 (100% 频率)"},
        "en": "at all times; on all occasions.",
        "eg": "He always arrives at the office on time.",
        "cn": "他总是按时到达办公室。"
    },
    "American": {
        "forms": {"单数 (Singular)": "American", "复数 (Plural)": "Americans"},
        "en": "relating to the United States of America or its people.",
        "eg": "She is an American student studying English literature.",
        "cn": "她是一名正在学习英国文学的美国学生。"
    },
    "among": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "基本用法": "在...之中 (三者及以上)"},
        "en": "situated more or less centrally in relation to several other things.",
        "eg": "The small cottage is hidden among the green trees.",
        "cn": "那栋小农舍掩映在绿树丛中。"
    },
    "and": {
        "forms": {"词性 (Part of Speech)": "连词 (Conjunction)", "基本用法": "并且，和"},
        "en": "used to connect words of the same part of speech, clauses, or sentences.",
        "eg": "Give me a cup of tea and a piece of cake, please.",
        "cn": "请给我一杯茶和一块蛋糕。"
    },
    "angry": {
        "forms": {"比较级 (Comparative)": "angrier", "最高级 (Superlative)": "angriest", "常用搭配": "be angry with sb."},
        "en": "feeling or showing strong annoyance or displeasure.",
        "eg": "The teacher was very angry with him because he was late.",
        "cn": "老师对他很生气，因为他迟到了。"
    },
    "animal": {
        "forms": {"单数 (Singular)": "animal", "复数 (Plural)": "animals"},
        "en": "a living organism that feeds on organic matter.",
        "eg": "Dogs and cats are common domestic animals.",
        "cn": "狗和猫是常见的家养动物。"
    },
    "another": {
        "forms": {"词性 (Part of Speech)": "限定词/代词", "基本用法": "另一个 (三者以上泛指)"},
        "en": "used to refer to an additional person or thing of the same type.",
        "eg": "Would you like another cup of coffee?",
        "cn": "你想再来一杯咖啡吗？"
    },
    "answer": {
        "forms": {"第三人称单数": "answers", "一般过去时": "answered", "过去分词": "answered", "现在分词": "answering"},
        "en": "to reply to a question, letter, or telephone call.",
        "eg": "Please answer the telephone; it is ringing.",
        "cn": "请去接电话，铃声正在响。"
    },
    "any": {
        "forms": {"词性 (Part of Speech)": "限定词/代词", "基本用法": "任何，一些 (疑问/否定句)"},
        "en": "used to refer to one or some of a thing or number of things, no matter how much or how many.",
        "eg": "Is there any milk in the bottle? — No, there isn't any.",
        "cn": "瓶子里有牛奶吗？— 没有，一点也没有。"
    },
    "apple": {
        "forms": {"单数 (Singular)": "apple", "复数 (Plural)": "apples"},
        "en": "a round fruit with red or green skin and a whitish inside.",
        "eg": "An apple a day keeps the doctor away.",
        "cn": "一天一苹果，医生远离我。"
    },
    "appointment": {
        "forms": {"单数 (Singular)": "appointment", "复数 (Plural)": "appointments", "搭配": "make an appointment"},
        "en": "an arrangement to meet someone at a particular time and place.",
        "eg": "I have an appointment with the doctor at ten o'clock.",
        "cn": "我和医生在十点钟有个预约。"
    },
    "armchair": {
        "forms": {"单数 (Singular)": "armchair", "复数 (Plural)": "armchairs"},
        "en": "a comfortable chair with side supports for a person's arms.",
        "eg": "My grandfather is sitting in the armchair near the fireplace.",
        "cn": "我祖父正坐在壁炉旁的扶手椅里。"
    },
    "arrive": {
        "forms": {"第三人称单数": "arrives", "一般过去时": "arrived", "过去分词": "arrived", "现在分词": "arriving"},
        "en": "to reach a place at the end of a journey or stage.",
        "eg": "The train will arrive at the station in ten minutes.",
        "cn": "火车将在十分钟后到达车站。"
    },
    "asleep": {
        "forms": {"词性 (Part of Speech)": "形容词 (表语)", "常用短语": "fall asleep (入睡)"},
        "en": "in a state of sleep; not awake.",
        "eg": "The little baby fell asleep quickly in his mother's arms.",
        "cn": "小婴儿在母亲怀里很快入睡了。"
    },
    "aspirin": {
        "forms": {"单数 (Singular)": "aspirin", "复数 (Plural)": "aspirins"},
        "en": "a synthetic medicine used to relieve mild or chronic pain and reduce fever.",
        "eg": "You should take two aspirins and go to bed.",
        "cn": "你应该吃两片阿司匹林然后去睡觉。"
    },
    "at": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "基本用法": "在(某时间/地点)"},
        "en": "expressing location or arrival in a particular place or position.",
        "eg": "I will meet you at the cinema at eight o'clock.",
        "cn": "我将在八点钟在电影院和你碰面。"
    },
    "aunt": {
        "forms": {"单数 (Singular)": "aunt", "复数 (Plural)": "aunts"},
        "en": "the sister of one's father or mother or the wife of one's uncle.",
        "eg": "My aunt lives in a beautiful village in the country.",
        "cn": "我姑妈住在乡下一个美丽的村庄里。"
    },
    "autumn": {
        "forms": {"单数 (Singular)": "autumn", "同义词": "fall (美式)"},
        "en": "the season after summer and before winter.",
        "eg": "Leaves turn yellow and fall in autumn.",
        "cn": "秋天树叶变黄并落下来。"
    },
    "awful": {
        "forms": {"比较级 (Comparative)": "more awful", "最高级 (Superlative)": "most awful"},
        "en": "very bad, unpleasant, or shocking.",
        "eg": "I had an awful cold yesterday and couldn't get up.",
        "cn": "我昨天得了糟糕的重感冒，起不来床。"
    },
    "baby": {
        "forms": {"单数 (Singular)": "baby", "复数 (Plural)": "babies"},
        "en": "a very young child, especially one newly or recently born.",
        "eg": "The baby is crying because she is hungry.",
        "cn": "婴儿正在哭泣，因为她饿了。"
    },
    "back": {
        "forms": {"单数 (Singular)": "back", "复数 (Plural)": "backs", "副词用法": "回到原处 (go back)"},
        "en": "the rear surface of the human body from the shoulders to the hips.",
        "eg": "He hurt his back when he lifted the heavy box.",
        "cn": "他搬那个沉重的箱子时扭伤了背部。"
    },
    "bad": {
        "forms": {"原级 (Positive)": "bad", "比较级 (Comparative)": "worse", "最高级 (Superlative)": "worst"},
        "en": "of poor quality or a low standard; unpleasant or severe.",
        "eg": "The weather today is even worse than yesterday.",
        "cn": "今天的天气比昨天还要糟糕。"
    },
    "bag": {
        "forms": {"单数 (Singular)": "bag", "复数 (Plural)": "bags"},
        "en": "a flexible container with an opening at the top.",
        "eg": "She put the apples and oranges into her bag.",
        "cn": "她把苹果和橙子放进了她的包里。"
    },
    "baker": {
        "forms": {"单数 (Singular)": "baker", "复数 (Plural)": "bakers", "面包房": "baker's"},
        "en": "a person who makes bread and cakes, especially commercially.",
        "eg": "Can you buy a loaf of fresh bread at the baker's?",
        "cn": "你能去面包房买一条新鲜的面包吗？"
    },
    "banana": {
        "forms": {"单数 (Singular)": "banana", "复数 (Plural)": "bananas"},
        "en": "a long curved fruit which grows in clusters and has soft pulpy flesh.",
        "eg": "He likes eating a banana after breakfast.",
        "cn": "他喜欢在早餐后吃一根香蕉。"
    },
    "bandage": {
        "forms": {"单数 (Singular)": "bandage", "复数 (Plural)": "bandages"},
        "en": "a strip of material used to bind up a wound or protect an injury.",
        "eg": "The nurse tied a clean bandage around his injured arm.",
        "cn": "护士在他受伤的手臂上缠了一条干净的绷带。"
    },
    "bank": {
        "forms": {"单数 (Singular)": "bank", "复数 (Plural)": "banks"},
        "en": "a financial establishment, or the land alongside a body of water.",
        "eg": "They walked along the river bank after visiting the bank.",
        "cn": "他们去完银行后沿着河岸散步。"
    },
    "bar": {
        "forms": {"单数 (Singular)": "bar", "复数 (Plural)": "bars", "量词搭配": "a bar of soap/chocolate"},
        "en": "a piece of solid material that is longer than it is wide, or a counter where drinks are served.",
        "eg": "Please give me two bars of chocolate and a tube of toothpaste.",
        "cn": "请给我两块巧克力和一管牙膏。"
    },
    "basket": {
        "forms": {"单数 (Singular)": "basket", "复数 (Plural)": "baskets"},
        "en": "a container made of woven material such as rushes or twigs.",
        "eg": "There are some fresh eggs and apples in the basket.",
        "cn": "篮子里有一些新鲜的鸡蛋和苹果。"
    },
    "bath": {
        "forms": {"单数 (Singular)": "bath", "复数 (Plural)": "baths", "搭配": "have a bath (洗澡)"},
        "en": "an act of washing the body in a tub of water.",
        "eg": "He is having a hot bath in the bathroom right now.",
        "cn": "他现在正在浴室里洗热水澡。"
    },
    "bathroom": {
        "forms": {"单数 (Singular)": "bathroom", "复数 (Plural)": "bathrooms"},
        "en": "a room containing a bath or shower and typically also a washbasin and a toilet.",
        "eg": "The bathroom is on the first floor on the left.",
        "cn": "浴室在二楼的左手边。"
    },
    "beautiful": {
        "forms": {"原级 (Positive)": "beautiful", "比较级 (Comparative)": "more beautiful", "最高级 (Superlative)": "most beautiful"},
        "en": "pleasing the senses or mind aesthetically.",
        "eg": "Paris is one of the most beautiful cities in the world.",
        "cn": "巴黎是世界上最美丽的城市之一。"
    },
    "because": {
        "forms": {"词性 (Part of Speech)": "连词 (Conjunction)", "引导从句": "原因状语从句 (不与 so 连用)"},
        "en": "for the reason that; since.",
        "eg": "I stayed in bed yesterday because I was ill.",
        "cn": "我昨天卧床休息，因为我生病了。"
    },
    "bed": {
        "forms": {"单数 (Singular)": "bed", "复数 (Plural)": "beds", "固定短语": "go to bed / stay in bed"},
        "en": "a piece of furniture for sleep or rest.",
        "eg": "The doctor told him to stay in bed for three days.",
        "cn": "医生嘱咐他卧床休息三天。"
    },
    "bedroom": {
        "forms": {"单数 (Singular)": "bedroom", "复数 (Plural)": "bedrooms"},
        "en": "a room used for sleeping in.",
        "eg": "She is sweeping the floor in the bedroom.",
        "cn": "她正在卧室里扫地。"
    },
    "beef": {
        "forms": {"单数 (Singular)": "beef", "复数 (Plural)": "[不可数名词 Uncountable]"},
        "en": "the flesh of a cow, bull, or ox, used as food.",
        "eg": "Would you like some beef or lamb for dinner tonight?",
        "cn": "今晚晚饭你想吃牛肉还是羊肉？"
    },
    "beer": {
        "forms": {"单数 (Singular)": "beer", "复数 (Plural)": "beers (杯/罐)"},
        "en": "an alcoholic drink made from yeast-fermented malt flavoured with hops.",
        "eg": "He drinks a bottle of cold beer every Saturday evening.",
        "cn": "他每个周六晚上都会喝一瓶冰啤酒。"
    },
    "before": {
        "forms": {"词性 (Part of Speech)": "介词/连词", "基本用法": "在...之前"},
        "en": "during the period of time preceding a particular event or time.",
        "eg": "Wash your hands before you have dinner, please.",
        "cn": "吃晚饭前请洗手。"
    },
    "behind": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "基本用法": "在...后面"},
        "en": "at or to the far side or back of something.",
        "eg": "The kettle is on the stove behind the teapot.",
        "cn": "水壶在炉子上茶壶的后面。"
    },
    "believe": {
        "forms": {"第三人称单数": "believes", "一般过去时": "believed", "过去分词": "believed", "现在分词": "believing"},
        "en": "to accept that something is true, especially without proof.",
        "eg": "I believe that he will pass the examination.",
        "cn": "我相信他会通过这次考试。"
    },
    "belong": {
        "forms": {"第三人称单数": "belongs", "一般过去时": "belonged", "过去分词": "belonged", "常用搭配": "belong to (属于)"},
        "en": "to be the property of someone.",
        "eg": "This handbag belongs to my sister.",
        "cn": "这个手提包属于我姐姐。"
    },
    "beside": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "基本用法": "在...旁边 (靠近)"},
        "en": "at the side of, next to.",
        "eg": "She is sitting beside her mother on the sofa.",
        "cn": "她正坐在沙发上她母亲身旁。"
    },
    "better": {
        "forms": {"原级 (Positive)": "good / well", "比较级 (Comparative)": "better", "最高级 (Superlative)": "best"},
        "en": "more desirable, satisfactory, or effective; partly recovered from illness.",
        "eg": "Do you feel better today? — Yes, thank you.",
        "cn": "你今天感觉好点了吗？— 是的，谢谢。"
    },
    "between": {
        "forms": {"词性 (Part of Speech)": "介词 (Preposition)", "固定搭配": "between... and... (在两者之间)"},
        "en": "in the space separating two objects, points, or people.",
        "eg": "The small village lies between two green hills.",
        "cn": "这个小村庄座落在两座青山之间。"
    },
    "bicycle": {
        "forms": {"单数 (Singular)": "bicycle", "复数 (Plural)": "bicycles", "简称": "bike"},
        "en": "a vehicle composed of two wheels held in a frame one behind the other.",
        "eg": "He rides his bicycle to school every morning.",
        "cn": "他每天早晨骑自行车去上学。"
    },
    "big": {
        "forms": {"原级 (Positive)": "big", "比较级 (Comparative)": "bigger", "最高级 (Superlative)": "biggest"},
        "en": "of considerable size, extent, or intensity.",
        "eg": "They live in a big house with a lovely garden.",
        "cn": "他们住在一栋带着漂亮花园的大房子里。"
    },
    "bill": {
        "forms": {"单数 (Singular)": "bill", "复数 (Plural)": "bills"},
        "en": "a printed or written statement of the money owed for goods or services.",
        "eg": "Can we have the bill, please? We want to pay now.",
        "cn": "请买单好吗？我们现在想付账。"
    },
    "biscuit": {
        "forms": {"单数 (Singular)": "biscuit", "复数 (Plural)": "biscuits", "搭配": "a packet of biscuits"},
        "en": "a small baked unleavened cake, typically crisp, flat, and sweet.",
        "eg": "He ate two sweet biscuits with his afternoon tea.",
        "cn": "他喝下午茶时吃了两块甜饼干。"
    },
    "black": {
        "forms": {"原级 (Positive)": "black", "比较级 (Comparative)": "blacker", "最高级 (Superlative)": "blackest"},
        "en": "of the very darkest colour owing to the absence of or complete absorption of light.",
        "eg": "He is wearing a black coat and a black hat.",
        "cn": "他戴着一顶黑帽子，穿一件黑大衣。"
    },
    "blouse": {
        "forms": {"单数 (Singular)": "blouse", "复数 (Plural)": "blouses"},
        "en": "a woman's upper garment resembling a shirt.",
        "eg": "She bought a white silk blouse yesterday.",
        "cn": "她昨天买了一件白色真丝女衬衫。"
    },
    "blue": {
        "forms": {"原级 (Positive)": "blue", "比较级 (Comparative)": "bluer", "最高级 (Superlative)": "bluest"},
        "en": "of a colour intermediate between green and violet, as of the sky or sea on a sunny day.",
        "eg": "The sky is clear and blue today.",
        "cn": "今天的天空清澈碧蓝。"
    },
    "boat": {
        "forms": {"单数 (Singular)": "boat", "复数 (Plural)": "boats"},
        "en": "a small vessel for travelling over water.",
        "eg": "There are some small boats on the river.",
        "cn": "河上有几只小船。"
    },
    "book": {
        "forms": {"单数 (Singular)": "book", "复数 (Plural)": "books", "动词用法": "book (预订)"},
        "en": "a written or printed work consisting of pages bound together.",
        "eg": "Open your book and turn to Lesson 30, please.",
        "cn": "请打开你的书，翻到第30课。"
    },
    "bookcase": {
        "forms": {"单数 (Singular)": "bookcase", "复数 (Plural)": "bookcases"},
        "en": "a piece of furniture with shelves used for storing books.",
        "eg": "He is going to paint the bookcase pink.",
        "cn": "他打算把那个书架漆成粉红色。"
    },
    "boot": {
        "forms": {"单数 (Singular)": "boot", "复数 (Plural)": "boots"},
        "en": "a sturdy item of footwear covering the foot and ankle.",
        "eg": "You should put on your leather boots today; it is snowing.",
        "cn": "今天下雪了，你该穿上你的皮靴。"
    },
    "bottle": {
        "forms": {"单数 (Singular)": "bottle", "复数 (Plural)": "bottles", "量词搭配": "a bottle of milk"},
        "en": "a glass or plastic container with a narrow neck, used for storing drinks or other liquids.",
        "eg": "Is there any milk in the bottle? — Yes, there is some.",
        "cn": "瓶子里有牛奶吗？— 有，还有一些。"
    },
    "box": {
        "forms": {"单数 (Singular)": "box", "复数 (Plural)": "boxes"},
        "en": "a container with a flat base and sides, typically square or rectangular.",
        "eg": "He put the old books into a large wooden box.",
        "cn": "他把旧书放进了一个大木箱里。"
    },
    "bread": {
        "forms": {"单数 (Singular)": "bread", "复数 (Plural)": "[不可数名词 Uncountable]", "量词搭配": "a loaf / slice of bread"},
        "en": "food made of flour, water, and yeast or another leavening agent, mixed and baked.",
        "eg": "Give me two loaves of bread and some butter, please.",
        "cn": "请给我两条面包和一些黄油。"
    },
    "breakfast": {
        "forms": {"单数 (Singular)": "breakfast", "复数 (Plural)": "breakfasts", "搭配": "have breakfast"},
        "en": "a meal eaten in the morning, the first of the day.",
        "eg": "I usually have bread and a cup of coffee for breakfast.",
        "cn": "我早餐通常吃面包喝一杯咖啡。"
    },
    "bridge": {
        "forms": {"单数 (Singular)": "bridge", "复数 (Plural)": "bridges"},
        "en": "a structure carrying a road, path, railway, or canal across a river, ravine, or road.",
        "eg": "They walked across the stone bridge over the river.",
        "cn": "他们走过了那座横跨河流的石桥。"
    },
    "briefcase": {
        "forms": {"单数 (Singular)": "briefcase", "复数 (Plural)": "briefcases"},
        "en": "a flat, rectangular case with a handle, for carrying books and papers.",
        "eg": "The teacher opened his leather briefcase and took out the exam papers.",
        "cn": "老师打开皮质公文包，拿出了试卷。"
    },
    "brother": {
        "forms": {"单数 (Singular)": "brother", "复数 (Plural)": "brothers"},
        "en": "a man or boy in relation to other sons and daughters of his parents.",
        "eg": "My brother is an engineer in a computer company.",
        "cn": "我兄弟是一家电脑公司的工程师。"
    },
    "brown": {
        "forms": {"原级 (Positive)": "brown", "比较级 (Comparative)": "browner", "最高级 (Superlative)": "brownest"},
        "en": "of a colour produced by mixing red, yellow, and blue.",
        "eg": "He bought a brown leather coat last winter.",
        "cn": "去年冬天他买了一件棕色皮大衣。"
    },
    "bus": {
        "forms": {"单数 (Singular)": "bus", "复数 (Plural)": "buses", "搭配": "by bus / catch a bus"},
        "en": "a large motor vehicle carrying passengers by road.",
        "eg": "Mr. Sawyer usually goes to work by bus.",
        "cn": "索耶先生通常坐公共汽车去上班。"
    },
    "busy": {
        "forms": {"原级 (Positive)": "busy", "比较级 (Comparative)": "busier", "最高级 (Superlative)": "busiest"},
        "en": "having a great deal to do; keeping oneself occupied.",
        "eg": "The doctor is very busy this morning.",
        "cn": "这位医生今天早晨非常忙碌。"
    },
    "but": {
        "forms": {"词性 (Part of Speech)": "连词 (Conjunction)", "基本用法": "但是，然而 (表转折)"},
        "en": "used to introduce a phrase or clause contrasting with what has already been mentioned.",
        "eg": "He speaks French well, but he cannot write it.",
        "cn": "他法语说得很好，但他不会写。"
    },
    "butcher": {
        "forms": {"单数 (Singular)": "butcher", "复数 (Plural)": "butchers", "肉铺": "butcher's"},
        "en": "a person whose trade is the cutting up and selling of meat in a shop.",
        "eg": "My mother bought two pounds of beef at the butcher's.",
        "cn": "我母亲在肉铺买了两磅牛肉。"
    },
    "butter": {
        "forms": {"单数 (Singular)": "butter", "复数 (Plural)": "[不可数名词 Uncountable]"},
        "en": "a pale yellow edible fatty substance made by churning cream and used as a spread or in cooking.",
        "eg": "Put some butter on the bread, please.",
        "cn": "请在面包上抹点黄油。"
    },
    "buy": {
        "forms": {"第三人称单数": "buys", "一般过去时": "bought", "过去分词": "bought", "现在分词": "buying"},
        "en": "to obtain in exchange for payment.",
        "eg": "He bought a new car yesterday.",
        "cn": "他昨天买了一辆新车。"
    }
}
