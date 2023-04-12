from Model.Preference import Preference 
from DB import DB
import json


class User:  

    async def get_users_filtered(**args):
        conn = await DB.get_connection()  
        
        async with conn.cursor() as cur:        
            sql = "SELECT name, surname, email, user_name, password, preferences  FROM user WHERE 1=1"
            params = []
            if 'id' in args:
                sql += " AND user_id = %s"
                params.append(args['id']) 
            if 'name' in args:
                sql += " AND name LIKE %s"
                params.append(f"%{args['name']}%")  
            if 'surname' in args:
                sql += " AND surname LIKE %s"
                params.append(f"%{args['surname']}%")  
            if 'email' in args:
                sql += " AND email LIKE %s"
                params.append(f"%{args['email']}%") 
            if 'user_name' in args:
                sql += " AND user_name LIKE %s"
                params.append(f"%{args['user_name']}%") 
            if 'limit' in args:
                sql+= " LIMIT %s"
                params.append(args['limit'])
                sql+= " OFFSET 0"

            await cur.execute(sql, params)
            results = await cur.fetchall()  
        
        users = []
        keys = ('name', 'surname', 'email', 'user_name', 'password')
        
        for result in results:
            results_dict = dict(zip(keys, result[:5]))
            preferences_dict = json.loads(result[5])
            results_dict['preference'] = preferences_dict
            user = User()
            
            if 'name' in results_dict and results_dict['name']:
                user.name = results_dict['name']
            if 'surname' in results_dict and results_dict['surname']:
                user.surname = results_dict['surname']
            if 'email' in results_dict and results_dict['email']:
                user.email = results_dict['email']
            if 'user_name' in results_dict and results_dict['user_name']:
                user.user_name = results_dict['user_name']
            if 'password' in results_dict and results_dict['password']:
                user.password = results_dict['password']
            if 'preference' in results_dict and results_dict['preference']:
                user.preferences = Preference(results_dict['preference']['color'],  results_dict['preference']['language'])
        
            users.append(user)
        
        return users

    async def create_user(self,**args): 
        conn = await DB.get_connection()
        async with conn.cursor() as cur:  
            preferences = args['user']['preferences']
            preference = Preference(preferences['color'], preferences['language'])
            preference_json = json.dumps(preference.__dict__)
            await cur.execute("INSERT INTO user (name, surname, email, user_name, password, preferences) VALUES (%r, %r, %r, %r, %r, %r)" % (args['user']['name'], args['user']['surname'], args['user']['email'], args['user']['user_name'], args['user']['password'], preference_json,))
            user_id = cur.lastrowid
            await conn.commit()
        conn.close()

        self.user_id = user_id
        self.name = args['user']['name']
        self.surname = args['user']['surname']
        self.email = args['user']['email']
        self.user_name = args['user']['user_name']
        self.password = args['user']['password']
        self.preferences = preference

    async def update_user(self,**args):
        conn = await DB.get_connection()
        sql = "UPDATE user SET"
        params = []
        if 'name' in args['user']:
            sql += " name = %s,"
            params.append(args['user']['name'])
        if 'surname' in args:
            sql += " surname = %s,"
            params.append(args['user']['surname'])  
        if 'email' in args:
            sql += " email = %s,"
            params.append(args['user']['email']) 
        if 'user_name' in args:
            sql += " user_name = %s,"
            params.append(args['user']['user_name'])
        
        sql.rstrip(',')
        async with conn.cursor() as cur:
            await cur.execute(sql, params)
            await conn.commit()
                    
        self.name = args['user']['name']
        self.surname = args['user']['surname']
        self.email = args['user']['email']
        self.user_name = args['user']['user_name']
    

    async def delete_user(**args):
        conn = await DB.get_connection()
        if 'id' in args:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM user WHERE user_id = %s", (args['id']))
                await conn.commit()
        user = await User.get_users_filtered(id=(args['id']))       
        
        if len(user) == 0:
            return True
        else:
            return False