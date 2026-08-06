import argparse

from pref.game import play_game


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starting_points", type=int, default=30)
    parser.add_argument("--max_rounds", type=int, default=10)


def main(starting_points: int, max_rounds: int) -> None:
    results = play_game(starting_points, max_rounds)
    print(results)


if __name__ == "__main__":
    main(**vars(parse_args()))
