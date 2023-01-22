CREATE VIEW Ever_Ordered
AS
SELECT DISTINCT title,hID FROM  (SELECT *
FROM RecordOrders UNION SELECT * FROM RecordReturns) AS EVER_ORDERED;

GO

CREATE VIEW More_Than_3_Legal_Rates
AS
SELECT PR.title,COUNT(rank) AS Ranking_Times FROM ProgramRanks PR JOIN Ever_Ordered EO ON PR.title=EO.title AND PR.hID=EO.hID
GROUP BY PR.title
HAVING COUNT(rank)>=3;

GO

CREATE VIEW Average_Rank
AS
SELECT DISTINCT title, CAST(AVG(CAST(rank AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS rank
FROM ProgramRanks
GROUP BY title;

GO

CREATE VIEW High_Level_Program
AS
SELECT MN.title FROM (SELECT title,COUNT(hID) AS Number_Of_Returns FROM RecordReturns
                                             GROUP BY title HAVING COUNT(hID)>9) AS MN
JOIN (SELECT title,COUNT(RF.hID) AS RICH_RATED FROM RecordReturns RN JOIN (SELECT hID FROM Households WHERE netWorth>7) AS RF
    ON RN.hID=RF.hID
GROUP BY title) AS RR ON MN.title=RR.title WHERE RICH_RATED*2>Number_Of_Returns;

GO

CREATE VIEW FamilyNumOfOrders
AS
SELECT H.hID,COUNT(title) AS NumberOfOrders
FROM
    RecordOrders R
        JOIN
        Households H
            ON R.hID = H.hID
GROUP BY H.hID;

GO

CREATE VIEW HouseHoldsZeroChildren
AS
SELECT hID FROM Households WHERE ChildrenNum=0;


