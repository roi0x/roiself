import sqlite3
from discord.ext import commands
import discord
import asyncio
from datetime import datetime
import os

def setup(client, openai_api_key):

    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'deleted_messages.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deleted_messages (
            channel_id INTEGER PRIMARY KEY,
            author_name TEXT,
            content TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

    @client.event
    async def on_message_delete(message):

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO deleted_messages (channel_id, author_name, content, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                message.channel.id,
                message.author.display_name,
                message.content,
                message.created_at.isoformat()
            ))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur SQLite dans on_message_delete : {str(e)}")
        finally:
            conn.close()

    @client.command()
    async def snipe(ctx):

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
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT author_name, content, timestamp
                FROM deleted_messages
                WHERE channel_id = ?
            ''', (ctx.channel.id,))
            result = cursor.fetchone()

            if not result or not result[1]:
                await ctx.send("Aucun message supprimé récent trouvé dans ce salon.", delete_after=5)
                return

            author, content, timestamp = result
            timestamp = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d à %H:%M')
            snipe_message = (
                f"__**Dernier message supprimé**__\n"
                f"**Auteur** : {author}\n"
                f"**Contenu** : {content}\n"
                f"**Envoyé le** : {timestamp}"
            )
            await ctx.send(snipe_message, delete_after=20)

        except discord.Forbidden:
            print("Je n'ai pas la permission d'envoyer des messages.")
        except Exception as e:
            print(f"{str(e)}")
        finally:
            conn.close()