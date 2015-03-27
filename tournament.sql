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

CREATE TABLE Round(
					RoundId SERIAL PRIMARY KEY		NOT NULL,
					RoundNum INT 			NOT NULL
);

CREATE TABLE Match(
					MatchId SERIAL PRIMARY KEY		NOT NULL,
					RoundId	INT REFERENCES Round	NOT NULL
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


CREATE TABLE PlayerMatch(
						OutcomeID INT REFERENCES Outcome 	NOT NULL,
						MatchId SERIAL REFERENCES Match	    NOT NULL,
						PlayerId SERIAL References Player   NOT NULL
)
