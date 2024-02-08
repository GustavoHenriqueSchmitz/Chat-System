class Messages:
    def __init__(self, connection):
        self.connection = connection
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute(
            """
            create table if not exists messages (
                id integer primary key auto_increment,
                content varchar(1000) not null,
                id_sender int not null,
                id_chat char(36) not null,
                send_date datetime not null,
                
                foreign key (id_sender) references users(id),
                foreign key (id_chat) references chats(id)
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

    def find_messages(self, id=None, id_sender=None, id_chat=None):
        self.database.execute(
            """
            select id, content, id_sender, id_chat, send_date from messages
            where 1=1 {} {} {}
        """.format(
                "and id = '{}'".format(id) if id is not None else "",
                "and id_sender = '{}'".format(id_sender)
                if id_sender is not None
                else "",
                "and id_chat = '{}'".format(id_chat) if id_chat is not None else "",
            ),
        )
        messages = self.database.fetchall()
        self.connection.commit()

        if id is not None:
            if messages == []:
                raise Exception("MessageNotFound")
            else:
                return {
                    "id": messages[0][0],
                    "content": messages[0][1],
                    "id_sender": messages[0][2],
                    "id_chat": messages[0][3],
                }
        else:
            messages_formatted = []
            for message in messages:
                messages_formatted.append(
                    {
                        "id": message[0],
                        "content": message[1],
                        "id_sender": message[2],
                        "id_chat": message[3],
                    }
                )
            return messages_formatted

    def update_message(
        self, id, content=None, id_sender=None, id_chat=None, send_date=None
    ):
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
