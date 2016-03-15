# DatabaseInit
# main program

#This tidies all of the SQL queries into another namespace.
import SqlDictionary
import random
import hashlib
import sqlite3

def gen_pw_hash(password):
    phash = hashlib.md5()
    phash.update(bytes(password, "UTF-8"))
    return phash.hexdigest()

class Database:
    """This is the general database wrapper that I'll use throughout the system"""
    def __init__(self, child, database_name="cmsdb.db"):
        #print("[INFO] Created database object")

        self.db_name = database_name

    def _connect_and_execute(self, sql="", database_name=None):
        #print(sql)
        if database_name == None:
            database_name = self.db_name

        with sqlite3.connect(self.db_name) as dbcon:
            cursor = dbcon.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

        #print("[INFO] Executed SQL query \"{0}\"".format(sql))
        return results


class ResourcesInfo(Database):
    def __init__(self):
        super().__init__(self)
        self.create_table()

    def create_table(self):
        self._connect_and_execute(SqlDictionary.CREATE_RESOURCES)

    def get_all_resources(self):
        return self._connect_and_execute(SqlDictionary.GET_ALL_RESOURCES)

    def add_resources(self):
        pass


class UsersInfo(Database):
    def __init__(self, uid = 0):
        super().__init__(self)
        self.create_table()

    # NB: all input MUST be sanitized at this point.
    def create_table(self):
        self._connect_and_execute(SqlDictionary.CREATE_USERS)
        self._create_initial_admin_user()

    def _create_initial_admin_user(self):
        # This is to create an initial administrative user in case something happens to the database
        pwd = "".join([chr(random.choice(range(ord('A'), ord('z')))) for c in range(10)])

        new_user_info = {"Name":"ADMIN - TMP", "Username":"default_admin", "Password": gen_pw_hash(pwd), "Permissions": 29}

        if len(self.get_all_users("WHERE(Username = 'default_admin')")) == 0:
            print("[INFO] Empty users table detected, adding default user...")
            self.add_user(new_user_info)
            print("[INFO] Default user added,\n\tUsername: 'default_admin'\n\tPassword: '{0}'".format(pwd))

    def get_all_users(self, condition = ""): # Add a SQL condition? maybe? TODO: refactor this bit
        return self._connect_and_execute(SqlDictionary.GET_ALL_USERS.format(condition))

    def get_uid_by_username(self, username=""):
        return self._connect_and_execute((SqlDictionary.GET_USER_ID.format(username)))[0][0]

    def get_username_by_uid(self, uid=None):
        return self._connect_and_execute(SqlDictionary.GET_USERNAME_BY_UID.format(uid))[0][0]

    def add_user(self, info):
        #info follows the format {"SQL value":Data value}
        values = "'{0}', '{1}', '{2}', {3}".format(info["Name"], info["Username"], info["Password"], info["Permissions"])

        return self._connect_and_execute(SqlDictionary.ADD_USER.format(values))

    def update_user_password(self, password, uid):
        sql = SqlDictionary.UPDATE_PASSWORD.format("'{0}'".format(password), uid)
        return self._connect_and_execute(sql)


class TasksInfo(Database):

    def __init__(self):
        super().__init__(self)
        self.create_table()

    def create_table(self):
        self._connect_and_execute(SqlDictionary.CREATE_TASKS)
        self._connect_and_execute(SqlDictionary.CREATE_TASKATTENDEE)

    def get_info_by_id(self, task_id):
        sql = SqlDictionary.GET_TASK.format("WHERE (TaskID = {0})".format(task_id))
        raw = self._connect_and_execute(sql)[0]
        return {"TaskID":raw[0], "Title":raw[1], "Description":raw[2], "OwnerID":raw[3], "Attendees":raw[4]}

    def get_ids_by_owner(self, owner_id):
        sql = SqlDictionary.GET_TASK_ID_LIST.format("WHERE Owner = {0}".format(owner_id))
        output_ids = []
        for row in self._connect_and_execute(sql):
            output_ids.append(row[0])
        return output_ids

    def add_task(self, info):
        SQL_DATA = """'{0}', '{1}', {2}, {3}""".format(info["Title"], info["Description"], info["OwnerID"], info["Attendees"])
        self._connect_and_execute(SqlDictionary.ADD_TASK.format(SQL_DATA))



class MeetingsInfo(Database):
    def __init__(self, meeting_info = None):
        super().__init__(self)
        self.create_table()
        self.meeting_info = meeting_info
        self.id = None

    def create_table(self):
        self._connect_and_execute(SqlDictionary.CREATE_MEETINGS)
        self._connect_and_execute(SqlDictionary.CREATE_MEETINGS_ATTENEDEES)

    def add_meeting(self):
        SQL_DATA = "{0}, '{1}', '{2}', '{3}'".format(self.meeting_info["OwnerID"],
            self.meeting_info["Title"],
            self.meeting_info["ISOTime"],
            self.meeting_info["Location"])
        self._connect_and_execute(SqlDictionary.ADD_MEETING.format(SQL_DATA)) #TODO Sort out the formatting.
        self.id = self._connect_and_execute("SELECT Max(MeetingID) FROM Meetings;")[0][0]

    def get_meeting_info(self):
        sql_condition = "WHERE (MeetingID = {0})".format(self.meeting_info['MeetingID'])
        q = SqlDictionary.GET_MEETING.format(sql_condition)
        results = self._connect_and_execute(q)
        return results[0]

    def add_meeting_attendee(self, user_id):
        sql_values = """{0}, {1}, 0""".format(self.id, user_id)
        return self._connect_and_execute(SqlDictionary.ADD_MEETING_ATTENDEE.format(sql_values))


    def get_meetings_by_owner(self, OwnerID):
        sql_condition = "WHERE (OwnerID = {0})".format(OwnerID)
        q = SqlDictionary.GET_MEETING_ID_LIST.format(sql_condition)
        return self._connect_and_execute(q)

    def get_outstanding_meetings(self, OwnerID):
        results = self._connect_and_execute(SqlDictionary.GET_OUTSTANDING_MEETINGS_TO_BE_ATTENDED.format(OwnerID))
        return results

    def get_meeting_attendees(self, MeetingID):
        return self._connect_and_execute(SqlDictionary.GET_MEETING_ATTENDEES.format(MeetingID))

    def respond_to_attendance_request(self, attending, MeetingID, UserID):
        if attending:
            self._connect_and_execute(SqlDictionary.ACCEPT_MEETING.format("UserID = {0} AND MeetingID = {1}".format(UserID, MeetingID)))
        else:
            self._connect_and_execute(SqlDictionary.REJECT_MEETING.format("UserID = {0} AND MeetingID = {1}".format(UserID, MeetingID)))
