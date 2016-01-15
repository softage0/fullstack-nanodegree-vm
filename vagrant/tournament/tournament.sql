-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE players ( name TEXT,
                     id SERIAL PRIMARY KEY);

CREATE TABLE matches ( winner INTEGER REFERENCES players(id),
                     loser INTEGER REFERENCES players(id),
                     draw INTEGER REFERENCES players(id),
                     id SERIAL PRIMARY KEY);

CREATE VIEW wins AS
SELECT players.id, count(matches.winner)
FROM players LEFT JOIN matches
ON players.id = matches.winner
GROUP BY players.id;
