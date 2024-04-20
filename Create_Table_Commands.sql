CREATE TABLE Households(
    hID             INTEGER PRIMARY KEY,
    netWorth        INTEGER,
    ChildrenNum     INTEGER
);


CREATE TABLE Programs(
    title       VARCHAR(45) PRIMARY KEY,
    genre       VARCHAR(25),
    duration    INTEGER
);


CREATE TABLE RecordOrders(
    title       VARCHAR(45),
    hID         INTEGER,
    PRIMARY KEY (title, hID),
    FOREIGN KEY (title) REFERENCES Programs
        ON DELETE CASCADE,
    FOREIGN KEY (hID) REFERENCES Households
        ON DELETE CASCADE,
);

CREATE TABLE RecordReturns(
    title       VARCHAR(45),
    hID         INTEGER,
    PRIMARY KEY (title, hID),
    FOREIGN KEY (title) REFERENCES Programs
        ON DELETE CASCADE,
    FOREIGN KEY (hID) REFERENCES Households
        ON DELETE CASCADE,
);

CREATE TABLE ProgramRanks(
    title       VARCHAR(45),
    hID         INTEGER,
    rank        INTEGER,
    PRIMARY KEY (title, hID),
    FOREIGN KEY (title) REFERENCES Programs
        ON DELETE CASCADE,
    FOREIGN KEY (hID) REFERENCES Households
        ON DELETE CASCADE,
    CHECK(1<=rank AND rank<=5)
);

