from sqlite3 import connect 
import sqlite3
import time
import datetime
from datetime import date
from discord.ext import commands,tasks
import asyncio
import discord
from datetime import date , datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')
Announcement=768467811521134632

class DB_MANAGER():
    def __init__(self):
        self.db_connection = connect('heckorbot.db')
        self.crsr = self.db_connection.cursor()

    def creeateTable(self):
        try:
            sqlCommand = """
            CREATE TABLE events (  
            eventname VARCHAR(200) PRIMARY KEY,
            date DATE)
            """
            self.crsr.execute(sqlCommand)
            return "[DB UP AND RUNING]"
        except Exception as e:
            return e
    
    def addEntry(self,eventname,timestamp = str(date.today())):
        try:
            sqlCommand = """
            INSERT INTO events (eventname,date) VALUES (?,?)
            """
            print(timestamp)
            self.crsr.execute(sqlCommand,(eventname,timestamp,))
            self.db_connection.commit()
            return "Entry Successfull made with timestamp : " + str(time.time())
        except Exception as e:
            return e
    
    def removeEntry(self,eventname):
        try:
            sqlCommand = """
            DELETE FROM events WHERE eventname = (?)
            """
            self.crsr.execute(sqlCommand,(eventname,))
            self.db_connection.commit()
            return "Entry deleted : " + eventname
        except Exception as e:
            return e
    
    def moddifyEntry(self,stat,modifiedVal,ofEvent):
        if stat == "time":
            try:
                sql_Command = """
                UPDATE events SET date = (?) where eventname =(?) 
                """
                self.crsr.execute(sql_Command,(modifiedVal,ofEvent,))
                self.db_connection.commit()
                return "Entry modified " + stat+"with " + modifiedVal + "for " + ofEvent
            except Exception as e:
                return e
        elif stat == "eventname":
            try:
                sql_Command = """
                UPDATE events SET eventname = (?) where eventname =(?) 
                """
                self.crsr.execute(sql_Command,(modifiedVal,ofEvent,))
                self.db_connection.commit()
                return "Entry modified " + stat +" with " + modifiedVal + "for " + ofEvent
            except Exception as e:
                return e

    def showall(self):
        try:
            sql_Command = """
            SELECT * from events 
            """
            return self.crsr.execute(sql_Command).fetchall()
        except Exception as e:
            return e

    def todayslog(self):
        try:
            today = datetime.strftime(datetime.now(IST),'%d-%m')
            sql_Command = """
            SELECT date FROM events   
            """
            stats = self.crsr.execute(sql_Command).fetchall()
            for date in stats:
                if today in date[0]:
                    sql_Command = """SELECT * FROM events where date = ?"""
                    return self.crsr.execute(sql_Command,(date[0],)).fetchall()
        except Exception as e:
            return e

# db = DB_MANAGER()
# db.addEntry("ungli diwas",'2020-11-21')

class eventmanager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = DB_MANAGER()
        self.eventlog.start()
        self.flag = False

    @commands.group()
    async def event(self, ctx):
        pass
    
    @event.command(pass_context = True)
    async def help(self,ctx):
        await ctx.send(embed = discord.Embed(
            name = "!! HELP !!",
            description = """
            ```
            -----------------
            |   EVENTS LOG  |
            -----------------
1. add -> .event add "<eventname>" "<date(%d-%m-%y)>"
2. show -> .event show
3. delete -> .event delete "<eventname>"
4. modify -> .event <time/eventname> "<to_chng_value>" "<eventname>"```
            """,
            colour=0x4262F4,
        ))

    @event.command(pass_context=True)
    async def add(self,ctx,eventname,date):
        status = self.db.addEntry(eventname,date)
        await ctx.send(status)

    @event.command(pass_context=True)
    async def show(self,ctx):
        embeds = []
        status = self.db.showall()
        for details in status:
            embed = discord.Embed(
                title="Events",
                # description= '```  ```',
                colour=0x4262F4,
            )
            embed.add_field(name="Event", value='```' + details[0] + '```', inline=True)
            embed.add_field(name="Date", value='```' + details[1] + '```', inline=True)
            embeds.append(embed)
        for embed in embeds:
            await ctx.send(embed = embed)

    @event.command(pass_context=True)
    async def delete(self,ctx,eventname):
        status = self.db.removeEntry(eventname)
        await ctx.send(status)

    @event.command(pass_context=True)
    async def modify(self,ctx,stat,modified,modify):
        status = self.db.moddifyEntry(stat,modified,modify)
        await ctx.send(status)

    @tasks.loop(seconds = 1)
    async def eventlog(self):
        embeds = []
        now = datetime.now(IST)
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            await self.client.wait_until_ready()
            channel = self.client.get_channel(int(Announcement))
            status = self.db.todayslog()
            for details in status:
                embed = discord.Embed(
                    title="Today's Events",
                    # description= '```  ```',
                    colour=0x4262F4,
                )
                embed.add_field(name="Event", value='```' +
                                details[0] + '```', inline=True)
                embed.add_field(name="Date", value='```' +
                                details[1] + '```', inline=True)
                embeds.append(embed)
                self.flag = True
            for embed in embeds:
                await channel.send(embed = embed)
    
    @eventlog.after_loop
    async def chnageP(self):
        self.eventlog.cancel()
        self.eventlog.change_interval(hours=24.0,minutes=0.0,seconds=0.0)
        self.eventlog.start()