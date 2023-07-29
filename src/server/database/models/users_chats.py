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
                id_chat char(36) not null,
                
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

    def find_users_chats(self, config):
        """
        This function allows to search for data of the relation table users_chats
        Having the following config parameter:

        :-> where: To filter the data that you want to get.
        :-> join: To join the relationed tables. Define the following dictionaries, according the tables that you want to add.
        :-> attributes: Define the columns that you want to get data from.

        {
            "where": {
                "id_user": int,
                "id_chat": str
            },
            "join": {
                "users": {
                    "join_type": ["inner", "left", "right"],
                    "on_condition": {"id_user": str}
                },
                "chats": {
                    "join_type": ["inner", "left", "right"],
                    "on_condition": {"id_chat": str}
                }
            },
            "attributes": {
                id: bool,
                id_chat: bool,
                id_user: bool
            }
        }

        Deactivating parameters or options:
        If you don't want to use some option or parameter you can attribute None value to this.
        You can pass None value directly to the parameter to ignore it. Or if you want to use a parameter, but don't want
        use one or more of your options, you can pass None value to the option you want to ignore.
        Except for the attribute parameter options, which are boolean values.
        """

        attributes = ""
        for counter, attribute, activated in enumerate(
            config.get("attributes", {}).items()
        ):
            if activated:
                if len(config["attributes"]) > 1 and counter + 1 < len(
                    config["attributes"]
                ):
                    attributes = attributes + f"{attribute},"
                else:
                    attributes = attributes + attribute

        self.database.execute(
            """
            select {} from users_chats
            {} {} {}
            {} {} {}
            where 1=1 {} {}
        """.format(
                attributes if config.get("attributes", {}) else "*",
                config["join"]["users"]["join_type"]
                if config.get("join", {}).get("users", {}).get("join_type", "")
                else "",
                f"join users" if config.get("join", {}).get("users", {}) else "",
                f'on id_user = {config["join"]["users"]["on_condition"]}'
                if config.get("join", {}).get("users", {}).get("on_condition", "")
                else "",
                config["join"]["chats"]["join_type"]
                if config.get("join", {}).get("chats", {}).get("join_type", "")
                else "",
                f"join chats" if config.get("join", {}).get("chats", {}) else "",
                f'on id_chat = {config["join"]["chats"]["on_condition"]}'
                if config.get("join", {}).get("chats", {}).get("on_condition", "")
                else "",
                "and id_user = '{}'".format(config["where"]["id_user"])
                if config.get("where", {}).get("id_user", 0)
                else "",
                "and id_chat = '{}'".format(config["where"]["id_chat"])
                if config.get("where", {}).get("id_chat", "")
                else "",
            ),
        )

        columns = [column[0] for column in self.database.description]
        results = []
        for row in self.database.fetchall():
            results.append(dict(zip(columns, row)))
        self.connection.commit()

        return results

    def update_user_chat(self, id, new_id_user=None, new_id_chat=None):
        self.database.execute(
            """
        UPDATE users_chats
        SET id = {} {} {}
        WHERE id = %s
        """.format(
                id,
                ",id_user = '{}'".format(new_id_user)
                if new_id_user is not None
                else "",
                ",id_chat = '{}'".format(new_id_chat)
                if new_id_chat is not None
                else "",
            ),
            (id,),
        )
        self.connection.commit()

    def delete_user_chat(self, id=None, id_user=None, id_chat=None):
        self.database.execute(
            """
            delete from users_chats where 1=1 {} {} {}
            """.format(
                "and id = '{}'".format(id) if id is not None else "",
                "and id_user = '{}'".format(id_user) if id_user is not None else "",
                "and id_chat = '{}'".format(id_chat) if id_chat is not None else "",
            ),
        )
        self.connection.commit()
