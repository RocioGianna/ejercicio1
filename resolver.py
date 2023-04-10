from db import get_user_by_id, get_users, get_users_filtered, create_user, delete_user, update_user, create_preferences, get_preferences


def resolve_get_user_by_id(id):
    return get_user_by_id(id)


def resolve_get_users_filtered(**args):
    return get_users_filtered(**args)

def resolve_get_users():
    return get_users()

def resolve_create_user(**args):
    return create_user(**args)


def resolve_update_user(**args):
    return update_user(**args)


def resolve_delete_user(id):
    return delete_user(id)

def resolve_create_preferences(**args):
    return create_preferences(**args)

def resolve_get_preferences():
    return get_preferences()