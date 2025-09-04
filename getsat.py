def getDomains(information_and_ideas,
               craft_and_structure,
               expression_of_ideas,
               standard_english_conventions,
               algebra,
               advanced_math,
               problem_solving_data_analysis,
               geometry_and_trig):
    num = 0
    num = num | (1 << 0) if information_and_ideas else num
    num = num | (1 << 1) if craft_and_structure else num
    num = num | (1 << 2) if expression_of_ideas else num
    num = num | (1 << 3) if standard_english_conventions else num
    num = num | (1 << 4) if algebra else num
    num = num | (1 << 5) if advanced_math else num
    num = num | (1 << 6) if problem_solving_data_analysis else num
    num = num | (1 << 7) if geometry_and_trig else num

def getQuestions():
    pass