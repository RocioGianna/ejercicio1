from ariadne import QueryType, MutationType, make_executable_schema, gql
from resolver import resolve_get_user_by_id, resolve_get_users, resolve_get_users_filtered, resolve_create_user, resolve_update_user, resolve_delete_user
from ariadne.asgi import GraphQL
import asyncio

type_defs = gql("""
    type User {
        id: Int!
        firstName: String!
        lastName: String!
        email: String!
        username: String!
        preferences: [String!]
    }
    
    type Query {
        getUser(id: Int!): User!
        getUsersFiltered(name: String, surname: String, email: String, user_name: String, 
            limit: Int = 10, offset: Int = 0): [User!]
        getUsers: [User!]
    }
    
    type Mutation {
        createUser(name: String!, surname: String!, email: String!, user_name: String!,
            password: String!, preferences: [String!]): User!
        updateUser(id: Int!, name: String, surname: String, email: String, user_name: String,
            password: String, preferences: [String!]): User!
        deleteUser(id: Int!): Boolean!
    }   
""")

query = QueryType()

@query.field("getUser")
def get_user_by_id(id):
    return resolve_get_user_by_id(id)

@query.field("getUsersFiltered")
def get_all_users_filtered(name, surname, email, user_name, limit=10, offset=0):
    return resolve_get_users_filtered(name, surname, email, user_name, limit, offset)

@query.field("getUsers")
def get_all_users():
    return resolve_get_users()

mutation = MutationType()

@mutation.field("createUser")
def create_user(info,name, surname, email, user_name, password, preferences):
    return resolve_create_user(info, name, surname, email, user_name, password, preferences)

@mutation.field("updateUser")
def update_user():
    return resolve_update_user()

@mutation.field("deleteUser")
def delete_user(id):
    return resolve_delete_user(id)



async def main():
    ''' print(await get_user_by_id(27))
    
    print(await get_all_users())
    
    print(await delete_user(30))
    
    print(await get_all_users())'''
    
    schema = make_executable_schema(type_defs, [query, mutation])
    app = GraphQL(schema, debug=True)
    
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main())
    print(app)
