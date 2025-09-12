import requests
import random
import html
from enum import Enum
import re
import os
import htmlrender

GET_QUESTIONS_API = "https://practicesat.vercel.app/api/get-questions"
QUESTION_BY_ID_API = "https://practicesat.vercel.app/api/question-by-id"

BIN = "/home/container/wk/bin/wkhtmltoimage" #in server
LIB = "/home/container/wk/lib"
os.environ["LD_LIBRARY_PATH"] = LIB + ":" + os.environ.get("LD_LIBRARY_PATH", "")

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

    def toString(self):
        stringLookup = { QuestionDifficulty.EASY: "Easy",
                         QuestionDifficulty.MEDIUM: "Medium",
                         QuestionDifficulty.HARD: "Hard" }

        return stringLookup.get(self)        

class Question():
    def __init__(self, id:str, difficulty:QuestionDifficulty, skill:str, domain:str, type:QuestionType, ansOptions, ansCorrect, rationale:str, stimulus:str, stem:str, images:list):
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
        self.images = images

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

def discordifyTable(tablematch):
    tablehtml = tablematch.group()
    
    caption = re.search("<caption.*?>.*?<p.*?>(.*?)</p>.*?</caption>", tablehtml).group(1)
    

    # table = "## " + re.search("<caption.*?>(.*?)</caption>", tablehtml)
    seperatedtheadMatch = re.search("<thead.*?>(.*?)</thead>(.*)", tablehtml)
    insidethead = seperatedtheadMatch.group(1)
    outsidethead = seperatedtheadMatch.group(2)
    tableHeaders = re.findall("<th\\b.*?>(.*?)</th>", insidethead)

    tableRows = re.findall("<tr\\b.*?>(.*?)</tr>", outsidethead)

    for i in range(len(tableRows)):
        row = re.findall("<td\\b.*?>(.*?)</td>|<th\\b.*?>(.*?)</th>", tableRows[i])

        tableRows[i] = [c[0] or c[1] for c in row]

    numRows = len(tableRows)
    numColumns = len(tableHeaders)
    columnWidths = [0] * numColumns
    
    for i in range(numColumns):
        columnWidths[i] = max(columnWidths[i], len(tableHeaders[i]))

        for j in range(numRows):
            columnWidths[i] = max(columnWidths[i], len(tableRows[j][i]))


    discordified = "# " + caption + "\n```"
    for i in range(len(tableHeaders)):
        discordified += tableHeaders[i]
        discordified += (" " * (columnWidths[i] - len(tableHeaders[i]) + (2 if i < numColumns - 1 else 0)))

    discordified += "\n"
    discordified += "-" * ((len(tableHeaders) - 1) * 2 + sum(columnWidths))

    for i in range(len(tableRows)):
        discordified += "\n"
        for j in range(len(tableRows[i])):
            discordified += tableRows[i][j]
            discordified += (" " * (columnWidths[j] - len(tableRows[i][j]) + (2 if j < numColumns - 1 else 0)))

    discordified += "```"
    return discordified
    
# discordifyTable(r'<thead><tr><th scope="col" style="text-align: center;vertical-align: bottom;">Country</th><th scope="col" style="text-align: center;vertical-align: bottom;">1995</th><th scope="col" style="text-align: center;vertical-align: bottom;">2020</th></tr></thead><tbody><tr><th scope="row" style="text-align: left;">Canada</th><td style="text-align: center;">0.73</td><td style="text-align: center;">0.59</td></tr><tr><th scope="row" style="text-align: left;">Indonesia</th><td style="text-align: center;">0.44</td><td style="text-align: center;">0.51</td></tr><tr><th scope="row" style="text-align: left;">Kazakhstan</th><td style="text-align: center;">0.26</td><td style="text-align: center;">0.55</td></tr><tr><th scope="row" style="text-align: left;">Chile</th><td style="text-align: center;">2.49</td><td style="text-align: center;">5.73</td></tr></tbody>')

def discordifyHTML(rawhtml:str, images:list=[]):
    print(rawhtml)
    print("-------------------------------")
    noEntities = html.unescape(rawhtml)

    discordified = re.sub(r'[\u00A0\u2007\u202F]+', " ", noEntities).strip()
    imagehtmls = re.findall("<figure.*?>.*?</figure>", discordified)

    for imagehtml in imagehtmls:
        images.append(htmlrender.getImageBytes(imagehtml))

    discordified = re.sub("<p.*?>", "", discordified)
    discordified = re.sub("</p.*?>", "\n", discordified)

    discordified = re.sub("</?em.*?>", "*", discordified)
    discordified = re.sub("<span.*?>blank</span>", "", discordified)
    discordified = re.sub("</?span.*?>", "", discordified)
    discordified = str.replace(discordified, "_", "\\_")

    discordified = discordified.removesuffix("\n")
    return discordified

def getRandomQuestion(domains:int):
    questions = getQuestions(domains)["data"]
    questionID = questions[random.randint(0, len(questions) - 1)].get("questionId")

    questionjson = getQuestionByID(questionID).get("data")
    
    question = questionjson.get("question")
    problem = questionjson.get("problem")
    images = []
    
    return Question(
        question.get("questionId"),
        QuestionDifficulty.fromEMH(question.get("difficulty")),
        question.get("skill_desc"),
        question.get("primary_class_cd_desc"),
        QuestionType.fromMS(problem.get("type")),
        { k: discordifyHTML(v) for k, v in problem.get("answerOptions", dict()).items() },
        list(map(discordifyHTML, problem.get("correct_answer", []))),
        discordifyHTML(problem.get("rationale", "")),
        discordifyHTML(problem.get("stimulus" , ""), images),
        discordifyHTML(problem.get("stem", ""), images),
        images
    )
    
# print(discordifyHTML(r'<p><figure class="table"><table class="gdr"><caption style="caption-side: top;"><p style="text-align: center;">Millions of Metric Tons of Copper Mined in 1995 and 2020</p></caption><thead><tr><th scope="col" style="text-align: center;vertical-align: bottom;">Country</th><th scope="col" style="text-align: center;vertical-align: bottom;">1995</th><th scope="col" style="text-align: center;vertical-align: bottom;">2020</th></tr></thead><tbody><tr><th scope="row" style="text-align: left;">Canada</th><td style="text-align: center;">0.73</td><td style="text-align: center;">0.59</td></tr><tr><th scope="row" style="text-align: left;">Indonesia</th><td style="text-align: center;">0.44</td><td style="text-align: center;">0.51</td></tr><tr><th scope="row" style="text-align: left;">Kazakhstan</th><td style="text-align: center;">0.26</td><td style="text-align: center;">0.55</td></tr><tr><th scope="row" style="text-align: left;">Chile</th><td style="text-align: center;">2.49</td><td style="text-align: center;">5.73</td></tr></tbody></table></figure></p>'))
    
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