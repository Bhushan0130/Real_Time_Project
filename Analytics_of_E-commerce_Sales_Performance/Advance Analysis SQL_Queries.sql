create database e_commerce_db;
use e_commerce_db;

select count(*) from dbo.sku_detail_tbl;

/*
In 2021, In which month was the highest total transaction value (after_discount) recorded?
Note: is_valid = not canceled or actual transaction  
*/

select * from dbo.order_detail_tbl;

select MONTH(order_date) as month_name,
		sum(after_discount) as sum_transaction
from dbo.order_detail_tbl
where year(order_date) = 2021 and is_valid = 1
group by month(order_date) 
order by sum(after_discount) desc;

-- Answer: Auguest has the highest total transaction with 227 Million


/*
2. In 2022, which category generated the highest transaction value?
*/

select sd.category,
		round(sum(od.after_discount),2) as total_sum
from dbo.order_detail_tbl as od
left join dbo.sku_detail_tbl as sd
on od.sku_id = sd.id
where year(od.order_date) = 2022 and od.is_valid = 1
group by sd.category order by sum(od.after_discount) desc;

--Answer:Mobile & tablets cateogy generated 918 Million transactions


/*
Campare transaction values for each category in 2021 and 2022.
Identify categoration with increased or decreased transactions value from 2021 and 2022
*/

select * from dbo.sku_detail_tbl;

with transaction_record_2021 as 
( 
select sd.category,
		round(sum(od.after_discount),2) as sum_total_2021
from dbo.order_detail_tbl as od 
left join dbo.sku_detail_tbl as sd
on od.sku_id = sd.id
where od.is_valid =1 and year(od.order_date)=2021
group by sd.category
), 
transaction_record_2022 as 
( 
select sd.category,
		round(sum(od.after_discount),2) as sum_total_2022
from dbo.order_detail_tbl as od 
left join dbo.sku_detail_tbl as sd
on od.sku_id = sd.id
where od.is_valid =1 and year(od.order_date)=2022
group by sd.category
)

select t1.category, 
t1.sum_total_2021, 
t2.sum_total_2022 ,
case 
	when t2.sum_total_2022 > t1.sum_total_2021 then 'Increased'
	else 'Decreased'
end as Status_col
from transaction_record_2021 t1
left join transaction_record_2022 t2
on t1.category = t2.category 


-- Fasted approch
select * from dbo.sku_detail_tbl;
select * from dbo.order_detail_tbl;


select sd.category, 
	sum(case when year(od.order_date) = 2021 then od.after_discount end) as transaction_2021,
	sum(case when year(od.order_date) = 2022 then od.after_discount end) as transaction_2022,
	case
		when sum(case when year(od.order_date) = 2022 then od.after_discount end)>
			sum(case when year(od.order_date) = 2021 then od.after_discount end)
			then 'Increased' else 'Decreased' end as comparision_col
from dbo.order_detail_tbl od
left join dbo.sku_detail_tbl sd
on od.sku_id = sd.id
where od.is_valid = 1
group by sd.category;


/* 
Show the top 5 most popular payment methods used in 2022 
(based on total unique orders).
*/

select * from dbo.payment_detail_tbl;
select * from dbo.order_detail_tbl;

select top 5 pd.payment_method, count(od.payment_id) as Record_count
from dbo.order_detail_tbl as od
left join dbo.payment_detail_tbl as pd
on od.payment_id = pd.id
where od.is_valid = 1 and year(order_date) =2022
group by pd.payment_method
order by count(od.payment_id) desc;

-- COD  with 1591 

/* 
Rank the following 5 products by transaction value: Samsung, Apple, 
Sony, Huawei, and Lenovo
*/

select * from dbo.order_detail_tbl;
select * from dbo.sku_detail_tbl;


with product_table as (
select * , 
case 
	when lower(sku_name) like '%samsumg%' then 'Samsung'
	when lower(sku_name) like '%apple%' then 'Apple'
	when lower(sku_name) like '%macbook%' then 'Apple'
	when lower(sku_name) like '%sony%' then 'Sony'
	when lower(sku_name) like '%lenovo%' then 'Lenovo'
	when lower(sku_name) like '%iphone%' then 'Apple'
	when lower(sku_name) like '%huawei%' then 'Huawei'
	else 'Other'
	end  as Product_Name
from dbo.sku_detail_tbl
)

select pt.Product_Name,
		sum(od.after_discount) as transaction_sum
from dbo.order_detail_tbl od 
left join product_table as pt
on od.sku_id  = pt.id
where pt.Product_Name <> 'Other' and od.is_valid = 1
group by pt.Product_Name 
order by sum(od.after_discount) desc;


/* Bringing Data all together  */


SELECT 
    od.id AS order_id,
    od.customer_id,
    od.order_date,
    od.price,
    sd.cogs,
	sd.base_price,
    pd.payment_method,
    sd.sku_name,
    sd.category,
    od.qty_ordered,
    od.before_discount,
    ISNULL(od.discount_amount, 0) AS discount_amount,
    od.after_discount,
    od.is_gross,
    od.is_valid,
    od.is_net,

    CASE 
        WHEN LOWER(sd.sku_name) LIKE '%samsung%' THEN 'Samsung'
        WHEN LOWER(sd.sku_name) LIKE '%apple%' 
          OR LOWER(sd.sku_name) LIKE '%iphone%' 
          OR LOWER(sd.sku_name) LIKE '%macbook%' THEN 'Apple'
        WHEN LOWER(sd.sku_name) LIKE '%sony%' THEN 'Sony'
        WHEN LOWER(sd.sku_name) LIKE '%huawei%' THEN 'Huawei'
        WHEN LOWER(sd.sku_name) LIKE '%lenovo%' THEN 'Lenovo'
        ELSE 'Other'
    END AS brand_name
into e_commerce_db.dbo.ecommerce_sales_data

FROM dbo.order_detail_tbl od
INNER JOIN dbo.payment_detail_tbl pd
    ON od.payment_id = pd.id
INNER JOIN dbo.sku_detail_tbl sd
    ON od.sku_id = sd.id;
