import argparse

from Classes.SalClasses import Sal


def get_args():
    parser = argparse.ArgumentParser(description='This is the Stevens Automation Loader.')
    parser.add_argument('--env_key', type=str, default="dev", help='an integer for the accumulator')
    parser.add_argument('--do_startup_message', type=str, default="true", help='Bool if bot should do startup message.')

    args = parser.parse_args()
    args.do_startup_message = args.do_startup_message.lower() == "true"
    return args


def main():

    args = get_args()

    sal_bot = Sal.Sal(env_key=args.env_key, do_startup_message=args.do_startup_message)
    sal_bot.watch_messages()


if __name__ == '__main__':
    main()
