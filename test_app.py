import unittest
import json
from app import app, battles
import pandas as pd
from io import StringIO
from unittest.mock import patch

class PokemonAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a sample DataFrame
        cls.sample_data = """name,type,attack,defense
        Bulbasaur,Grass,49,49
        Charmander,Fire,52,43
        Squirtle,Water,48,65
        Pidgey,Flying,45,40
        Rattata,Normal,56,35
        """
        cls.df = pd.read_csv(StringIO(cls.sample_data))
        
        # Mock the pandas read_csv function to return the sample DataFrame
        cls.patcher = patch('app.pd.read_csv', return_value=cls.df)
        cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_list_pokemons(self):
        response = self.app.get('/list_pokemons?page=1&page_size=2')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['page_size'], 2)
        self.assertEqual(len(data['data']), 2)
        self.assertTrue(data['has_next'])

    def test_start_battle(self):
        # Mock the get_pokemon_data and battle functions
        with patch('okemon.get_pokemon_data') as mock_get_pokemon_data, \
             patch('okemon.battle') as mock_battle:
            
            mock_get_pokemon_data.return_value = {'name': 'Charmander', 'type': 'Fire', 'attack': 50, 'defense': 50}
            mock_battle.return_value = ('Charmander', 10)
            
            response = self.app.post('/start_battle', json={
                'pokemon_a': 'Charmander',
                'pokemon_b': 'Bulbasaur'
            })
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('battle_id', data)
            self.assertEqual(battles[data['battle_id']]['status'], 'BATTLE_IN_PROGRESS')

    def test_battle_status(self):
        # Pre-create a battle ID and set status for testing
        battle_id = 'test-battle-id'
        battles[battle_id] = {"status": "BATTLE_COMPLETED", "result": {"winnerName": "Charmander", "wonByMargin": 10}}
        
        response = self.app.get(f'/battle_status/{battle_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'BATTLE_COMPLETED')
        self.assertEqual(data['result']['winnerName'], 'Charmander')

if __name__ == '__main__':
    unittest.main()
