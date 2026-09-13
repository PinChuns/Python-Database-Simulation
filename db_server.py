import os
import socket

END_OF_TRANSMISSION = chr(4)

class DBServer:

    def __init__(self):
        self.storage_folder_path = os.path.join(os.getcwd(), "databases")
        os.makedirs(self.storage_folder_path, exist_ok=True)
        self.db_name = ""

        self.preserved_words = {
            "use", "create", "drop", "alter", "insert", "select",
            "update", "join", "and", "or", "delete", "where", "from",
            "into", "values", "set", "null", "on", "==", ">", "<",
            ">=", "<=", "!=", "like", "true", "false"
        }

    def check_name(self, name):
        for x in name:
            if not (x.isalnum() or x == "_"):
                return False
        return True

    def spilt_token(self, command):
        tokens = []
        temp = ""
        in_quotes = False
        i = 0
        length = len(command)
        while i < length:
            c = command[i]
            if c == "'" and not in_quotes:
                in_quotes = True
                temp = temp + c
            elif c == "'" and in_quotes:
                temp = temp + c
                tokens.append(temp)
                temp = ""
                in_quotes = False
            elif in_quotes:
                temp = temp + c
            elif c.isalnum() or c == "." or c == "_":
                temp = temp + c
            else:
                if temp != "":
                    tokens.append(temp)
                    temp = ""
                if c in (" ", "\n", "\t"):
                    pass
                elif i + 1 < length and command[i:i + 2] in ("==", "!=", ">=", "<="):
                    tokens.append(command[i:i + 2])
                    i += 1
                else:
                    tokens.append(c)
            i += 1
        if temp != "":
            tokens.append(temp)
            temp = ""
        return tokens

    def read_table(self, name):
        table = []
        if self.db_name == "":
            print("[ERROR] Unknown database")
            return table
        filepath = os.path.join(self.storage_folder_path, self.db_name, name + ".tab")
        try:
            with open(filepath, "r") as f:
                for line in f:
                    if line.strip() != "":
                        values = line.rstrip("\n").split("\t")
                        table.append(values)
        except IOError:
            print("Can not find table: " + name)
        return table

    def write_table(self, table_name, table):
        filepath = os.path.join(self.storage_folder_path, self.db_name, table_name + ".tab")
        try:
            with open(filepath, "w") as f:
                for row in table:
                    f.write("\t".join(row))
                    f.write("\n")
        except IOError as e:
            print("Cannot write table: " + str(e))

    # command

    def use_command(self, command):
        if len(command) != 3:
            return "[ERROR] Error SQL syntax"
        db_candidate = command[1]
        if db_candidate.lower() in self.preserved_words:
            return "[ERROR] Can not use preserved word as database name"
        db_path = os.path.join(self.storage_folder_path, db_candidate)
        if os.path.isdir(db_path):
            self.db_name = db_candidate
            return "[OK]"
        else:
            return "[ERROR] Database does not exist"

    def create_command(self, command):
        # CREATE DATABASE name;
        # CREATE TABLE name (col1, col2, ...);
        if len(command) < 4:
            return "[ERROR] Error SQL syntax"

        create_type = command[1].lower()

        if create_type == "database":
            db_name = command[2]
            if not self.check_name(db_name):
                return "[ERROR] Invalid database name"
            db_path = os.path.join(self.storage_folder_path, db_name)
            if os.path.isdir(db_path):
                return "[ERROR] Database already exists"
            os.makedirs(db_path)
            return "[OK]"

        elif create_type == "table":
            if self.db_name == "":
                return "[ERROR] Unknown database"
            table_name = command[2]
            if not self.check_name(table_name):
                return "[ERROR] Invalid table name"

            columns = ["id"]
            # CREATE TABLE name;
            if len(command) > 4 and command[3] == "(":
                i = 4
                while i < len(command) and command[i] != ")":
                    if command[i] != ",":
                        columns.append(command[i])
                    i += 1

            filepath = os.path.join(self.storage_folder_path, self.db_name, table_name + ".tab")
            if os.path.exists(filepath):
                return "[ERROR] Table already exists"
            with open(filepath, "w") as f:
                f.write("\t".join(columns))
                f.write("\n")
            return "[OK]"

        else:
            return "[ERROR] Error SQL syntax"

    def insert_command(self, command):
        # INSERT INTO tableName VALUES ('v1', 'v2', ...) ;
        if len(command) < 6:
            return "[ERROR] Error SQL syntax"
        if self.db_name == "":
            return "[ERROR] Unknown database"
        if command[1].lower() != "into":
            return "[ERROR] Error SQL syntax"

        table_name = command[2]
        if command[3].lower() != "values":
            return "[ERROR] Error SQL syntax"
        if command[4] != "(":
            return "[ERROR] Error SQL syntax"

        values = []
        i = 5
        while i < len(command) and command[i] != ")":
            if command[i] != ",":
                v = command[i]
                if v.startswith("'") and v.endswith("'") and len(v) >= 2:
                    v = v[1:-1]
                values.append(v)
            i += 1

        table = self.read_table(table_name)
        if not table:
            return "[ERROR] Table does not exist"

        headers = table[0]
        if len(values) != len(headers) - 1:
            return "[ERROR] Column count does not match"

        # new id
        max_id = 0
        for row in table[1:]:
            try:
                max_id = max(max_id, int(row[0]))
            except ValueError:
                pass
        new_row = [str(max_id + 1)] + values
        table.append(new_row)
        self.write_table(table_name, table)
        return "[OK]"

    def evaluate_condition(self, row, headers, condition):
        # support only one condition, EX: name == 'Bob' or age >= 18
        if len(condition) != 3:
            return False
        col_name, op, value = condition
        value = value.strip("'")

        col_index = -1
        for idx, h in enumerate(headers):
            if h.lower() == col_name.lower():
                col_index = idx
                break
        if col_index == -1:
            return False

        cell = row[col_index]

        try:
            cell_num = float(cell)
            value_num = float(value)
            is_number = True
        except ValueError:
            is_number = False

        if op == "==":
            return cell == value
        elif op == "!=":
            return cell != value
        elif op == "like":
            return value.lower() in cell.lower()
        elif is_number:
            if op == ">":
                return cell_num > value_num
            elif op == "<":
                return cell_num < value_num
            elif op == ">=":
                return cell_num >= value_num
            elif op == "<=":
                return cell_num <= value_num
        return False

    def select_command(self, command):
        # SELECT * FROM tableName ;
        # SELECT * FROM tableName WHERE col == 'value' ;
        if len(command) < 4:
            return "[ERROR] Error SQL syntax"
        if self.db_name == "":
            return "[ERROR] Unknown database"

        if command[1] != "*":
            return "[ERROR] Only 'SELECT *' is supported in this simplified version"
        if command[2].lower() != "from":
            return "[ERROR] Error SQL syntax"

        table_name = command[3]
        table = self.read_table(table_name)
        if not table:
            return "[ERROR] Table does not exist"

        headers = table[0]
        rows = table[1:]

        if len(command) > 5:
            if command[4].lower() != "where":
                return "[ERROR] Error SQL syntax"
            condition = command[5:len(command) - 1] 
            filtered = [row for row in rows if self.evaluate_condition(row, headers, condition)]
            rows = filtered

        result_lines = ["[OK]"]
        result_lines.append("\t".join(headers))
        for row in rows:
            result_lines.append("\t".join(row))
        return "\n".join(result_lines)

    def command_parser(self, tokens):
        if len(tokens) == 0:
            return "[ERROR] Error SQL syntax"
        if tokens[-1] != ";":
            return "[ERROR] missing ';'"

        command_type = tokens[0].lower()

        if command_type == "use":
            return self.use_command(tokens)
        elif command_type == "create":
            return self.create_command(tokens)
        elif command_type == "insert":
            return self.insert_command(tokens)
        elif command_type == "select":
            return self.select_command(tokens)
        else:
            return "[ERROR] Command not supported in this simplified version"

    def handle_command(self, command):
        if len(command) == 0:
            return "[ERROR] Error SQL syntax"
        tokens = self.spilt_token(command)
        return self.command_parser(tokens)

    # socket

    def blocking_listen_on(self, port_number):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", port_number))
        server_socket.listen(5)
        print("Server listening on port " + str(port_number))
        try:
            while True:
                self.blocking_handle_connection(server_socket)
        finally:
            server_socket.close()

    def blocking_handle_connection(self, server_socket):
        conn, addr = server_socket.accept()
        print("Connection established")
        try:
            buffer = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data.decode("utf-8")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    print("Received message: " + line)
                    result = self.handle_command(line)
                    conn.sendall((result + "\n" + END_OF_TRANSMISSION + "\n").encode("utf-8"))
        except Exception as e:
            print("Error handling connection: " + str(e))
        finally:
            conn.close()
            print("Client disconnected")


if __name__ == "__main__":
    server = DBServer()
    server.blocking_listen_on(8888)
