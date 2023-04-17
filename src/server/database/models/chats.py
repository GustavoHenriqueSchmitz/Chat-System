class chats:
    def __init__(self, connection):
        self.database = connection.cursor()
        self.create_table()
        
    def create_table(self):
        self.database.execute("""
            create table if not exists chats (
                id integer primary key auto_increment,
                name varchar(100) not null,
                chat_type varchar(15) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        