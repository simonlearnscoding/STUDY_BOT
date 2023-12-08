
class update_table():
    def __init__(self):
        pass

    async def update(table, objects, filter):
        # TODO: Test
        for object in objects:
            await self.get_or_create(Pillar, filter, object)
        objects_db = await self.table.all()
        await self.remove_redundant_from_db(objects_db, objects, filter)

    async def get_or_create(table, filter, data, custom_create=None):
        # TODO: TEST
        object = table.filter(filter)
        if not object:
            # Does scope work the same in python??
            await self.create()
        if object != data:
            object.update(data)
        return object

        async def create():
            if custom_create:
                await self.custom_create(data)
            else:
                object = table.create(data)
                object.save()

    async def remove_redundant_from_db(db_objects, actual_objects, filter):
        # TODO: Test
        for db_entry in db_objects:
            if db_entry[filter] not in actual_objects:
                await self.db_entry.delete()


# Put this in on_ready


class user_manager(user):
    def __init__(self):
        super().__init__()
    async def sync_users(server):
        # TODO: Test
        users = guild.users
        for user in users:
            user = await self.self.get_or_create_user(user)
            user_server = UserServer.filter(server=server, user=user)
            if user_server is None:
                user_server = UserServer.create(server=server, user=user)


class user():

    def __init__(self):
        super().__init__()

    async def get_or_create_user(user):
        user_data = create_user_object(user)
        user = await self.get_or_create(User, filter=discord_id, data=user_data, custom_create=create_user)

        async def create_user(user_data):
            # TODO: Test
            pillars = await self.Pillar.all()
            user = await self.User.create(user_data)
            user.save()
            for pillar in pillars:
                UserPillar.create(user=user, pillar=pillar)
            pass

        def create_user_object(user):
            return {
                'discord_id': user.id,
                'display_name': user.display_name
            }



async def create_pillars():
    pillars = [
        {name: 'VITALITAS',
         description: 'workout and mental health',
         color: '#000000'},
        {name: 'STUDY',
         description: 'workout and mental health',
         color: '#000000'},
        {name: 'DISCIPLINE',
         description: 'workout and mental health',
         color: '#000000'}, ]
    await self.update_table(Pillar, pillars, name)


async def create_roles():
    roles = [
        {name: 'VITALITAS',
         description: 'workout and mental health',
         color: '#000000'},
        {name: 'STUDY',
         description: 'workout and mental health',
         color: '#000000'},
        {name: 'DISCIPLINE',
         description: 'workout and mental health',
         color: '#000000'}, ]
    await self.update_table(Roles, roles, name)
