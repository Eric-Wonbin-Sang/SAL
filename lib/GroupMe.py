import requests
import time
import datetime


groupme_character_limit = 450
groupme_tab = "    "


class GroupChat:

    def __init__(self, **kwargs):

        self.id = kwargs.get("id")
        self.groupme_access_token = kwargs.get("groupme_access_token")
        self.refresh_rate = kwargs.get("refresh_rate", 1)

    def get_message_list(self):
        while True:
            try:
                overall_response = requests.get('https://api.groupme.com/v3/groups/{id}/messages'.format(id=self.id),
                                                params={'token': self.groupme_access_token})
                if overall_response.status_code == 200:
                    return [Message(raw_message) for raw_message in overall_response.json()['response']['messages']]
                return []
            except Exception as e:
                print(type(e), e)

    def get_newest_valid_message(self):
        return message_list[0] if (message_list := self.get_message_list()) and message_list[0].text != "" else None

    def get_first_valid_message(self):
        while True:
            if curr_message := self.get_newest_valid_message():
                return curr_message
            time.sleep(self.refresh_rate)


class Message:

    def __init__(self, raw_message):

        self.raw_message = raw_message

        self.attachments = raw_message["attachments"]
        self.avatar_url = raw_message["avatar_url"]
        self.created_at = datetime.datetime.fromtimestamp(raw_message["created_at"])
        self.favorited_by = raw_message["favorited_by"]
        self.group_id = raw_message["group_id"]
        self.id = raw_message["id"]
        self.name = raw_message["name"]
        self.sender_id = raw_message["sender_id"]
        self.sender_type = raw_message["sender_type"]
        self.source_guid = raw_message["source_guid"]
        self.system = raw_message["system"]
        self.text = raw_message["text"]
        self.user_id = raw_message["user_id"]
        self.platform = raw_message["platform"]

    def __str__(self):
        return "{} {} - {}".format(self.created_at, self.name, self.text)


class Bot:

    def __init__(self, name, call_code, bot_id, groupchat_id , groupme_access_token):

        self.name = name
        self.call_code = call_code
        self.bot_id = bot_id

        self.groupchat_id = groupchat_id
        self.groupme_access_token = groupme_access_token
        self.group = self.get_group()

        self.character_limit = groupme_character_limit

    def get_group(self):
        return GroupChat(id=self.groupchat_id, groupme_access_token=self.groupme_access_token)

    def is_bot_called(self, message):
        return message.text.lower().startswith(self.call_code.lower())

    def write_text(self, text):

        str_ret_list = []

        output_string = ""
        for i, split_text in enumerate(text.split("\n")):
            if i != 0:
                output_string += "\n"
            if len(output_string + split_text) >= self.character_limit:
                if output_string[-1] == "\n":
                    str_ret_list.append(output_string[:-1])     # this removes the trailing newline
                else:
                    str_ret_list.append(output_string)
                output_string = ""
            output_string += split_text
        if output_string != "":
            str_ret_list.append(output_string)

        print("------------ SAL Response ----------")
        for str_ret in str_ret_list:
            for string in [str_ret[0 + i:self.character_limit + i]
                           for i in range(0, len(str_ret), self.character_limit)]:
                time.sleep(1)
                print(string)
                requests.post('https://api.groupme.com/v3/bots/post', params={'bot_id': self.bot_id, 'text': string})
        print("-----------------------------------")
