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
        createStr = '''CREATE TABLE "notes" (
                "id"	INTEGER NOT NULL UNIQUE,
                "name"	TEXT NOT NULL,
                "path"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
                );'''
        cur.execute(createStr)
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
        return (fileName, filePath)

    @pynvim.command("NoterAddFile")
    def addFile(self):
        # Get file metadata of the current buffer and
        # add a record to the directory's Noter DB
        # TODO Check if file already exists before adding it
        fileName, filePath = self.getFileMetadata()
        if self.checkFile() is False:
            raise Exception("File already exists in noter.db")
        con = sqlite3.connect(dbPath)
        result = con.execute(
            f'INSERT INTO notes (name, path) VALUES ("{fileName}", "{filePath}")')
        con.commit()
        self.nvim.out_write("Current file added to noter.db\n")
        return result

    @pynvim.command("NoterCheckFile")
    def checkFile(self):
        # Get file metadata of the current buffer and
        # check the Noter DB for an existing record
        fileName, filePath = self.getFileMetadata()
        con = sqlite3.connect(dbPath)
        countStatement = f'SELECT COUNT(*) FROM notes WHERE name="{fileName}" AND path="{filePath}"'
        self.nvim.out_write(f'{countStatement}\n')
        result = con.execute(countStatement)
        count = result.fetchone()[0]
        if count == 0:
            return False
        return True
