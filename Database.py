__author__ = 'PerArne'
import peewee as pw

import datetime

#db = pw.MySQLDatabase("mydb", host="mydb.crhauek3cxfw.us-west-2.rds.amazonaws.com", port=3306, user="user", passwd="password")
db = pw.SqliteDatabase("wee.db")

class BaseModel(pw.Model):
    class Meta:
        database = db

class Teacher(BaseModel):
    id = pw.PrimaryKeyField(primary_key=True)
    name = pw.CharField(null=False, unique=True)

class Course(BaseModel):
    id = pw.PrimaryKeyField(primary_key=True)
    name = pw.CharField(null=False)
    value = pw.CharField(null=False, unique=True)
    season = pw.CharField(null=False)
    type = pw.CharField(null=False)

    indexes = (
        (('value', 'season'), True)
    )

class Subject(BaseModel):
    id = pw.PrimaryKeyField(primary_key=True)
    date_from = pw.DateTimeField(null=False)
    date_to = pw.DateTimeField(null=False)
    activity = pw.CharField()
    room = pw.CharField()
    educator = pw.CharField()
    course = pw.ForeignKeyField(Course, related_name="course", null=False)

