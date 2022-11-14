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

create table keyboards(
	id_keyboard integer primary key autoincrement,
	keyboard_name varchar(255) UNIQUE,
	button varchar(255)
);

create table instructions(
	id_instruction integer primary key autoincrement,
	instruction_name varchar(255) UNIQUE,
	docx blob,
	html blob
);

create table contacts(
	id_contact integer primary key autoincrement,
	contact varchar(255)
);

insert into admins(user_name)
values
	("AlexanderKomyakov");

insert into contacts(contact)
values
	("Контакты");

insert into users(user_name, first_name, last_name, phone_number)
values
	("User_name", "First_name", "Last_name", "8-888-888-88-88"),
	("Ivan", "First_name", "Last_name", "8-888-888-88-88"),
	("Ilia", "First_name", "Last_name", "8-888-888-88-88");


insert into questions(question, user_name)
values
	("Принтер не печатает", "Ivan"),
	("Тормозит компьютер", "Ilia");

insert into keyboards(keyboard_name, button)
values
	("admin_menu", "🤷 Юзеры'🤷 Добавить'🤷 Удалить;❓ Вопросы'❓ Удалить;🔔 Рассылка'🔕 Отключить"),
	("instruction", "Инструкция"),
	("user_menu", "✉️ Обращение в IT отдел'📖 Инструкции;📞 Контакты'♥️ Пожелания");

values
	("Инструкция", readfile('instruction/tutorialOpenVPN.html'), readfile("instruction/Инструкция_по_удаленному_подключению_OpenVPN.docx"));
