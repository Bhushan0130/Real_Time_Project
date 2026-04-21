USE e_commerce_db;

SELECT * FROM dbo.blinkit_data;

SELECT COUNT(*) FROM dbo.blinkit_data;


SELECT DISTINCT(Item_Fat_Content) FROM DBO.blinkit_data;
-- Found different entries for same type
-- Updation for Item Fat_content

UPDATE dbo.blinkit_data
SET Item_Fat_Content = 
CASE 
	WHEN Item_Fat_Content in ('low fat', 'LF') THEN 'Low Fat'
	WHEN Item_Fat_Content  = 'reg' THEN 'Regular'
	ELSE Item_Fat_Content
	END

SELECT DISTINCT(Item_Fat_Content) FROM DBO.blinkit_data;

---------------------------------------------------------------------
-- 1. Total Sales: The overall revenue generated from all items sold

SELECT CAST ( SUM(sales)/1000000 AS decimal(10,2)) AS TOTAL_SALES_Millions
FROM DBO.blinkit_data;  

---------------------------------------------------
-- 2. Average sales: The average revenue per sale
SELECT CAST ( AVG(sales) AS decimal(10,2)) AS TOTAL_SALES_Millions
FROM DBO.blinkit_data;  
--------------------------------------------------------------------

-- 3. Number of items: The total count of different item sold.

SELECT COUNT(Item_Type) FROM DBO.blinkit_data;
------------------------------------------------------

-- Total Sales by Fat Content.

SELECT Item_Fat_Content,
CONCAT (CAST(SUM(Sales)/1000 AS decimal(10,2)), 'K' ) AS TOTAL_SALES ,
CAST(AVG(Sales)AS decimal(10,2)  ) AS AVG_SALES ,
CAST(AVG(Rating) AS decimal(10,2)) AS AVG_RATING ,
COUNT(Item_Type) AS ITEM_COUNT
FROM DBO.blinkit_data
GROUP BY Item_Fat_Content
ORDER BY SUM(Sales) DESC;

-- Total sales by item type
SELECT TOP 5 Item_Type,
CONCAT (CAST(SUM(Sales)/1000 AS decimal(10,2)), 'K' ) AS TOTAL_SALES ,
CAST(AVG(Sales)AS decimal(10,2)  ) AS AVG_SALES ,
CAST(AVG(Rating) AS decimal(10,2)) AS AVG_RATING ,
COUNT(Item_Type) AS ITEM_COUNT
FROM DBO.blinkit_data
GROUP BY Item_Type
ORDER BY SUM(Sales) DESC;


-- FAT CONTENT BY OUTLT FOR TOTAL SALES

SELECT Item_Fat_Content, Outlet_Type,
CONCAT (CAST(SUM(Sales)/1000 AS decimal(10,2)), 'K' ) AS TOTAL_SALES ,
CAST(AVG(Sales)AS decimal(10,2)  ) AS AVG_SALES ,
CAST(AVG(Rating) AS decimal(10,2)) AS AVG_RATING ,
COUNT(Item_Type) AS ITEM_COUNT
FROM DBO.blinkit_data
GROUP BY Item_Fat_Content, Outlet_Type
ORDER BY SUM(Sales) DESC;


-- FAT CONTENT BY OUTLET FOR TOTAL SALES
SELECT * FROM DBO.blinkit_data;

SELECT Outlet_Location_Type, 
SUM(CASE 
	WHEN Item_Fat_Content = 'Regular' 
	THEN Sales 
	ELSE 0 END)  AS Regular_Set,

SUM(CASE 
	WHEN Item_Fat_Content = 'Low Fat'
	THEN Sales
	ELSE 0 END) AS Low_Fat

FROM DBO.blinkit_data
GROUP BY Outlet_Location_Type;


-- TOTAL SALES BY OUTLET ESTABLISHMENT

SELECT Outlet_Establishment_Year,
	CAST(SUM(Sales) AS DECIMAL (10,2)) AS TOTAL_SALES,
	CAST(AVG(Sales) AS DECIMAL (10,1)) AS TOTAL_SALES,
	COUNT(*) AS No_of_items,
	CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating
FROM DBO.blinkit_data
GROUP BY Outlet_Establishment_Year;

-- PERCENTAGE OF SALES BY OUTLET SIZE
SELECT * FROM DBO.blinkit_data

SELECT Outlet_Size,
		CAST(SUM(sales) AS DECIMAL(10,2)) AS TOTAL_SALES,
		CAST ((SUM(Sales) * 100.0 / SUM(SUM(Sales)) OVER()) AS decimal(10,2)) AS  Sales_Percentage

FROM DBO.blinkit_data
GROUP BY Outlet_Size ORDER BY TOTAL_SALES DESC;
