create table if not exists role(
	id serial primary key,
	name varchar(32) unique,
	permission integer
);


create table if not exists webuser(
	id serial primary key,
	username varchar(112),
	email varchar(112),
	authenticated bool default false,
	admin_authenticated bool default false,
	public_key varchar(250) unique,
	private_key varchar(250) unique,
	restricted bool default false,
	_password varchar(225),
	role_id integer references role (id)

);

create table if not exists employee(
id serial primary key,
employee_id integer unique,
first_name varchar(200),
last_name varchar(200),
email varchar(200),
phone_number varchar(200),
hire_date timestamp,
job_id varchar(100),
salary integer,
manager_id integer,
department_id integer
);


create table if not exists notification(
	id serial primary key,
	name varchar(122) not null,
	message text not null,
	"date" timestamp not null,
	seen bool default false,
	link text,
	notification_type integer
);

/* make all sequences editable */
grant usage, select on all sequences in schema public to publicuser;



/* notification permissions */
grant insert on notification to publicuser;

/* webuser permissions */
grant update on webuser to publicuser;
grant insert on webuser to publicuser;
grant delete on webuser to publicuser;
grant select on webuser to publicuser;



GRANT SELECT on  notification, role to publicuser;
