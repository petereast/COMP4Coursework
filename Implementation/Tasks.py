# This one's for taking the data out of the database

from DatabaseInit import TasksInfo

class Task:
    def __init__(self, title="", subtitle="", priority=1, databaseid=None):
        self.text = ""
        if databaseid == None:
            self.title = title
            self.priority = priority
            self.subtitle = subtitle
            self.text  = self.title + "\n  " + self.subtitle
        else:
            self.info = TasksInfo().get_info_by_id(databaseid)
            self.text = self.info["Title"] +"\n  "+self.info["Description"]
            # TODO: The tasks are gonna need a due date and priority in the database so that
            # the listings can be ordered by priority.
            pass

    def load_task_from_database(self, taskid):
        pass

    def complete(self):
        self.title+= " [Done]"
        self.priority = -1
