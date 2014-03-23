drop table if exists posts;
drop table if exists users;

create table posts (
    id integer primary key autoincrement, 
    title text not null,
    content text not null,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table users (
    id integer primary key autoincrement,
    username text not null,
    pw_hash text not null,
    token text default null,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
