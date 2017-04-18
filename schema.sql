drop table if exists results;
create table results (
  id integer primary key autoincrement,
  pkg text not null,
  pkg1_release text not null,
  pkg1_arch text not null,
  pkg2_release text not null,
  pkg2_arch text not null,
  result text not null
);

