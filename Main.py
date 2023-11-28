import discord
import openai
import discord_webhook
import socket


WEBHOOK_URL = "Your_Webook_url"  # not mandatory 
openai.api_key = "Your_api_key" # obtainable on the openai website

messages = []
args = []
refresh = []

intents = discord.Intents.all()
client = discord.Client(intents=intents)


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)

    async def on_message(self, message):
        if message.content.startswith('!restart'):
            global messages
            messages = []
            await message.channel.send('MEMORY RESET')
            
            embed = discord_webhook.DiscordEmbed(description=f"RESET MEMORY")
            embed.set_author(name=f"{message.author.name}")

            discord_webhook.DiscordWebhook(url=WEBHOOK_URL, username='GPTLOG', embeds=[embed]).execute()
            
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith('!ip'):
            host_name = socket.gethostname()
            ip_address = socket.gethostbyname(host_name)
            
            host_name="Host: "+host_name
            ip_address="IP: "+ip_address

            await message.channel.send(host_name)
            await message.channel.send(ip_address)
                
        
        if message.content.startswith(''):
            args = message.content.split()
        if len(args) > 1:
            demande = ' '.join(args[1:])
            
            messages.append({"role": "user", "content": demande})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", # You can change the model for more details go on openai website
                messages=messages
            )

            reponse_chatGPT = completion.choices[0].message.content
            print(f'ChatGPT: {reponse_chatGPT}')
            
            messages.append({"role": "assistant", "content": reponse_chatGPT})
            
            
            await message.channel.send(format(reponse_chatGPT))
            
            embed = discord_webhook.DiscordEmbed(description=f"{demande}\n\n{reponse_chatGPT}")
            embed.set_author(name=f"{message.author.name}")

            
            
        else:
            await message.channel.send('Hello, here are the different commands available:\n=> !restart `Delete conversation memory`\n=> !prog `Sends the currently running program`\n=> !ip `Donne l\'host et l\'ip de l\'host`')


client = MyClient()
client.run('Your_bot's_token') # obtaineable on developer portal (discord)
