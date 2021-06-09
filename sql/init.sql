-- Standard
drop table tilt.tilt_log;
create table tilt.tilt_log
(
	id serial primary key,
	time timestamp with time zone,
	gravity int,
	temp_farenheit smallint,
	signal smallint,
	battery smallint
);
create unique index "time" on tilt.tilt_log (time);
alter table tilt.tilt_log cluster on "time";

-- Optimized for timescaleDB
drop table tilt.tilt_log;
create table tilt.tilt_log
(
	time timestamp with time zone,
	gravity int,
	temp_farenheit smallint,
	signal smallint,
	battery smallint
);

select create_hypertable('tilt.tilt_log', 'time');