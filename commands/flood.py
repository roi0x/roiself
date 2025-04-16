import sqlite3
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
    @client.event
    async def on_message(message):
        if message.author == client.user and message.content == '-snipe':
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT author_name, content, timestamp
                    FROM deleted_messages
                    WHERE channel_id = ?
                ''', (message.channel.id,))
                result = cursor.fetchone()
                if not result or not result[1]:
                    await message.channel.send("Aucun message supprimé récent trouvé dans ce salon.", delete_after=1)
                    return
                author, content, timestamp = result
                timestamp = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d à %H:%M')
                snipe_message = (
                    f"__**Dernier message supprimé**__\n"
                    f"**Auteur** : {author}\n"
                    f"**Contenu** : {content}\n"
                    f"**Envoyé le** : {timestamp}"
                )
                await message.channel.send(snipe_message, delete_after=10)
            except Exception as e:
                print(f"Erreur : {str(e)}")
            finally:
                conn.close()
        await client.process_commands(message)
