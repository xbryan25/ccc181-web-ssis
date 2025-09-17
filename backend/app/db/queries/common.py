

class CommonQueries:

    INSERT = "INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    GET_BY_ID = "SELECT * FROM {table} WHERE {pk} = %s LIMIT 1"
    GET_ALL = "SELECT * FROM {table}"
    UPDATE_BY_ID = "UPDATE {table} SET {set_clause} WHERE {pk} = %s"
    DELETE_BY_ID = "DELETE FROM {table} WHERE {pk} = %s"
