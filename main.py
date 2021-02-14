import cleverbotfree.cbfree
import sys
import discord
import asyncio
import json
import random, time, threading
from discord.ext.tasks import loop
bot = discord.Client(description="xddd", self_bot=True)
gs={"a":"text"}
writer=""
olw=""
token = "ODA4Nzk0ODQ2NjAwMzY0MDM0.YCLv-A.eH_ZKb2MvEzyEOgeL98o1CwISQw"
print("Creating handler...")
gs["rs"]=cleverbotfree.cbfree.Cleverbot()
gs["rs"].browser.get(gs["rs"].url)
gs["rs"].get_form()
print("Loading discord api...")
illegal_character = [':','<','>','_',"'","-"]
@bot.event
async def on_ready():
        print("Logged in")
@bot.event
async def on_message(message):
  print("called")
  if message.author == bot.user:
    return
  global illegal_character, gs, writer
  if message.guild:
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
    writer=writer+"\n"+(str(message.guild)+"("+str(message.author)+"):"+message.content)
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
def ns():
  global gs
  while True:
    if not "rs" in gs:
      print("making new...")
      gs["rs"]=cleverbotfree.cbfree.Cleverbot()
      gs["rs"].browser.get(gs["rs"].url)
      gs["rs"].get_form()
      print("made new")
    time.sleep(2)
nss=threading.Thread(target=ns)
nss.start()
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
