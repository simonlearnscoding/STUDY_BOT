from utils.error_handler import error_handler
from Cogs.VC_events import VCEvent
from model_managers_tortoise.user_manager import user_manager


@error_handler
async def ensure_user_exists(func):
    def wrapper(vc_event: VCEvent, *args, **kwargs):
        # Assuming this is an async function
        # await create_user_if_not_exists(vc_event.member)

        # TODO: call create user if not exists
        # I have to test if this works or if
        # this implementation even makes sense

        user_manager = user_manager()
        user = user_manager.get_or_create_user(vc_event.member)
        # print('called ensure user exists')
        return func(vc_event, *args, **kwargs)
    return wrapper


@error_handler
async def ensure_user_has_active_session(func):
    def wrapper(vc_event: VCEvent, *args, **kwargs):
        # Assuming this is an async function
        # await create_user_if_not_exists(vc_event.member)
        # TODO: call create user if not exists
        # print('called ensure user has active sessions')
        return func(vc_event, *args, **kwargs)
    return wrapper
