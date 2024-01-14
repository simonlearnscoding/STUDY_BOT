
TORTOISE_ORM = {
    "connections": {"default": "mysql://simon:3112@localhost:3306/discordjs"},
    "apps": {
        "models": {
            "models": ["aerich.models", "tortoise_models"],
            "default_connection": "default",
        },
    },
}
# "mysql://root:123456@127.0.0.1:3306/test"
