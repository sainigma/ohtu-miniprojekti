create table Bookmarks (id integer primary key, title text);
create table TagTypes (id integer primary key, title text);
create table Tags (id integer primary key, bookmarkid integer, tagtypeid integer, content text);