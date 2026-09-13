# Python Database-Simulation（JAVA Database-Simulation 簡化版改寫）

將原本的 Java `DBServer` 改寫成 Python，作為 socket-based 的簡易資料庫伺服器。

## 執行方式

啟動伺服器：
```bash
python3 db_server.py
```

另開一個終端機，啟動 client 測試：
```bash
python3 db_client.py
```

## 支援的指令（簡化版）

- `CREATE DATABASE dbname;`
- `USE dbname;`
- `CREATE TABLE tablename (col1, col2, ...);`
- `INSERT INTO tablename VALUES ('v1', 'v2', ...);`
- `SELECT * FROM tablename;`
- `SELECT * FROM tablename WHERE col op value;`
  - 支援運算子：`==`、`!=`、`>`、`<`、`>=`、`<=`、`like`

## 範例

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

## 尚未實作（原 Java 版有，這裡先省略，之後可再補）

- `DROP` / `ALTER` / `UPDATE` / `DELETE` / `JOIN`
- `SELECT` 指定欄位（目前只支援 `SELECT *`）
- 多重條件（`AND` / `OR`）

## 已完成並經人工測試驗證的函式

- `check_name`：驗證資料庫/表格名稱合法性
- `spilt_token`：SQL 指令 tokenizer（含引號字串、雙字元運算子處理）
- `read_table` / `write_table`：讀寫 `.tab` 資料表檔案
- `use_command` / `create_command` / `insert_command` / `select_command`
- `command_parser` / `handle_command`：指令分派與整體流程
- Socket server（`blocking_listen_on` / `blocking_handle_connection`）
