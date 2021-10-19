# Views
from flask.views import MethodView


class TasksView(MethodView):
    """
    TasksView have the methods to handle all tasks
    """
    def post(self):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        # ToDo
        return "Create new task"

    def get(self):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        # ToDo
        return "Return all Tasks"


class TaskView(MethodView):
    """
    TaskView have the methods to handle one task
    """
    def get(self, id_task):
        """
        Post method of tasks view
        Retrieve all tasks
        :return:
        """
        # ToDo
        return f"Return one task: {id_task}"

    def delete(self, id_task):
        """
        Post method of tasks view
        Create a new task.
        :return:
        """
        # ToDo
        return f"Delete one task: {id_task}"
