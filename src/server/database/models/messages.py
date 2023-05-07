class Messages:
    def __init__(self, connection):
        self.database = connection.cursor()
        self.create_table()
        
    def create_table(self):
        self.database.execute("""
            create table if not exists messages (
                id integer primary key auto_increment,
                content varchar(1000) not null,
                id_sender int not null,
                id_chat int not null,
                send_date datetime not null,
                
                foreign key (id_sender) references users(id),
                foreign key (id_chat) references chats(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)