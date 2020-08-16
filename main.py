import argparse
import datetime

from Classes import Sal, EnvProfile
from lib import GroupMe
from General import Functions


def get_args():
    parser = argparse.ArgumentParser(description='This is the Stevens Automation Loader.')
    parser.add_argument('--env_key', type=str, default="dev", help='an integer for the accumulator')
    return parser.parse_args()


def main():

    args = get_args()

    env_profile = EnvProfile.EnvProfile(env_key=args.env_key)
    group = GroupMe.GroupChat(id=env_profile.profile_dict["credentials_json"]["groupchat_id"],
                              groupme_access_token=open(env_profile.common_dict["groupme_access_token"]).read())
    sal_bot = Sal.Sal(env_profile, group)

    prev_message = None
    while True:

        curr_message = sal_bot.group.get_newest_valid_message()

        if curr_message and prev_message and curr_message.created_at != prev_message.created_at:
            print(curr_message)

            if sal_bot.is_bot_called(curr_message):
                sal_bot.write_text("hello")

        prev_message = curr_message

        # if curr_message and curr_message != prev_message:
        #
        #     if prev_message and prev_message.text != curr_message.text:
        #         print("{} - {}: {}".format(curr_message.created_at, curr_message.name, curr_message.text))
        #
        #     if sal_bot.is_bot_called(curr_message):
        #         sal_bot.write_text("hello")
        #
        #     prev_message = curr_message


if __name__ == '__main__':
    main()
