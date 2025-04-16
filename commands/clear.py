from discord.ext import commands
import discord
import asyncio

def setup(client, openai_api_key):

    @client.command()
    async def clear(ctx, amount: int = None):

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print("Je n'ai pas la permission de supprimer le message de commande.")
        except discord.HTTPException as e:
            if e.code == 20028:
                print("Limite de vitesse atteinte pour la suppression, je continue...")
                await asyncio.sleep(5)
            else:
                raise e

        try:
            if amount is None:
                amount = 100
            else:
                if amount <= 0:
                    return
                if amount > 100:
                    return

            def check(message):
                return message.author == client.user and message.created_at < ctx.message.created_at

            deleted_count = 0
            if isinstance(ctx.channel, discord.DMChannel):
                async for message in ctx.channel.history(limit=amount):
                    if check(message):
                        await message.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.5) 
            else:
                while deleted_count < amount:
                    batch_size = min(amount - deleted_count, 50)
                    deleted = await ctx.channel.purge(limit=batch_size, check=check)
                    deleted_count += len(deleted)
                    if deleted_count < amount and len(deleted) > 0:
                        await asyncio.sleep(1)
                    else:
                        break

            await ctx.send(f"{deleted_count} message(s) supprimé(s).", delete_after=1)

        except discord.Forbidden:
            print("Je n'ai pas la permission de supprimer des messages.")
        except discord.HTTPException as e:
            if e.code == 20028:
                print("Limite de vitesse atteinte, je réessaye dans 5 secondes...")
                await asyncio.sleep(5)
            else:
                print(f"Erreur : {str(e)}")
        except Exception as e:
            print(f"Erreur : {str(e)}")
