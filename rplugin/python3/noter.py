import pynvim
import sqlite3
import os


# Hardcoded env variables - for now...
dbPath = r"./noter.db"


@pynvim.plugin
class NoterPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("TestNoter")
    def testNoter(self, args):
        # Quick test to output to nvim console
        return "Noter Plugin operational"

    @pynvim.function("NoterBuildDB")
    def buildDB(self, args):
        # Check for an existing SQLite DB
        # Create one if it is missing
        # otherwise flash the user with an err
        if os.path.exists(dbPath):
            raise Exception("The DB has already been created")
        con = sqlite3.connect(dbPath)
        cur = con.cursor()
        cur.execute("CREATE TABLE notes(id INT, name TEXT, path TEXT)")

        return
