# py_diary テーブル設計

## setting

-   id primary key auto_increment
-   key varchar(255) unique not_null
-   value text not_null

## diary

-   id primary key auto_increment
-   created_at datetime not_null
-   updated_at datetime not_null
-   activity_log text not_null
-   comment text
-   todo text
