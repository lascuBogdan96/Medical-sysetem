-- drop database hw;
create database hw;
use hw;

create table sect(
    id int auto_increment not null,
    name varchar(20) not null,
    primary key (id)
) engine=innodb;

create table doct(
    id int auto_increment not null,
    name varchar(30) not null,
    email varchar(50),
    telephone varchar(15),
    section int,

    index par_ind (section),
    foreign key (section) references sect(id) on delete cascade,
    primary key(id)
) engine=innodb;

create table pat(
    id int auto_increment not null,
    name varchar(30) not null,
    age int,
    email varchar(50),
    telephone varchar(15),
    reason varchar(1000),
    date_arrival datetime default now(),
    doctor int not null,

    index par_ind (doctor),
    foreign key (doctor) references doct(id) on delete cascade,
    primary key(id)
) engine=innodb;


create table hist(
    id int auto_increment not null,
    action varchar(10) not null,
    patient_name varchar(30) not null,
    doctor int not null,
    money int default 0,
    actdate datetime,

    index par_ind (doctor),
    foreign key (doctor) references doct(id) on delete cascade,

    primary key(id)
) engine=innodb;

create table daygrade(
    loday int not null,
    hiday int not null,
    score int not null
) engine=innodb;

insert into daygrade(loday, hiday, score) values(0, 0, 100);
insert into daygrade(loday, hiday, score) values(1, 3, 200);
insert into daygrade(loday, hiday, score) values(4, 6, 250);
insert into daygrade(loday, hiday, score) values(7, 10, 330);
insert into daygrade(loday, hiday, score) values(11, 15, 500);
insert into daygrade(loday, hiday, score) values(16, 31, 700);

delimiter $$
create procedure insert_doct(in name_in varchar(30), in email_in varchar(50), in telephone_in varchar(15), in section_in int)
begin
    insert into doct(name, email, telephone, section) values(name_in, email_in, telephone_in, section_in);
end$$
 
create procedure insert_pat(in name_in varchar(30), in age_in int, in email_in varchar(50), in telephone_in varchar(15), in reason_in varchar(1000), in date_arrival_in datetime, in doctor_in int)
begin
    insert into pat(name, age, email, telephone, reason, date_arrival, doctor) values(name_in, age_in, email_in, telephone_in, reason_in, date_arrival_in, doctor_in);
end$$

create procedure delete_pat(in id_in int)
begin
    delete from pat where id = id_in;
end$$

create procedure get_history()
begin
    select hist.action 'ACTION', hist.patient_name 'PATIENT NAME', doct.name 'DOCTOR NAME', sect.name 'SECTION', money 'MONEY', date(actdate) 'DATE'  
        from hist, doct, sect 
        where hist.doctor = doct.id and doct.section = sect.id
        order by actdate;
end$$

create function get_doct_name(doctor_in int)
returns varchar(30)
begin
    declare name_out varchar(30);
    select name into name_out from doct where id = doctor_in;
    return name_out;
end$$

create function get_doct_sect(doctor_in int)
returns varchar(30)
begin
    declare name_out varchar(30);
    select sect.name into name_out from sect, doct where doct.id = doctor_in and doct.section = sect.id;
    return name_out;
end$$

create procedure get_doct_pats(in doctor_in int)
begin
    select concat('The name of the doctor is ', get_doct_name(doctor_in), ' and is in the section ' , get_doct_sect(doctor_in)) '';
    
    select pat.id 'ID', pat.name 'NAME', pat.age 'AGE', pat.email 'EMAIL', pat.telephone 'TELEPHONE', pat.reason 'REASON', pat.date_arrival 'DATE', calc_money(sect.id, pat.date_arrival) 'MONEY'
    from pat, doct, sect
    where pat.doctor = doctor_in and doct.id = doctor_in and sect.id = doct.section;
end$$

create function calc_money(section int, date_arrival datetime)
returns int 
begin
    declare diff_days int;
    declare result int default 0;
    declare score2 int;

    set diff_days = day(now()) - day(date_arrival);
    select score into score2 from daygrade where diff_days >= loday and diff_days <= hiday;
    set result = score2 / 1.5;

    -- La chirurgie se plateste mai mult.
    if (section = 2) then
        set result = result * 1.2;
    end if;

    return result;
end$$

create trigger hist_update_on_insert
    before insert on pat
    for each row
begin
    insert into hist(action, patient_name, doctor, actdate)
    values('Internare', new.name, new.doctor, new.date_arrival);
end$$

create trigger hist_update_on_delete
    before delete on pat
    for each row
begin
    declare section2 int;
    set section2 = (select doct.section from doct, pat where pat.doctor = doct.id and pat.id = old.id);
    insert into hist(action, patient_name, doctor, money, actdate)
    values('Externare', old.name, old.doctor, calc_money(section2, old.date_arrival), now());
end$$

delimiter ;

insert into sect(name) values('General');
insert into sect(name) values('Chirurgie');
insert into sect(name) values('Paliatii');
insert into sect(name) values('Pediatrie');

insert into doct(name, email, telephone, section) values('Bogdan', 'bogdan@gmail.com', '0733367741', 1);
insert into doct(name, email, telephone, section) values('Mihai', 'mihai@gmail.com', '0733111234', 1);
insert into doct(name, email, telephone, section) values('Mihaela', 'mihaela@gmail.com', '0733335541', 2);
insert into doct(name, email, telephone, section) values('Georgeta', 'georgeta@gmail.com', '0733411307', 2);
insert into doct(name, email, telephone, section) values('Razvan', 'razvan@gmail.com', '0733111071', 3);
insert into doct(name, email, telephone, section) values('Maria', 'maria@gmail.com', '0736116736', 3);
insert into doct(name, email, telephone, section) values('Daniel', 'daniel@gmail.com', '0736022337', 3);
insert into doct(name, email, telephone, section) values('Alexandra', 'alexandra@gmail.com', '0733353734', 4); 
call insert_doct('Cristi', 'cristi@gmail.com', '0734675987', 4);

insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient0',  30, 'patient0@gmail.com',  '0722006611', 'Sunt bolnav', 1, str_to_date('04-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient1',  33, 'patient1@gmail.com',  '0722367752', 'Sunt bolnav', 2, str_to_date('06-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient2',  36, 'patient2@gmail.com',  '0726567674', 'Sunt bolnav', 4, str_to_date('07-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient3',  4,  'patient3@gmail.com',  '0726674141', 'Sunt bolnav', 9, str_to_date('03-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient4',  39, 'patient4@gmail.com',  '0773640731', 'Sunt bolnav', 8, str_to_date('06-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient5',  37, 'patient5@gmail.com',  '0773641226', 'Sunt bolnav', 4, str_to_date('08-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient6',  42, 'patient6@gmail.com',  '0722111517', 'Sunt bolnav', 2, str_to_date('03-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient7',  44, 'patient7@gmail.com',  '0726654464', 'Sunt bolnav', 3, str_to_date('02-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient8',  47, 'patient8@gmail.com',  '0722141362', 'Sunt bolnav', 4, str_to_date('04-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient9',  41, 'patient9@gmail.com',  '0726031136', 'Sunt bolnav', 5, str_to_date('03-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient10', 27, 'patient10@gmail.com', '0726031136', 'Sunt bolnav', 2, str_to_date('06-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient11', 23, 'patient11@gmail.com', '0722141246', 'Sunt bolnav', 5, str_to_date('05-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient12', 23, 'patient12@gmail.com', '0725023450', 'Sunt bolnav', 6, str_to_date('01-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient13', 58, 'patient13@gmail.com', '0732737120', 'Sunt bolnav', 2, str_to_date('07-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient14', 50, 'patient14@gmail.com', '0725722051', 'Sunt bolnav', 1, str_to_date('03-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient15', 35, 'patient15@gmail.com', '0722263302', 'Sunt bolnav', 7, str_to_date('08-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient16', 30, 'patient16@gmail.com', '0722131761', 'Sunt bolnav', 3, str_to_date('02-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient17', 29, 'patient17@gmail.com', '0727047401', 'Sunt bolnav', 2, str_to_date('03-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient18', 22, 'patient18@gmail.com', '0725434326', 'Sunt bolnav', 3, str_to_date('06-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient19', 25, 'patient19@gmail.com', '0725110240', 'Sunt bolnav', 6, str_to_date('03-01-2019', '%d-%m-%Y'));
insert into pat(name, age, email, telephone, reason, doctor, date_arrival) values ('Patient20', 24, 'patient20@gmail.com', '0722235544', 'Sunt bolnav', 4, str_to_date('06-01-2019', '%d-%m-%Y'));
call insert_pat('Patient21', 27, 'patient21@gmail.com', '0729035524', 'Sunt bolnav', str_to_date('07-01-2019', '%d-%m-%Y'), 3);

delete from pat where name = 'Patient1';
delete from pat where name = 'Patient9';
delete from pat where name = 'Patient10';
delete from pat where name = 'Patient17';
call delete_pat(3);

call get_history();

call get_doct_pats(4);
