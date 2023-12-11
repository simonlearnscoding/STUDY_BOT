import discord
from discord.ext import commands
from setup.bot_instance import bot

from tortoise_models import Channel
# from types.VC_events import VCEvent


async def was_channel_created_by_my_bot(ChannelEvent):
    try:
        guild = ChannelEvent.after.guild
        channel = ChannelEvent.after  # Assuming ChannelEvent.after is the channel object

        # Fetch the audit logs for channel creation
        async for entry in guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=1):
            # Check if the channel created in the logs is the same as the one in question
            if entry.target.id == channel.id:
                return entry.user.id == bot.user.id  # Returns True if created by your bot

        # Return False if no relevant audit log entry is found
        return False

    except discord.NotFound:
        # Return False if unable to access the audit log entry
        return False
    except discord.Forbidden:
        # Handle lack of permissions
        print("Bot does not have permissions to view audit logs.")
        return False


def channel_renamed(ChannelEvent):
    if ChannelEvent.event_str != 'on_guild_channel_update':
        return False
    if ChannelEvent.before.name != ChannelEvent.after.name:
        return True
    return False


def excluding_condition_is_met(ChannelEvent):
    if ChannelEvent.event_str != 'on_guild_channel_update':
        return False
    if ChannelEvent.before.name == ChannelEvent.after.name:
        return True
    return False


async def get_channel_type_from_db(channel):
    channel = await Channel.get_or_none(discord_id=channel.id)
    if channel is None:
        return 'pass'

    channel_type = str(channel.channel_type.value).lower()
    return channel_type


async def get_channel_type_from_discord(channel):
    return str(channel.type.name).lower()
