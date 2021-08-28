from django.db import connection


def dict_fetch_all(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def sql(query, get_tuple=False, no_return=False):
    with connection.cursor() as cursor:
        cursor.execute(query)
        if not no_return:
            if get_tuple:
                return cursor.fetchall()
            return dict_fetch_all(cursor)
