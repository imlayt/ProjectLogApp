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

# thelogfilehome = 'C:\Users\imlay\Downloads\ProjectLog.db'

thelogfile = 'c:/Users/imlay/Downloads/ProjectLog.db'  # Default log file
thelogtable = 'LogEntries'  # Default tablename
lightblue = '#b9def4'  # color used by PySimpleGUI
mediumblue = '#d2d2df'  # color used by PySimpleGUI
mediumblue2 = '#534aea'  # color used by PySimpleGUI

recordlist = []  # list of records for the selector listbox

class ProjectLog:
    def __init__(self, logfile, table='LogEntries'):
        self.logfile = logfile
        self.table = table
        id = 0  # record key
        logtype = ''  # Issue, risk, action item, decision, etc.
        title = ''  # short name for reporting
        shortdescription = ''  # short description for reporting
        longdescription = ''  # optional detailed description
        probability = 0.0  # likely hood of a risk
        impact = 0.0  # impact to the project of the risk or issue
        complexity = 0.0  # complexity multiplier for Risks and issues
        criticality = 0.0  # criticality multiplier for Risks and Issues
        exposure = 0.0  # calculated exposure of the project based on probability, impact, complexity and criticality
        owner = ''  # Person accountable for mitigating the risk, remediating the issue, etc.
        startdate = ''  # Planned date for starting the mitigation/remediation
        duedate = ''  # Target finish date for mitigation/remediation
        workstream = ''  # sub-project to which this log item applies
        project = ''  # Name of the project to which this log item applies
        notes = ''  # General notes about the log item

    def verifylogfile(self):  # returns a connection object or None if it can't connect
        if not os.path.isfile(self.logfile):
            # sg.Popup('No Database File Found', keep_on_top=True)
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

                print('sql2 => ', sql2)
                curr = conn.cursor()
                curr.execute(sql2)

                thetablename = curr.fetchall()
                print('thetablename =>', thetablename)

                if len(thetablename)==0:
                    # print('len(tablename) == 0')
                    return False
                else:
                    # print('len(tablename) != 0')
                    return True
            except Error as e:
                print(e)
                sg.Popup('Could not connect to the database', keep_on_top=True)
                return False
        else:
            sg.Popup('Database file does not exist - it will be created')
            return False

    def createtable(self):  # return True if the table is created, else return False
        create_query = '''
            CREATE TABLE "LogEntries" (
    "ID"    INTEGER PRIMARY KEY AUTOINCREMENT,
    "LogType"	TEXT NOT NULL,
    "Title"	TEXT NOT NULL,
    "ShortDescription"	TEXT NOT NULL,
    "LongDescription"	TEXT,
    "Probability"	REAL,
    "Impact"	REAL,
    "Complexity"	REAL,
    "Criticality"	REAL,
    "Exposure"	REAL,
    "Owner"	TEXT NOT NULL,
    "StartDate"	TEXT,
    "DueDate"	TEXT NOT NULL,
    "Workstream"	TEXT,
    "Project"	TEXT,
    "Notes"	TEXT ); '''

        try:
            conn = sqlite3.connect(self.logfile)
            curr = conn.cursor()
            curr.execute(create_query)
            return True
        except:
            sg.Popup('Creating table FAILED(', self.table, ')', keep_on_top=True)
            return False

    def addlogentry(self, valuelist):  # returns the ID value if the addition was successful else returns None
        pass

    def readlogentry(self):  # returns a log record
        pass

    def updatelogentry(self, logidvalue, valuelist):  # returns True if the update was successful
        pass

    def deletelogentry(self, logidvalue):  # returns True if the record was deleted
        pass

    def findlogentry(self, field, searchvalue):  # returns a log record
        pass

    def reportlogentries(self, searchquery):  # returns a list of log records
        pass


def setmessage(window, message):
    window.FindElement('_MESSAGEAREA_').Update(message)
    window.Refresh()


def fillrecordselector(window, fieldkey, valuelist):
    pass


maincolumn1 = [[sg.Text('Title', size=(15, 1), justification='right'), sg.Multiline(size=(40, 3), key='_TITLE_')],
               [sg.Text('Short Desc.', size=(15, 1), justification='right'),
                sg.Multiline(size=(40, 3), key='_SHORTDESC_')],
               [sg.Text('Long Desc.(opt)', size=(15, 1), justification='right'),
                sg.Multiline(size=(40, 3), key='_LONGDESC_')],
               [sg.Text('Project.', size=(15, 1), justification='right'),
                sg.InputText(size=(40, 1), key='_PROJECT_')],
               [sg.Text('Workstream.', size=(15, 1), justification='right'),
                sg.InputText(size=(40, 1), key='_WORKSTREAM_')],
               [sg.Text('Notes', size=(15, 1), justification='right'),
                sg.Multiline(size=(40, 4), key='_NOTES_')]]

maincolumn2 = [[sg.Text('Log Item Type', size=(15, 1), justification='right'),
                sg.InputText(size=(20, 1), key='_LOGITEMTYPE_')],
               [sg.Text('Probability', size=(15, 1), justification='right'),
                sg.InputText(size=(20, 1), key='_PROBABILITY_')],
               [sg.Text('Severity', size=(15, 1), justification='right'), sg.InputText(size=(20, 1), key='_SEVERITY_')],
               [sg.Text('Complexity', size=(15, 1), justification='right'),
                sg.InputText(size=(20, 1), key='_COMPLEXITY_')],
               [sg.Text('Exposure', size=(15, 1), justification='right'), sg.InputText(size=(20, 1), key='_EXPOSURE_')]
               ]

maincolumn3 = [[sg.Text('Owner', justification='right', size=(15, 1)), sg.InputText(size=(20, 1), key='_OWNER_')],
               [sg.Text('tbd', justification='right', size=(15, 1)), sg.InputText(size=(20, 1), key='_TBD_')],
               [sg.Text('Start', justification='right', size=(15, 1)), sg.InputText(size=(20, 1), key='_START_'),
                sg.CalendarButton('Cal', target='_START_')],
               [sg.Text('Due Date', justification='right', size=(15, 1)), sg.InputText(size=(20, 1), key='_DUEDATE_'),
                sg.CalendarButton('Cal', target='_DUEDATE_')],
               ]

maincolumn4 = [[sg.Column(maincolumn2, background_color=mediumblue),
                sg.Column(maincolumn3, background_color=mediumblue)],
               [sg.Text('Record Selector', justification='center', size=(60, 1))],
               [sg.Listbox(values=recordlist, size=(87, 8), key='_RECORDSELECTOR_')]
               ]

fileinfo = thelogfile + '  |  ' + thelogtable
# Define the mainscreen layout using the above layouts
mainscreenlayout = [[sg.Column(maincolumn1, background_color=lightblue),
                     sg.Column(maincolumn4, background_color=mediumblue2)],
                    [sg.Text('Message Area', size=(131, 1), key='_MESSAGEAREA_')],
                    [sg.Button('Add New', key='_ADDNEW_'),
                     sg.Button('Save Changes', key='_SAVECHANGES_'),
                     sg.Button('Cancel', key='_CANCEL_')],
                    [sg.Exit(), sg.Text(fileinfo, key='_FILEINFO_')]]

def main():
    global thelogfile
    global thelogtable

    # ########################################
    # initialize main screen window
    sg.SetOptions(element_padding=(2, 2))
    window = sg.Window('Project Log App', background_color=mediumblue,
            default_element_size=(15, 1)).Layout(mainscreenlayout)
    window.Finalize()
    window.Refresh()

    # instantiate a ProjectLog
    mylog = ProjectLog(thelogfile, thelogtable)

    if mylog.verifylogfile() is None:
        sg.Popup('ERROR: Could not open the logfile')
        logfile = sg.PopupGetFile('Enter a logfile')
        print('logfile => ', logfile)

        if logfile is None or len(logfile)==0:
            print('logfile not found')
            # break
        else:
            mylog.logfile = logfile
            print('mylog.table => ', mylog.table)
            if not mylog.verifylogfile():
                sg.Popup('2nd file verification failed - EXITING Program')
                # break
            else:
                # sg.Popup('Opened the logfile')
                fileinfo = mylog.logfile + '  |  ' + mylog.table
                window.FindElement('_FILEINFO_').Update(fileinfo)
                setmessage(window, fileinfo)
                window.Refresh()
    # else:
    # sg.Popup('Opened the logfile')

    if not mylog.verifytable():
        logtable = sg.PopupGetText('Enter a tablename or Cancel to exit the program.')
        print('logtable => ', logtable)

        if logtable is None or len(logtable)==0:
            print('logtable not found')
            # break
        else:
            mylog.table = logtable
            print('mylog.table => ', mylog.table)
            if not mylog.verifytable():
                sg.Popup('2nd table verification failed - EXITING Program')
                # break
            else:
                # sg.Popup('connected to the table')
                fileinfo = mylog.logfile + '  |  ' + mylog.table
                window.FindElement('_FILEINFO_').Update(fileinfo)
                setmessage(window, fileinfo)
                window.Refresh()
    # else:
    # sg.Popup('connected to the table')

    if fillrecordselector(window, 'fieldkey', 'valuelist'):
        sg.Popup('fillrecordselector SUCCEDED')
        # pop the list and load the first record into the input boxes
    else:
        sg.Popup('fillrecordselector FAILED')
        # sys.exit(1)

    while True:  # Event Loop
        event, values = window.Read()
        if event is None or event=="Exit":
            sys.exit(1)

        if event=='_ADDNEW_':
            sg.Popup('Add New Button')

        if event=='_SAVECHANGES_':
            sg.Popup('Save Changes Button')

        if event=='_CANCEL_':
            sg.Popup('Cancel Button')

        if event=='_FILEINFO_':
            sg.Popup('File Info Button')


if __name__=="__main__":
    # execute only if run as a script
    main()
