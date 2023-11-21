
from Cogs.VC_events import VCEvent


def ensure_user_exists(func):
    def wrapper(vc_event: VCEvent, *args, **kwargs):
        # Assuming this is an async function
        # await create_user_if_not_exists(vc_event.member)
        # TODO: call create user if not exists
        # print('called ensure user exists')
        return func(vc_event, *args, **kwargs)
    return wrapper


def ensure_user_has_active_session(func):
    def wrapper(vc_event: VCEvent, *args, **kwargs):
        # Assuming this is an async function
        # await create_user_if_not_exists(vc_event.member)
        # TODO: call create user if not exists
        # print('called ensure user has active sessions')
        return func(vc_event, *args, **kwargs)
    return wrapper
