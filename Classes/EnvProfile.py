import os

from General import Functions


class EnvProfile:

    common_dir = Functions.get_curr_parent_dir() + "/0 - Secrets/SAL/common"
    env_profiles_dir = Functions.get_curr_parent_dir() + "/0 - Secrets/SAL/EnvProfiles"

    def __init__(self, env_key):

        self.env_key = env_key

        self.google_sheets_creds = self.common_dir + "/Google API - StevensLTBots.json"
        self.groupme_access_token = self.common_dir + "/Groupme Access Token.txt"
        self.yahoo_weather_api_json = self.common_dir + "/yahoo_weather_api_creds.json"

        self.profile_json_path = self.get_profile_json_path()
        self.profile_dict = Functions.parse_json(self.profile_json_path)

    def get_profile_json_path(self):
        for filename in os.listdir(EnvProfile.env_profiles_dir):
            if self.env_key == filename.split(".json")[0]:
                return EnvProfile.env_profiles_dir + "/" + filename
        raise UserWarning("env_key {} does not exist in EnvProfiles dir".format(self.env_key))
