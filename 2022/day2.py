import fileinput

OPPONENT_MOVES = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}

# ME_MOVES = {
#     "Y": "paper",
#     "X": "rock",
#     "Z": "scissors"
# }

ME_RESULTS = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}

MOVE_POINTS = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

DRAW_POINTS = 3

WIN_POINTS = 6

LOSS_POINTS = 0

my_score = 0


def get_move(opponent_move, result):
    wins = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    };
    if result == "draw":
        return opponent_move
    if result == "lose":
        return wins[opponent_move]
    reverse_wins = dict(map(reversed, wins.items()))
    return reverse_wins[opponent_move]


for line in map(str.strip, fileinput.input()):
    opponent_code, my_code = line.split()
    # my_move = ME_MOVES[my_code]
    opponent_move = OPPONENT_MOVES[opponent_code]
    my_result = ME_RESULTS[my_code]
    my_move = get_move(opponent_move, my_result)

    my_score += MOVE_POINTS[my_move]

    if my_move == opponent_move:
        my_score += DRAW_POINTS
    elif (my_move, opponent_move) in {
        ("rock", "scissors"),
        ("paper", "rock"),
        ("scissors", "paper")
    }:
        my_score += WIN_POINTS
    else:
        my_score += LOSS_POINTS


print("SCORE", my_score)
