import argparse

from Classes.SalClasses import Sal


def get_args():
    parser = argparse.ArgumentParser(description='This is the Stevens Automation Loader.')
    parser.add_argument('--env_key', type=str, default="dev", help='an integer for the accumulator')
    return parser.parse_args()


def main():

    args = get_args()

    sal_bot = Sal.Sal(env_key=args.env_key)
    sal_bot.watch_messages()


if __name__ == '__main__':
    main()
