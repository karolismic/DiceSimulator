import random
from collections import defaultdict

class WeightedDiceSimulator:
    def __init__(self, history_file="throw_history_weighted.txt"):
        self.throw_history = []
        self.history_file = history_file
        self._load_history()

    def _load_history(self):
        try:
            with open(self.history_file, "r") as file:
                history = [line.strip() for line in file.readlines()]
                self.throw_history = [list(map(int, throw.split(','))) for throw in history]
        except FileNotFoundError:
            pass

    def throw_dice(self, num_dice=1, weights=None, num_throws=1):
        if not (1 <= num_dice <= 5):
            raise ValueError("Number of dice must be between 1 and 5.")
        if weights and not all(isinstance(w, dict) for w in weights):
            raise ValueError("Weights must be a list of dictionaries.")

        results = []
        for _ in range(num_throws):
            throw_result = [self._weighted_roll(weights[i] if weights else None) for i in range(num_dice)]
            results.append(throw_result)
            self._update_history(throw_result)
        return results

    def _weighted_roll(self, weight_dict):
        if not weight_dict:
            return random.randint(1, 100)  # Default to a 100-sided die
        total = sum(weight_dict.values())
        rand_val = random.uniform(0, total)
        upto = 0
        for side, weight in sorted(weight_dict.items()):
            if upto + weight >= rand_val:
                return side
            upto += weight

    def _update_history(self, throw_result):
        self.throw_history.append(throw_result)
        self.throw_history = self.throw_history[-100:]
        self._save_history_to_file()

    def _save_history_to_file(self):
        with open(self.history_file, "w") as file:
            for throw in self.throw_history:
                file.write(','.join(map(str, throw)) + "\n")

    def get_history(self):
        return self.throw_history

# Example Usage
# Define the weights for a 100-sided die with biases towards 8 specific sides
biased_sides = {8, 16, 24, 32, 40, 48, 56, 64}
weights = [{i: 10 if i in biased_sides else 1 for i in range(1, 101)}]

simulator = WeightedDiceSimulator()
again = True
while again:
    num_throws = 0
    while num_throws not in range(1, 6):
        try:
            num_throws = int(input("How many times do you want to throw the dice? (1-5): "))
            if num_throws not in range(1, 6):
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid integer.")

    results = simulator.throw_dice(num_dice=1, weights=weights, num_throws=num_throws)
    for result in results:
        print(', '.join(map(str, result)))

    another_roll = input("Want to roll the dice again? (y/n): ")
    if another_roll.lower() != "y":
        again = False

#print("Throw History:", simulator.get_history())
