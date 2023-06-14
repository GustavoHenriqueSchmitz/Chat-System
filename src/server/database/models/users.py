class Users:
    def __init__(self, connection):
        self.connection = connection
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute(
            """
            create table if not exists users (
                id integer primary key auto_increment,
                name varchar(100) not null,
                phone_number varchar(25) not null unique,
                password varchar(255) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        )
        self.connection.commit()

    def create_user(self, name, phone_number, password):
        self.database.execute(
            """
            insert into users (name, phone_number, password)
            values (%s, %s, %s)
        """,
            (name, phone_number, password),
        )
        self.connection.commit()

    def find_user(self, phone_number):
        self.database.execute(
            """
            select name, phone_number, password from users
            where phone_number = %s
        """,
            (phone_number,),
        )
        user = self.database.fetchone()
        self.connection.commit()

        if user == None:
            raise Exception("User not found.")
        else:
            return {"name": user[0], "phone_number": user[1], "password": user[2]}

    def update_user(self, phone_number, new_phone_number, new_name, new_password):
        self.database.execute(
            """
        UPDATE users
        SET {} {} {}
        WHERE phone_number = %s
        """.format(
                "name = '{}'".format(new_name) if new_name is not None else "",
                "phone_number = '{}'".format(new_phone_number)
                if new_phone_number is not None
                else "",
                "password = '{}'".format(new_password)
                if new_password is not None
                else "",
            ),
            (phone_number,),
        )
        self.connection.commit()

    def delete_user(self, phone_number):
        self.database.execute(
            """
            delete from users where phone_number = %s
            """,
            (phone_number,),
        )
        self.connection.commit()
