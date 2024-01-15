import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


    async def create_table_products(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Products (
            id SERIAL PRIMARY KEY,

            -- Mahsulot kategoriyasi
            category_code VARCHAR(20) NOT NULL,
            category_name VARCHAR(50) NOT NULL,

            -- mahsulot kategoriya ichida katgoriyasi ("Go'sht"-"Mol go'shti")
            subcategory_code VARCHAR(20) NOT NULL,
            subcategory_name VARCHAR(50) NOT NULL,
            -- Mahsulot haqida malumot
            productname VARCHAR(50) NOT NULL,
            photo VARCHAR(255) NULL,
            price INT NOT NULL,
            description VARCHAR(3000) NULL
            );
        """
        await self.execute(sql, execute=True)
    
    async def add_product(self, category_code,category_name,subcategory_code,subcategory_name,productname,photo,price,description):
        sql = "INSERT INTO Products (category_code,category_name,subcategory_code,subcategory_name,productname,photo,price,description)"
        return await self.execute(sql,parameters=(category_code, category_name, subcategory_code, subcategory_name, productname, photo, price, description), commit=True)
    
    async def get_categories(self):
        sql = "SELECT DISTINCT category_name, category_code FROM Products"
        return await self.execute(sql, fetch=True)
    
    async def get_subcategories(self, category_code):
        sql = f"SELECT DISTINCT subcategory_name, subcategory_code FROM Products WHERE category_code='{category_code}'"
        return await self.execute(sql, fetch=True)
    
    async def count_products(self, category_code, subcategory_code=None):
        if subcategory_code:
            sql = f"SELECT COUNT(*) FROM Products WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        else:
            sql = f"SELECT COUNT(*) FROM Products WHERE category_code='{category_code}'"
        return await self.execute(sql, fetchaval=True)
    
    async def get_products(self, category_code, subcategory_code):
        sql = f"SELECT * FROM Products WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        return await self.execute(sql, fetch=True)
    
    # aynan bitta product uchun
    async def get_product(self, product_id):
        sql = f"SELECT * FROM Products WHERE id={product_id}"
        return await self.execute(sql, fetchrow=True)
    
    async def drop_products(self):
        await self.execute("DROP TABLE Products", execute=True)
        

    


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")