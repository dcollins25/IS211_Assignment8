import random
import time
import argparse


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def play(self):
        pass

    def roll_dice(self):
        return random.randint(1, 6)


class HumanPlayer(Player):
    def play(self):
        print(f"{self.name}'s turn")
        roll_again = 'y'
        turn_score = 0
        while roll_again == 'y':
            roll = self.roll_dice()
            if roll == 1:
                print(f"{self.name} rolled a 1 and lost the turn!")
                return 0
            else:
                turn_score += roll
                print(f"{self.name} rolled a {roll}, turn score is {turn_score}, total score is {self.score + turn_score}")
                roll_again = input("Roll again? (y/n): ").lower()
        self.score += turn_score
        print(f"{self.name} got {turn_score} points this turn, total score is {self.score}")
        return self.score


class ComputerPlayer(Player):
    def play(self):
        print(f"{self.name}'s turn")
        turn_score = 0
        while turn_score < min(25, 100 - self.score):
            roll = self.roll_dice()
            if roll == 1:
                print(f"{self.name} rolled a 1 and lost the turn!")
                return 0
            else:
                turn_score += roll
                print(f"{self.name} rolled a {roll}, turn score is {turn_score}, total score is {self.score + turn_score}")
                time.sleep(1)
        self.score += turn_score
        print(f"{self.name} got {turn_score} points this turn, total score is {self.score}")
        return self.score


class PlayerFactory:
    def create_player(self, name, player_type):
        if player_type == 'human':
            return HumanPlayer(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        current_player = self.player1
        while self.player1.score < 100 and self.player2.score < 100:
            current_score = current_player.play()
            if current_score == 0:
                current_player = self.player2 if current_player == self.player1 else self.player1
            else:
                if current_player == self.player1:
                    current_player = self.player2
                else:
                    current_player = self.player1
        winner = self.player1 if self.player1.score >= 100 else self.player2
        print(f"{winner.name} won the game with {winner.score} points!")

class TimedGameProxy(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.start_time = time.time()

    def play(self):
        while time.time() - self.start_time < 60:
            super().play()
        print("Time's up!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play the Pig game')
    parser.add_argument('--player1', choices=['human', 'computer'], required=True, help='Player 1 type')
    parser.add_argument('--player2', choices=['human', 'computer'], required=True, help='Player 2 type')
    parser.add_argument('--timed', action='store_true', help='Play a timed game')
    args = parser.parse_args()

    player_factory = PlayerFactory()
    player1 = player_factory.create_player('Player 1', args.player1)
    player2 = player_factory.create_player('Player 2', args.player2)

    if args.timed:
        game = TimedGameProxy(player1, player2)
    else:
        game = Game(player1, player2)

    game.play()