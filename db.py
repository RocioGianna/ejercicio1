import  aiomysql


async def get_connection():
    pool = await aiomysql.create_pool(
            host='localhost',
            user='root',
            password='test',
            db='ejercicio_1' 
        )
    
    conn = await pool.acquire()
    return conn
     
async def get_user_by_id(user_id):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
        result = await cur.fetchone()
      
        user = {
            "user_id": result[0],
            "name": result[1],
            "surname": result[2],
            "email": result[3],
            "user_name": result[4],
            "password": result[5]
        }  
            
    return user

async def get_users_filtered(**args):
    conn = await get_connection()
    async with conn.cursor() as cur:        
        sql = "SELECT * FROM user WHERE 1=1"
        params = []
        if 'name' in args:
            print(args['name'])
            sql += " AND name LIKE %s"
            params.append(f"%{args['name']}%")  
        if 'surname' in args:
            sql+= " AND surname = %s"
            params.append(args['surname']) 
        if 'email' in args:
            sql+= " AND email = %s"
            params.append(args['email']) 
        if 'user_name' in args:
            sql+= " AND user_name = %s"
            params.append(args['user_name']) 
        sql+= " LIMIT %s"
        params.append(args['limit'])
        sql+= " OFFSET %s"
        params.append(args['offset'])
        print(sql) 
        
        await cur.execute(sql, params)
        results = await cur.fetchall()  
        

    users = []
    for result in results:
        user = {
            "user_id": result[0],
            "name": result[1],
            "surname": result[2],
            "email": result[3],
            "user_name": result[4],
            "password": result[5]
        }
        users.append(user)
        
    return users

async def get_users():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM user u JOIN preferences p ON p.user_id = u.user_id")
        results = await cur.fetchall()   

    users = []
    for result in results:
        user = {
            "user_id": result[0],
            "name": result[1],
            "surname": result[2],
            "email": result[3],
            "user_name": result[4],
            "password": result[5],
            "preference_color": result[9],
            "preference_languaje": result[8],
        }
        users.append(user)
        
    return users

async def create_user(**args):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("INSERT INTO user (name, surname, email, user_name, password) VALUES (%r, %r, %r, %r, %r)" % (args['name'], args['surname'], args['email'], args['user_name'], args['password']))
        user_id = cur.lastrowid
        await conn.commit()
    conn.close()
    
    return await get_user_by_id(user_id)


async def update_user(**args):
    conn = await get_connection()
    set_clauses = []
    id = args["id"]
    
    for key, value in args.items():
        if key != "id":
            set_clauses.append(f"{key} = '{value}'")
    set_clause_str = ", ".join(set_clauses) 
    
    sql = f"UPDATE user SET {set_clause_str} WHERE user_id = {id}" 

    async with conn.cursor() as cur:
        await cur.execute(sql)
        await conn.commit()
                
    return await get_user_by_id(id)

async def delete_user(user_id):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("DELETE FROM user WHERE user_id = %s", (user_id))
        await conn.commit()
                
    return True

async def create_preferences(**args):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("INSERT INTO preferences (user_id, color, language) VALUES (%s, %r, %r)"% (args['user_id'], args['color'], args['language']))
        await conn.commit()

    conn.close()

async def get_preferences():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM preferences")
        results = await cur.fetchall()   
    
    preferences = []
    for result in results:
        preference = {
            "id": result[0],
            "user_id": result[1],
            "color": result[2],
            "language": result[3],
        }
        preferences.append(preference)
        
    return preferences