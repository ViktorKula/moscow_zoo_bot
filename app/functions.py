from quiz import questions
import random


def get_totem_animal(user_answers):
    totem_count = {
        "Тигр": 0,
        "Слон": 0,
        "Енот": 0,
        "Пингвин": 0,
        "Лиса": 0,
        "Фламинго": 0,
        "Черепаха": 0,
        "Лягушка": 0,
        "Ёж": 0,
        "Капибара": 0,
    }
    for answer in user_answers:
        for question in questions:
            if answer in question['answer']:
                for animal in question['answer'][answer]:
                    totem_count[animal] += 1

    max_count = max(totem_count.values())
    totem_animals = [animal for animal, count in totem_count.items() if count == max_count]

    if len(totem_animals) == 1:
        return totem_animals[0]
    else:
        return random.choice(totem_animals)


def get_animal_photo(totem_animal):
    paths = {
        'Тигр': '.\\photo\\tiger.jpeg',
        'Слон': '.\\photo\\elephant.jpeg',
        'Енот': '.\\photo\\racoon.jpg',
        'Пингвин': '.\\photo\\penguin.jpeg',
        'Лиса': '.\\photo\\fox.jpeg',
        'Фламинго': '.\\photo\\flamingo.jpeg',
        'Черепаха': '.\\photo\\turtle.jpeg',
        'Лягушка': '.\\photo\\frog.jpeg',
        'Ёж': '.\\photo\\hedgehog.jpeg',
        'Капибара': '.\\photo\\kapibara.jpg',
    }
    return paths.get(totem_animal)
