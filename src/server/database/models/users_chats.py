class UsersChats:
    def __init__(self, connection):
        self.connection = connection
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute(
            """
            create table if not exists users_chats (
                id integer primary key auto_increment,
                id_user integer not null,
                id_chat integer not null,
                
                foreign key (id_user) references users(id),
                foreign key (id_chat) references chats(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        )

    def create_user_chat(self, id_user, id_chat):
        self.database.execute(
            """
            insert into users_chats (id_user, id_chat)
            values (%s, %s)
        """,
            (id_user, id_chat),
        )
        self.connection.commit()

    def find_users_chats(self, id_user=None, id_chat=None):
        self.database.execute(
            """
            select id, id_user, id_chat from users_chats
            where 1=1 {} {}
        """.format(
                "and id_user = '{}'".format(id_user) if id_user is not None else "",
                "and id_chat = '{}'".format(id_chat) if id_chat is not None else "",
            ),
        )
        users_chats = self.database.fetchall()
        self.connection.commit()

        users_chats_formatted = []
        for user_chat in users_chats:
            users_chats_formatted.append(
                {
                    "id": user_chat[0],
                    "id_user": user_chat[1],
                    "id_chat": user_chat[2],
                }
            )
        return users_chats_formatted

    def update_user_chat(self, id, new_id_user=None, new_id_chat=None):
        self.database.execute(
            """
        UPDATE messages
        SET {} {}
        WHERE id = %s
        """.format(
                "id_user = '{}'".format(new_id_user) if new_id_user is not None else "",
                "id_sender = '{}'".format(new_id_chat)
                if new_id_chat is not None
                else "",
            ),
            (id,),
        )
        self.connection.commit()

    def delete_user_chat(self, id):
        self.database.execute(
            """
            delete from users_chats where id = %s
            """,
            (id,),
        )
        self.connection.commit()
