from sqlite3 import connect 
import sqlite3
import time
import datetime
from datetime import date
from discord.ext import commands
import asyncio

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
                UPDATE events SET time = (?) where eventname =(?) 
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
                return "Entry modified " + stat +"with " + modifiedVal + "for " + ofEvent
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
    
    @commands.group()
    async def event(self, ctx):
        self.db = DB_MANAGER()

    @event.commands(pass_context=True)
    async def add(self,ctx,eventname,date):
        status = self.db.addEntry(eventname,date)
        await ctx.send(status)