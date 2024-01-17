from dataclasses import dataclass
from model_managers_tortoise.database_managers import *
from tortoise_models import Server, User, Channel, TextChannelEnum, UserServer
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from model_managers_tortoise.database_managers import database_base_class
from model_managers_tortoise.table_manager import *
from datetime import datetime
from model_managers_tortoise.user_role_discord import update_user_roles

from utils.error_handler import class_error_handler

class UserServerEntity:
    def __init__(self, user, guild):
        self.user = user
        self.guild = guild
        self.name = user.name
        self.id = user.id


class GetUserServerEntitiesStrategy(GetChildEntitiesStrategy):
    def get_child_entities(self):
        members = self.guild.members
        user_server_entities = [
            UserServerEntity(user=member, guild=self.guild)
            for member in self.guild.members
        ]
        return user_server_entities


class UserServerGetDataStrategy(GetDataStrategy):
    async def get_data(self):
        await self.set_server()
        await self.set_user()
        now = datetime.now()
        return {"user": self.user_db, "server": self.server_db, "joined_at": now}


class UserServerFilterStrategy(FilterStrategy):
    async def filter(self):
        await self.set_server()
        await self.set_user()
        return await self.table.filter(user=self.user_db, server=self.server_db).first()

class UserServerDeleteStrategy(DeleteStrategy):
    async def delete(self):
        self.db_entry = await self.filter_strategy.filter(self)
        if self.db_entry:
            await self.db_entry.delete()
            print('deleting user_server entry')


class UserServerUpdateStrategy(UpdateStrategy):
    async def update(self):
        await update_user_roles(self.user.entity)

class UserServerCreateStrategy(CreateStrategy):
    async def create(self):
        await update_user_roles(self.user.entity)
@class_error_handler
class user_server_class(database_base_class, ServerSetterMixin, UserSetterMixin):
    def __init__(
        self,
        bot,
        entity,
    ):
        database_base_class.__init__(
            self,
            entity=entity,
            bot=bot,
            table=UserServer,
            filter_strategy=UserServerFilterStrategy,
            get_data_strategy=UserServerGetDataStrategy,
            update_strategy=UserServerUpdateStrategy,
            create_strategy=UserServerCreateStrategy
        )
        self.delete_strategy=UserServerDeleteStrategy
        self.user = self.entity.user
        self.guild = self.entity.guild

@class_error_handler
class user_server_manager(table_manager, ServerSetterMixin):
    def __init__(self, bot, entity):
        super().__init__(
            table=UserServer,
            bot=bot,
            child_entities_strategy=GetUserServerEntitiesStrategy,
            child_class=user_server_class,
        )
        self.entity = entity
        self.guild = entity

    async def get_all_db_entries(self):
        await self.set_server()
        entries = await self.table.filter(server=self.server_db)
        return entries

    async def get_db_entry_id(self, db_entry):
        # I need to get the user discord id as int
        discord_user = await db_entry.user
        return int(discord_user.discord_id)

    async def check_and_delete_if_redundant(self, db_entry, valid_ids):

        """
        checks and deletes the db_entry if it's not in valid_ids.
        """
        db_entry_id = await self.get_db_entry_id(db_entry)
        if db_entry_id not in valid_ids:
            await self.delete_strategy.delete(self, db_entry)
