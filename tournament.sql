-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE Player(
					PlayerId SERIAL PRIMARY KEY		NOT NULL,
					FullName VARCHAR										
);



CREATE TABLE Outcome(
					Outcome varchar(4)				NOT NULL,
					Value INT						NOT NULL,
					OutcomeID SERIAL PRIMARY KEY    NOT NULL
);

INSERT INTO Outcome(Outcome, Value)
Values
					('win', 1),
					('loss',-1),
					('tie',0);


CREATE TABLE Match(
						OutcomeID INT REFERENCES Outcome,
						MatchId SERIAL 	    NOT NULL,
						PlayerId INT References Player   NOT NULL,
						PRIMARY KEY(MatchID, PlayerId) 
)
