create table users(
	id_user integer primary key autoincrement,
	user_name varchar(255) UNIQUE,
	first_name varchar(255),
	last_name varchar(255),
	phone_number varchar(255)
);

create table admins(
	id_user integer primary key autoincrement,
	user_name varchar(255) UNIQUE,
	chat_id varchar(255)
);

create table questions(
	id_quest integer primary key autoincrement,
	question varchar(255),
	user_name varchar(255),
	foreign key (user_name) references users(user_name)
);


/*insert into admins(user_name)
values
	("Admin_name");
*/

insert into users(user_name, first_name, last_name, phone_number)
values
	("User_name", "First_name", "Last_name", "8-888-888-88-88"),


insert into questions(question, user_name)
values
	("Принтер не печатает", "Ivan"),
	("Тормозит компьютер", "Ilia");
