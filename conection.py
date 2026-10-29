from dotenv import load_dotenv
import asyncpg
import os


load_dotenv()
pasw  = os.getenv("PASSWORD_DB")





async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="my_sql",
            password=pasw
        )
        return conn
    except Exception as Error:
        print(f"Connection Error {Error}")
    
    
    
async def create_table():
    try:
        conn=await connection_db()
        await conn.execute("""
             CREATE TABLE IF NOT EXISTS users(
                 user_id serial primary key,
                 full_name varchar(100),
                 username varchar(100),
                 telegram_id varchar(100),
                 is_admin boolean default false,
                 is_active boolean default true,
                 create_at timestamp default now()
             );              
                           
                           
                           
            CREATE TABLE IF NOT exists autors(
                autor_id serial primary key,
                full_name varchar(100),
                country varchar(100),
                 is_active boolean default true,
                 create_at timestamp default now()            
            );
            
            CREATE TABLE IF NOT exists category (
                category_id serial primary key,
                category varchar(100),
                is_active boolean default true,
                create_at timestamp default now()
                
            ); 
            CREATE TABLE IF NOT exists books(
                books_id serial primary key,
                title varchar(100),
                caption text,
                autor_id int references autors(autor_id),
                publisher varchar(100),
                category_id int references category(category_id),
                is_active boolean default true,
                create_at timestamp default now()
                
            )                
                           
                           """)
        print("Table created")
    except Exception as Error:
        print(f"Create Error: {Error}")
    finally:
        await conn.close()
        
        