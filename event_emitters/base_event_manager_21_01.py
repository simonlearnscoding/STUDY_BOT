from discord.ext import commands
from utils.error_handler import class_error_handler
from typing import List
from abc import ABC, abstractmethod


class EventConditionNode(ABC):
    def __init__(self, state, bot, event):
        self.man_state = state
        self.bot = bot
        self.event = event
        self.state = None

    async def evaluate(self):
        if self.state is None:
            self.state = await self.handle()
        return self.state

    
    async def evaluate_condition(self, condition_name):
        condition_node = self.man_state.get(condition_name)
        if condition_node:
            return await condition_node.evaluate()
        else:
            raise ValueError(f"Condition '{condition_name}' not found in man_state")

    @abstractmethod
    async def handle(self):
        pass


class EventEmitter(ABC):
    def __init__(self, bot):
        self.bot = bot

    async def handle_event(self, event_name):
        method = getattr(self, event_name, None)
        if callable(method):
            await method()
        else:
            raise AttributeError(f"Method '{event_name}' not found in {self.__class__.__name__}")


@class_error_handler
class EventManager:
    def __init__(self, conditionals, conditions_with_actions, bot, event):
        self.bot = bot
        self.event = event
        self.conditionals = {}  # Initialize as empty dictionary

        # Populate the dictionary
        for cls in conditionals:
            self.conditionals[cls.__name__] = cls(bot=bot, event=event, state=self.conditionals)

        self.conditions_with_actions = conditions_with_actions

    async def evaluate_all(self):
        await self.event.get_event_db_entries()
        for condition_name in self.conditions_with_actions:
            condition_node = self.conditionals[condition_name]
            if condition_node and await condition_node.evaluate():
                await self.event.handle_event(condition_name)
                break  # Break the loop if a condition evaluates to True
