from discord.ext import commands
import discord
import asyncio
import os

def setup(client, openai_api_key):

    @client.command()
    async def flood(ctx, file_path: str = None):

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print("Je n'ai pas la permission de supprimer le message.")
        except discord.HTTPException as e:
            if e.code == 20028:  
                await asyncio.sleep(5)
            else:
                raise e

        if not file_path:
            print("Veuillez spécifier un fichier texte. Exemple : `-flood mots.txt`")
            return
        
        if not os.path.isfile(file_path):
            print(f"Le fichier '{file_path}' n'existe pas ou n'est pas accessible.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                words = content.split()

            if not words:
                print("Le fichier est vide.")
                return

            sent_count = 0
            print(f"Envoi de {len(words)} mot(s) en cours...")
            for word in words:
                if word.strip():
                    try:
                        await ctx.send(word)
                        sent_count += 1
                        await asyncio.sleep(0)  
                    except discord.HTTPException as e:
                        if e.code == 20028:  
                            print("Limite de vitesse atteinte, je réessaye...")
                            await asyncio.sleep(1)
                            await ctx.send(word)
                            sent_count += 1
                        else:
                            raise e

            print(f"{sent_count} message(s) envoyé(s).")

        except discord.Forbidden:
            print("Je n'ai pas la permission d'envoyer des messages.")
        except Exception as e:
            print(f"Erreur : {str(e)}")
