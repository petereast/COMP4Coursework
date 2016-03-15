# sql dictionary
# This file will contain all of the SQL references used throughout the system, with string formatting already
# added

#initialisation scripts

CREATE_USERS = """CREATE TABLE IF NOT EXISTS Users
                (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Username TEXT,
                Password TEXT,
                Permissions INTEGER
                );
"""

#Permissions: Like unix file permissions but using denary instead of octal
# and there are 5 bits rather than several.
# eg 0b11010 - will give the user permission to use the meetings, tasks and user admin, and not resources management or privac.

# time to design databases - NOW!

CREATE_MEETINGS = """CREATE TABLE IF NOT EXISTS Meetings
                (MeetingID INTEGER PRIMARY KEY AUTOINCREMENT,
                OwnerID INTEGER,
                Title TEXT,
                ISOTime TEXT,
                Location TEXT
                );
"""

CREATE_MEETINGS_ATTENEDEES = """CREATE TABLE IF NOT EXISTS MeetingAttendee(
    MeetingID INTEGER,
    UserID INTEGER,
    Confirmed BOOLEAN
);"""

CREATE_TASKS = """CREATE TABLE IF NOT EXISTS Tasks
                (TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Description TEXT,
                Owner INTEGER,
                Attendees INTEGER
                );"""

CREATE_TASKATTENDEE = """CREATE TABLE IF NOT EXISTS TaskAttendee
                (
                TaskId INTEGER,
                UserId INTEGER
                );
"""

CREATE_RESOURCES = """CREATE TABLE IF NOT EXISTS Resources
                (ResourceID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Cost INTEGER,
                QuantityAvailable INTEGER,
                QuantityRequired INTEGER
);
"""

# Users

GET_ALL_USERS = """ SELECT * FROM Users {0}; """

GET_USER_ID = """ SELECT UserID FROM Users WHERE (Username = '{0}');"""

ADD_USER = """INSERT INTO Users(Name, Username, Password, Permissions) VALUES({0});"""

UPDATE_PASSWORD = """UPDATE Users SET Password = {0} WHERE UserID = {1};"""

# Meetings

ADD_MEETING = """INSERT INTO Meetings(OwnerID, Title, ISOTime, Location) VALUES({0})"""

GET_MEETING = """SELECT * FROM Meetings {0};"""

GET_OUTSTANDING_MEETINGS_TO_BE_ATTENDED = """SELECT * FROM MeetingAttendee WHERE (UserID = {0} AND Confirmed = 0);"""

GET_MEETING_ID_LIST = """SELECT MeetingID FROM Meetings {0};"""

ADD_MEETING_ATTENDEE = """INSERT INTO MeetingAttendee(MeetingID, UserID, Confirmed) VALUES({0})"""

GET_MEETING_ATTENDEES = """SELECT UserID FROM MeetingAttendee WHERE (MeetingID = {0})"""

ACCEPT_MEETING = """UPDATE MeetingAttendee SET Confirmed = 1 WHERE {0}"""

REJECT_MEETING = """UPDATE MeetingAttendee SET Confirmed = 0 WHERE {0}"""

DELETE_MEETING = """DELETE FROM MeetingAttendee WHERE {0}"""

# Tasks

GET_TASK = """SELECT * FROM Tasks {0};"""

GET_TASK_ID_LIST = "SELECT TaskID FROM Tasks {0};"""

ADD_TASK = """INSERT INTO Tasks(Title, Description, Owner, Attendees) VALUES({0});"""

GET_USERNAME_BY_UID = """SELECT Name FROM Users WHERE(UserID = {0})"""

# Resources

CREATE_RESOURCES = """CREATE TABLE IF NOT EXISTS Resources
                (ResourceID INTEGER PRIMARY KEY AUTOINCREMENT,
                ResourceName TEXT,
                ResourceCost INTEGER,
                ResourceQuantity INTEGER,
                ResourceRequiredQuantity INTEGER);
                """
GET_ALL_RESOURCES = """SELECT * FROM Resources;"""
