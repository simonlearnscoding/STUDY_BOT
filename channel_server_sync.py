from django.db import models
#TODO: Import Tortoise instead


class BaseClassManager(models.Manager):
    def sync_from_discord(self, discord_object, defaults):
        model_class = self.model  # The model class that uses this manager
        discord_id = str(discord_object.id)
        instance, created = model_class.objects.update_or_create(
            discord_id=discord_id,
            defaults=defaults
        )
        return instance


class ServerManager(BaseClassManager):
    def sync_from_discord(self, guild):
        defaults = {'name': guild.name}  # Add other fields as necessary
        return super().sync_from_discord(guild, defaults)

    def update_all_servers(self, bot):
        for guild in bot.guilds:
            self.sync_from_discord(guild, {'name': guild.name})


class ChannelManager(BaseClassManager):
    pass
    # def sync_from_discord(self, channel):
    #     server = Server.objects.sync_from_discord(channel.guild)
    #     defaults = {
    #         'name': channel.name,
    #         'server': server  # Assuming a ForeignKey to Server
    #         # Add other fields as necessary
    #     }
    #     return super().sync_from_discord(channel, defaults)
