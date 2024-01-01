import re


def parser(answer):
    link_pattern = re.compile(r'https?://\S+')
    results = link_pattern.findall(answer)

    for result in results:
        answer = answer.replace(f" {result}", f' [Link]({result})')

    return answer
