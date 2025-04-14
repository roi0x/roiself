import discord
from discord.ext import commands
import json
import os

try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Erreur : config.json introuvable.")
    exit(1)

client = commands.Bot(command_prefix='-', self_bot=True)
client.remove_command('help')

@client.event
async def on_ready():
    print(f'Connecté a ton compte !')

utils_dir = os.path.join(os.path.dirname(__file__), 'commands')
for filename in os.listdir(utils_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]  
        try:
            module = __import__(f'commands.{module_name}', fromlist=['setup'])
            module.setup(client, config['openai_api_key'])
            print(f'Commande {module_name} chargée.')
        except Exception as e:
            print(f'Erreur lors du chargement de {module_name} : {str(e)}')

try:
    client.run(config['discord_token'], bot=False)
except discord.errors.LoginFailure:
    print("Erreur : Token Discord invalide. Vérifie config.json.")
except Exception as e:
    print(f"Erreur lors du démarrage du selfbot : {str(e)}")