from typing import List
from model_managers_tortoise.functional_methods import async_apply_to_each
from discord import Member, utils, Guild, role, Color
import discord
from tortoise_models import Server, User, Channel, TextChannelEnum, UserServer, Role

from utils.error_handler import error_handler

def get_user_roles(member: Member) -> List[str]:
    # Extract role names from the member's roles
    return [role.name for role in member.roles]


async def remove_all_spqr_roles(member, user_current_role):

    async def get_all_spqr_roles() -> List[str]:
        roles = await Role.all()
        array = []
        for role in roles:
            array.append(role.name)
        # TODO:
        return array

    def get_intersecting_array(user_roles, spqr_roles) -> List[str]:
        return [role for role in user_roles if role in spqr_roles]

    async def get_intersecting_roles(member) -> List[str]:
        current_user_role: List[str] = get_user_roles(member)
        spqr_roles: List[str] = await get_all_spqr_roles()
        return get_intersecting_array(current_user_role, spqr_roles)

    async def remove_role(member: Member, role_name: str):
        # Check if the role already exists on the member

        role = discord.utils.get(member.roles, name=role_name)

        if role:
            # If the role exists, remove it from the member
            await member.remove_roles(role)

    async def remove_array_of_roles(member, roles):
        for role in roles:
            await remove_role(member, role)

    def remove_actual_user_role_from_intersecting_role_array(user_current_role, roles_to_delete):
        if user_current_role in roles_to_delete:
            roles_to_delete.remove(user_current_role)

    async def main_function(member):
        roles_to_delete = await get_intersecting_roles(member)
        remove_actual_user_role_from_intersecting_role_array(user_current_role, roles_to_delete)
        await remove_array_of_roles(member, roles_to_delete)

    await main_function(member)


async def give_member_current_spqr_role(member, user_current_role):
    async def get_or_create_role(user_current_role) -> role.Role:
        # Check if the role already exists in the server
        existing_role = utils.get(member.guild.roles, name=user_current_role.name)

        if existing_role:
            # If the role exists, return it
            return existing_role
        else:
            # If the role doesn't exist, create a new role
            new_role = await member.guild.create_role(name=user_current_role.name)
            int_color = int(user_current_role.color[1:], 16)  # Remove the leading #
            await new_role.edit(color=Color(int_color))
            return new_role

    async def main_function(member, user_current_role):
        role = await get_or_create_role(user_current_role)
        await member.add_roles(role)

    async def give_member_a_role(member, role):
        # TODO:
        pass

    await main_function(member, user_current_role)

@error_handler
async def update_user_roles(member):

    async def get_member_current_spqr_role(member):
        user = await User.filter(discord_id=member.id).first()
        role = await user.role.first()
        return role

    async def main_function(member):
        print(f'updating {member.name} roles')
        user_current_role = await get_member_current_spqr_role(member)
        await remove_all_spqr_roles(member, user_current_role.name)
        if user_current_role in get_user_roles(member): # TODO: AND no other roles in there
            return
        await give_member_current_spqr_role(member, user_current_role)

    await main_function(member)
