from sqlite3 import connect 
import sqlite3
import time
import datetime
from datetime import date
from discord.ext import commands,tasks
import asyncio
import discord

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

# db = DB_MANAGER()
# db.addEntry("ungli diwas",'2020-11-21')

class eventmanager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = DB_MANAGER()
    
    @commands.group()
    async def event(self, ctx):
        pass
    
    @event.command(pass_context = True)
    async def help(self,ctx):
        ctx.send(embed = discord.Embed(
            name = "!! HELP !!"
            description = """
            EVENTS LOG
            add - .event add "<eventname>" "<date(%d - %m - %y)>"
            show - .event show
            delete - .event delete "<eventname>"
            modify - .event <time/eventname> "<to_chng_value>" "<eventname>"
            """ 
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
                description= '```  ```',
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