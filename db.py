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