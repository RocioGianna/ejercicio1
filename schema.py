from ariadne import QueryType, MutationType, make_executable_schema, gql
from resolver import resolve_get_user_by_id, resolve_get_users, resolve_get_users_filtered
from ariadne.asgi import GraphQL
import asyncio

type_defs = gql("""
    type User {
        id: Int!
        firstName: String!
        lastName: String!
        email: String!
        username: String!
        preferences: Preferences
    }
    
    type Preferences{
        language: String
        interfaceColor: String
    }
    
    type Query {
        getUser(id: Int!): User!
        getUsersFiltered(name: String, surname: String, email: String, user_name: String, 
            limit: Int = 10, offset: Int = 0): [User!]
        getUsers: [User!]
    }
    
    type Mutation {
        createUser(firstName: String!, lastName: String!, email: String!, username: String!,
            password: String!, preferences: Preferences): User!
        updateUser(id: Int!, firstName: String, lastName: String, email: String, username: String,
            password: String, preferences: Preferences): User!
        deleteUser(id: Int!): Boolean!
    }   
""")

query = QueryType()

@query.field("getUser")
def get_user_by_id(id):
    return resolve_get_user_by_id(id)

@query.field("getUsersFiltered")
def get_all_users_filtered(firstName, lastName, email, usaername, limit=10, offset=0):
    return resolve_get_users_filtered(firstName, lastName, email, usaername, limit, offset)

@query.field("getUsers")
def get_all_users():
    return resolve_get_users()

'''mutation = MutationType()

@mutation.field("createUser")
def create_user():
    return resolve_create_user()


schema = make_executable_schema(type_defs, [query, mutation])
app = GraphQL(schema, debug=True)

 '''

async def main():
    print(await get_user_by_id(27))
    
    print(await get_all_users())
    
    schema = make_executable_schema(type_defs, [query])
    
    app = GraphQL(schema, debug=True)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main())
    print(app)
