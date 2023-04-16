drop table if exists Marketing_team CASCADE;
drop table if exists Agent_Works_with CASCADE;
drop table if exists Traveler_Advise CASCADE;
drop table if exists Report_to CASCADE;
drop table if exists Makes_Travel_order CASCADE;
drop table if exists Involved_in CASCADE;
drop table if exists Associated_with CASCADE;
drop table if exists Location CASCADE;
drop table if exists Transport CASCADE;
drop table if exists Hotel CASCADE;
drop table if exists Trip_details CASCADE;
drop table if exists Travel_order_consists_of_Trip_details CASCADE;
drop table if exists Offers_Travel_plans CASCADE;



create table Marketing_team(
SSN	 char(11) primary key,
Name varchar(128),
Contact	varchar(128) 	
);

  
create table Agent_Works_with(
SSN	 	char(11),
Name	varchar(128),
Contact	varchar(128),
Marketing_team_SSN char(11),
primary key(SSN),
foreign key(Marketing_team_SSN) references Marketing_team(SSN)
);

Create table Traveler_Advise(
SSN	 char(11)	 primary key,
Name varchar(128),
Contact	varchar(128),
Agent_SSN char(11) not null,
Marketing_team_SSN char(11),
foreign key (Agent_SSN) references Agent_Works_with(SSN)	 	
);
  

create table Report_to(
Supervisor_SSN		char(11),
Subordinate_SSN		char(11),		
primary key (Supervisor_SSN, Subordinate_SSN),
foreign key (Supervisor_SSN) references Agent_Works_with(SSN),
foreign key (Subordinate_SSN) references Agent_Works_with(SSN)
);

create table Makes_Travel_order(
Order_id varchar(128),
Travel_year varchar(128),
Travel_month varchar(128),
Agent_SSN char(11) not null,
primary key(Order_id),
foreign key(Agent_SSN) references Agent_Works_with(SSN)
);
 

create table Involved_in(
Traveler_SSN char(11),
Order_id varchar(128),
primary key (Traveler_SSN, Order_id),
foreign key (Order_id) references Makes_Travel_order(Order_id),
foreign key (Traveler_SSN) references Traveler_Advise(SSN)
);



create table Associated_with(
Association_id varchar(128),
Marketing_team_SSN     char(11),
Traveler_SSN	 char(11),
primary key(Marketing_team_SSN, Traveler_SSN),
foreign key(Marketing_team_SSN) references Marketing_team(SSN),
foreign key(Traveler_SSN) references Traveler_Advise(SSN)
);



create table Location(
Country varchar(128),
City varchar(128),
primary key(Country, City)
);

create table Transport(
Ticket_no varchar(128)		primary key,
Transportation_mode varchar(128),
Travelling_to_city varchar(128),
Travelling_from_city varchar(128),
Travelling_to_country varchar(128),
Travelling_from_country varchar(128),
Fare_in_usd integer
);

create table Hotel (
Registration_no varchar(128) 	primary key,
Name varchar(128),
Room_type varchar(128),
City varchar(128),
Country varchar(128),
Rating integer,
Price_in_usd integer
);


create table Trip_details(
Location_country varchar(128),
Location_city varchar(128),
Transport_Ticket_no varchar(128),
Hotel_Registration_no varchar(128),
primary key(Location_country, Location_city, Transport_Ticket_no, Hotel_Registration_no),
foreign key(Location_country, Location_city) references Location(Country, City),
foreign key(Transport_Ticket_no) references Transport(Ticket_no),
foreign key(Hotel_Registration_no) references Hotel(Registration_no)
);



create table Travel_order_consists_of_Trip_details(
Travel_order_Order_id varchar(128),
Location_city varchar(128),
Location_country varchar(128),
Transport_Ticket_no varchar(128),
Hotel_Registration_no varchar(128),

primary key(Travel_order_Order_id, Location_Country, Location_city, Transport_Ticket_no, Hotel_Registration_no),

foreign key(Location_Country, Location_city, Transport_Ticket_no, Hotel_Registration_no) references Trip_details(Location_Country, Location_city, Transport_Ticket_no, Hotel_Registration_no),

foreign key(Travel_order_order_id) references Makes_Travel_order(Order_id)
);


create table Offers_Travel_plans(
Travel_plan_id	varchar(128)	primary key,
City varchar(128), 
Country varchar(128), 
Festival varchar(128), 
Festival_month varchar(128),
Marketing_team_SSN 	char(11),
Foreign key(Marketing_team_SSN) references Marketing_team(SSN)
);