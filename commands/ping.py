from discord.ext import commands

def setup(client, openai_api_key):

    @client.command()
    async def ping(ctx):
        latency = client.latency * 1000 
        await ctx.send(f"Latence : {latency:.2f} ms")