import telebot
import random
import config

bot = telebot.TeleBot(config.TOKEN)
key = ""
again = False


def check(message):
    global again
    for j in used:
        if not used[j]:
            return True
    again = True
    bot.send_message(message.chat.id, "Congratulations, you've tried to translate all the words you've got!\nStart "
                                      "over?\n")
    return False
    # if again == "no":
    #     print("Nice work, see ya)")
    #     exit(0)
    # for j in used:
    #     used[j] = False


words = []
eng_ru_words = {}
used = {}
with open('words.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        key = ""
        s = 0
        while line[s + 1] != '-':
            key += line[s]
            s += 1
        s += 1
        words.append(key)
        used[key] = False
        us = ""
        uk = ""
        flag = False
        for i in range(s, len(line)):
            if line[i] == ',':
                flag = True
                continue
            if flag:
                if line[i] != '-' and line[i] != '\n':
                    uk += line[i]
            else:
                if line[i] != '-' and line[i] != '\n':
                    us += line[i]
            if len(uk) != 0:
                if uk[0] == ' ':
                    uk = uk[1:len(uk)]
            if len(us) != 0:
                if us[0] == ' ':
                    us = us[1:len(us)]
        eng_ru_words[key] = [uk, us]


@bot.message_handler(commands=['start'])
def welcome(message):
    global key
    bot.send_message(message.chat.id,
                     "Hello adventurer {0.first_name}!\nI'm <b>{1.first_name}</b>, let's practise some English".format(
                         message.from_user, bot.get_me()), parse_mode='html'
                     )
    key = random.choice(words)
    bot.send_message(message.chat.id,
                     "What is an English (or American) equivalent for the '{}'?".format(key))


@bot.message_handler(content_types=['text'])
def answer(message):
    global key
    if message.chat.type == 'private':
        reply = message.text
        if key != "":
            if check(message):
                used[key] = True
                eng = eng_ru_words[key]
                if reply in eng and reply != '':
                    bot.send_message(message.chat.id, "Oh yes, you're right.")
                    if '' not in eng:
                        bot.send_message(message.chat.id, "Also check the {} option: '{}'.".format(
                            "US" if eng[0] == reply else "UK", eng[1] if eng[0] == reply else eng[0]
                        ))
                else:
                    if '' in eng:
                        bot.send_message(message.chat.id, "Oh no, you are wrong.\nThe right answer is '{}'.".format(eng[0] if eng[0] != '' else eng[1]))
                    else:
                        bot.send_message(message.chat.id, "Oh no, you are wrong.\nThe right answer is"
                                                          " '{}'(US) or '{}'(UK)".format(eng[0], eng[1]))
                while used[key]:
                    key = random.choice(words)
                bot.send_message(message.chat.id, "What is an English (or American) equivalent for the '{}'?".format(key))
            else:
                key = ""
        else:
            if again:
                if reply in ["no", "No", "nope", "Nope", "нет", "не"]:
                    bot.send_message(message.chat.id, "See you later!")
                    return
                else:
                    bot.send_message(message.chat.id, "OK, the more the better!")
                    key = random.choice(words)
                    for j in used:
                        used[j] = False
                    bot.send_message(message.chat.id,
                                     "What is an English (or American) equivalent for the '{}'?".format(key))


# RUN
bot.polling(none_stop=True)