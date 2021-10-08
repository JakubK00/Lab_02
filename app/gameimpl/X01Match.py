from datatype.enums import DartMultiplier
from service.match_service import MatchVisitTemplate
from service.match_service import MatchManager


CHECKOUTS = {
    170: "T20 T20 Bull",
    167: "T20 T19 Bull",
    164: "T20 T18 B ull ",
    161: "T20 T17 B ull ",
    160: "T20 T20 D20",
    136: "T20 T20 D8",
    36: "D18"
}

STARTING_TOTAL = 501


class X01Match(MatchManager, MatchVisitTemplate):

    def __init__(self):
        super().__init__()
        self.scores = []  # list of scores remaining parallel top layers
        self.averages = []  # single−dart average(x3 for 3−dart average)
        self.first9 = []  # average for first 9 darts

    def post_init(self):
        for i in range(0, len(self.match.players)):
            self.scores.append(None)
            self.averages.append(None)

    def validate_visit(self, player_index, visit):
        if self.match.last_player_index is player_index:
            return False, "player" + str(player_index + 1) + "is not in the correct sequence. Visit ignored."
        if not self.match.active:
            return False, "Game has ended."

        self.match.last_player_index = player_index
        return True, None

    def check_winning_condition(self, player_index, visit):
        i = 0
        for darts in visit.darts:
            i = i + 1
            if darts.multiplier == DartMultiplier.DOUBLE and self.scores[player_index] - darts.get_score() == 0:
                self.scores[player_index] = 0
                self.match.active = False
                return i
            else:
                self.scores[player_index] -= darts.get_score()

        return 0

    def record_statistics(self, player_index, visit, result):
        if result is not 0:
            visit.remove_trailing_darts(result)

        self.match.visits[player_index].append(visit)

        if len(self.match.visits[player_index]) == 3:
            self.first9[player_index] = (STARTING_TOTAL - self.scores[player_index])/3

        # calculate single dart average taking account of the double being hit with dart 1 or 2 when checking out
        num_darts_throw = (len(self.match.visits[player_index]) - 1) * 3
        num_darts_throw += 3 if result is 0 else result

        if result is not 0:
            self.match.winning_num_darts = num_darts_throw
            self.match.winning_player_index = player_index

        self.averages[player_index] = (STARTING_TOTAL - self.scores[player_index]) / num_darts_throw

        def format_summary(self, player_index, visit):
            # Include suggested checkout if remaining score can be checked out in 3 darts
            summary = "Last visit was by " + self.match.players[player_index] + " with " + visit.to_string() + "\n"

            if self.match.winning_player_index is not -1:
                summary += self.match.players[self.match.winning_player_index] + " wins in " \
                           + str(self.match.winning_num_darts) + " darts\n"

            i = 0
            for player in self.match.players:
                summary = summary + player + ": " + str(self.scores[i]) + " Remaining"
                if self.scores[i] in CHECKOUTS.keys():
                    summary += " (" + CHECKOUTS.get(self.scores[i]) + ")"
                if self.first9[i]:
                    summary += "\n - [First 9 Avg: " + '{0:.2f}'.format(self.first9[i]) + "] "
                if self.averages[i]:
                    summary += "\n - [3-dart Avg: " + '{0:.2f}'.format(self.averages[i] * 3) + "] "
                i = i + 1
                summary += "\n"
            return summary

    class X01MatchBuilder:
        """
        This could be extended to include dynamic key-value pair parameters (see object_factory.py),
        or make it a singleton, etc.
        """

        def __init__(self):
            pass

        def __call__(self):
            return X01Match()
