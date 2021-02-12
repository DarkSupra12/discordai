import cleverbotfree.cbfree
import sys
import discord
import asyncio
import json
import random
from discord.ext.tasks import loop
bot = discord.Client(description="xddd", self_bot=True)

token = "token"

illegal_character = [':','<','>','_',"'","-"]
def st(cb):
  try:
    cb.browser.get(cb.url)
  except:
    cb.browser.close()
    sys.exit()
  try:
    cb.get_form()
  except:
    sys.exit()
@bot.event
async def on_ready():
        print("Logged in")
gs={"a":"text"}
writer=""
olw=""
@bot.event
async def on_message(message):
  print("called")
  if message.author == bot.user:
    return
  global illegal_character, gs, writer
  if bot.user.mentioned_in(message):
    if not message.guild in gs:
      gs[message.guild]=gs.pop("rs")
    userInput = (message.content)
    for z in illegal_character:
      userInput="".join(userInput.split(z))
    print(userInput)
    
    if userInput in illegal_character:
            print(f"{message.author} has said an illegal character")
    x = random.uniform(0.4, 1.5)
    print("typing...")
    await asyncio.sleep(x)
    async with message.channel.typing():
      gs[message.guild].send_input(userInput)
      b = gs[message.guild].get_response()
    await message.channel.send(b)
    print(str(message.guild)+":"+message.content)
    print("bot:" + b)
    writer=writer+"\n"+(str(message.guild)+":"+message.content)
    writer=writer+"\n"+("bot:" + b)
  elif not message.guild:
    if not message.author in gs:
      gs[message.author]=gs.pop("rs")
    userInput = (message.content)
    for z in illegal_character:
      userInput="".join(userInput.split(z))
    print(userInput)
    
    if userInput in illegal_character:
            print(f"{message.author} has said an illegal character")
    x = random.uniform(0.4, 1.5)
    print("typing...")
    await asyncio.sleep(x)
    async with message.channel.typing():
      gs[message.author].send_input(userInput)
      b = gs[message.author].get_response()
    await message.channel.send(b)
    print(str(message.author)+":"+message.content)
    print("bot:" + b)
    writer=writer+"\n"+(str(message.author)+":"+message.content)
    writer=writer+"\n"+("bot:" + b)
@loop(seconds=5)
async def ns():
  global gs
  if not "rs" in gs:
    print("making new...")
    gs["rs"]=cleverbotfree.cbfree.Cleverbot()
    try:
      gs["rs"].browser.get(gs["rs"].url)
    except:
      gs["rs"].browser.close()
      sys.exit()
    try:
      gs["rs"].get_form()
    except:
      sys.exit()
    print("made new")
ns.start()
@loop(seconds=2)
async def wri():
  global olw,writer
  if writer!=olw:
    print("log updated")
    olw=writer
    f=open("text.log","w")
    f.write(olw)
    f.close()
wri.start()
bot.run(token, bot=False)
