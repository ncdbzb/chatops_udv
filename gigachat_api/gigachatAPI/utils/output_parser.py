import re


async def parse_output(text: str, current_que_number: int = 0, total_que_number: int = 0) -> tuple[str, int]:
    pattern = re.compile(r"(\d+\. .*?\n(a\) .*?\n|b\) .*?\n|c\) .*?\n|d\) .*?\n)+)")

    matches = pattern.findall(text)[:total_que_number] if total_que_number else pattern.findall(text)

    result = ''
    for num, i in enumerate(matches, start=1):
        result += f'{num}{i[0][i[0].index("."):]}'
        if i != matches[-1]:
            result += '\n'
    if current_que_number:
        return result, total_que_number - len(matches)
    else:
        return result, 0
