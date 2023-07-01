class Chats:
    def __init__(self, connection):
        self.connection = connection
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute(
            """
            create table if not exists chats (
                id integer primary key auto_increment,
                name varchar(100) not null,
                chat_type varchar(15) not null,
                chat_code varchar(60) not null unique
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        )

    def create_chat(self, name, chat_type, chat_code):
        self.database.execute(
            """
            insert into chats (name, chat_type, chat_code)
            values (%s, %s, %s)
        """,
            (name, chat_type, chat_code),
        )
        self.connection.commit()

    def find_chats(self, id, chat_code):
        self.database.execute(
            """
            select id, name, chat_type, chat_code from chats
            where 1=1 {} {}
        """.format(
                "and id = '{}'".format(id)
                if id is not None
                else "",
                "and chat_code = '{}'".format(chat_code)
                if chat_code is not None
                else "",
            ),
        )
        chats = self.database.fetchall()
        self.connection.commit()

        if id is not None or chat_code is not None:
            if chats == []:
                raise Exception("Chat not found")
            return {
                "id": chats[0][0],
                "name": chats[0][1],
                "chat_type": chats[0][2],
                "chat_code": chats[0][3],
            }
        else:
            chats_formatted = []
            for chat in chats:
                chats_formatted.append(
                    {
                        "id": chat[0],
                        "name": chat[1],
                        "chat_type": chat[2],
                        "chat_code": chat[3],
                    }
                )
            return chats_formatted

    def update_chat(self, chat_code, new_name, new_chat_type):
        self.database.execute(
            """
        UPDATE chats
        SET {} {}
        WHERE chat_code = %s
        """.format(
                "name = '{}'".format(new_name) if new_name is not None else "",
                "chat_type = '{}'".format(new_chat_type)
                if new_chat_type is not None
                else "",
            ),
            (chat_code,),
        )
        self.connection.commit()

    def delete_chat(self, chat_code):
        self.database.execute(
            """
            delete from chats where chat_code = %s
            """,
            (chat_code,),
        )
        self.connection.commit()
