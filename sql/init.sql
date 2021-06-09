create table tilt.tilt_log
(
	id serial primary key,
	time timestamp,
	gravity int,
	temp_farenheit smallint,
	signal smallint,
	battery smallint
);
create unique index "time" on tilt.tilt_log (time);

alter table tilt.tilt_log cluster on "time";