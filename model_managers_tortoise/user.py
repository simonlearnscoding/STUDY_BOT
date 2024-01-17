from dataclasses import dataclass
from model_managers_tortoise.database_managers import *
from tortoise_models import Server, User, Channel, TextChannelEnum, UserPillar, Pillar
from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from model_managers_tortoise.database_managers import database_base_class
from model_managers_tortoise.table_manager import *


class UserFilterStrategy(FilterStrategy):
    async def filter(self):
        return await self.table.filter(discord_id=str(self.id)).first()


class UserGetDataStrategy(GetDataStrategy):
    async def get_data(self):
        return {"discord_id": self.entity.id, "display_name": self.entity.name}


class UserUpdateStrategy(UpdateStrategy):
    async def update(self):
        pass


class UserCreateStrategy(CreateStrategy):
    async def create(self):
        pillars = await Pillar.all()
        await UserPillar.filter(user=self.db_entry).delete()
        for pillar in pillars:
            await UserPillar.create(pillar=pillar, user=self.db_entry, xp=0, level=0)


class user_class(database_base_class):
    def __init__(
        self,
        bot,
        entity,
    ):
        database_base_class.__init__(
            self,
            entity=entity,
            bot=bot,
            table=User,
            filter_strategy=UserFilterStrategy,
            get_data_strategy=UserGetDataStrategy,
            update_strategy=UserUpdateStrategy,
            create_strategy=UserCreateStrategy
        )

    async def did_user_reach_new_level(user):
        return True

    async def did_user_reach_new_role(user):
        return True


class GetUserEntitiesStrategy(GetChildEntitiesStrategy):
    def get_child_entities(self):
        members = set()  # Set to store unique members
        for guild in self.bot.guilds:
            # Add each member to the set
            members.update(guild.members)
        return members


class user_manager(table_manager):
    def __init__(self, bot):
        super().__init__(
            table=User,
            bot=bot,
            child_entities_strategy=GetUserEntitiesStrategy,
            child_class=user_class,
        )

