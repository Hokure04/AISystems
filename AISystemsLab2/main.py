from pyswip import Prolog
import re
from templates_translation import templates, character_translation

prolog = Prolog()
prolog.consult("game.pl")


def query_parser(question):
    question = translate(question)
    query = question.lower()
    query = re.sub(r'[^\w\s]', '', query)

    for template in templates:
        match = re.search(template["pattern"], query)
        if match:
            # Проверка есть ли группа ответов
            if match.lastindex is not None and match.lastindex >= 1:
                return template["query"](match.group(1).strip())
            else:
                return template["query"](None)

    return None


def response(query_str):
    try:
        result = list(prolog.query(query_str))

        if result:
            if "Count" in result[0]:
                return f"Количество способностей: {result[0]['Count']}"
            elif "Ability" in result[0]:
                abilities = ', '.join(res['Ability'] for res in result)
                return f"Способности: {abilities}"
            elif "X" in result[0]:
                characters = ', '.join(res['X'] for res in result)
                return f"Персонажи: {characters}"
            elif "Foe" in result[0]:
                foes = ', '.join(res['Foe'] for res in result)
                return f"{foes}"
            elif "List" in result[0]:
                if result[0]['List']:
                    count = result[0]['Count']
                    return f"Персонаж победил {count} врагов"
                else:
                    return "Персонаж никого не победил"
            elif "Ally" in result[0]:
                allies = ', '.join(res['Ally'] for res in result)
                return f"Союзники: {allies}"
            else:
                return "Да"
        else:
            return "Нет"
    except Exception as e:
        return f"Ошибка: {str(e)}"


def show():
    print("Все шаблоны запросов:")
    for idx, template in enumerate(templates, 1):
        print(f"{idx}. {template['pattern']}")


def translate(question):
    for rus_name, en_name in character_translation.items():
        question = question.replace(rus_name, en_name)
    return question


def user_input():
    while True:
        input_from_user = input("Введите вопрос или 'stop' для выхода: ")
        if input_from_user.lower() == "stop":
            break
        elif input_from_user.lower() == "show":
            show()
        else:
            prolog_query = query_parser(input_from_user)
            if prolog_query:
                result = response(prolog_query)
                print(result)
            else:
                print("Извините, не получилось разобрать запрос")


user_input()
