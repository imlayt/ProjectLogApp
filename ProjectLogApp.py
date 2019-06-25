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
mediumgreen = '#66b3b3'  # color used by PySimpleGUI

recordlist = []  # list of records for the selector listbox

class ProjectLog:
    def __init__(self, logfile, table='LogEntries'):
        '''
        :param logfile:
        :param table:
        '''
        self.logfile = logfile
        self.table = table
        id = 0  # record key
        logtype = ''  # Issue, risk, action item, decision, etc.
        title = ''  # short name for reporting
        shortdescription = ''  # short description for reporting
        longdescription = ''  # optional detailed description
        probability = 0.0  # likely hood of a risk
        severity = 0.0  # impact to the project of the risk or issue
        complexity = 0.0  # complexity multiplier for Risks and issues
        criticality = 0.0  # criticality multiplier for Risks and Issues
        exposure = 0.0  # calculated exposure of the project based on probability, severity, complexity and criticality
        owner = ''  # Person accountable for mitigating the risk, remediating the issue, etc.
        startdate = ''  # Planned date for starting the mitigation/remediation
        duedate = ''  # Target finish date for mitigation/remediation
        workstream = ''  # sub-project to which this log item applies
        project = ''  # Name of the project to which this log item applies
        notes = ''  # General notes about the log item

    def verifylogfile(self):  # returns a connection object or None if it can't connect
        '''
        :return: returns a connection object or None if it can't connect
        '''
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
        '''
        :return: returns True if the table exists, otherwise False
        '''
        if os.path.isfile(self.logfile):
            try:
                conn = sqlite3.connect(self.logfile)

                sql2 = "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE '%s' ;" % self.table

                # print('sql2 => ', sql2)
                curr = conn.cursor()
                curr.execute(sql2)

                thetablename = curr.fetchall()
                # print('thetablename =>', thetablename)

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
        '''
        :return: return True if the table is created, else return False
        '''
        create_query = '''
            CREATE TABLE "LogEntries" (
    "ID"    INTEGER PRIMARY KEY AUTOINCREMENT,
    "LogType"	TEXT NOT NULL,
    "Title"	TEXT NOT NULL,
    "ShortDescription"	TEXT NOT NULL,
    "LongDescription"	TEXT,
    "Probability"	REAL,
    "Severity"	REAL,
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

    def addlogentry(self, valuelist):  # returns the ID value if addition was successful else returns None
        '''
        :param valuelist:
        :return: the ID value if the addition was successful else returns None
        '''
        insertsql = '''
                    INSERT INTO LogEntries( 
                    LogType, 
                    Title, 
                    ShortDescription, 
                    LongDescription, 
                    Probability, 
                    Severity, 
                    Complexity, 
                    Criticality, 
                    Exposure, 
                    Owner, 
                    StartDate, 
                    DueDate, 
                    Workstream, 
                    Project, 
                    Notes)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ; '''

        try:
            conn = sqlite3.connect(self.logfile)
            # print('conn succeeded')
            curr = conn.cursor()
            # print('curr creation succeeded')
            # print('insertsql =>', insertsql)
            curr.execute(insertsql, valuelist)
            # commit the changes
            conn.commit()
            # print('curr.execute succeeded')
            return True
        except Error as e:
            print(e)
            print('addlogentry FAILED(', valuelist, ')')
            return False

    def readlogentry(self, recordid):  # returns a log record or None
        '''
        :param recordid:
        :return: log record or None
        '''

        readquery = 'SELECT * from %s WHERE ID IS ?' % self.table
        # print('readquery => ', readquery)
        try:
            conn = sqlite3.connect(self.logfile)
            # print('conn succeeded')
            curr = conn.cursor()
            # print('curr creation succeeded')
            curr.execute(readquery, [recordid, ])
            # print('curr.execute succeeded')
            therecords = curr.fetchall()
            # print('therecords => ', therecords)
            return therecords
        except:
            sg.Popup('readlogentry FAILED(', readquery, ')', keep_on_top=True)
            return False

    def readlogentries(self, searchquery):  # returns a list of log records
        '''
        :param searchquery:
        :return: returns a list of log records
        '''
        searchquery = searchquery.replace('thetable', self.table)
        # print('searchquery => ', searchquery)
        try:
            conn = sqlite3.connect(self.logfile)
            curr = conn.cursor()
            curr.execute(searchquery)
            therecords = curr.fetchall()
            return therecords
        except:
            sg.Popup('Creating table FAILED(', self.table, ')', keep_on_top=True)
            return False

    def updatelogentry(self, logidvalue, valuelist):  # returns True if the update was successful
        '''
        :param logidvalue:
        :param valuelist:
        :return: returns True if the update was successful
        '''
        # UPDATE table_name SET column_name=new_value [, ...] WHERE expression
        updatesql = '''
            UPDATE LogEntries SET 
            LogType=?, 
            Title=?, 
            ShortDescription=?, 
            LongDescription=?, 
            Probability=?, 
            Severity=?, 
            Complexity=?, 
            Criticality=?, 
            Exposure=?, 
            Owner=?, 
            StartDate=?, 
            DueDate=?, 
            Workstream=?, 
            Project=?, 
            Notes=?
            WHERE ID = ?
                    ; '''

        try:
            conn = sqlite3.connect(self.logfile)
            # print('conn succeeded')
            curr = conn.cursor()
            # print('curr creation succeeded')
            # print('updatesql =>', updatesql)
            curr.execute(updatesql, valuelist)
            # commit the changes
            conn.commit()
            # print('curr.execute succeeded')
            return True
        except Error as e:
            print(e)
            print('updatelogentry FAILED(', valuelist, ')')
            return False

    def deletelogentry(self, logidvalue):  # returns True if the record was deleted
        pass

    def findlogentry(self, field, searchvalue):  # returns a log record
        pass


def setmessage(window, message):
    '''
    :param window:
    :param message:
    :return:
    '''
    window.FindElement('_MESSAGEAREA_').Update(message)
    window.Refresh()


def fillformfields(window, therecords):
    '''

    :param window:
    :param therecords:
    :return: True if all fields were filled else return false
    '''
    # print('therecords =>', therecords)
    # print('therecords[0][1] =>', therecords[0][1])
    try:
        window.FindElement('_CURRENTRECORD_').Update(therecords[0][0])
        window.FindElement('_LOGITEMTYPE_').Update(therecords[0][1])
        window.FindElement('_TITLE_').Update(therecords[0][2])
        window.FindElement('_SHORTDESC_').Update(therecords[0][3])
        window.FindElement('_LONGDESC_').Update(therecords[0][4])
        window.FindElement('_PROBABILITY_').Update(therecords[0][5])
        window.FindElement('_SEVERITY_').Update(therecords[0][6])
        window.FindElement('_COMPLEXITY_').Update(therecords[0][7])
        window.FindElement('_CRITICALITY_').Update(therecords[0][8])
        window.FindElement('_EXPOSURE_').Update(therecords[0][9])
        window.FindElement('_OWNER_').Update(therecords[0][10])
        window.FindElement('_STARTDATE_').Update(therecords[0][11])
        window.FindElement('_DUEDATE_').Update(therecords[0][12])
        window.FindElement('_WORKSTREAM_').Update(therecords[0][13])
        window.FindElement('_PROJECT_').Update(therecords[0][14])
        window.FindElement('_NOTES_').Update(therecords[0][15])
        window.Refresh()
        return True
    except:
        sg.Popup('fillformfields FAILED')
        return False


def clearformfields(window):
    '''

    :param window:
    :param therecords:
    :return: True if all fields were filled else return false
    '''
    # print('therecords =>', therecords)
    # print('therecords[0][1] =>', therecords[0][1])
    try:
        window.FindElement('_CURRENTRECORD_').Update('')
        window.FindElement('_LOGITEMTYPE_').Update('')
        window.FindElement('_TITLE_').Update('')
        window.FindElement('_SHORTDESC_').Update('')
        window.FindElement('_LONGDESC_').Update('')
        window.FindElement('_PROBABILITY_').Update('')
        window.FindElement('_SEVERITY_').Update('')
        window.FindElement('_COMPLEXITY_').Update('')
        window.FindElement('_CRITICALITY_').Update('')
        window.FindElement('_EXPOSURE_').Update('')
        window.FindElement('_OWNER_').Update('')
        window.FindElement('_STARTDATE_').Update('')
        window.FindElement('_DUEDATE_').Update('')
        window.FindElement('_WORKSTREAM_').Update('')
        window.FindElement('_PROJECT_').Update('')
        window.FindElement('_NOTES_').Update('')
        window.Refresh()
        return True
    except:
        sg.Popup('clearformfields FAILED')
        return False


def getrecordvalues(values, includerecid=True):
    '''
    :param window: 
    :return: list with all record values from the window 
    '''
    # print('get record values =>', values)
    # print('valuelist[0][1] =>', valuelist[0][1])
    valuelist = []
    # try:
    valuelist.append(values['_LOGITEMTYPE_'])
    valuelist.append(values['_TITLE_'])
    valuelist.append(values['_SHORTDESC_'])
    valuelist.append(values['_LONGDESC_'])
    valuelist.append(values['_PROBABILITY_'])
    valuelist.append(values['_SEVERITY_'])
    valuelist.append(values['_COMPLEXITY_'])
    valuelist.append(values['_CRITICALITY_'])
    valuelist.append(values['_EXPOSURE_'])
    valuelist.append(values['_OWNER_'])
    valuelist.append(values['_STARTDATE_'])
    valuelist.append(values['_DUEDATE_'])
    valuelist.append(values['_WORKSTREAM_'])
    valuelist.append(values['_PROJECT_'])
    valuelist.append(values['_NOTES_'])

    if includerecid:
        valuelist.append(values['_CURRENTRECORD_'])

    # print('valulist =>', valuelist)
    return valuelist
    # except:
    #     sg.Popup('could not fill the record list')



def fillrecordselector(window, listboxkey, log):
    '''
    :param window:
    :param log:
    :return: Record count if successful, else None
    '''
    searchquery = 'select LogType, ID, Title, Owner, Workstream, Project FROM thetable ORDER BY LogType'
    # print('searchquery =>', searchquery)
    listofrecords = log.readlogentries(searchquery)
    if listofrecords is None:
        return False
    else:
        # print('listofrecords =>', listofrecords)
        window.FindElement(listboxkey).Update(listofrecords)
        window.Refresh()
        return len(listofrecords)


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
               [sg.Text('Criticality', size=(15, 1), justification='right'),
                sg.InputText(size=(20, 1), key='_CRITICALITY_')],
               [sg.Text('Exposure', size=(15, 1), justification='right'), sg.InputText(size=(20, 1), key='_EXPOSURE_')]
               ]

maincolumn3 = [[sg.Text('Owner', justification='right', size=(15, 1)), sg.InputText(size=(20, 1), key='_OWNER_')],
               [sg.Text('Start', justification='right', size=(15, 1)), sg.InputText(size=(20, 1), key='_STARTDATE_'),
                sg.CalendarButton('Cal', target='_STARTDATE_')],
               [sg.Text('Due Date', justification='right', size=(15, 1)), sg.InputText(size=(20, 1), key='_DUEDATE_'),
                sg.CalendarButton('Cal', target='_DUEDATE_')],
               ]

maincolumn4 = [[sg.Column(maincolumn2, background_color=mediumgreen),
                sg.Column(maincolumn3, background_color=lightblue)],
               [sg.Text('Record Selector', justification='center', size=(56, 1)),
                sg.Text('Cuurent Record'), sg.InputText(size=(10, 1), key='_CURRENTRECORD_')],
               [sg.Listbox(values=recordlist, size=(87, 8), key='_RECORDSELECTOR_', enable_events=True)]
               ]

fileinfo = thelogfile + '  |  ' + thelogtable
# Define the mainscreen layout using the above layouts
mainscreenlayout = [[sg.Column(maincolumn1, background_color=mediumgreen),
                     sg.Column(maincolumn4, background_color=mediumblue2)],
                    [sg.Text('Message Area', size=(134, 1), key='_MESSAGEAREA_')],
                    [sg.Button('New Log Entry', key='_NEW_'),
                     sg.Button('Save New', key='_ADDNEW_', disabled=True),
                     sg.Button('Save Changes', key='_SAVECHANGES_'),
                     sg.Button('Cancel', key='_CANCEL_')],
                    [sg.Text(fileinfo, key='_FILEINFO_', size=(134, 1), justification='center'), sg.Exit()]
                    ]

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

    if fillrecordselector(window, '_RECORDSELECTOR_', mylog):
        setmessage(window, 'fillrecordselector SUCCEEDED')
        # load the first record into the input boxes
        therecords = mylog.readlogentry(1)
        fillformfields(window, therecords)
    else:
        sg.Popup('fillrecordselector FAILED')
        # sys.exit(1)

    while True:  # Event Loop
        event, values = window.Read()
        if event is None or event=="Exit":
            sys.exit(1)

        if event=='_NEW_':
            clearformfields(window)
            window.FindElement('_ADDNEW_').Update(disabled=False)
            window.FindElement('_SAVECHANGES_').Update(disabled=True)

        if event=='_ADDNEW_':
            # Add the current values as a new record
            valuelist = getrecordvalues(values, False)
            if mylog.addlogentry(valuelist):
                therecords = mylog.readlogentry(1)
                fillformfields(window, therecords)
                if fillrecordselector(window, '_RECORDSELECTOR_', mylog):
                    window.FindElement('_ADDNEW_').Update(disabled=True)
                    window.FindElement('_SAVECHANGES_').Update(disabled=False)
                    window.Refresh()

            else:
                sg.Popup('Save New Logentry FAILED')

        if event=='_SAVECHANGES_':
            # update the table with th current values
            valuelist = getrecordvalues(values)
            if mylog.updatelogentry(values['_CURRENTRECORD_'], valuelist):
                therecords = mylog.readlogentry(values['_CURRENTRECORD_'])
                # fillformfields(window, therecords)
                recordid = values['_RECORDSELECTOR_'][0][1]
                setmessage(window, 'recordid => ' + str(recordid))
                therecords = mylog.readlogentry(recordid)
                fillformfields(window, therecords)
                if fillrecordselector(window, '_RECORDSELECTOR_', mylog):
                    window.Refresh()
            else:
                sg.Popup('Save Changes FAILED')

        if event=='_CANCEL_':
            sys.exit(23)
            # sg.Popup('Cancel Button')

        if event=='_FILEINFO_':
            sg.Popup('File Info Button')

        if event=='_RECORDSELECTOR_':
            recordid = values['_RECORDSELECTOR_'][0][1]
            setmessage(window, 'recordid => ' + str(recordid))
            window.Refresh()
            therecords = mylog.readlogentry(recordid)
            fillformfields(window, therecords)



if __name__=="__main__":
    # execute only if run as a script
    main()
