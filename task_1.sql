CREATE TABLE Orders (
  client_id INT NOT NULL,
  purchase_date DATE NOT NULL
);


INSERT INTO Orders (client_id, purchase_date) VALUES (165, '6/18/2015'), (205, '6/23/2015'), (235, '6/15/2015'), (250, '5/25/2015'), (250, '6/24/2015'), 
                                                     (250, '7/24/2015'), (251, '5/2/2015'), (251, '6/1/2015'), (251, '7/1/2015'), (253, '5/20/2015'), 
                                                     (253, '6/19/2015'), (253, '7/19/2015'), (400, '6/3/2015'), (440, '6/10/2015'), (472, '6/10/2015'), 
                                                     (527, '5/13/2015'), (527, '6/12/2015'), (527, '7/12/2015'), (611, '6/23/2015'), (641, '5/4/2015'),
                                                     (641, '7/28/2015'), (669, '6/5/2015'), (747, '5/25/2015'), (747, '6/24/2015'), (747, '7/24/2015'), 
                                                     (766, '6/21/2015'), (781, '6/29/2015'), (827, '6/9/2015'), (886, '5/2/2015'), (886, '6/1/2015');


/*1. Новые торговые точки*/
SELECT 
    DATE_TRUNC('month', b.purchase_date) month_time, 
    COUNT(DISTINCT b.client_id) new_clients
FROM 
    Orders a 
FULL OUTER JOIN
    Orders b ON a.client_id = b.client_id
        AND DATE_TRUNC('month', a.purchase_date) = DATE_TRUNC('month', b.purchase_date) - interval '1 month'
WHERE
	a.client_id IS NULL
GROUP BY
    DATE_TRUNC('month', b.purchase_date);
    

/*2. Торговые точки, сделавшие заказ в прошлом месяце и в этом*/
SELECT 
    DATE_TRUNC('month', a.purchase_date) month_time, 
    COUNT(DISTINCT a.client_id) retained_clients
FROM 
    Orders a 
JOIN 
    Orders b ON a.client_id = b.client_id
        AND DATE_TRUNC('month', a.purchase_date) = DATE_TRUNC('month', b.purchase_date) + interval '1 month'
GROUP BY
    DATE_TRUNC('month', a.purchase_date);


/*3. Торговые точки, которые когда-то что-то заказали(только не в прошлом месяце) и вернувшиеся*/
SELECT
	b.client_id client_id,
    DATE_TRUNC('month', b.purchase_date) month_date
INTO clients_churns
FROM 
    Orders a 
FULL OUTER JOIN
    Orders b ON a.client_id = b.client_id
        AND DATE_TRUNC('month', a.purchase_date) = DATE_TRUNC('month', b.purchase_date) + interval '1 month'
WHERE 
    a.client_id IS NULL
GROUP BY
    DATE_TRUNC('month', b.purchase_date),
    b.client_id;


SELECT 
    DATE_TRUNC('month', a.purchase_date) month_date,
    COUNT(DISTINCT A.client_id) returned_clients
FROM 
	Orders a
JOIN 
	clients_churns b 
    ON a.client_id = b.client_id AND DATE_TRUNC('month', a.purchase_date) > b.month_date
GROUP BY 
	DATE_TRUNC('month', a.purchase_date);
    
    
/*4. Торговые точки, отвалившиеся в этом месяце*/
SELECT 
    DATE_TRUNC('month', b.purchase_date) month_time, 
    COUNT(DISTINCT b.client_id) churned_clients
FROM 
    Orders a 
FULL OUTER JOIN
    Orders b ON a.client_id = b.client_id
        AND DATE_TRUNC('month', a.purchase_date) = DATE_TRUNC('month', b.purchase_date) + interval '1 month'
WHERE 
    a.client_id IS NULL
GROUP BY
    DATE_TRUNC('month', b.purchase_date);