from Model.User import User

async def resolve_get_users_filtered(**args):
    users = await User.get_users_filtered(**args)
    return users

async def resolve_create_user(**args):
    user = User()
    await user.create_user(**args)
    return user

async def resolve_update_user(**args):
    user = User()
    await user.update_user(**args)
    return user

def resolve_delete_user(**args):
    return User.delete_user(**args)
