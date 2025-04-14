from discord.ext import commands
import discord
import asyncio

def setup(client, openai_api_key):

    @client.command()
    async def help(ctx):

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print("Je n'ai pas la permission de supprimer le message.")
        except discord.HTTPException as e:
            if e.code == 20028:  
                print("Limite de vitesse atteinte pour la suppression, je continue...")
                await asyncio.sleep(5)
            else:
                raise e

        try:
            help_message = (
                "**Aide**\n\n"
                "**-chat <message>**\n"
                "Interagit avec ChatGPT.\n"
                "Exemple : `-chat Salut, ça va ?`\n\n"
                "**-clear [nombre]**\n"
                "Supprime les messages de l'utilisateur, si vous souhaitez clear sans nombre précis, c'est possible ! Il suffit de faire -clear.\n"
                "Exemple : `-clear 10` ou `-clear`\n\n"
                "**-flood <fichier.txt>**\n"
                "Envoie chaque mot d'un fichier texte comme un message.\n"
                "Exemple : `-flood mots.txt`\n\n"
                "**-help**\n"
                "Affiche cette aide.\n"
                "Exemple : `-help`\n\n"
                "**-ping**\n"
                "Donne le ping du Selfbot.\n"
                "Exemple : `-ping`\n\n"
                "**-snipe**\n"
                "Donne le dernier message supprimé enregistré par le Selfbot.\n"
                "Exemple : `-snipe`\n\n"
                "**Créateur** : https://github.com/roi0x/"
            )
            await ctx.send(help_message, delete_after=50)

        except discord.Forbidden:
            print("Je n'ai pas la permission d'envoyer des messages.")
        except Exception as e:
            print(f"Erreur : {str(e)}")