from ariadne import QueryType, MutationType, make_executable_schema, gql
from resolver import resolve_get_users_filtered, resolve_create_user, resolve_update_user, resolve_delete_user

type_defs = gql("""
    type User {
        user_id: Int!
        name: String!
        surname: String!
        email: String!
        user_name: String!
        password: String!
        preferences: Preference!
    }
    
    type Preference{
        language:String!
        color:String!
    }
    
    input PreferenceInput {
        language: String!
        color: String!
    }
    
    input UserInput {
        name: String!
        surname: String!
        email: String!
        user_name: String!
        password: String!
        preferences: PreferenceInput!
    }
    
    type Query {
        usersFiltered(id: Int, name: String, surname: String, email: String, user_name: String, limit: Int): [User!]    
    }
    
    type Mutation {
        createUser(user:UserInput): User!
        updateUser(user:UserInput): User!
        deleteUser(id: Int!): Boolean!
    }   
""")

query = QueryType()

@query.field("usersFiltered")
def all_users_filtered(source, info,**args):
    return resolve_get_users_filtered(**args)


mutation = MutationType()

@mutation.field("createUser")
def create_user(source, info,**args):
    return resolve_create_user(**args)

@mutation.field("updateUser")
def update_user(source, info, **args):
    return resolve_update_user(**args)

@mutation.field("deleteUser")
def delete_user(source, info,**args):
    return resolve_delete_user(**args)
 
    
schema = make_executable_schema(type_defs, [query, mutation])
   
