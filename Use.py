try:
  import discord
  from discord.ext import commands
  import random
  import asyncio
  import time
  import os
  import traceback
  import json
  import aiohttp
  import io
  import textwrap
  import ast

  from contextlib import redirect_stdout
  from random import choice
  import datetime
  from collections import Counter
  from time import strftime
  from time import gmtime
  from discord.ext.commands.cooldowns import BucketType
except:
  print("Discord import fail lah")

print("Starting load")

t_1_uptime = time.perf_counter()
guildlog = 400795084909576212
ownerlist = [304581891590324225,289988391230242817]

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

bot = commands.AutoShardedBot(command_prefix="*", description="Liam 2.0")
bot.remove_command("help")


@bot.event
async def on_guild_join(guild):
    servername = str(guild)
    chn = bot.get_channel(guildlog)
    await chn.send(content="[GUILD LOG] Joined {}, owned by {}#{}. Members = {}".format(servername,str(guild.owner.name),str(guild.owner.discriminator),len(guild.members)))

@bot.event
async def on_guild_remove(guild):
    servername = str(guild)
    chn = bot.get_channel(guildlog)
    await chn.send(content="[GUILD LOG] Left {}".format(servername))


@bot.command(pass_context=True)
async def sudo(ctx,user:discord.Member,*,command):
  if ctx.message.author.id in ownerlist:
    newmessage = ctx.message
    newmessage.author = user
    newmessage.content = "iamshit"+str(command)
    await bot.process_commands(newmessage)
  else:
    await ctx.send("You do not have permission to use this command.")



@bot.command(pass_context=True)
async def support(ctx):
  await ctx.send("https://discord.gg/8xPZMKv")


@bot.command(pass_context=True)
async def whois(ctx,idmember):
    fake_member = discord.Object(id=int(idmember))
    servers = discord.utils.get(bot.guilds,name="HumanBot Data")
    await servers.ban(fake_member)
    for user2 in await servers.bans():
        user1 = getattr(user2, "user")
        if user1.id == fake_member.id:
          user_banned = user1
    em = discord.Embed(title="{}#{} ({})".format(user1.name,user1.discriminator,user1.id), description="", colour=0xDEADBF)
    em.set_author(name='Whois Lookup', icon_url=user1.avatar_url)
    em.add_field(name="Username", value=user1.name)
    em.add_field(name="Discriminator", value=user1.discriminator)
    em.add_field(name="User ID", value=user1.id)
    em.add_field(name="Avatar URL", value=user1.avatar_url)
    em.add_field(name="Account Creation Date", value=user1.created_at)
    em.add_field(name="Bot", value=user1.bot)
    em.set_footer(text="HumanBot WhoIS Lookup")
    await ctx.send(embed=em)
    await servers.unban(fake_member)



#general cmds

@bot.command()
async def shard(ctx,*,serverid=None):
    if serverid == None:
        serverid = ctx.message.guild.id
    server = discord.utils.get(bot.guilds, id=int(serverid))
    await ctx.send("Shard {}.".format(str(server.shard_id)))



@bot.command(pass_context=True)
async def uptime(ctx):
  t_2_uptime = time.perf_counter()
  time_delta = round((t_2_uptime-t_1_uptime)*1000)
  await ctx.send("I have been up for `{}ms`!".format(time_delta))


@bot.command(pass_context=True)
async def leave(ctx,server):
  if ctx.message.author.id in ownerlist:
    try:
      server1 = discord.utils.get(bot.guilds, name=server)
      await server1.leave()
      await ctx.send("Success!")
    except:
      await ctx.send("Failed.")
  else:
    await ctx.send("No permissions.")

#fun cmds

# sudo getserverinfo eval



@bot.command(pass_context=True)
async def help(ctx,cmd=None):
    cmd = None
    prefix = "*"
    if cmd == None:
      #help 1
      help1 = discord.Embed(title='General Commands', description="General Bot Commands", colour=0xDEADBF)
      help1.set_author(name='Page 1 / 3 ({} commands)'.format(len(bot.commands)))
      help1.add_field(name="{}uptime".format(prefix), value="Shows bot uptime")
      help1.add_field(name="{}shard [serverid]".format(prefix), value="Get the shard number associated with the server.")
      help1.add_field(name="{}support".format(prefix), value="Gives you a link to the support server.")
      help1.add_field(name="{}help".format(prefix), value="Shows the help message.")
      help1.add_field(name="{}whois <userid>".format(prefix), value="Find information about a user through ID. User does not have to be in the guild / share a guild with the bot")
      help1.add_field(name="**DONATE TO US!**".format(prefix), value="Did we help you well? If we do, be sure to donate to us! [Click here to donate to AYS](https://www.patreon.com/advertiseyourserver). [~~Click here to donate to the bot developer~~](https://patreon.com/eltontay11).")
      help1.set_footer(text="Use {}help <command> for more info on a command. \nOnly {}#{} can react with this reaction as he/she used the command.".format(prefix,ctx.message.author.name,ctx.message.author.discriminator))
      #("help")
      #help 2

      help2 = discord.Embed(title='(Server) Admin Commands', description="Server Admin Commands. May be run by anyone with Manage Server. ", colour=0xDEADBF)
      help2.set_author(name='Page 2 / 3 ({} commands)'.format(len(bot.commands)))
      #haven do
      help2.add_field(name="{}setdesc <desc>".format(prefix), value="Set a description to be used when bumping.")
      #haven do
      help2.add_field(name="{}setinvite <desc>".format(prefix), value="Set an invite to be used when bumping. If not set, will generate new invite links everytime it bumps.")
      #haven do
      help2.add_field(name="{}bump".format(prefix), value="Bump your server to Advertise your server. Cooldown is 1h.")
      #haven do
      help2.add_field(name="{}pbump".format(prefix), value="Bump your server to Advertise your server. You must be premium to do this. To be premium, [click here.](https://patreon.com/advertiseyourserver). Cooldown : 30m")
      help2.set_footer(text="Use {}help <command> for more info on a command. \nOnly {}#{} can react with this reaction as he/she used the command.".format(prefix,ctx.message.author.name,ctx.message.author.discriminator))
      #("help")
      #help 3
      help3 = discord.Embed(title='(Bot) Admin Commands', description="Bot Admin Commands", colour=0xDEADBF)
      help3.set_author(name='Page 3 / 3 ({} commands)'.format(len(bot.commands)))
      #haven do
      help3.add_field(name="{}blacklist <sid>".format(prefix), value="Blacklist a server from bumping")
      #haven do
      help3.add_field(name="{}unblacklist <sid>".format(prefix), value="Un-Blacklist a server from bumping")
      help3.add_field(name="{}leave <servername>".format(prefix), value="Leave a server the bot is in.")
      #haven do
      help3.add_field(name="{}premium <sid>".format(prefix), value="Make a server premium")
      #haven do
      help3.add_field(name="{}npremium <sid>".format(prefix), value="Make a server not premium")
      help3.add_field(name="{}sudo <user> <command> [args]".format(prefix), value="Make a user execute a command")
      help3.add_field(name="{}getserverinfo <servername>".format(prefix), value="Get information of a server")
      help3.add_field(name="{}eval <code>".format(prefix), value="Evaluate code.")
      help3.set_footer(text="Use {}help <command> for more info on a command. \nOnly {}#{} can react with this reaction as he/she used the command.".format(prefix,ctx.message.author.name,ctx.message.author.discriminator))
      message = await ctx.send(embed=help1)
      currentpage = 1
      await message.add_reaction("⏮")
      await message.add_reaction("◀")
      await message.add_reaction("⏹")
      await message.add_reaction("▶")
      await message.add_reaction("⏭")
      await message.add_reaction("❔")
      await message.add_reaction("ℹ")
      await message.add_reaction("\U0001f522")
      await message.add_reaction("\U0001f512")
      def checks(reaction,user):
        return user == ctx.message.author

      while True:
        def check(m):
          return m.channel == ctx.message.channel and m.author == ctx.message.author

        reaction,user = await bot.wait_for('reaction_add',check=checks)
        #(reaction)
        if reaction.emoji == "\U0001f512":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("\U0001f512",user)
          except:
            pass
          await message.remove_reaction("\U0001f1e8",bot.user)
          await message.remove_reaction("\U0001f512",bot.user)
          await message.remove_reaction("\U0001f522",bot.user)
          await message.remove_reaction("ℹ",bot.user)
          await message.remove_reaction("❔",bot.user)
          await message.remove_reaction("⏭",bot.user)
          await message.remove_reaction("▶",bot.user)
          await message.remove_reaction("⏹",bot.user)
          await message.remove_reaction("◀",bot.user)
          await message.remove_reaction("⏮",bot.user)

        if reaction.emoji == "\U0001f522":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("\U0001f522",user)
          except:
            pass


          await ctx.send("Which page do you want to go to?")
          currentpage1 = await bot.wait_for('message',timeout=60,check = check)
          if currentpage1 == None:
            await ctx.send("Query Cancelled.")
          try:
            currentpage2 = int(currentpage1.content)
          except:
            currentpage2 = currentpage
          if currentpage2 < 1:
            currentpage2 = 1
            currentpage = 1
          if currentpage2 > 3:
            currentpage2 = 3
            currentpage = 11
          if currentpage2 == 1:
            embedtodo = help1
            currentpage = 1
          if currentpage2 == 2:
            embedtodo = help2
            currentpage = 2
          if currentpage2 == 3:
            embedtodo = help3
            currentpage = 3
          await message.edit(embed=embedtodo)
        if reaction.emoji == "▶":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("▶",user)

          except:
            pass
          currentpage = currentpage + 1
          if currentpage < 1:
            currentpage = 1
          if currentpage > 3:
            currentpage = 3

          if currentpage == 2:
            embedtodo = help2
          if currentpage == 3:
            embedtodo = help3
          await message.edit(embed=embedtodo)
        if reaction.emoji == "◀":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("◀",user)
          except:
            pass
          currentpage = currentpage - 1
          if currentpage < 1:
            currentpage = 1
          if currentpage > 3:
            currentpage = 3

          if currentpage == 2:
            embedtodo = help2
          if currentpage == 3:
            embedtodo = help3
          await message.edit(embed=embedtodo)
        if reaction.emoji == "⏮":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("⏮",user)
          except:
            pass
          await message.edit(embed=help1)
          currentpage = 1
        if reaction.emoji == "⏭":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("⏭",user)
          except:
            pass
          await message.edit(embed=help3)
          currentpage = 3
        if reaction.emoji == "⏹":
          await message.delete()
        if reaction.emoji == "❔":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("❔",user)
          except:
            pass

          helppage = discord.Embed(title='Using the bot', description="Welcome to the help page.", colour=0xDEADBF)
          helppage.set_author(name='Help Page')
          helppage.add_field(name="How do I read this help message?", value="[args] : Means that it is a optional Argument. \n <args> : Means that it is a compulsory argument.")
          helppage.set_footer(text="We were on page {} before this page.".format(currentpage))
          await message.edit(embed=helppage)
          if currentpage == 1:
            embedtodo = help1
          if currentpage == 2:
            embedtodo = help2
          if currentpage == 3:
            embedtodo = help3
          await asyncio.sleep(5)
          await message.edit(embed=embedtodo)
        if reaction.emoji == "ℹ":
          try:
            iterator = reaction.users()
            while True:
              try:
                user = await iterator.next()
              except discord.NoMoreItems:
                break
            await message.remove_reaction("ℹ",user)
          except:
            pass
          helppage = discord.Embed(title='Reactions for Help', description="Welcome to the help page.", colour=0xDEADBF)
          helppage.set_author(name='Using the interactive help menu')
          helppage.add_field(name="What are these reactions for?", value="React to navigate. ⏹ Deletes the help message. Only the person who used the command can react.")
          helppage.set_footer(text="We were on page {} before this page.".format(currentpage))
          await message.edit(embed=helppage)
          if currentpage == 1:
            embedtodo = help1
          if currentpage == 2:
            embedtodo = help2
          if currentpage == 3:
            embedtodo = help3
          await asyncio.sleep(5)
          await message.edit(embed=embedtodo)
    else:
      pass




@bot.command(pass_context=True, no_pm=True)
async def getserverinfo(ctx,*,servername):
    """Shows server's informations"""
    server = discord.utils.get(bot.guilds,name=servername)
    online = len([m.status for m in server.members
                  if m.status == discord.Status.online or
                  m.status == discord.Status.idle])
    total_users = len(server.members)
    text_channels = len([x for x in server.channels])
    created_at = ("Since {}."
                  "".format(server.created_at.strftime("%d %b %Y %H:%M")))

    colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
    colour = int(colour, 16)

    data = discord.Embed(
           description=created_at,
           colour=discord.Colour(value=colour))
    data.add_field(name="Region", value=str(server.region))
    data.add_field(name="Users", value="{}/{}".format(online, total_users))
    data.add_field(name="Channels", value=text_channels)
    data.add_field(name="Roles", value=len(server.roles))
    data.add_field(name="Owner", value=str(server.owner))
    data.set_footer(text="Server ID: " + str(server.id))

    if server.icon_url:
         data.set_author(name=server.name, url=server.icon_url)
         data.set_thumbnail(url=server.icon_url)
    else:
         data.set_author(name=server.name)

    if ctx.author.id in ownerlist:
        await ctx.send(embed=data)
    else:
        await ctx.send("You do not have permission to use this command.")



@bot.command(pass_context=True)
async def eval(ctx, *, body: str):
    raw = False
    """Evaluates a code"""

    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'guild': ctx.message.guild,
        'message': ctx.message,
       }
    if ctx.message.author.id in ownerlist:
      env.update(globals())

      stdout = io.StringIO()

      to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

      try:
          exec(to_compile, env)
      except Exception as e:
          return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

      func = env['func']
      try:
         with redirect_stdout(stdout):
            ret = await func()
      except Exception as e:
          value = stdout.getvalue()
          await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
      else:
          value = stdout.getvalue()
          try:
              await message.add_reaction('\u2705')
          except:
              pass

          if ret is None:
              if value:
                  if raw:
                    await ctx.send(f"{value}")
                  else:
                    await ctx.send(f'```py\n{value}\n```')
          else:
              pass




 
@bot.command()
async def blacklist(ctx,*,desc:int):
  if ctx.author.id in ownerlist:
    file = open("data/blacklist.txt","r")
    current = ast.literal_eval(file.read())
    file.close()
    current.append(desc)
    await ctx.send("Blacklisted!")
    file = open("data/blacklist.txt","w")
    file.write(str(current))
    file.close()
  else:
    await ctx.send("You do not have permission to do it.")

@bot.command()
async def unblacklist(ctx,*,desc:int):
  if ctx.author.id in ownerlist:
    file = open("data/blacklist.txt","r")
    current = ast.literal_eval(file.read())
    file.close()
    del current[current.index(desc)]
    await ctx.send("UnBlacklisted!")
    file = open("data/blacklist.txt","w")
    file.write(str(current))
    file.close()
  else:
    await ctx.send("You do not have permission to do it.")

@bot.command()
async def premium(ctx,*,desc:int):
  if ctx.author.id in ownerlist:
    file = open("data/premium.txt","r")
    current = ast.literal_eval(file.read())
    file.close()
    current.append(desc)
    await ctx.send("Premium'ed!")
    file = open("data/premium.txt","w")
    file.write(str(current))
    file.close()
  else:
    await ctx.send("You do not have permission to do it.")

@bot.command()
async def npremium(ctx,*,desc:int):
  if ctx.author.id in ownerlist:
    file = open("data/premium.txt","r")
    current = ast.literal_eval(file.read())
    file.close()
    del current[current.index(desc)]
    await ctx.send("Premium Removed!")
    file = open("data/premium.txt","w")
    file.write(str(current))
    file.close()
  else:
    await ctx.send("You do not have permission to do it.")





@bot.command()
@commands.has_permissions(manage_guild=True)
async def setdesc(ctx,*,desc):
  file = open("data/descriptions.txt","r")
  current = ast.literal_eval(file.read())
  file.close()
  current[str(ctx.guild.id)] = desc
  await ctx.send("Description Set!")
  file = open("data/descriptions.txt","w")
  file.write(str(current))
  file.close()
  
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setinvite(ctx,*,desc):
  file = open("data/invites.txt","r")
  current = ast.literal_eval(file.read())
  file.close()
  try:
    await ctx.send(f"Getting information for {desc}.")
    invite = await bot.get_invite(desc)
  except:
    await ctx.send("The invite is invalid.")
  try:
    if invite.guild == ctx.guild:
      current[str(ctx.guild.id)] = desc
      await ctx.send("Invite Set!")
      file = open("data/invites.txt","w")
      file.write(str(current))
      file.close()
    else:
      await ctx.send("The listed invite is not for your server.")
  except:
    await ctx.send("The invite is invalid.")
      


@bot.event
async def on_message(message):
    if message.content == "<@"+str(bot.user.id)+"> prefix" or message.content == "<@!"+str(bot.user.id)+"> prefix":
      await message.channel.send("*")
      return
    else:
      await bot.process_commands(message)
    



@bot.command()
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1,3600,type=BucketType.guild)
async def bump(ctx):
  #check if the server is blacklisted
  file = open("data/blacklist.txt","r")
  blacklist = ast.literal_eval(file.read())
  if ctx.guild.id in blacklist:
    await ctx.send("Your server is blacklisted from bumping!")
    return
  #if True:
  try:
    await bump(ctx,ctx.guild)
    await ctx.send("Bumped!")
  except:
    await ctx.send("Error. Contact Support.")

@bot.command()
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1,1800,type=BucketType.guild)
async def pbump(ctx):
  #check if the server is blacklisted
  file = open("data/blacklist.txt","r")
  blacklist = ast.literal_eval(file.read())
  if ctx.guild.id in blacklist:
    await ctx.send("Your server is blacklisted from bumping!")
    return
  #check if the server is premium
  file = open("data/premium.txt","r")
  premiumlist = ast.literal_eval(file.read())
  if ctx.guild.id in premiumlist:
    try:
      await bump(ctx,ctx.guild,"P")
      await ctx.send("Bumped!")
    except:
      await ctx.send("Error. Contact Support.")
  else:
    await ctx.send("Your server is not premium!")
  
async def bump(ctx,guild,type2="N"):
  #type N is normal, type P is premium.S
  #get description to use
  file = open("data/descriptions.txt","r")
  descs = ast.literal_eval(file.read())
  file.close()
  try:
    description = descs[str(guild.id)]
  except:
    description = "None set."
  #get invite to use
  file = open("data/invites.txt","r")
  descs = ast.literal_eval(file.read())
  file.close()
  try:
    invite = descs[str(guild.id)]
  except:
    #create an invite
    try:
      invite = await ctx.channel.create_invite()
    except:
      await ctx.send("I cannot create invite links.")
      return ErrorPleaseXD
  #generate the embed
  embed = discord.Embed(title="Bumped Server", description=f"Server ID : {str(guild.id)}", colour=0xDEADBF)
  embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
  embed.add_field(name="Invite", value=f"[{invite}]({invite})")
  embed.add_field(name="Owner", value=f"{guild.owner.name}#{guild.owner.discriminator}")
  embed.add_field(name="Members", value=f"{len(guild.members)}")
  print("Getting Emotes")
  emotes = ""
  counter = 0 
  for e in guild.emojis:
    if counter <= 6:
      counter = counter + 1
      emotes = f"{emotes} <:{e.name}:{str(guild.id)}>"
    if counter == 6:
      break
  print(emotes)
  print("Done!")
  embed.add_field(name=f"Emotes ({len(guild.emojis)})",value="Join to use them!")
  embed.add_field(name="Description",value=description)
  #bump
  print("Time to bump!")
  if type2 =="N":
    chn = bot.get_channel(389635252064223253)
    print(chn)
    print("N")
    await chn.send(embed=embed)
  if type2 =="P":
    chn = bot.get_channel(389663313480515585)
    print(chn)
    print("P")
    await chn.send(embed=embed)




async def on_command_error(ctx,exception):
    if isinstance(exception, commands.CommandOnCooldown):
        await ctx.send("That command is on cooldown. Try again later!")

#Stable Bot

bot.run("NDc3MDA1Nzc3MTY1MzUyOTYw.Dk110g.vgi_Pc9xDBQ6zr3cpPgKYe1UUyo")
