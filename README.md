# Python Database-Simulation（JAVA Database-Simulation Simplified Rewrite）

Reimplemented the original Java `DBServer` in Python as a simple socket-based database server.

## How to Run

Start the Server：
```bash
python3 db_server.py
```

Open Another Terminal and Start the Client for Testing：
```bash
python3 db_client.py
```

## Supported Commands (Simplified Version)

- `CREATE DATABASE dbname;`
- `USE dbname;`
- `CREATE TABLE tablename (col1, col2, ...);`
- `INSERT INTO tablename VALUES ('v1', 'v2', ...);`
- `SELECT * FROM tablename;`
- `SELECT * FROM tablename WHERE col op value;`
  - Supported Operation：`==`、`!=`、`>`、`<`、`>=`、`<=`、`like`

## Examplte

```
SQL:> CREATE DATABASE school;
[OK]
SQL:> USE school;
[OK]
SQL:> CREATE TABLE student (name, age);
[OK]
SQL:> INSERT INTO student VALUES ('Alice', '20');
[OK]
SQL:> SELECT * FROM student WHERE age >= 18;
[OK]
id	name	age
1	Alice	20
```

## Not Yet Implemented (Available in the Original Java Version)

- `DROP` / `ALTER` / `UPDATE` / `DELETE` / `JOIN`
- `SELECT` 指定欄位（目前只支援 `SELECT *`）
- 多重條件（`AND` / `OR`）

## Implemented and Tested Functions

- `check_name`：驗證資料庫/表格名稱合法性
- `spilt_token`：SQL 指令 tokenizer（含引號字串、雙字元運算子處理）
- `read_table` / `write_table`：讀寫 `.tab` 資料表檔案
- `use_command` / `create_command` / `insert_command` / `select_command`
- `command_parser` / `handle_command`：指令分派與整體流程
- Socket server（`blocking_listen_on` / `blocking_handle_connection`）
