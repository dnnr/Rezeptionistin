#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: set ts=2 sw=2:

import re
import sys
import random
import socket
import urllib2
import logging
import ConfigParser
from pyquery import PyQuery as pq
from wikitools import wiki
from wikitools import category
from asyncirc.ircbot import IRCBot

config = ConfigParser.ConfigParser()
if not config.read("config.ini"):
  print "Error: your config.ini could not be read"
  exit(1)

server=config.get('IRC','server')
port=int(config.get('IRC', 'port'))
nick=config.get('IRC', 'nick')
ircchan=config.get('IRC', 'ircchan')
debugchan=config.get('IRC', 'debugchan')
useragent=config.get('HTTP', 'useragent')
site = wiki.Wiki(config.get('MediaWiki', 'wikiapiurl'))
site.login(config.get('MediaWiki', 'user'), config.get('MediaWiki', 'password'))
httpregex=re.compile(r'https?://')

if sys.hexversion > 0x03000000:
  raw_input = input

logging.basicConfig(level=logging.DEBUG)
irc = IRCBot(server, port, nick)

# Custom Functions
def netcat(hostname, port, content):
  s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  s.connect((hostname, port))
  s.shutdown(socket.SHUT_WR)
  while 1:
    data = s.recv(1024)
    if data == "":
      break
    f = data
  s.close()
  return f

def wikiupdate(title, url):
  cat = category.Category(site, "Linklist")
  for article in cat.getAllMembersGen(namespaces=[0]):
    article.edit(appendtext="\n* {title} - {url} \n".format(title=title, url=url))

def geturlfrommsg(message):
  url = re.search("(?P<url>https?://[^\s]+)", message).group("url")
  return url

def geturltitle(url):
  try:
    page = pq(url, headers={'user-agent': useragent})
    t = page("title").text().lstrip().encode('ascii','ignore')
  except:
    t = ""
  return t

def send_message(self, recipient, msg):
  self.msg(recipient, "\x0F" + msg)
def send_command(self, recipient, cmd):
  self.msg(recipient, cmd)

# IRC Handlers

@irc.on_msg
def on_msg(self, nick, host, channel, message):
  if message.lower().startswith('!help'):
    send_message(self, nick, "Erzaehl mir doch was du brauchst, mein Junge.")
    send_message(self, nick, "Ich kann bisher:")
    send_message(self, nick, "!kt - Zeige aktuelle Temperatur in der K4CG.")
    send_message(self, nick, "!gt - Guten Tag wuenschen.")
    send_message(self, nick, "!np - Dir sagen welche Musik so laeuft.")
    send_message(self, nick, "!beleidige <nick> - Jemanden beleidigen.")
    send_message(self, nick, "!lobe <nick> - Jemandem ein Kompliment machen.")
    send_message(self, nick, "oder dir den Titel von URLs sagen die du in den Channel postest")
  if message.lower().startswith('!kt'):
    temp = netcat("2001:a60:f073:0:21a:92ff:fe50:bdfc", 31337, "9001")
    send_message(self, channel, "Die aktuelle Temperatur in der K4CG ist{temp} Grad".format(temp=temp) )
  if message.lower().startswith('!gt'):
    send_message(self, channel, "Ich lebe noch, {nick}".format(nick=nick))
  if message.lower().startswith('!np'):
    send_message(self, channel, "Das funktioniert noch nicht.")
  if message.lower().startswith('!beleidige'):
    if len(message.split()) >= 2:
      send_message(self, channel, message.split()[1] + ", du " + random.choice(list(open('lists/insults.txt'))))
  if message.lower().startswith('!lobe'):
    if len(message.split()) >= 2:
      send_message(self, channel, message.split()[1] + ", " + random.choice(list(open('lists/flattery.txt'))))
  if message.lower().startswith('!utf8'):
      send_message(self, channel, "hällö")
  if httpregex.search(message.lower()) is not None:
    url = geturlfrommsg(message)
    title = geturltitle(url)
    if not title == "":
      send_message(self, channel, "Title: {title}".format(title=title))
      wikiupdate(title, url)

@irc.on_privmsg
def on_privmsg(self, nick, host, message):
  if message.lower().startswith('!gt'):
    send_message(self, nick, "Ich lebe noch, {nick}".format(nick=nick))

# Start Bot
irc.start()
irc.join(ircchan)
irc.join(debugchan)

# Run Eventloop
try:
  while irc.running:
    irc.send_raw(raw_input(""))
except KeyboardInterrupt:
  print("Received exit command")
finally:
  irc.stop()
