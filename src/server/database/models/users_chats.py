class UsersChats:
    def __init__(self, connection):
        self.database = connection.cursor()
        self.create_table()
        
    def create_table(self):
        self.database.execute("""
            create table if not exists users_chats (
                id integer primary key auto_increment,
                id_user integer not null,
                id_chat integer not null,
                
                foreign key (id_user) references users(id),
                foreign key (id_chat) references chats(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)