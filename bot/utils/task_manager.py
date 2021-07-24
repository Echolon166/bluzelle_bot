import itertools


class task:
    id_iter = itertools.count()

    def __init__(self, channel_id, latest_execution, interval, kwargs, function):
        self.id = next(self.id_iter)
        self.channel_id = channel_id
        self.latest_execution = latest_execution
        self.interval = interval
        self.kwargs = kwargs
        self.function = function


active_tasks = []


def add_task(task: task):
    active_tasks.append(task)


def delete_task(id: int):
    task = get_task(id)
    if task is None:
        return False

    active_tasks.remove(task)
    return True


def get_task(id: int):
    task = [d for d in active_tasks if d.id == id]
    if not task or len(task) == 0:
        return None

    return task[0]


def get_tasks():
    return active_tasks
