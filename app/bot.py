import telebot
from telebot import types
from quiz import TOKEN, quiz_data, questions, review, result
from functions import get_totem_animal, get_animal_photo

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    username = message.chat.username if message.chat.username else "пользователь"

    photo = open('./photo/Timosha.jpeg', 'rb')
    bot.send_photo(
        message.chat.id,
        photo,
        caption=(
            f'Привет, {username}! Меня зовут Манул Тимоша🐱. '
            'Я живу в Московском Зоопарке. '
            f'Хочешь узнать свое тотемное животное? '
            'Нажми на эту кнопочку и ты узнаешь: /letsgo'
        )
    )
    photo.close()


@bot.message_handler(commands=['letsgo'])
def start_quiz(message):
    user_id = message.chat.id
    if user_id not in quiz_data:
        quiz_data[user_id] = {'current_question': 0, 'answers': []}
    send_questions(user_id)


@bot.message_handler(commands=['getreview'])
def get_review(admin_id):
    admin_id = '588200056'
    for rev in review:
        bot.send_message(admin_id, rev)


def send_questions(user_id):
    user = quiz_data.get(user_id)
    if not user:
        bot.send_message(user_id, "Сначала пройдите викторину.")
        return

    question_index = user['current_question']
    try:
        if question_index < len(questions):
            question_data = questions[question_index]
            question_text = question_data['question']
            answers = question_data['answer']

            markup = types.InlineKeyboardMarkup()
            for answer in answers.keys():
                markup.add(types.InlineKeyboardButton(text=answer, callback_data=f'{question_index}_{answer}'))
            bot.send_message(user_id, question_text, reply_markup=markup)
        else:
            result[user_id] = get_totem_animal(user['answers'])
            totem_animal = get_totem_animal(user['answers'])
            photo = open(get_animal_photo(totem_animal), 'rb')

            markup_end = types.InlineKeyboardMarkup()
            markup_end.add(types.InlineKeyboardButton(text='Поделиться результатом в соцсетях', callback_data='share'))
            markup_end.add(types.InlineKeyboardButton(text='Узнать больше о Программе опеки в Московском зоопарке', url='https://moscowzoo.ru/about/guardianship'))
            markup_end.add(types.InlineKeyboardButton(text='Оставить отзыв', callback_data='review'))
            markup_end.add(types.InlineKeyboardButton(text='Задать вопрос сотруднику Зоопарка', callback_data='question'))
            markup_end.add(types.InlineKeyboardButton(text='Пройти викторину заново', callback_data='replay'))

            bot.send_photo(user_id, photo, caption=(
                f'Твоё тотемное животное это - {totem_animal}!'
                f'А ты знал, что {totem_animal} нуждается в опекуне? '
                'И ты без труда можешь им стать! '
                'Всю информацию о программе опекунства в Московском зоопарке ты сможешь найти по '
                'ссылке ниже. '
                'Возьмите животное под опеку! Станьте участником программы «Клуб друзей зоопарка».'
            ), reply_markup=markup_end)
            photo.close()

    except Exception as e:
        bot.send_message(user_id, "Произошла ошибка. Пожалуйста, попробуйте снова.")
        print(f"Error: {e}")
        quiz_data[user_id]['current_question'] = 0
        quiz_data[user_id]['answers'] = []


@bot.callback_query_handler(func=lambda call: '_' in call.data)
def callback_query(call):
    user_id = call.message.chat.id
    user = quiz_data[user_id]

    question_index, user_answer = call.data.split('_')
    question_index = int(question_index)

    user['answers'].append(user_answer)
    user['current_question'] = question_index + 1
    send_questions(user_id)


@bot.callback_query_handler(func=lambda call: call.data in ['replay', 'review', 'question', 'share'])
def handle_special_buttons(call):
    user_id = call.message.chat.id
    if call.data == 'replay':
        if user_id in quiz_data:
            del result[user_id]
            quiz_data[user_id]['current_question'] = 0
            quiz_data[user_id]['answers'] = []
            send_questions(user_id)
        else:
            bot.send_message(user_id, "Нет активной викторины для перезапуска.")

    elif call.data == 'review':
        mesg = bot.send_message(user_id,
                                'Оставьте отзыв в графе сообщения\nЭто поможет нам стать лучше для вас\nПолностью анонимно')
        bot.register_next_step_handler(mesg, add_review)

    elif call.data == 'question':
        ques = bot.send_message(user_id,
                                'Введите ваш вопрос в графе сообщения в формате:\n<Ваш вопрос>\n<@UserName для обратной связи>')
        bot.register_next_step_handler(ques, send_ques)

    elif call.data == 'share':
        bot.send_message(user_id, "Поделитесь своим результатом в соцсетях!")

    bot.answer_callback_query(call.id)


def add_review(message):
    review.append(message.text)
    bot.send_message(message.chat.id, 'Спасибо за оставленный отзыв!')


def send_ques(message):
    user_id = message.chat.id
    admin_id = '588200056'
    ques = f'Результат викторины: {result[user_id]}\nСообщение: {message.text}'
    bot.send_message(chat_id=admin_id, text=ques)
    bot.send_message(user_id, 'Ваше сообщение успешно отправлено!')


if __name__ == "__main__":
    bot.polling(none_stop=True)