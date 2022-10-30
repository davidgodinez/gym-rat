--DROP TABLE [dbo].[Session], [dbo].[Machines], [dbo].[Gym_Address],[dbo].[Gym], [dbo].[Weights], [dbo].[Users] 

CREATE TABLE Users (
    User_id int PRIMARY KEY,
    User_name varchar(255),
)


CREATE TABLE Gym (
	Gym_id int PRIMARY KEY,
	Gym_name varchar(255),
	Gym_address_id varchar(255),
	Open_hours varchar(255)
)

CREATE TABLE Gym_address (
	Gym_id int FOREIGN KEY REFERENCES Gym(Gym_id),
	Street varchar(255),
	City varchar(255),
	State varchar(255),
	Zip_Code varchar(255)
)

CREATE TABLE Weights (
	Weight_id int PRIMARY KEY,
	Weight_lbs float
)

Create TABLE Machine (
	Machine_id int PRIMARY KEY,
	Machine_name varchar(255),
    Gym_id int FOREIGN KEY REFERENCES Gym(Gym_id)
)


CREATE TABLE Session (
	Gym_id int FOREIGN KEY REFERENCES Gym(Gym_id),
	Machine_id int FOREIGN KEY REFERENCES Machine(Machine_id),
	User_id int FOREIGN KEY REFERENCES Users(User_id),
	Rep_count int,
	Weight_id int FOREIGN KEY REFERENCES Weights(Weight_id),
	Reptime varchar(255)
)


-- Test Data

INSERT INTO [dbo].[Users]
	VALUES
	(1, 'David Godinez')


INSERT INTO [dbo].[Gym]
    VALUES 
    (1, '24-Hour Fitness 57', 1, 24)

INSERT INTO [dbo].[Gym_Address]
    VALUES 
    (1, '1513 W 18th St', 'Houston', 'TX', '77008')


INSERT INTO [dbo].[Weights]
    VALUES 
    (1, 25.0)

INSERT INTO [dbo].[Machine]
    VALUES 
    (1, 'Chest Flys')

