#google colab selenium setup, run once and then remove
!pip install selenium
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install discord
#end of setup
import sys
import discord
import asyncio
import json
import random
import threading
import codecs
from discord.ext.tasks import loop
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep
import re
require_ping=False
token = "token"

class Cleverbot:
    def __init__(self):

        # initialize selenium options/arguments
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.opts.add_argument('--no-sandbox')
        self.opts.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(options=self.opts)
        self.url = 'https://www.cleverbot.com'
        self.hacking = False
        self.count = -1

    def get_form(self):

        # find the form tag to enter your message
        try:
            self.browser.find_element_by_id('noteb').click()
        except ElementNotInteractableException:
            pass

        while True:
            try:
                self.elem = self.browser.find_element_by_class_name('stimulus')
            except BrokenPipeError:
                continue
            break

    def send_input(self, userInput):

        # submits your message
        fOne = '<\/?[a-z]+>|<DOCTYPE'
        fTwo = '/<[^>]+>/g'
        if re.search(fOne, userInput) != None or re.search(fTwo, userInput) != None:
            self.hacking = True
            userInput = 'I will hack you'
        while True:
            try:
                self.elem.send_keys(userInput + Keys.RETURN)
            except BrokenPipeError:
                continue
            break

    def get_response(self):
        while self.hacking is False:
            try:
                while True:
                    try:
                        line = self.browser.find_element_by_id('line1')
                        sleep(3)
                        newLine = self.browser.find_element_by_id('line1')
                        if line.text != newLine and newLine.text != ' ' and newLine.text != '':
                            line = self.browser.find_element_by_id('line1')
                            sleep(3)
                            break
                    except StaleElementReferenceException:
                        self.url = self.url + '/?' + str(int(self.count + 1))
                        continue
            except BrokenPipeError:
                continue
            break
        if self.hacking is True:
            self.botResponse = 'Silly rabbit, html is for skids.'
        elif self.hacking is False:
            self.botResponse = line.text
        self.hacking = False
        return self.botResponse
bot = discord.Client(description="xddd", self_bot=True)
gs={"a":"text"}
writer=""
olw=""
print("Initializing bot...")
gs["rs"]=Cleverbot()
gs["rs"].browser.get(gs["rs"].url)
gs["rs"].get_form()
print("Starting discord...")
illegal_character = [':','<','>','_',"'","-"]
@bot.event
async def on_ready():
  print("Logged in")
  print("Bot is ready")
@bot.event
async def on_message(message):
  print("called")
  if message.author == bot.user:
    return
  global illegal_character, gs, writer, require_ping
  if bot.user.mentioned_in(message) or (message.guild and (not require_ping)):
    ma=message.guild
  elif not message.guild:
    ma=message.author
  if not ma in gs:
    print("New user")
    while not "rs" in gs:
      asyncio.sleep(1)
      print("Waiting for open thread...")
    gs[ma]=gs.pop("rs")
  userInput = (message.content)
  for z in illegal_character:
    userInput="".join(userInput.split(z))
  print(userInput)
  x = random.uniform(0.4, 1.5)
  print("typing...")
  await asyncio.sleep(x)
  async with message.channel.typing():
    gs[ma].send_input(userInput)
    b = gs[ma].get_response()
  await message.channel.send(b)
  if ma==message.author:
    print(str(message.author)+":"+message.content)
    print("bot:" + b)
    writer=writer+"\n"+(str(message.author)+":"+message.content)
    writer=writer+"\n"+("bot:" + b)
  else:
    print(str(message.guild)+":"+message.content)
    print("bot:" + b)
    writer=writer+"\n"+(str(message.guild)+"("+str(message.author)+"):"+message.content)
    writer=writer+"\n"+("bot:" + b)
def ns():
  global gs
  while True:
    if not "rs" in gs:
      #print("making new...")
      gs["rsh"]=Cleverbot()
      gs["rsh"].browser.get(gs["rsh"].url)
      gs["rsh"].get_form()
      gs["rs"]=gs.pop("rsh")
      #print("made new")
def wri():
  global olw,writer
  while True:
    if writer!=olw:
      print("log updated")
      olw=writer
      f=codecs.open("text.log", 'w', encoding='utf-8',errors='ignore')
      f.write(olw)
      f.close()
writ=threading.Thread(target=wri)
writ.start()
n=threading.Thread(target=ns)
n.start()
bot.run(token, bot=False)
