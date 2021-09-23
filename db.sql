drop table if exists users;

create table users
(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(64) NOT NULL,
    email VARCHAR(40) NOT NULL,
    date_joined DATE NOT NULL,
    space_invaders INT NOT NULL,
    chicken_run INT NOT NULL,
    primary key (username)
);


drop table if exists scores;

create table scores
(
    score_num int NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    game VARCHAR(25) NOT NULL,
    score INT,
    date_scored DATE NOT NULL,
    primary key (score_num)
);
