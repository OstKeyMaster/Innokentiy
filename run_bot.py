import random

import requests
import vk_api
from config import *
from origami import *


def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 1000)})


def write_msg_attach(user_id, text, att_url):
    vk_bot.method('messages.send', {'user_id': user_id,
                                    'attachment': att_url,
                                    'message': text,
                                    'random_id': random.randint(0, 1000)})


def mark_read(user_id):
    st_mes = update[0][1]
    vk_bot.method('messages.markAsRead', {'peer_id': user_id,

                                          'start_message_id': st_mes})
def get_wall3last():
    vk_bot.method('photos.get', {'owner_id': GROUP_ID, 'count': 3,})

vk_bot = vk_api.VkApi(token=TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll["ts"]
print("готов к работе" + str(long_poll))

while True:
    long_poll = requests.get(
        'https://{server}?act={act}&key={key}&ts={ts}&wait=500'.format(server=server,
                                                                       act='a_check',
                                                                       key=key,
                                                                       ts=ts)).json()

    update = long_poll['updates']
    if update[0][0] == 4:
        print(update)
        user_id = update[0][3]
        usr_txt = update[0][6]

        if 'Хочу' in usr_txt and 'оригами' in update[0][6]:
            write_msg(user_id, CATEG_LIST)
        elif 'амолёт' in update[0][6] or '1' in update[0][6]:  # PLANES
            write_msg_attach(user_id, PLANE_LIST, 'photo-174738498_456239022')

            # send pics from album


        elif 'Кто ты' in usr_txt or 'Ты кто' in usr_txt:
            group_info = vk_bot.method('groups.getById', {'group_id': GROUP_ID, 'fields': 'name'})
            write_msg(user_id, 'Я - ' + group_info[0]['name'] + ', твой друг и товарищ))')
        elif 'фотку' in usr_txt:
            write_msg_attach(user_id, 'Лови', 'photo358546480_456240994')  # some features


        else:
            user_name = vk_bot.method('users.get', {'user_ids': user_id})
            if 'Чуитс' in usr_txt:
                write_msg(user_id, 'Чуитс, ' + (user_name[0]['first_name']))
            elif 'Привет' in usr_txt:
                write_msg(user_id, 'Привет, ' + (user_name[0]['first_name']))
            print(str(user_name[0]['first_name']) + ' ' +
                  str(user_name[0]['last_name']) + ' написал(а) боту - ' + str(usr_txt))  # msg for us

        mark_read(user_id)
    # Меняем ts для следующего запроса
    ts = long_poll['ts']
