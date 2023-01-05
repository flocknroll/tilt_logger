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
create extension timescaledb;

drop table tilt.tilt_log;
create table tilt.tilt_log
(
	time timestamp with time zone not null,
	gravity int,
	temp_farenheit smallint,
	signal smallint,
	battery smallint
);

select create_hypertable('tilt.tilt_log', 'time');

grant all on table tilt.tilt_log to tilt;