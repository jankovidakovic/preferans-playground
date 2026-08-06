import argparse

from pref.game import play_game


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starting_points", type=int, default=30)
    parser.add_argument("--max_rounds", type=int, default=10)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = play_game(**vars(args))
    print(results)


if __name__ == "__main__":
    main()
