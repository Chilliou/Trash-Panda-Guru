create table Site(
    siteID int auto_increment PRIMARY KEY,
    siteUrl varchar(255) not null,
    siteJSON json not null,
    motID int 
);

create table Mots(
    motID int auto_increment PRIMARY KEY,
    mot varchar(255) not null,
    siteID int,
    FOREIGN KEY (siteID) REFERENCES Site(siteID)
);

create table SiteMots(
    siteID int,
    motID int,
    nbOccurence int not null,
    tf float,
    idf float,
    tfidf float as (tf * idf),
    PRIMARY KEY (siteID, motID),
    FOREIGN KEY (siteID) REFERENCES Site(siteID),
    FOREIGN KEY (motID) REFERENCES Mots(motID)
);

