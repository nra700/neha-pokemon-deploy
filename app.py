import os
import pandas as pd
from flask import Flask, request, jsonify
import uuid
import threading
import time
from okemon import get_pokemon_data, battle

app = Flask(__name__)
battles = {}

df = pd.read_csv('pokemon.csv')

@app.route('/list_pokemons', methods=['GET'])
def list_pokemons():
    
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 5))
    
    # Calculate the start and end indices for the requested page
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    # Get the paginated data
    paginated_data = df.iloc[start_idx:end_idx].to_dict(orient='records')
    
    # Total number of items
    total_items = len(df)
    
    # Calculate total number of pages
    total_pages = (total_items + page_size - 1) // page_size
    
    # Check if there is a next page
    has_next = page < total_pages
    
    # Return the paginated results with metadata
    return jsonify({
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": has_next,
        "data": paginated_data
    })
    
@app.route('/start_battle', methods=['POST'])
def start_battle():
    
    # data = request.json
    
    # try:
    #     pokemon_a = get_pokemon_data(data['pokemon_a'], df)
    #     pokemon_b = get_pokemon_data(data['pokemon_b'], df)
    # except ValueError as e:
    #     return jsonify({"error": str(e)}), 400
    
    # battle_id = str(uuid.uuid4())
    # battles[battle_id] = {"status": "BATTLE_IN_PROGRESS", "result": None}
    # print(f"Battle started with ID: {battle_id}, status: {battles[battle_id]}")

    # def run_battle(battle_id, pokemon_a, pokemon_b):
    #     print(f"Running battle {battle_id}")
    #     time.sleep(3)  # Simulate battle duration
    #     winner, margin = battle(pokemon_a, pokemon_b)
    #     battles[battle_id] = {"status": "BATTLE_COMPLETED", "result": {"winnerName": winner, "wonByMargin": margin}}
    #     print(f"Battle {battle_id} completed with status: {battles[battle_id]}")
    
    # threading.Thread(target=run_battle, args=(battle_id, pokemon_a, pokemon_b)).start()
    
    # return jsonify({"battle_id": battle_id})
    data = request.json
    
    try:
        # Extract Pokémon names
        pokemon_a = get_pokemon_data(data['pokemon_a'], df)
        pokemon_b = get_pokemon_data(data['pokemon_b'], df)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    # Generate a unique battle ID
    battle_id = str(uuid.uuid4())
    battles[battle_id] = {"status": "BATTLE_IN_PROGRESS", "result": None}
    
    # Function to run the battle asynchronously
    def run_battle(battle_id, pokemon_a, pokemon_b):
        print(f"Starting battle {battle_id}")
        time.sleep(2)  # Simulate some delay in processing the battle
        winner, margin = battle(pokemon_a, pokemon_b)
        battles[battle_id] = {"status": "BATTLE_COMPLETED", "result": {"winnerName": winner, "wonByMargin": margin}}
        print(f"Battle {battle_id} completed with winner {winner}")
    
    # Start the battle in a new thread
    battle_thread = threading.Thread(target=run_battle, args=(battle_id, pokemon_a, pokemon_b))
    battle_thread.start()
    
    # Return the battle ID immediately
    return jsonify({"battle_id": battle_id})


@app.route('/battle_status/<battle_id>', methods=['GET'])
def battle_status(battle_id):
    # return jsonify(battles.get(battle_id, {"status": "BATTLE_NOT_FOUND"}))
    status = battles.get(battle_id, {"status": "BATTLE_NOT_FOUND"})
    print(f"Status of battle {battle_id}: {status['status']}")
    return jsonify(status)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Default to port 5000 if no PORT env variable is found
    app.run(host='0.0.0.0', port=port)

