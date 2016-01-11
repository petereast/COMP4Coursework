BEGIN TRANSACTION;
CREATE TABLE Users
                (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Username TEXT,
                Password TEXT,
                Permissions INTEGER
                );
CREATE TABLE Tasks
                (TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Description TEXT,
                Owner INTEGER,
                Attendees INTEGER
                );
CREATE TABLE TaskAttendee
                (
                TaskId INTEGER,
                UserId INTEGER
                );
CREATE TABLE `Resources` (
	`ResourceID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ResourceName`	TEXT,
	`ResourceCost`	INTEGER,
	`ResourceQuantity`	INTEGER,
	`ResourceRequiredQuantity`	INTEGER
);
CREATE TABLE Meetings
                (MeetingID INTEGER PRIMARY KEY AUTOINCREMENT,
                OwnerID INTEGER,
                Title TEXT,
                ISOTime TEXT,
                Location TEXT,
                Attendees INTEGER
                );
CREATE TABLE MeetingAttendee
(
    MeetingID INTEGER,
    UserID INTEGER,
    Confirmed BOOLEAN
);
COMMIT;
