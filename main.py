import base64
import discord
import asyncio
import requests
import re
import openai
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from discord.ext import commands
from io import BytesIO
from PIL import Image
from craiyon import Craiyon
from wordlists import *
from blackjack import *


perms = 3072
bot_perms = discord.Permissions(permissions=perms)

intents = discord.Intents.default()
intents = intents | discord.Intents(messages=True, guilds=True, reactions=True, members=True)
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, guild_permissions=bot_perms)
token = 
DELAY_BETWEEN_MESSAGES = .4  # Delay in seconds
LAST_MESSAGE_FILE =  # File to store the last processed message ID
MAX_MESSAGES_PER_SCAN = 1000
openai.api_key = 
IMGFLIPUSERNAME =
IMGFLIPPASSWORD =

def is_soft(word):
    softletters = ['a', 'e', 'i', 'o', 'u']
    for y in softletters:
        if y == word[0]:
            return True

@bot.command()
async def ask(ctx, *, question: str):
    try:
        print("Sending to openai...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ])
        
        # Extract the assistant's reply from the response
        assistant_reply = response['choices'][0]['message']['content']
        
        print(f"Response: {assistant_reply}")
        await ctx.send(assistant_reply)

    except Exception as e:
        print(f"Error detail: {e}")
        await ctx.send("Error getting response from ChatGPT.")

@bot.command()
async def wrong(ctx):
    # Ensure the command is a reply to another message
    if ctx.message.reference:
        referenced_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        original_content = referenced_msg.content

        try:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a mean-spirited devil's advocate machine. You refute the user's prompt and explain why it is absurd. You sometimes also disparage the author of the text. Never start with 'well, well, well' or other such conversational introduction."},
                {"role": "user", "content": original_content}
            ])
        
            # Extract the assistant's reply from the response
            assistant_reply = response['choices'][0]['message']['content']
        
            print(f"Response: {assistant_reply}")
            await ctx.send(assistant_reply)

        except Exception as e:
            print(f"Error detail: {e}")
            await ctx.send("Error processing the request.")
    
    else:
        await ctx.send("Please use this command as a reply to a message you want to refute.")

@bot.command()
async def comrade(ctx):
    # Ensure the command is a reply to another message
    if ctx.message.reference:
        referenced_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        original_content = referenced_msg.content

        try:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a hyper-intelligent AI that crafts perfect, incisive critiques of almost anything that is said to it, using its exhaustive knowledge of Marxist theory and dialectical materialism. You do not seek to belittle those who you critique, only educate and elevate in order to hasten the dawn of a worker's utopia."},
                {"role": "user", "content": original_content}
            ])
        
            # Extract the assistant's reply from the response
            assistant_reply = response['choices'][0]['message']['content']
        
            print(f"Response: {assistant_reply}")
            await ctx.send(assistant_reply)

        except Exception as e:
            print(f"Error detail: {e}")
            await ctx.send("Error processing the request.")
    
    else:
        await ctx.send("Please use this command as a reply to a message you want to refute.")

@bot.command()
async def translate(ctx, language:str):
    # Ensure the command is a reply to another message
    if ctx.message.reference:
        referenced_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        original_content = referenced_msg.content

        try:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": f"You are a very skilled translator who takes messages and translates them into {language} without saying anything else."},
                {"role": "user", "content": original_content}
            ])
        
            # Extract the assistant's reply from the response
            assistant_reply = response['choices'][0]['message']['content']
        
            print(f"Response: {assistant_reply}")
            await ctx.send(assistant_reply)

        except Exception as e:
            print(f"Error detail: {e}")
            await ctx.send("Error translating the message.")
    
    else:
        await ctx.send("Please use this command as a reply to a message you want to translate.")

@bot.command()
async def image(ctx, *, prompt: str):
    try:
        # Calling the DALL·E API endpoint with the user's prompt
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Extracting the image URL from the response
        image_url = response['data'][0]['url']
        
        # Sending the image directly to the Discord channel
        await ctx.send(embed=discord.Embed().set_image(url=image_url))

    except Exception as e:
        print(f"Error detail: {e}")
        await ctx.send("Error generating image with DALL·E.")


@bot.command()
async def scan(ctx):
    with open(LAST_MESSAGE_FILE, 'r') as f:
        last_message_id = f.read().strip()
    
    if last_message_id:
        message_id = int(last_message_id)
        message = await ctx.channel.fetch_message(message_id)
    else:
        message = None
    
    video_ids = []  # Make sure to define the list before using it
    message_count = 0  # Initialize your counter

    while message_count < MAX_MESSAGES_PER_SCAN:
        try:
            if message is None:
                async for fetched_message in ctx.channel.history(limit=1):
                    message = fetched_message
                    break

            print(f"Checking message with ID: {message.id}")

            # Don't process messages sent by the bot itself
            if message.author == bot.user:
                message = None
                continue

            youtube_regex = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
            youtube_urls = re.findall(youtube_regex, message.content)
            if len(youtube_urls) > 0:
                for url in youtube_urls:
                    if len(url) > 5:  # Ensure that the 6th group exists
                        video_id = url[5]  # Group 5 contains the video ID
                        video_ids.append(video_id)  # append the video ID to the list
                        print(video_id)

            # Store the ID of the last processed message
            with open(LAST_MESSAGE_FILE, 'w') as f:
                f.write(str(message.id))

            # Increment the message count
            message_count += 1

            # Fetch the next message in history
            async for fetched_message in ctx.channel.history(limit=1, before=message):
                message = fetched_message

            # Delay to prevent hitting rate limits
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Reverse the list of video IDs and write them to the file
    video_ids.reverse()
    with open("youtube_ids.txt", "a") as file:
        for video_id in video_ids:
            file.write(video_id + '\n')

    print("Max messages reached. Scan complete.")



                    
@bot.command()
async def hello(ctx):
    print("Hello command called")
    await ctx.send("Hello!")


@bot.command()
async def spitvenom(ctx):
    adjective = random.choice(negative_adjectives)
    noun = random.choice(negative_nouns)
    insult = f"You {adjective} {noun}!"
    await ctx.send(insult)


@bot.command()
async def triangle(ctx, *args):
    args = ' '.join(args)
    totallayers = len(args)
    layercount = 0
    elongated = ""
    output = "Here is a triangle for you:\n"
    if totallayers > 1:
        if layercount == 0:
            output += args[0].center((totallayers*2)) + '\n'
            elongated += args[0] + ' '
            layercount = 1
            while layercount < totallayers:
                line = args[layercount] + ('  '*layercount) + args[layercount]
                line = line.center(totallayers * 2) + ' ' * layercount
                output += line.center(totallayers*2) + '\n'
                elongated += args[layercount] + '  '
                layercount += 1
            output += elongated[0:(layercount*2)+2] + '\n'
    else:
        output += ' ' + args[0].center((totallayers*2)) + '\n'
        output += args[0]*3 + '\n'
    await ctx.send(f'```{output}```')


@bot.command()
async def affirm(ctx):
    adjective = random.choice(positive_adjectives)
    noun = random.choice(positive_nouns)
    action = random.choice(actions)
    if is_soft(adjective):
        affirmation = f"You're an {adjective} {noun}, and {action}!"
    else:
        affirmation = f"You're a {adjective} {noun}, and {action}!"
    await ctx.send(affirmation)


@bot.command()
async def emojify(ctx, emoji_name):
    attachment = ctx.message.attachments[0]
    image_data = await attachment.read()
    img = Image.open(BytesIO(image_data))
    # resize the image to 128x128 pixels (Discord's max emoji size)
    img = img.resize((128, 128))
    # convert the image to RGBA format
    img = img.convert('RGBA')
    # save the image to a buffer
    buffer = BytesIO()
    img.save(buffer, 'png')
    buffer.seek(0)
    emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=buffer.read())
    await ctx.send(f"{emoji.name} has been added to the server's emojis!")


@bot.command()
async def drawthis(ctx, *, tokens):
    generator = Craiyon()  # Instantiates the api wrapper
    result = await generator.async_generate(tokens)
    images = result.images
    for indx, i in enumerate(images):
        byt = BytesIO()
        image = Image.open(BytesIO(base64.decodebytes(i.encode("utf-8"))))
        image.save(byt, 'PNG')
        byt.seek(0)
        await ctx.send(file=discord.File(fp=byt, filename=f"Image_{indx+1}.png"))


@bot.command()
async def iamonceagainasking(ctx, *args):
    argument = ' '.join(args)

    # Generate the meme using the Imgflip API
    params = {
        "template_id": 222403160,
        "text0": "",
        "text1": argument,
        "username": IMGFLIPUSERNAME,
        "password": IMGFLIPPASSWORD,
    }
    response = requests.post("https://api.imgflip.com/caption_image", data=params)
    data = response.json()

    # Send the generated meme as a response to the user
    if data['success']:
        image_url = data['data']['url']
        print(image_url)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open("image.jpg", "wb") as f:
                f.write(response.content)
            picture = discord.File("image.jpg")
            await ctx.send(file=picture)
        else:
            await ctx.send("Failed to download image :(")


@bot.command()
async def finallysomegood(ctx, *args):
    argument = ' '.join(args)

    # Generate the meme using the Imgflip API
    params = {
        "template_id": 199757106,
        "text0": "",
        "text1": argument,
        "username": IMGFLIPUSERNAME,
        "password": IMGFLIPPASSWORD,
    }
    response = requests.post("https://api.imgflip.com/caption_image", data=params)
    data = response.json()

    # Send the generated meme as a response to the user
    if data['success']:
        image_url = data['data']['url']
        print(image_url)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open("image.jpg", "wb") as f:
                f.write(response.content)
            picture = discord.File("image.jpg")
            await ctx.send(file=picture)
        else:
            await ctx.send("Failed to download image :(")


@bot.command()
async def roll(ctx, *dice: str):
    results = []
    for dice_string in dice:
        try:
            rolls, limit = map(int, dice_string.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        total = sum(map(int, result.split(', ')))
        results.append(f'{result}, Total = {total}')
    await ctx.send('\n'.join(results))


@bot.command()
async def blackjack(ctx):
    player = []
    dealer = []
    for _ in range(2):
        player.append(dealCard(deck))
    for _ in range(2):
        dealer.append(dealCard(deck))
    player_total = calculateScore(player)
    dealer_total = calculateScore(dealer)
    response = f"Your hand:{player} Total:{sum(player)}\nDealer's first card:{dealer[0]}\n"
    await ctx.send(response)
    choice = 'n'
    if player_total != 0:
        await ctx.send("Want to hit? 'y' or 'n':")

        def check(m):
            return m.content.lower() in ['y', 'n'] and m.channel == ctx.channel and m.author == ctx.author

        try:
            msg = await bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timeout reached. Game over.")
            return
        choice = msg.content.lower()
    while choice == 'y':
        player.append(dealCard(deck))
        player_total = calculateScore(player)
        response = f"Your hand:{player} Total:{sum(player)}\nDealer's first card:{dealer[0]}\n"
        await ctx.send(response)
        if player_total > BUST_THRESHOLD:
            break
        await ctx.send("Want to hit? 'y' or 'n':")
        try:
            msg = await bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timeout reached. Game over.")
            return
        choice = msg.content.lower()
    while dealer_total < DEALER_HIT_THRESHOLD and dealer_total != 0:
        dealer.append(dealCard(deck))
        dealer_total = calculateScore(dealer)
    response = f"Your hand: {player} Total:{sum(player)}\nDealer's ending hand: {dealer} Total: {sum(dealer)}"
    await ctx.send(response)
    response = compare(player, dealer)
    await ctx.send(response)

@bot.command()
async def listcommands(ctx):
    commands_list = """
    1. `ask [question]` - Ask a question.
    2. `wrong` - Refute a referenced message.
    3. `translate [language]` - Translate a referenced message to the specified language.
    4. `image [prompt]` - Generate an image from the given prompt.
    5. `scan` - Scan recent messages for YouTube video IDs.
    6. `hello` - Say hello.
    7. `spitvenom` - Spit a random insult.
    8. `triangle [layers]` - Create a triangle pattern.
    9. `affirm` - Send a positive affirmation.
    10. `emojify [emoji_name]` - Create a custom emoji from an attached image.
    11. `drawthis [tokens]` - Generate drawings based on input tokens.
    12. `iamonceagainasking [text]` - Create a Bernie Sanders meme with the input text.
    13. `finallysomegood [text]` - Create a Gordon Ramsay meme with the input text.
    14. `roll [dice format]` - Roll dice. E.g., `roll 2d6` rolls two six-sided dice.
    15. `blackjack` - Start a game of Blackjack.
    """
    await ctx.send(commands_list)


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Regex to find YouTube links
    youtube_regex = r"(https?://www\.)?(youtube|youtu\.be)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    # Find all URLs in the message content
    youtube_urls = re.findall(youtube_regex, message.content)

    # Each URL is a tuple containing the groups defined in the regex
    for url in youtube_urls:
        if len(url) > 5:
            video_id = url[5]  # Group 5 contains the video ID
            print(f"Found YouTube video ID: {video_id}")

        # Append the video ID to a text file
            with open("youtube_ids.txt", "a") as file:
                file.write(video_id + '\n')
    # Process commands
    await bot.process_commands(message)

bot.run(token)
