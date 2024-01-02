import re


def parser(answer):
    link_pattern = re.compile(r'https?://\S+')
    results = link_pattern.findall(answer)

    for result in results:
        if result[-1] in ['.']:
            result = result[:-1]
        answer = answer.replace(f" {result}", f' [Link]({result})')

    return answer
