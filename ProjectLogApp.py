#
# ##############################################
#
# ProjectLogApp
# This app is used to log project RAID items - Risk, Action Items, Issues, Decisions.
# The data is stored in a SQLite database.
#
# The gui is built with PySimpleGUI.
# ##############################################

import os
import sys
import PySimpleGUI as sg
import sqlite3
from sqlite3 import Error

thelogfile = 'c:\\Users/timlay/Dowloads/ProjectLog.db'  # Default log file
thelogtable = 'LogEntries'  # Default tablename
lightblue = '#b9def4'  # color used by PySimpleGUI
mediumblue = '#d2d2df'  # color used by PySimpleGUI
mediumblue2 = '#534aea'  # color used by PySimpleGUI

class ProjectLog:
    def __init__(self, logfile, table='LogEntries'):
        self.logfile = logfile
        self.table = table
        id = 0  # record key
        logtype = ''  # Issue, risk, action item, decision, etc.
        title = ''  # short name for reporting
        shortdescription = ''  # short description for reporting
        longdescription = ''  # Detailed description
        probability = 0.0  # likely hood of a risk
        impact = 0.0  # impact to the project of the risk or issue
        complexity = 0.0  # complexity multiplier for Risks and issues
        exposure = 0.0  # calculated expodure of the project based on probability, impact, and complexity
        owner = ''  # Person accountable for mitigating the risk, remediating the issue, etc.
        startdate = ''  # Planned date for starting the mitigation/remediation
        duedate = ''  # Target finish date for mitigation/remediation
        workstream = ''  # sub-project to which this log item applies
        project = ''  # Name of the project to which this log item applies
        notes = ''  # General notes about the log item

    def verifylogfile(self):  # returns a connection object or None if it can't connect
        if not os.path.isfile(self.logfile):
            sg.Popup('No Database File Found', keep_on_top=True)
            return None
        try:
            conn = sqlite3.connect(self.logfile)
            print("sqlite3 version=", sqlite3.version)
            return conn
        except Error as e:
            print(e)
            sg.Popup('Could not connect to the database', keep_on_top=True)
            return None

    def verifytable(self):  # returns True if the table exists, otherwise False
        if os.path.isfile(self.logfile):
            try:
                conn = sqlite3.connect(self.logfile)

                sql2 = "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE '%s' ;" % self.table

                curr = conn.cursor()
                curr.execute(sql2)

                thetablename = curr.fetchall()

                if len(thetablename)==0:
                    return False
                else:
                    return True
            except Error as e:
                print(e)
                sg.Popup('Could not connect to the database', keep_on_top=True)
                return False
        else:
            sg.Popup('Database file does not exist - it will be created')
            return False

    def createtable(self):  # return True if the table is created, else return False
        try:
            create_query = '''
            CREATE TABLE "LogEntries" (
    "ID"    INTEGER PRIMARY KEY AUTOINCREMENT,
    "LogType"  TEXT NOT NULL,
    "Title"	TEXT NOT NULL,
    "ShortDescription"  TEXT NOT NULL,
    "LongDescription"   TEXT,
    "Probability"	REAL,
    "Impact"	REAL,
    "Complexity"	REAL,
    "Exposure"	REAL,
    "Owner"	TEXT NOT NULL,
    "StartDate"	TEXT,
    "DueDate"	TEXT NOT NULL,
    "Workstream"	TEXT,
    "Project"	TEXT,
    "Notes"	TEXT );
            '''

            conn = sqlite3.connect(self.logfile)
            curr = conn.cursor()
            curr.execute(create_query)
            return True
        except:
            sg.Popup('Creating table FAILED(', self.table, ')', keep_on_top=True)
            return False

    def addlogentry(self, logentrylist):  # returns True if the addition was successful
        
        pass

    def readlogentry(self):  # returns a log record
        pass

    def updatelogentry(self):  # returns True if the update was successful
        pass

    def deletelogentry(self):  # returns True if the record was deleted
        pass

    def findlogentry(self):  # returns a log record
        pass

    def reportlogentries(self):  # returns a list of log records
        pass


def setmessage(window, messagestr):
    window.FindElement('_MESSAGEAREA_').Update(messagestr)
    window.Refresh()
    

# Define the mainscreen layout using the above layouts
mainscreenlayout = [[sg.Text('Message Area', size=(131, 1), key='_MESSAGEAREA_')],
                    [sg.Button('Check Log File', key='_CHECKLOGFILE_'), sg.Button('Check Log Table', key='_CHECKLOGTABLE_')],
                    [sg.Button('Convert', key='_CONVERT_'),
                     sg.Exit()]]

def main():
    global thelogfile
    global thelogtable

    # ########################################
    # initialize main screen window
    sg.SetOptions(element_padding=(2, 2))
    mainwindow = sg.Window('Project Log App', background_color=mediumblue,
            default_element_size=(15, 1)).Layout(mainscreenlayout)
    mainwindow.Finalize()
    mainwindow.Refresh()
    
    # instantiate a ProjectLog
    mylog = ProjectLog(thelogfile, thelogtable)
    
    while True:  # Event Loop
        event, values = mainwindow.Read()
        if event is None or event=="Exit":
            sys.exit(1)

        if event == '_CHECKLOGFILE_':
            if mylog.verifylogfile() is None:
                thelogtable = sg.Popup('ERROR: Could not connect to the database')
                break
        if event == '_CHECKLOGTABLE_':
            if not mylog.verifytable():
                if thelogtable == 'Cancel' or thelogtable is None:


                # sg.Popup('ERROR: the table does not exist')
                sg.POPUP_BUTTONS_OK_CANCEL('Enter a tablename or Cancel to exit the program.')
                # sg.PopupGetText('Enter a tablename or Cancel to exit the program.')
                    break
            else:
                sg.Popup('Table is OK.')



if __name__=="__main__":
    # execute only if run as a script
    main()
