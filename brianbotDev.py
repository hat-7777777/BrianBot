import discord, requests, random, os
from discord.ext import commands
from pydub import AudioSegment
from pydub.playback import play

# Replace "INSERT TOKEN HERE" with your Discord bot token
token = "INSERT TOKEN HERE"

global playing
global muted
playing = False
muted = False
client = commands.Bot(command_prefix="!brian ")

client.remove_command("help")

@client.event
async def on_ready():
    print(f"Brian logged in as {client.user.name} with id {client.user.id}")
    await client.change_presence(activity=discord.Game("!brian help"))


# function that didnt work for asynchronous tasks, maybe fix it later
# async def playsound(audiofile):
#        await play(audiofile)

###COMMANDS###

# help command
@client.command()
async def help(ctx):
       await ctx.send("```HELP \n!brian help: Shows this message\n!brian tts <message>: Play a "
                      "message with Brian Text-To-Speech™\n!brian mute: Disable text-to-speech (Owner only)\n"
                      "!brian unmute: Enable text-to-speech (Owner only)```")

# muting commands
@client.command()
@commands.is_owner()
async def mute(ctx):
    global muted
    if muted == True:
        await ctx.send("Already muted. Use **!brian unmute** to unmute.")
    else:
        muted = True
        await ctx.send("Muted audio :mute:")


@client.command()
@commands.is_owner()
async def unmute(ctx):
    global muted
    if muted == True:
        muted = False
        extra = random.randint(0, 29)
        if extra == 0:
            await ctx.send("kill me")
        else:
            await ctx.send("Unmuted audio :loud_sound:")
    else:
        await ctx.send("Already unmuted. Use **!brian mute** to mute.")


# text to speech command
@client.command()
async def tts(ctx, *, payload):
    global playing
    global muted
    if muted == True:
        await ctx.send("Muted, unable to play message until unmuted.")
    elif playing == True:
        await ctx.send("Message is already being played, hold on!")
    else:
        await ctx.send(f'Playing message: "{payload}" :arrow_forward:')
        playing = True
        print(f"incoming message: {payload}")
        req = requests.get("https://api.streamelements.com/kappa/v2/speech?voice=Brian&text=" + str(payload))
        print("getting audio from", req.url)

        print("creating file")
        r1 = random.randint(1, 1000000)
        randfile = str(r1) + ".mp3"

        print(f"writing audio to {randfile}")
        with open(randfile, "wb") as my_file:
            my_file.write(req.content)

        print("preparing audio file")
        audiofile = AudioSegment.from_mp3(randfile)

        print("playing audio")
        play(audiofile)
        # playsound(audiofile)

        print(f"removing file {randfile}")
        os.remove(randfile)
        playing = False
        await ctx.send("Done :thumbsup:")


client.run(token)
