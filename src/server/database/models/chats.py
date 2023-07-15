class Chats:
    class ChatNotFoundError(Exception):
        pass

    def __init__(self, connection):
        self.connection = connection
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute(
            """
            create table if not exists chats (
                id char(36) primary key,
                name varchar(100) not null,
                chat_type varchar(15) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        )

    def create_chat(self, id, name, chat_type):
        self.database.execute(
            """
            insert into chats (id, name, chat_type)
            values (%s, %s, %s)
        """,
            (id, name, chat_type),
        )
        self.connection.commit()

    def find_chats(self, id=None, chat_type=None):
        self.database.execute(
            """
            select id, name, chat_type from chats
            where 1=1 {} {}
        """.format(
                "and id = '{}'".format(id) if id is not None else "",
                "and chat_type = '{}'".format(chat_type)
                if chat_type is not None
                else "",
            ),
        )
        chats = self.database.fetchall()
        self.connection.commit()

        if id is not None:
            if chats == []:
                raise self.ChatNotFoundError("Chat not Found")
            else:
                return {
                    "id": chats[0][0],
                    "name": chats[0][1],
                    "chat_type": chats[0][2],
                }
        else:
            chats_formatted = []
            for chat in chats:
                chats_formatted.append(
                    {
                        "id": chat[0],
                        "name": chat[1],
                        "chat_type": chat[2],
                    }
                )
            return chats_formatted

    def update_chat(self, id, new_name=None, new_chat_type=None):
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
