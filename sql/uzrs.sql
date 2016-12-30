create table uzrs (
  uuid text primary key,
  name text,
  password text,
  bio text,
  admin boolean
);

create table recipe (
  uuid text primary key,
  owner text,
  title text,
  content text,
  image text
);
