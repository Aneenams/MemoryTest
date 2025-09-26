import random

class MemoryGame:
    def __init__(self):
        """Initializes the game and loads the knowledge base directly."""
        # The data is now inside the code, no more CSV file needed.
        self.knowledge_base = {
            "actors": [
                "Mohanlal", "Mammootty", "Dulquer Salman", "Brad Pitt", "Leonardo DiCaprio",
                "Scarlett Johansson", "Tom Cruise", "Amitabh Bachchan", "Chris Hemsworth",
                "Emma Watson", "Shah Rukh Khan", "Prithviraj Sukumaran"
            ],
            "movies": [
                "Titanic", "Inception", "Bahubali", "Avatar", "Interstellar", "The Dark Knight",
                "Avengers", "Jurassic Park", "Spider-Man", "Forrest Gump", "Life of Pi",
                "The Matrix", "KGF", "Drishyam", "Jawan"
            ],
            "sports": [
                "Football", "Cricket", "Basketball", "Tennis", "Hockey", "Sachin Tendulkar",
                "Lionel Messi", "Serena Williams", "Roger Federer", "Virat Kohli",
                "Cristiano Ronaldo", "LeBron James", "MS Dhoni"
            ],
            "cars": [
                "Ferrari", "BMW", "Tesla", "Audi", "Lamborghini", "Porsche", "Mercedes",
                "Jaguar", "Ford", "Chevrolet", "Mahindra Thar", "Toyota Fortuner"
            ]
        }
        self.players = []
        self.sequence = []
        self.current_stream = None
        self.game_over = False
        self.turn = 0

    def setup_game(self):
        """Sets up the game settings like stream and players."""
        print("🎮 Welcome to the Memory Master Game!\n")
        
        print("Available streams:", ", ".join(self.knowledge_base.keys()))
        
        stream_choice = input("Choose a stream: ").strip().lower()
        if stream_choice not in self.knowledge_base:
            print("❌ Invalid stream! Game over.")
            self.game_over = True
            return
        self.current_stream = stream_choice
        
        mode = input("Play with (1) Humans or (2) Computer? Enter 1 or 2: ").strip()
        if mode == '1':
            try:
                num_players = int(input("Enter number of players (2 or more): "))
                if num_players < 2: raise ValueError
                self.players = [f"Player {i+1}" for i in range(num_players)]
            except ValueError:
                print("❌ Invalid number. Defaulting to 2 players.")
                self.players = ["Player 1", "Player 2"]
        else:
            player_name = input("Enter your name: ").strip() or "Player 1"
            self.players = [player_name, "Computer"]

    def _computer_turn(self):
        """Handles the computer's move."""
        seq_lower = {item.lower() for item in self.sequence}
        # This will now correctly use the chosen stream's word list
        options = [item for item in self.knowledge_base[self.current_stream] if item.lower() not in seq_lower]
        
        if not options:
            print(f"💻 Computer is out of unique words from the '{self.current_stream}' stream! You win!")
            self.game_over = True
            return

        new_item = random.choice(options)
        self.sequence.append(new_item)
        print(f"💻 Computer adds: {new_item}")
        print(f"✅ Current sequence: {', '.join(self.sequence)}")

    def play_turn(self):
        """Manages a single turn for a human or computer player."""
        player_index = self.turn % len(self.players)
        current_player = self.players[player_index]

        print(f"\n👉 {current_player}'s turn. Current sequence length: {len(self.sequence)}")
        
        if current_player == "Computer":
            self._computer_turn()
            return

        prompt = f"Repeat the sequence and add one more item (comma-separated): "
        user_input = input(prompt).strip()
        
        if not user_input:
            print(f"❌ {current_player} didn't enter anything!")
            self._eliminate_player(current_player)
            return

        user_list = [item.strip() for item in user_input.split(',')]
        
        correct_sequence_lower = [item.lower() for item in self.sequence]
        user_sequence_part_lower = [item.lower() for item in user_list[:-1]]
        
        if len(user_list) != len(self.sequence) + 1 or user_sequence_part_lower != correct_sequence_lower:
            print(f"💥 Wrong sequence! The correct sequence was: {', '.join(self.sequence)}")
            self._eliminate_player(current_player)
        else:
            self.sequence = user_list
            print(f"✅ Correct! New sequence: {', '.join(self.sequence)}")

    def _eliminate_player(self, player):
        """Removes a player from the game."""
        player_index = self.players.index(player)
        self.players.remove(player)
        print(f"🚫 {player} has been eliminated!")

        if self.turn >= len(self.players) and len(self.players) > 0:
            self.turn = player_index % len(self.players)
        
        if len(self.players) < 2:
            self.game_over = True

    def run(self):
        """The main game loop."""
        self.setup_game()
        if self.game_over:
            return

        first_player = self.players[0]
        first_item = input(f"{first_player}, start the game with one '{self.current_stream}': ").strip()
        if not first_item:
            print("❌ You must start with something! Game over.")
            return
        self.sequence.append(first_item)
        print(f"✅ Sequence started: {', '.join(self.sequence)}")
        
        while not self.game_over:
            self.turn += 1
            self.play_turn()
        
        if self.players:
            print(f"\n🏆 Congratulations, {self.players[0]} is the Memory Master!")
        else:
            print("\nGame over!")

# To run the game:
if __name__ == "__main__":
    game = MemoryGame()
    game.run()
    