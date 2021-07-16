import dataset

from constants import *
from utils.ext import connect_db

"""
    Functions for managing a dataset SQL database
    # Schemas
    
    #################### channel_prefixes ######################
    guildId
    prefix
    
    #################### commands ####################
    name
    description
"""


@connect_db
def add_prefix_mapping(db, guild_id, prefix):
    table = db[CHANNEL_PREFIXES_TABLE]
    table.upsert(
        {
            GUILD_ID_KEY: guild_id,
            PREFIX_KEY: prefix,
        },
        [GUILD_ID_KEY],
    )


@connect_db
def get_prefix(db, guild_id):
    table = db[CHANNEL_PREFIXES_TABLE]
    row = table.find_one(guildId=guild_id)
    if row is not None:
        return row[PREFIX_KEY]
    return None


@connect_db
def add_command(db, name, description):
    table = db[COMMANDS_TABLE]
    table.upsert(
        {
            NAME_KEY: name,
            DESCRIPTION_KEY: description,
        },
        [NAME_KEY],
    )


@connect_db
def get_all_commands(db):
    table = db[COMMANDS_TABLE]
    return table.all()


@connect_db
def delete_all_commands(db):
    table = db[COMMANDS_TABLE]
    table.delete()


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
