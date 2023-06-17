class Chats:
    def __init__(self, connection):
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute(
            """
            create table if not exists chats (
                id integer primary key auto_increment,
                name varchar(100) not null,
                chat_type varchar(15) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        )

    def create_chat(self, name, chat_type):
        self.database.execute(
            """
            insert into chats (name, chat_type)
            values (%s, %s)
        """,
            (name, chat_type),
        )
        self.connection.commit()

    def find_chat(self, id):
        self.database.execute(
            """
            select id, name, chat_type from chats
            where id = %s
        """,
            (id,),
        )
        chat = self.database.fetchone()
        self.connection.commit()

        if chat == None:
            raise Exception("Chat not found.")
        else:
            return {"id": chat[0], "name": chat[1], "chat_type": chat[2]}

    def update_chat(self, id, new_name, new_chat_type):
        self.database.execute(
            """
        UPDATE chats
        SET {} {}
        WHERE id = %s
        """.format(
                "name = '{}'".format(new_name) if new_name is not None else "",
                "chat_type = '{}'".format(new_chat_type)
                if new_chat_type is not None
                else "",
            ),
            (id,),
        )
        self.connection.commit()

    def delete_chat(self, id):
        self.database.execute(
            """
            delete from chats where id = %s
            """,
            (id,),
        )
        self.connection.commit()
