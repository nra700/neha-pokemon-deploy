import os
from flask import Flask, request, jsonify
import uuid
from celery import Celery
import pandas as pd

# Load dataset
df = pd.read_csv('pokemon.csv')

# Initialize Flask app
app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL')
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Celery task to run a battle
@celery.task
def run_battle_task(battle_id, pokemon_a_data, pokemon_b_data):
    from okemon import get_pokemon_data, battle  

    pokemon_a = get_pokemon_data(pokemon_a_data['name'], df)
    pokemon_b = get_pokemon_data(pokemon_b_data['name'], df)
    
    winner, margin = battle(pokemon_a, pokemon_b)
    
    # store result
    battles[battle_id] = {"status": "BATTLE_COMPLETED", "result": {"winnerName": winner, "wonByMargin": margin}}

# battle status
battles = {}

@app.route('/list_pokemons', methods=['GET'])
def list_pokemons():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 5))
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated_data = df.iloc[start_idx:end_idx].to_dict(orient='records')
    total_items = len(df)
    total_pages = (total_items + page_size - 1) // page_size
    has_next = page < total_pages
    
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
    data = request.json

    if 'pokemon_a' not in data or 'pokemon_b' not in data:
        return jsonify({"error": "Both 'pokemon_a' and 'pokemon_b' must be provided"}), 400

    battle_id = str(uuid.uuid4())
    battles[battle_id] = {"status": "BATTLE_IN_PROGRESS", "result": None}

    # Enqueue the task
    run_battle_task.delay(battle_id, data['pokemon_a'], data['pokemon_b'])
    
    return jsonify({"battle_id": battle_id})

@app.route('/battle_status/<battle_id>', methods=['GET'])
def battle_status(battle_id):
    status = battles.get(battle_id, {"status": "BATTLE_NOT_FOUND"})
    return jsonify(status)

# if __name__ == '__main__':
#     app.run(debug=True)
