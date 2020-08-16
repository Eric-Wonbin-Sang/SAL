from lib import GroupMe

from Classes import EnvProfile
from General import Constants, Functions


class Sal(GroupMe.Bot):

    def __init__(self, env_key):

        self.env_profile = EnvProfile.EnvProfile(env_key=env_key)

        super().__init__(name=self.env_profile.profile_dict["name"],
                         call_code=self.env_profile.profile_dict["call_code"],
                         bot_id=self.env_profile.profile_dict["credentials_json"]["bot_id"],
                         groupchat_id=self.env_profile.profile_dict["credentials_json"]["groupchat_id"],
                         groupme_access_token=open(self.env_profile.common_dict["groupme_access_token"]).read())

    def watch_messages(self):
        prev_message = None
        while True:

            curr_message = self.group.get_newest_valid_message()

            if curr_message and prev_message and curr_message.created_at != prev_message.created_at:

                if curr_message.name != self.name:
                    print(curr_message)
                else:
                    print("----------- SAL Response ----------")
                    print(curr_message)
                    print("-----------------------------------")

                if curr_message.name != self.name and self.is_bot_called(curr_message):
                    self.write_text("hello")

            prev_message = curr_message
