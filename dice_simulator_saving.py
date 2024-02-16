import random

class DiceSimulator:
    def __init__(self, history_file="throw_history.txt"):
        self.throw_history = []
        self.history_file = history_file

    def throw_dice(self, num_dice=1, num_sides=6, num_throws=1):
        if not (1 <= num_dice <= 5 and 1 <= num_sides <= 100):
            raise ValueError("Dice number must be 1-5 and sides must be 1-100.")

        results = []
        for _ in range(num_throws):
            throw_result = [random.randint(1, num_sides) for _ in range(num_dice)]
            results.append(throw_result)
            self._update_history(throw_result)
        return results

    def _update_history(self, throw_result):
        # Append to in-memory history
        self.throw_history.append(throw_result)
        # Keep only the last 100 throws in-memory
        self.throw_history = self.throw_history[-100:]
        # Append the latest throw to the file as a single line
        self._append_to_file(throw_result)

    def _append_to_file(self, throw_result):
        # Convert the entire throw result to a single string with commas
        result_string = ', '.join(map(str, throw_result)) + "\n"

        # Read the existing history from the file
        try:
            with open(self.history_file, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []

        # Append the new throw
        lines.append(result_string)

        # Keep only the last 100 throws
        lines = lines[-100:]

        # Write the updated history back to the file
        with open(self.history_file, "w") as file:
            file.writelines(lines)

    def get_history(self):
        return self.throw_history

# Example Usage
simulator = DiceSimulator()
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
    
    # Collect all the results of the throws before writing to the file
    all_throw_results = []
    for _ in range(num_throws):
        throw = simulator.throw_dice(num_dice=1, num_sides=100, num_throws=1)
        all_throw_results.extend(throw[0])
    # Print the collected results
    print(', '.join(map(str, all_throw_results)))
    #print("Throw History:", simulator.get_history())
    # Update the file with the collected results of this set of throws
    simulator._append_to_file(all_throw_results)
    
    another_roll = input("Want to roll the dice again? (y/n): ")
    if another_roll.lower() != "y":
        again = False
