import discord, requests, random, os
from discord.ext import commands
from pydub import AudioSegment
from pydub.playback import play

#Replace "INSERT TOKEN HERE" with your Discord bot token
token = "NjUxMTQ4NjcyMTY3NTc1NTU0.XgV2AA.FckpM0P8piybx4xujysx0P7mQPQ"

global playing
playing = False
client = commands.Bot(command_prefix="!brian")

@client.event
async def on_ready():
        print("Brian is now active")
        await client.change_presence(activity=discord.Game("!briantts <message>"))

async def playsound(audiofile):
        await play(audiofile)

@client.command()
async def tts(ctx, *, payload):
        global playing
        if playing == True:
                ctx.send("Message is already being played, hold on!")
        else:
                await ctx.send(f'Playing message: "{payload}" :arrow_forward:')
                playing = True
                print(f"incoming message: {payload}")
                req = requests.get("https://api.streamelements.com/kappa/v2/speech?voice=Brian&text=" + str(payload))
                print("getting audio from", req.url)

                print("creating file")
                r1 = random.randint(1,1000000)
                randfile = str(r1)+".mp3"

                print(f"writing audio to {randfile}")
                with open(randfile, "wb") as my_file:
                        my_file.write(req.content)

                print("preparing audio file")
                audiofile = AudioSegment.from_mp3(randfile)

                print("playing audio")
                play(audiofile)
                #playsound(audiofile)

                print(f"removing file {randfile}")
                os.remove(randfile)
                playing = False
                await ctx.send("Done :thumbsup:")

client.run(token)
