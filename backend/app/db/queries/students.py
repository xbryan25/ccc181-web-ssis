

class StudentQueries:

    GET_STUDENT_DETAILS = "SELECT * FROM students WHERE id_number = %s"
    GET_YEAR_LEVEL_DEMOGRAPHICS = """SELECT yrlvl.year_level, 
                                        COUNT(s.year_level) AS count 
                                    FROM unnest(enum_range(NULL::year_level_enum)) AS yrlvl(year_level)
                                    LEFT JOIN students s 
                                        ON s.year_level = yrlvl.year_level
                                    GROUP BY yrlvl.year_level
                                    ORDER BY yrlvl.year_level;"""
    
    GET_GENDER_DEMOGRAPHICS = """SELECT g.gender, 
                                    COUNT(s.gender) AS count 
                                FROM unnest(enum_range(NULL::gender_enum)) AS g(gender)
                                LEFT JOIN students s 
                                    ON s.gender = g.gender
                                GROUP BY g.gender
                                ORDER BY g.gender;"""