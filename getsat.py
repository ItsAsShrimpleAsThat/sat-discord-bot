import requests
import random
import html
from enum import Enum
import re

GET_QUESTIONS_API = "https://practicesat.vercel.app/api/get-questions"
QUESTION_BY_ID_API = "https://practicesat.vercel.app/api/question-by-id"

DOMAINS_LOOKUP = { 
                   0: "", 
                   1: "INI", 
                   2: "CAS", 
                   4: "EOI", 
                   8: "SEC", 
                   16: "H", 
                   32: "P", 
                   64: "Q", 
                   128: "S", 
                }

class QuestionType(Enum):
    MULTIPLE_CHOICE = 0
    STUDENT_PRODUCED_RESPONSE = 1

    @classmethod
    def fromMS(cls, ms):
        if ms == "mcq": return cls.MULTIPLE_CHOICE
        elif ms == "spr": return cls.STUDENT_PRODUCED_RESPONSE
        else: raise ValueError('Expected "mcq" or "spr"')

class QuestionDifficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

    @classmethod
    def fromEMH(cls, emh):
        if emh == "E": return cls.EASY
        elif emh == "M": return cls.MEDIUM
        elif emh == "H": return cls.HARD
        else: raise ValueError('Expected "E", "M", or "H"')

class Question():
    def __init__(self, id:str, difficulty:QuestionDifficulty, skill:str, domain:str, type:QuestionType, ansOptions, ansCorrect, rationale:str, stimulus:str, stem:str):
        self.id = id
        self.difficulty = difficulty
        self.skill = skill
        self.domain = domain

        self.ansOptions = ansOptions
        self.ansCorrect = ansCorrect
        self.rationale = rationale
        self.stimulus = stimulus
        self.stem = stem
        self.type = type

def getDomains(information_and_ideas:bool,
               craft_and_structure:bool,
               expression_of_ideas:bool,
               standard_english_conventions:bool,
               algebra:bool,
               advanced_math:bool,
               problem_solving_data_analysis:bool,
               geometry_and_trig:bool):
    num = 0
    num = num | (1 << 0) if information_and_ideas else num
    num = num | (1 << 1) if craft_and_structure else num
    num = num | (1 << 2) if expression_of_ideas else num
    num = num | (1 << 3) if standard_english_conventions else num
    num = num | (1 << 4) if algebra else num
    num = num | (1 << 5) if advanced_math else num
    num = num | (1 << 6) if problem_solving_data_analysis else num
    num = num | (1 << 7) if geometry_and_trig else num
    return num

def getQuestionsRequestURL(domains:int):
    querystring = ""
    for i in range(8):
        masked = domains & (1 << i)
        domainID = DOMAINS_LOOKUP[masked]

        if(domainID != ""):
            querystring += domainID + ","

    querystring = querystring.removesuffix(",")
    return GET_QUESTIONS_API + "?domains=" + querystring

def getQuestions(domains:int):
    response = requests.get(getQuestionsRequestURL(domains))
    
    if(response.status_code == 200):
        return response.json()
    else:
        print(f"error requestion questions. status: {response.status_code}, message: {response.text}")

def getQuestionByID(id:str):
    url = QUESTION_BY_ID_API + "/" + id
    response = requests.get(url)
    
    if(response.status_code == 200):
        return response.json()
    else:
        print(f"error requestion questions. status: {response.status_code}, message: {response.text}")

def discordifyHTML(rawhtml:str):
    noEntities = html.unescape(rawhtml)

    discordified = re.sub(r'[\u00A0\u2007\u202F]+', " ", noEntities).strip()
    discordified = re.sub("<p.*?>", "", discordified)
    discordified = re.sub("</p.*?>", "\n", discordified)

    discordified = re.sub("</?em.*?>", "***", discordified)
    discordified = str.replace(discordified, "_", "\\_")

    discordified = discordified.removesuffix("\n")
    return discordified

def getRandomQuestion(domains:int):
    questions = getQuestions(domains)["data"]
    questionID = questions[random.randint(0, len(questions) - 1)].get("questionId")

    questionjson = getQuestionByID(questionID).get("data")
    
    question = questionjson.get("question")
    problem = questionjson.get("problem")
    
    return Question(
        question.get("questionId"),
        QuestionDifficulty.fromEMH(question.get("difficulty")),
        question.get("skill_desc"),
        question.get("primary_class_cd_desc"),
        QuestionType.fromMS(problem.get("type")),
        { k: discordifyHTML(v) for k, v in problem.get("answerOptions", dict()).items() },
        list(map(discordifyHTML, problem.get("correct_answer", []))),
        discordifyHTML(problem.get("rationale")),
        discordifyHTML(problem.get("stimulus")),
        discordifyHTML(problem.get("stem"))
    )
    
    
# randQuestion = getRandomQuestion(1)

# print(randQuestion.id)
# print(randQuestion.difficulty)
# print(randQuestion.skill)
# print(randQuestion.domain)
# print(randQuestion.type)
# print(randQuestion.ansOptions)
# print(randQuestion.ansCorrect)
# print(randQuestion.rationale)
# print(randQuestion.stimulus)
# print(randQuestion.stem)