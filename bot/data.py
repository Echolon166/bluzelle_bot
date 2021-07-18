import dataset

from constants import *
from utils.ext import connect_db

"""
    Functions for managing a dataset SQL database
    # Schemas
"""


@connect_db
def add_task(db, task):
    table = db[TASKS_TABLE]
    return table.insert(task)


@connect_db
def delete_task(db, id):
    table = db[TASKS_TABLE]
    return table.delete(id=id)


@connect_db
def update_task(db, task):
    table = db[TASKS_TABLE]
    table.update(task, ["id"])


@connect_db
def get_task(db, id):
    table = db[TASKS_TABLE]
    return table.find_one(id=id)


@connect_db
def get_tasks(db):
    table = db[TASKS_TABLE]
    return [t for t in table.all()]
