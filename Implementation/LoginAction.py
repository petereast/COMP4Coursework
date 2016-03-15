#Login action:
#   The code and database actions performed when the user attempts to log into the system.

import hashlib

from DatabaseInit import *
import SqlDictionary

class User:
    def __init__(self, uid=0):
        self.info = {} # info to be retrieved from the database
        self.permissions = {}
        self.user_id = uid

        self.dbinterface = UsersInfo()

        self.update_user_info()

    def gen_pw_hash(self, password):
        # Create a md5 hash of the password
        phash = hashlib.md5()
        # (Encode the password - the python md5 implementation  only accepts binary data.)
        phash.update(bytes(password, "UTF-8"))
        # return a hexadecimal representation of the md5 hash.
        return phash.hexdigest()

    def password_hash_cmp(self, password_input):
        currenthash = self.info["Password"]
        return currenthash == self.gen_pw_hash(password_input)

    def add_user(self, info=None):

        # If there's no info input, use the existing info for this instance of the
        # class.
        if info == None:
            info = self.info

        # Use the database module to add the user's info to the database.
        UsersInfo().add_user(info)

    def update_user_info(self):
        # get the first item in the list of users which have the UserID of
        # `self.user_id` (the length of the list should be 1)
        raw_info = self.dbinterface.get_all_users("WHERE(UserID = {0})".format(self.user_id))[0]

        # raw_info follows the format [id, Name, Username, Password, Permissions]
        # put the indidual parts of the raw data into a python dictionary
        self.info["UserID"] =  self.user_id
        self.info["Name"] = raw_info[1]
        self.info["Username"] = raw_info[2]
        self.info["Password"] =  raw_info[3]
        self.info["Permissions"] = raw_info[4]

        # Generate the permissions array for this user.
        self.gen_permissions()
        self.id = self.info["UserID"]

    def gen_permissions(self):
        # Get the denary integer value for the user's permissions
        perm = self.info["Permissions"]

        # Create a list of the default values for the user's permissions
        blist = [False, False, False, False, False]

        # For each item in a list of the individual binary digits
        # The python `bin` function outputs a string in the format '0b10101'
        # which is why we need to get rid of the first two characters
        for index, digit in enumerate(bin(int(perm))[2:]):
            # set each item in the b(inary)list as a python Bool so it can easily
            # be used in selection statements
            blist[index] = (bool(int(digit)))
        permissions = {}
        permissions["Meetings"] = blist[0]
        permissions["Tasks"] = blist[1]
        permissions["Resources"] = blist[2]
        permissions["ChangeOwnData"] = blist[3]
        permissions["Admin"] = blist[4]

        # Overwrite the existing permissions number with a dictionary.
        self.permissions = permissions
        return permissions
