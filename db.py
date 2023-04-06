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
        await cur.execute("SELECT * FROM user WHERE user_id = %s", (user_id))
        result = await cur.fetchone()  
        
    return result

async def get_users_filtered(name, surname, email, user_name, limit, offset):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM user WHERE name = %s AND surname = %s AND email = %s AND user_name = %s LIMIT = %s OFFSET = %s", (name, surname, email, user_name, limit, offset))
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
        await cur.execute("SELECT * FROM user")
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

async def create_user(name, surname, email, user_name, password):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("INSERT INTO user (name, surname, email, user_name, password) VALUES (%s, %s, %s, %s, %s)", (name, surname, email, user_name, password))
        user_id = cur.lastrowid
        await conn.commit()

    conn.close()
    return user_id

async def update_user(user_id, name, surname, email, user_name, password):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute(
            "UPDATE user SET name=%s, surname=%s, email=%s, user_name=%s, password=%s WHERE user_id=%s",
            (name, surname, email, user_name, password, user_id)
            )
        await conn.commit()
                
    return f"User with ID {user_id} has been modify"

async def delete_user(user_id):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("DELETE FROM user WHERE user_id = %s", (user_id))
        await conn.commit()
                
    return f"User with ID {user_id} has been deleted"