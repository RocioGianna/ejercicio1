from db import get_user_by_id, get_users, get_users_filtered


def resolve_get_user_by_id(id):
    return get_user_by_id(id)


def resolve_get_users_filtered(firstName, lastName, email, usaername, limit, offset):
    return get_users_filtered(firstName, lastName, email, usaername, limit, offset)

def resolve_get_users():
    return get_users()

'''def resolve_create_user(obj, info, **kwargs):
    return create_user(**kwargs)


def resolve_update_user(obj, info, **kwargs):
    return update_user(**kwargs)


def resolve_delete_user(obj, info, id):
    return delete_user(id)'''
