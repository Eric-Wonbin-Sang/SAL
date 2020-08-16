from lib import GroupMe

from General import Constants, Functions


class Sal(GroupMe.Bot):

    def __init__(self, env_profile, group):

        self.env_profile = env_profile
        self.group = group

        super().__init__(name=self.env_profile.profile_dict["name"],
                         call_code=self.env_profile.profile_dict["call_code"],
                         bot_id=self.env_profile.profile_dict["credentials_json"]["bot_id"],
                         groupchat_id=self.env_profile.profile_dict["credentials_json"]["groupchat_id"],
                         groupme_access_token=open(env_profile.common_dict["groupme_access_token"]).read())
