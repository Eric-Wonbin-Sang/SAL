import os

from General import Functions


class EnvProfile:

    api_keys_dir = Functions.get_curr_parent_dir() + "/API Keys"
    secrets_dir = Functions.get_curr_parent_dir() + "/API Keys/SAL"
    env_profiles_dir = "EnvProfiles"
    common_json_path = env_profiles_dir + "/common.json"

    def __init__(self, env_key):

        self.env_key = env_key

        self.common_dict = self.get_common_dict()
        self.profile_dict = self.get_profile_dict()

    def get_json_path(self):
        for filename in os.listdir(EnvProfile.env_profiles_dir):
            if self.env_key == "".join(filename.split(".json")[:-1]):
                return EnvProfile.env_profiles_dir + "/" + filename
        raise UserWarning("env_key does not exist in EnvProfiles dir")

    def get_common_dict(self):
        for key, value in (data_dict := Functions.parse_json(EnvProfile.common_json_path)).items():
            if "{api_keys_dir}" in value:
                data_dict[key] = value.format(api_keys_dir=self.api_keys_dir)
        return data_dict

    def get_profile_dict(self):
        for key, value in (data_dict := Functions.parse_json(self.get_json_path())).items():
            if "{secrets_dir}" in value:
                data_dict[key] = Functions.parse_json(value.format(secrets_dir=self.secrets_dir))
        return data_dict
