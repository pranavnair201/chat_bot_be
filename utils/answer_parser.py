

def ans_parser(answer):
    prefixes = ['\nAI:', '\nSystem:', '\nAnswer:']
    for prefix in prefixes:
        # if answer.startswith(prefix):
        answer = answer.replace(prefix, '\n')
    return answer