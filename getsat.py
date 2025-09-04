import requests

GET_QUESTIONS_API = "https://practicesat.vercel.app/api/get-questions"
QUESTION_BY_ID_API = "https://practicesat.vercel.app/api/question-by-id/"

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

