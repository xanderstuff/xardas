from argparse import ArgumentParser

from xardas import Xardas


def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default='config.yml', help='Use this config file instead.')
    args = parser.parse_args()

    bot = Xardas(args.config)
    bot.run()


if __name__ == '__main__':
    main()
