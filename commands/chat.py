from discord.ext import commands
import openai

def setup(client, openai_api_key):
    openai.api_key = openai_api_key

    @client.command()
    async def chat(ctx, *, message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message}
                ],
                max_tokens=150
            )
            
            ai_response = response.choices[0].message['content'].strip()
            
            await ctx.send(ai_response if ai_response else "Erreur : réponse vide.")
            
        except Exception as e:
            await print(f"Erreur : {str(e)}")