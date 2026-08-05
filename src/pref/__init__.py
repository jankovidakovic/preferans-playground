from pref.game import play_game


def main() -> None:
    results = play_game(starting_points=30, max_rounds=10)
    print(results)


if __name__ == "__main__":
    main()
