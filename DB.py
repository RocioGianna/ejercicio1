import  aiomysql

class DB:
    
    connection = None
    
    async def init_connection():
        if DB.connection is None:
            pool = await aiomysql.create_pool(
                    host='localhost',
                    user='root',
                    password='test',
                    db='ejercicio_1' 
                )
            DB.connection = await pool.acquire()
        
    async def get_connection():
        if DB.connection is None:
            await DB.init_connection()
        return DB.connection
