

class CommonQueries:

    INSERT = "INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    GET_TOTAL_COUNT = "SELECT COUNT(*) FROM {table}"
    GET_BY_ID = "SELECT * FROM {table} WHERE {pk} = %s LIMIT 1"
    GET_ALL = "SELECT * FROM {table}"
    GET_MANY = "SELECT * FROM {table} WHERE {search_by} LIKE %s ORDER BY {sort_field} {sort_order} LIMIT %s OFFSET %s"
    UPDATE_BY_ID = "UPDATE {table} SET {set_clause} WHERE {pk} = %s"
    DELETE_BY_ID = "DELETE FROM {table} WHERE {pk} = %s"
    GET_ALL_IDS = "SELECT {pk} FROM {table} ASCENDING"
 