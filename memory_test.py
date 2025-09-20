import random

# Knowledge bases for streams
actors = ["Mohanlal", "Mammootty", "Dulquer Salman", "Brad Pitt", "Leonardo DiCaprio",
          "Scarlett Johansson", "Tom Cruise", "Amitabh Bachchan", "Chris Hemsworth", "Emma Watson"]

movies = ["Titanic", "Inception", "Bahubali", "Avatar", "Interstellar", 
          "The Dark Knight", "Avengers", "Jurassic Park", "Spider-Man", "Forrest Gump"]

sports = ["Football", "Cricket", "Basketball", "Tennis", "Hockey",
          "Sachin Tendulkar", "Lionel Messi", "Serena Williams", "Roger Federer", "Virat Kohli"]

cars = ["Ferrari", "BMW", "Tesla", "Audi", "Lamborghini", "Porsche", "Mercedes", "Jaguar", "Ford", "Chevrolet"]

bikes = ["Ducati", "KTM", "Royal Enfield", "Harley Davidson", "Yamaha", "Suzuki", "Kawasaki", "Honda"]

plants = ["Rose", "Tulip", "Neem", "Bamboo", "Oak", "Mango Tree", "Maple", "Sunflower"]

random_stuff = ["Car", "Food", "Bench", "Pillar", "Laptop", "Phone", "Bottle", "Chair", "Bag", "Ball", "Book"]

knowledge_base = {
    "actors": actors,
    "movies": movies,
    "sports": sports,
    "cars": cars,
    "bikes": bikes,
    "plants": plants,
    "random_stuff": random_stuff
}

# Function for computer turn with case-insensitive duplicate check
def computer_turn(sequence, stream):
    seq_lower = [item.lower() for item in sequence]
    options = [item for item in knowledge_base[stream] if item.lower() not in seq_lower]
    if not options:
        options = knowledge_base[stream]  # fallback if all items used
    new_item = random.choice(options)
    sequence.append(new_item)
    print(f"💻 Computer adds: {new_item}")
    return sequence

# Main Game
def memory_test_game():
    print("🎮 Welcome to Memory Test Game!\n")
    
    # Choose stream
    print("Available streams:", ", ".join(knowledge_base.keys()))
    stream = input("Choose a stream: ").strip().lower()
    if stream not in knowledge_base:
        print("❌ Invalid stream!")
        return
    
    # Choose mode
    mode = input("Play with (1) Humans or (2) Computer? Enter 1 or 2: ").strip()
    
    if mode == "1":
        num_players = int(input("Enter number of players: "))
        players = [f"Player {i+1}" for i in range(num_players)]
        play_with_ai = False
    else:
        player_name = input("Enter your name: ").strip() or "Player"
        players = [player_name, "Computer"]
        play_with_ai = True
    
    sequence = []
    turn = 0  # index for player turns
    
    # First player starts
    first_player = players[turn % len(players)]
    first_item = input(f"{first_player}, enter the first item of {stream}: ").strip()
    if not first_item:
        print("❌ You must enter something! Game over.")
        return
    sequence.append(first_item)
    print(f"✅ Current sequence: {sequence}\n")
    turn += 1
    
    while len(players) > 1:
        current_player = players[turn % len(players)]
        print(f"👉 {current_player}'s turn")
        
        # Computer turn
        if play_with_ai and current_player == "Computer":
            sequence = computer_turn(sequence, stream)
            print(f"✅ Current sequence: {sequence}\n")
        else:
            user_input = input(f"{current_player}, repeat sequence and add one more: ").strip()
            if not user_input:
                print(f"❌ {current_player} didn't enter anything! Eliminated.")
                players.remove(current_player)
                turn %= len(players)
                continue
            user_list = [item.strip() for item in user_input.split(",")]
            
            # Case-insensitive check
            seq_lower = [item.lower() for item in sequence]
            user_lower = [item.lower() for item in user_list[:-1]]

            if len(user_list) != len(sequence) + 1 or user_lower != seq_lower:
                print(f"❌ {current_player} failed!")
                if len(players) == 2:
                    winner = [p for p in players if p != current_player][0]
                    print(f"🏆 {winner} wins the game!")
                    return
                else:
                    players.remove(current_player)
                    print(f"🚫 {current_player} is eliminated! Remaining: {players}")
                    if turn >= len(players):
                        turn = 0
                    continue
            
            sequence = user_list
            print(f"✅ Correct! Current sequence: {sequence}\n")
        
        turn += 1
    
    print(f"\n🏆 {players[0]} is the last one standing and WINS the game!")

# Run the game
memory_test_game()
