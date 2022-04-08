#from asyncio.windows_events import NULL
from email import message
from multiprocessing import Condition
#from turtle import addshape, title
import discord
from dotenv import load_dotenv
import os
import time
import asyncio
import random
from calculate import *
from sendmail_please import *
from discord.ext import commands
from generate_exp import *
from discord.utils import *

def main():
    client = commands.Bot(command_prefix='!')

    load_dotenv()
    
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_guild_join(guild):
        channelname = 'cb_quiz'
        condition = find(lambda x: x.name == 'cb_quiz', guild.text_channels)
        if not condition:
            await guild.create_text_channel(name='{}'.format(channelname))
        condition = find(lambda x: x.name == 'general', guild.text_channels)
        if condition:
            embed_message = discord.Embed(title=f"Hi! {guild.name}.", description="Say $help to view all commands. Lets all have some fun!", color=0xA3B3C1)
            for server in guild.text_channels:
                if server.name == 'general':
                    await server.send(embed=embed_message)
                    break
            


    @client.event
    #takes message as parameter since it's receiving message from discord
    async def on_message(message):
        #Also make it so that it doesn't do anything if the message is from itself.
        if message.author == client.user:
            return

        msg = message.content

        if msg.startswith('$calculate'):
            exp = ''
            for i in range(10, len(msg)):
                if(msg[i] != ' '):
                    exp += msg[i]

            result = ''
            try:
                result = str(calc(exp))
                await message.channel.send('Result: ' + result)
            except:
                await message.channel.send('ERROR. Check if you have any typos.\nWould you like to report this error? ($yes)')
                str_response = await client.wait_for('message', check=lambda m: m.author == message.author and m.channel == message.channel, timeout=30)
                if str_response.content == '$yes':
                    try:
                        Error_Catch(exp)
                        await message.channel.send('Error was reported successfully.')
                    except:
                        await message.channel.send('Error occurred while pending your request.')
        elif msg.startswith('$countdown'):
            desired_time = ''
            int_time = -1
            for i in range(10, len(msg)):
                if(msg[i] != ' '):
                    desired_time += msg[i]
            try:
                int_time = int(desired_time)
                if int_time < 0:
                    await message.channel.send('Negative numbers can\'t be tolerated in this command.')
                    return
                elif int_time > 86400:
                    await message.channel.send('Countdown shouldn\'t be longer than a day.')
                    return
            except:
                await message.channel.send('Number can\'t be recognized.')
                return
            try:
                await message.channel.send('Countdown request accepted!')
                await client.wait_for('message',check=lambda m: m.content == '$stop' and m.channel == message.channel and m.author == message.author, timeout=int_time)
                await message.channel.send(f'{message.author.mention} Your countdown has stopped!')
            except asyncio.TimeoutError:
                await message.channel.send(f'{message.author.mention} Your countdown has ended!')
        

            #while int_time > 0:
            #    m, s = divmod(int_time, 60)
            #    h, m = divmod(m, 60)
            #    return_msg = str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
            #    await message.channel.send(return_msg)
            #    time.sleep(1)
            #    int_time -= 1
        elif msg.startswith('$quiz'):
            if(message.channel.name != 'cb_quiz'):
                await message.channel.send('This command should only be used in \"cb_quiz\" channel.')
                return
            await message.channel.send(f'{message.author.mention} Your quiz starting in...')
            count = 3
            while(count > 0):
                await message.channel.send(f'{message.author.mention} ' + str(count))
                time.sleep(1)
                count -= 1
            
            correct = 0
            incorrect = 0
            problems = 1
            await message.channel.send(f'{message.author.mention}when writing your answer, your answer should not include any spaces, round answer to nearest integer if needed. Also we will use Banker\'s Rounding in here.')
            while(problems != 6):
                difficulty = random.randint(1, 3)
                exp = generate_expression(difficulty)
                answer = round(float(calc(exp)))
                exp = spacesAdd(exp)
                await message.channel.send(f'{message.author.mention}' + str(problems) + '. ' + exp + ' = ?\nGiven time: ' + str(60*difficulty) + " seconds.")
                
                try:
                    user_answer = await client.wait_for('message', check=lambda m: m.author == message.author and m.channel == message.channel, timeout=60*difficulty)
                    if user_answer.content == str(answer):
                        await message.channel.send(f'{message.author.mention} Well done.')
                        correct += 1
                    elif user_answer.content == '$screw':
                        await message.channel.send('Giving up so soon?')
                        break
                    else:
                        incorrect += 1
                        await message.channel.send(f'{message.author.mention} Wrong. Correct answer was: ' + str(answer))
                except asyncio.TimeoutError:
                    await message.channel.sand(f'{message.author.mention} Time up bruh. (It\'ll count as an incorrect)')
                    incorrect += 1
                problems += 1
            await message.channel.send(f'{message.author.mention} Result of your quiz: ' + str(correct) + ' correct(s), ' + str(incorrect) + ' incorrect(s)')
            if incorrect + correct != 5:
                return
            elif incorrect < 2:
                await message.channel.send('Decent.')
            elif incorrect < 5:
                await message.channel.send('It\'s not the most satisfying result I would say.')
            elif incorrect == 5:
                await message.channel.send('Maximum stupidity.')
        
        elif msg.startswith('$leave') and message.author.guild_permissions.kick_members:
            embed_goodbye = discord.Embed(title=f"Goodbye! {message.guild.name}.", description="Thank you for having me here! I wish y'all the best and hope we see each other again!", color=0xFF5733)
            await message.channel.send(embed=embed_goodbye)
            channel = get(message.guild.channels, name='cb_quiz')
            if channel is not None:
                await channel.delete()
            await discord.utils.get(client.guilds, name=message.guild.name).leave()

        elif msg.startswith('$help'):
            with open('_guideline.txt', 'r') as read_things:
                await message.channel.send(read_things.read())

    client.run(os.getenv("TOKEN"))

if __name__ == '__main__':
    main()