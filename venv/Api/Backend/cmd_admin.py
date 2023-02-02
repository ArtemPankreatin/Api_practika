import psycopg2


def main_instance():
    conn = psycopg2.connect(database="api",
                        host="54.37.74.248",
                        user="klim",
                        port="5432")
    cur = conn.cursor()
    login = input("Введите ваш логин: ")
    password = str(input("Введите ваш пароль: "))
    print(cur.execute(f"""SELECT * FROM testdb_user WHERE email='{login}'"""))
    # user = User.objects.get(email=login)

    # if user:
    #     if user.role == "admin":
    #         users_list = User.objects.filter(role="user")
    #         print(users_list)
    #     else:
    #         print("Вы не админ.")
    # else:
    #     print("Такого пользователя не существует.")


if __name__ == "__main__":
    main_instance()