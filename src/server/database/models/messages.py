class Messages:
    def __init__(self, connection):
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute(
            """
            create table if not exists messages (
                id integer primary key auto_increment,
                content varchar(1000) not null,
                id_sender int not null,
                id_chat int not null,
                send_date datetime not null,
                
                foreign key (id_sender) references messages(id),
                foreign key (id_chat) references messages(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        )

    def create_message(self, content, id_sender, id_chat, send_date):
        self.database.execute(
            """
            insert into messages (content, id_sender, id_chat, send_date)
            values (%s, %s, %s, %s)
        """,
            (content, id_sender, id_chat, send_date),
        )
        self.connection.commit()

    def find_message(self, id):
        self.database.execute(
            """
            select id, content, id_sender, id_chat, send_date from messages
            where id = %s
        """,
            (id,),
        )
        message = self.database.fetchone()
        self.connection.commit()

        if message == None:
            raise Exception("Message not found.")
        else:
            return {
                "id": message[0],
                "content": message[1],
                "id_sender": message[2],
                "id_chat": message[3],
                "send_date": message[4],
            }

    def update_message(self, id, content, id_sender, id_chat, send_date):
        self.database.execute(
            """
        UPDATE messages
        SET {} {}
        WHERE id = %s
        """.format(
                "name = '{}'".format(content) if content is not None else "",
                "chat_type = '{}'".format(id_sender) if id_sender is not None else "",
            ),
            (id,),
        )
        self.connection.commit()

    def delete_message(self, id):
        self.database.execute(
            """
            delete from messages where id = %s
            """,
            (id,),
        )
        self.connection.commit()
