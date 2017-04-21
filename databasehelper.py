# -*- coding: utf-8 -*-
import os
import sqlite3
from flask import Flask, g
from contextlib import closing
from server import *  # cross import, but ok here


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request.
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def query_db(query, args=(), one=False):
    """
    Query helper function.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_courses_from_profile(profile):
    query = ('SELECT B.course_code, B.course_name, B.advancement_level, B.credits, CP_A.required FROM Profile A '
             'INNER JOIN Course_Profile CP_A ON CP_A.profile = A.id '
             'INNER JOIN Course B ON CP_A.course = B.id '
             'WHERE A.abbreviation = ?')
    return [{'course_code': course_code, 'course_name': course_name, 'advancement_level': advancement_level,
             'credits': credits, 'required': required == 1}
            for course_code, course_name, advancement_level, credits, required in query_db(query, [profile])]


def get_all_courses():
    query = "select distinct course_code, course_name, advancement_level, credits from course"
    return [{'course_code': course_code, 'course_name': course_name, 'advancement_level': advancement_level,
             'credits': credits} for course_code, course_name, advancement_level, credits in query_db(query)]


def get_courses(profile1, profile2, semester, term):
    query = ('SELECT B.course_code, B.course_name, B.advancement_level, B.credits, CP_A.required, CP_B.semester, '
             'CP_B.term, SC.schedule_code FROM Profile A INNER JOIN Course_Profile CP_A ON CP_A.profile = A.id '
             'INNER JOIN Course B ON CP_A.course = B.id INNER JOIN CoursePart CP_B ON CP_B.course = B.id '
             'INNER JOIN ScheduleCode SC ON SC.course_part = CP_B.id WHERE CP_B.semester = ? AND CP_B.term = ? '
             'AND A.abbreviation = ? or A.abbreviation = ?')

    return [{'course_code': course_code, 'course_name': course_name, 'advancement_level': advancement_level,
             'credits': credits, 'required': bool(required), 'semester': semester, 'term': term,
             'schedule_code': schedule_code}
            for course_code, course_name, advancement_level, credits, required, semester, term, schedule_code in
            query_db(query, (semester, term, profile1, profile2))]


def get_course_parts(course_code):
    query = ('SELECT course_code, course_name, semester, term, schedule_code FROM CoursePart A '
             'INNER JOIN Course B ON A.course = B.id '
             'INNER JOIN ScheduleCode C ON C.course_part = A.id '
             'WHERE B.course_code = ?')

    return [{'course_code': course_code, 'course_name': course_name, 'semester': semester, 'term': term,
             'schedule_code': schedule_code} for course_code, course_name, semester, term, schedule_code
            in query_db(query, [course_code])]


def get_course_information(course_code):
    query = (
        'SELECT course_code, course_name, credits, advancement_level, semester, term, schedule_code FROM CoursePart A '
        'INNER JOIN Course B ON A.course = B.id '
        'INNER JOIN ScheduleCode C ON C.course_part = A.id '
        'WHERE B.course_code = ?')

    return [{'course_code': course_code, 'course_name': course_name, 'semester': semester, 'term': term,
             'schedule_code': schedule_code, 'advancement_level': advancement_level, 'credits': credits}
            for course_code, course_name, credits, advancement_level, semester, term, schedule_code
            in query_db(query, [course_code])]


def get_profile_names(profile_type):
    """
    :param profile_type: Can be 'bachelor' or 'master'
    """
    query = 'SELECT name FROM Profile WHERE type=?'
    return [t[0] for t in query_db(query, [profile_type])]


def get_extensive_course_information():
    query = (
        'select course_code, course_name, advancement_level, credits, semester, term from Course '
        'inner join coursepart '
        'on course.id = coursepart.course'
    )
    course_list = query_db(query)
    return [[course[0], course[1], course[2], course[3], int(course[4] % 2 == 0), course[5]] for course in course_list]


if __name__ == '__main__':
    pass
