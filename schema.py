from ariadne import QueryType, MutationType, make_executable_schema, gql
from resolver import resolve_get_user_by_id, resolve_get_users, resolve_get_users_filtered, resolve_create_user, resolve_update_user, resolve_delete_user, resolve_create_preferences, resolve_get_preferences

type_defs = gql("""
    type User {
        user_id: Int!
        name: String!
        surname: String!
        email: String!
        user_name: String!
        password: String!
    }
    
    type Preferences{
        languaje:String!
        color:String!
    }
    
    type Query {
        getUser(id: Int!): User!
        getUsersFiltered(name: String, surname: String, email: String, user_name: String, limit: Int!, offset:Int!): [User!]
        getUsers: [User!]
        getPreferences: [Preferences!]
    }
    
    type Mutation {
        createUser(name: String!, surname: String!, email: String!, user_name: String!,
            password: String!): User!
        updateUser(id: Int!, name: String, surname: String, email: String, user_name: String,
            password: String): User!
        deleteUser(id: Int!): Boolean!
        createPreferences(user_id: Int!, language: String!, color: String!): Preferences!
    }   
""")

query = QueryType()

@query.field("getUser")
def get_user_by_id(source, info,**args):
    return resolve_get_user_by_id(args['id'])

@query.field("getUsersFiltered")
def get_all_users_filtered(source, info,**args):
    return resolve_get_users_filtered(**args)

@query.field("getUsers")
def get_all_users(source, info):
    return resolve_get_users()

@query.field("getPreferences")
def get_all_preferences(source, info):
    return resolve_get_preferences()

mutation = MutationType()

@mutation.field("createUser")
def create_user(source, info,**args):
    return resolve_create_user(**args)

@mutation.field("updateUser")
def update_user(source, info, **args):
    return resolve_update_user(**args)

@mutation.field("deleteUser")
def delete_user(source, info,**args):
    return resolve_delete_user(args['id'])

@mutation.field("createPreferences")
def create_preferences(source, info,**args):
    return resolve_create_preferences(**args)
 
    
schema = make_executable_schema(type_defs, [query, mutation])
   
