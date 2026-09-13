from db_server import DBServer

db = DBServer()
print(db.handle_command("CREATE DATABASE school;"))
print(db.handle_command("USE school;"))
print(db.handle_command("CREATE TABLE student (name, age);"))
print(db.handle_command("INSERT INTO student VALUES ('Alice', '20');"))
print(db.handle_command("INSERT INTO student VALUES ('Serena', '20');"))
print(db.handle_command("INSERT INTO student VALUES ('Mike', '21');"))
print(db.handle_command("INSERT INTO student VALUES ('Jason', '21');"))
print(db.handle_command("INSERT INTO student VALUES ('Tom', '20');"))
print(db.handle_command("SELECT * FROM student;"))