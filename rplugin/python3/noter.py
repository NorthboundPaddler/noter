import pynvim
import sqlite3
import os


# Hardcoded env variables - for now...
dbPath = r"./noter.db"


@pynvim.plugin
class NoterPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("TestNoter")
    def testNoter(self):
        # Quick test to output to nvim console
        self.nvim.out_write("Noter Plugin operational\n")

    @pynvim.command("NoterBuildDB")
    def buildDB(self):
        # Check for an existing SQLite DB
        # Create one if it is missing
        # otherwise flash the user with an err
        if os.path.exists(dbPath):
            raise Exception("The DB has already been created")
        con = sqlite3.connect(dbPath)
        cur = con.cursor()
        cur.execute("CREATE TABLE notes(id INT, name TEXT, path TEXT)")
        self.nvim.out_write("Created database\n")

    @pynvim.command("NoterGetFileMetadata")
    def getFileMetadata(self):
        # Get the filename and path from the current buffer
        # Potentially turn this into the "Add new file to DB" function
        fullPath = self.nvim.current.buffer.name
        splitPath = fullPath.split(os.sep)
        fileName = splitPath[-1]
        filePath = os.sep.join(splitPath[0:-1])
        self.nvim.out_write(f"Current file '{fileName}' in '{filePath}'\n")
