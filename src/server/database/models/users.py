class Users:
    def __init__(self, connection):
        self.connection = connection
        self.database = connection.cursor()
        self.create_table()

    def create_table(self):
        self.database.execute("""
            create table if not exists users (
                id integer primary key auto_increment,
                name varchar(100) not null,
                number varchar(25) not null unique,
                password varchar(255) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        self.connection.commit()

    def create_user(self, name, phone_number, password):
        self.database.execute("""
            insert into users (name, number, password)
            values (%s, %s, %s)
        """, (name, phone_number, password))
        self.connection.commit()
