from flask import Flask, render_template, request, jsonify, session
import random
import csv
from thefuzz import fuzz, process

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key-for-memory-game'

    KNOWLEDGE_BASE = load_knowledge_base_from_csv()

    def computer_turn(sequence, available_words):
        options = []
        for word in available_words:
            best_match, score = process.extractOne(word, sequence)
            if score < 90:
                options.append(word)
        if not options:
            return "WIN"
        return random.choice(options)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/start-game', methods=['POST'])
    def start_game():
        data = request.get_json()
        stream = data.get('stream', '').lower()
        mode = data.get('mode')
        num_players = data.get('num_players', 2)

        if not stream or stream not in KNOWLEDGE_BASE:
            return jsonify({'status': 'error', 'message': 'Invalid stream selected'}), 400
        
        session.clear()
        session['current_stream'] = stream
        session['game_sequence'] = []
        session['stream_words'] = KNOWLEDGE_BASE[stream][:]
        session['mode'] = mode

        if mode == 'human':
            session['players'] = [f"Player {i+1}" for i in range(num_players)]
            session['current_player_index'] = 0
        else:
            session['players'] = ['Player 1', 'Computer']

        return jsonify({'status': 'success', 'first_player': session['players'][0]})

    @app.route('/submit-turn', methods=['POST'])
    def submit_turn():
        data = request.get_json()
        user_input = data.get('sequence', '')
        
        game_sequence = session.get('game_sequence', [])
        stream_words = session.get('stream_words', [])
        mode = session.get('mode')
        players = session.get('players', [])
        current_player_index = session.get('current_player_index', 0)
        current_player_name = players[current_player_index]
        
        # --- NEW ROBUST INPUT HANDLING ---
        # First, replace all commas with spaces, then split by whitespace.
        # This handles input like "a,b,c", "a b c", and "a, b, c".
        processed_input = user_input.replace(',', ' ')
        user_list = [item.strip() for item in processed_input.split() if item.strip()]

        def handle_mistake(message):
            if len(players) > 2 and mode == 'human':
                eliminated_player = players.pop(current_player_index)
                session['players'] = players
                if current_player_index >= len(players):
                    session['current_player_index'] = 0
                return jsonify({'status': 'player_eliminated', 'eliminated_player': eliminated_player, 'next_player': players[session['current_player_index']], 'sequence': game_sequence})
            else:
                winner_index = 1 if current_player_index == 0 else 0
                if winner_index < len(players):
                    winner = players[winner_index]
                    message = f"{message} - {winner} wins!"
                return jsonify({'status': 'game_over', 'message': message, 'correct_sequence': game_sequence, 'your_sequence': user_list})

        if len(user_list) != len(game_sequence) + 1:
            return handle_mistake(f"{current_player_name} repeated the wrong number of items!")

        for i in range(len(game_sequence)):
            similarity_ratio = fuzz.ratio(game_sequence[i].lower(), user_list[i].lower())
            if similarity_ratio < 75:
                return handle_mistake(f"{current_player_name} made a mistake in the sequence!")

        new_word_from_user = user_list[-1]
        
        if game_sequence:
            best_match_in_seq, score_in_seq = process.extractOne(new_word_from_user, game_sequence)
            if score_in_seq >= 90:
                return handle_mistake(f"'{new_word_from_user}' is a duplicate of '{best_match_in_seq}'!")

        new_sequence = user_list
        session['game_sequence'] = new_sequence

        best_match, score = process.extractOne(new_word_from_user, stream_words)
        if score < 75:
            stream_words.append("".join(new_word_from_user.title().split()))
            session['stream_words'] = stream_words

        if mode == 'vs_computer':
            new_word_from_computer = computer_turn(new_sequence, stream_words)
            if new_word_from_computer == "WIN":
                 return jsonify({'status': 'win', 'message': 'The computer ran out of words! You are the Memory Master!', 'sequence': new_sequence})
            session['game_sequence'] = new_sequence + [new_word_from_computer]
            return jsonify({'status': 'success_computer_played', 'new_word_from_computer': new_word_from_computer, 'sequence': new_sequence, 'next_player': 'Player 1'})
        else: # Human vs Human
            session['current_player_index'] = (current_player_index + 1) % len(players)
            return jsonify({'status': 'success_human_played', 'sequence': new_sequence, 'next_player': players[session['current_player_index']]})
            
    return app

def load_knowledge_base_from_csv(filename='streams.csv'):
    knowledge_base = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)
            for row in reader:
                if row:
                    stream_name = row[0].lower()
                    items_list = ["".join(item.strip().split()) for item in row[1].split(',')]
                    knowledge_base[stream_name] = items_list
        print("✅ Knowledge base loaded successfully from streams.csv")
    except FileNotFoundError:
        print(f"❌ ERROR: {filename} not found! The game will not work.")
        return {}
    return knowledge_base

app = create_app()

