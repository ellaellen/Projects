
--Table "employees"
CREATE TABLE gw_employees (
    emp_id  INT  NOT NULL AUTO_INCREMENT,
    store_id INT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    gender ENUM('M','F') ,
    birth_date DATE ,
    hire_date DATE NOT NULL,
    email VARCHAR(255),
    phonenumber VARCHAR(255),
    PRIMARY KEY (emp_id),
    FOREIGN KEY (store_id) REFERENCES gw_stores(sid),
    CONSTRAINT uq_NAME UNIQUE(first_name, last_name)
);
ALTER TABLE  'gw_employees' CHANGE  'birth_date'  'birth_date' DATE NOT NULL;

ALTER TABLE  'gw_employees' DROP INDEX  'uq_NAME',
ADD UNIQUE  'uq_NAME' ('first_name', 'last_name', 'birth_date');


--Table "stores"
CREATE TABLE gw_stores (
    sid INT NOT NULL AUTO_INCREMENT,
    manager_id INT NOT NULL,
    city VARCHAR(20),
    street VARCHAR(255),
    phonenumber VARCHAR(255),
    GST_number VARCHAR(255),
    PRIMARY KEY (sid)
    FOREIGN KEY (manager_id) REFERENCES gw_employees(emp_id)
);


--Table "employee_salary"
CREATE TABLE gw_employee_salary (
    id INT NOT NULL AUTO_INCREMENT,
    emp_id INT NOT NULL,
    SSN VARCHAR(9),
    jobtitle VARCHAR(255) NOT NULL,
    pay_type ENUM('HOUR','YEAR'),
    salary VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (emp_id) REFERENCES gw_employees(emp_id),
    CONSTRAINT uq_ID UNIQUE(emp_id)
    
);


--Table "customer"
CREATE TABLE gw_customer (
    customer_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,    
    email VARCHAR(255),
    PRIMARY KEY (customer_id),
    CONSTRAINT uq_NAME UNIQUE(first_name, last_name)
);
ALTER TABLE  'gw_customer' DROP INDEX  'uq_NAME',
ADD UNIQUE  'uq_NAME' ('first_name', 'last_name', 'birth_date');

--Table "customer_membership"
CREATE TABLE gw_customer_membership (
    cid INT NOT NULL,
    sid INT NOT NULL,
    join_date DATE NOT NULL,
    account_number VARCHAR(255) DEFAULT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (cid, sid),
    FOREIGN KEY (cid) REFERENCES gw_customer (customer_id),
    FOREIGN KEY (sid) REFERENCES gw_stores (sid)
);
   
--Table "products"
CREATE TABLE gw_products (
    product_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    supplier_id INT NOT NULL,
    unit_price FLOAT,
    quantity_instock INT,
    expire_date DATE NOT NULL,
    buy_price FLOAT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    PRIMARY KEY (product_id),
    FOREIGN KEY (supplier_id) REFERENCES gw_products_supplier (supplier_id),
    CONSTRAINT uq_NAME UNIQUE(name)
);


CREATE TABLE gw_products_withsupply (
    id INT NOT NULL AUTO_INCREMENT,
    product_id INT NOT NULL,
    supply_company INT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES gw_products(product_id),
    FOREIGN KEY (supply_company) REFERENCES gw_products_supplier (supply_id),
    CONSTRAINT uq_NAME UNIQUE(product_id)
);


--Table "supplier"
CREATE TABLE gw_products_supplier (
    supplier_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    contact_person VARCHAR(255),
    phonenumber VARCHAR(20),
    PRIMARY KEY (supplier_id)
);
ALTER TABLE  'gw_products_supplier' ADD UNIQUE ('name');

--Table "departments"
CREATE TABLE gw_departments (
    dept_id INT NOT NULL, 
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (dept_id)
);
ALTER TABLE  'gw_departments' ADD UNIQUE ('name');
ALTER TABLE  `gw_departments` CHANGE  `dept_id`  `dept_id` INT( 11 ) NOT NULL AUTO_INCREMENT; 

--TABLE "sales"
CREATE TABLE gw_sales (
    sale_id INT NOT NULL AUTO_INCREMENT,
    store_id INT NOT NULL,
    sale_date TIMESTAMP,
    payby ENUM('VISA','MASTERCARD','CASH', 'CHEQUE') NOT NULL,              
    subtotal FLOAT NOT NULL,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (store_id) REFERENCES gw_stores(sid)
);

CREATE TABLE gw_sales_withemp (
    id INT NOT NULL AUTO_INCREMENT,
    sale_id INT NOT NULL ,
    employee_id INT NOT NULL,
    customer_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (employee_id) REFERENCES gw_employees(emp_id),
    FOREIGN KEY (customer_id) REFERENCES gw_customer(customer_id),
    FOREIGN KEY (sale_id) REFERENCES gw_sales(sale_id),
    CONSTRAINT uq_sale UNIQUE(sale_id)
);


--Table "payment"
CREATE TABLE gw_sales_details (
    sid INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (sid, item_id),
    FOREIGN KEY (item_id) REFERENCES gw_products(product_id) 
);



--insert values to the tables
INSERT INTO gw_employees
VALUE 
(1,1,'ALMA','DAVIS','F','1978-02-24', '2009-05-01','ALMADAVIS@GREENWAY.COM','4033232233'),
(2,1,'KEVIN','SMITH','M','1980-08-07', '2010-02-23','KEVINSMITH@GREENWAY.COM','4032345678'),
(3,1,'TANYA','BOON','F','1978-08-30', '2012-02-25', 'TANYABOON@GREENWAY.COM', '4037893240'),
(4,1,'BOB','ADDISON','M','1970-07-05','2007-01-25', 'BOBADDISON@GREENWAY.COM','4039876540'),
(5,1,'TERRY','HOPKINS','M','1968-10-22','2003-04-13','TERRYHOPKINS@GREENWAY.COM','4031436587'),
(6,1,'BETTY','JONES','F','1980-09-22','2012-05-12','BETTYJONES@GREENWAY.COM','4038976321'),
(7,1,'STEVE','ZELLER','M','1982-12-22','2010-05-02','STEVEZELLER@GREENWAY.COM','4037874466'),
(8,1,'JACKY','ANDERSON','F','1975-03-21','2008-08-12','JACKYANDERSON@GREENWAY.COM','4032128789'),
(9,1,'CELIA','ONG','F','1977-11-08','2005-07-29','CELIAONG@GREENWAY.COM','4037778890'),
(10,1,'MICHAEL','SMITH','M','1982-02-18','2013-08-14','MICHAELSMITH@GREENWAY.COM','4033245569'),
(11,2,'VELERIE','BOYCE','F','1983-04-29','2012-07-05','VELERIEBOYCE@GREENWAY.COM','6479897230'),
(12,2,'KELLY','YOUNG','F','1990-02-10','2013-09-29','KELLYYOUNG@GREENWAY.COM','6472334564'),
(13,2,'LARRY','MACKAY','M','1965-12-29','2002-01-03','LARRYMACKAY@GREENWAY.COM','6472228790'),
(14,2,'SAM','ADAMS','M','1968-02-19','2004-11-15','SAMADAMS@GREENWAY.COM','6472314569'),
(15,2,'JENNIFER','BOYD','F','1987-03-18','2008-06-24','JENNIFERBOYD@GREENWAY.COM','6479807889'),
(16,2,'MATT','EWEN','M','1976-12-23','2001-08-13','MATTEWEN@GREENWAY.COM','6479082526'),
(17,2,'ETHAN','HOLMER','M','1985-08-01','2009-10-02','ETHANHOLMER@GREENWAY.COM','6479876999'),
(18,2,'CHRIS','BLOOM','M','1972-01-30','2001-07-21','CHRISBLOOM@GREENWAY.COM','6472217686'),
(19,2,'STELLY','WALKER','F','1980-03-16','2004-07-24','STELLYWALKER@GREENWAY.COM','6478789980'),
(20,2,'JACOB','LOPEZ','M','1979-11-20','2010-05-23','JACOBLOPEZ@GREENWAY.COM','6472829948'),
(21,3,'HEATHER','SANFORD','F','1985-04-25','2009-06-27','HEATHERSANFORD@GREENWAY.COM','2128987890'),
(22,3,'SARA','SEAMAN','F','1989-10-10','2013-08-20','SARASEAMAN@GREENWAY.COM','2123435461'),
(23,3,'JOHN','PARKER','M','1967-10-22','2002-12-02','JOHNPARKER@GREENWAY.COM','2123246657'),
(24,3,'SCOTT','COLWELL','M','1981-04-12','2003-02-09','SCOTTCOLWELL@GREENWAY.COM','2122329863'),
(25,3,'PERRY','COLLAR','M','1976-07-14','2005-10-22','PERRYCOLLAR@GREENWAY.COM','2129082890'),
(26,3,'TIFFANY','YOUNGER','F','1983-03-26','2008-07-13','TIFFANYYOUNGER@GREENWAY.COM','2129968790'),
(27,3,'EMILY','ELDER','F','1980-10-2','2006-02-18','EMILYELDER@GREENWAY.COM','2127786755'),
(28,3,'ROY','GILLMAN','M','1988-09-08','2010-05-03','ROYGILLMAN@GREENWAY.COM','2129808790'),
(29,3,'GORDON','MACLEEN','M','1972-04-18','2002-05-19','GORDONMACLEEN@GREENWAY.COM','2127784560'),
(30,3,'BELLE','ROCKWOOD','F','1991-02-22','2013-06-29','BELLEROCKWOOD@GREENWAY.COM','2125443242'),
(31,4,'GRACE','ROMNEY','F','1981-11-15','2006-12-19','GRACEROMNEY@GREENWAY.COM','4248906677'),
(32,4,'VICTOR','POSER','M','1979-05-24','2003-10-20','VICTORPOSER@GREENWAY.COM','4243502357'),
(33,4,'LINDA','TICE','F','1988-03-29','2009-06-10','LINDATICE@GREENWAY.COM','4249087768'),
(34,4,'JACOB','BOWMAN','M','1982-11-01','2010-03-28','JACOBBOWMAN@GREENWAY.COM','4248853029'),
(35,4,'JERREMY','KOHL','M','1987-02-10','2006-07-27','JERREMYKOHL@GREENWAY.COM','4243509867'),
(36,4,'STELLA','HUNTER','F','1979-03-04','2008-08-09','STELLAHUNTER@GREENWAY.COM','4245647768'),
(37,4,'CATHY','WOODSON','F','1975-12-18','2004-03-28','CATHYWOODSON@GREENWAY.COM','4245625533'),
(38,4,'JAMES','CONWAY','M','1978-03-27','2006-07-05','JAMESCONWAY@GREENWAY.COM','4245216621'),
(39,4,'OLIVA','GILLMAN','F','1975-04-23','2004-03-17','OLIVAGILLMAN@GREENWAY.COM','4243508090'),
(40,4,'NICK','JOHNSON','M','1978-05-20','2005-08-22','NICKJOHNSON@GREENWAY.COM','4246687292');

INSERT INTO gw_stores (manager_id, city, street, phonenumber, GST_number) 
VALUE
(5,'CALGARY','1609 MACLEOD TRAIL','4038296453','823964581'),
(16,'TORONTO','508 DUNDAS STREET','6472329561','732165342'),
(29,'NEW YORK','722 HARBOR DRIVE','2128086672','251937648'),
(37,'LOS ANGELES','900 FLORENCE AVE','4240553984','563284323');


INSERT INTO gw_customer (first_name, last_name, birth_date, email)
VALUE
('NICOLE','DAVIDSON','1980-03-07','NICOLEDAVIDSON@MYMAIL.COM'),
('BARB','ROMAN','1977-07-03','BARBROMAN@MYMAIL.COM'),
('REILEY','WOOD','1968-03-09','REILEYWOOD@MYMAIL.COM'),
('CINDY','BOLMER','1978-10-19','CINDYBOLMER@MYMAIL.COM'),
('PRICILA','PECKER','1972-09-08','PRICILAPECKER@MYMAIL.COM'),
('JADEN','KNAPP','1973-02-02','JADENKNAPP@MYMAIL.COM'),
('IRIS','HAKER','1980-11-09','IRISHAKER@MYMAIL.COM'),
('CINDY','LAMNEY','1982-08-16','CINDYLAMNEY@MYMAIL.COM'),
('BRYAN','LANHAM','1976-04-23','BRYANLANHAM@MYMAIL.COM'),
('JERRY','LONG','1969-03-09','JERRYLONG@MYMAIL.COM'),
('DEVEN','WHYMAN','1970-07-28','DEVENWHYMAN@MYMAIL.COM'),
('ALBERT','HAAS','1965-03-07','ALBERTHAAS@MYMAIL.COM'),
('ROLAND','WOLFREY','1969-04-06','ROLANDWOLFREY@MYMAIL.COM'),
('BESTY','SPARK','1976-08-07','BESTYSPARK@MYMAIL.COM'),
('JOEY','WOODMAN','1970-03-02','JOEYWOODMAN@MYMAIL.COM'),
('LINDSEY','LONGTON','1963-02-09','LINDSEYLONGTON@MYMAIL.COM'),
('LILLY','LYNCH','1986-06-26','LILLYLYNCH@MYMAIL.COM'),
('COREY','YOUNGER','1960-07-04','COREYYOUNGER@MYMAIL.COM'),
('LOUIS','WITTMAN','1970-06-03','LOUISWITTMAN@MYMAIL.COM'),
('DEREK','EWEN','1977-03-09','DEREKEWEN@MYMAIL.COM'),
('MOLLY','MABERRY','1984-03-29','MOLLYMABERRY@MYMAIL.COM'),
('ROSIE','MADISON','1977-08-04','ROSIEMADISON@MYMAIL.COM'),
('CHARLOTT','BOWMAN','1971-04-08','CHARLOTTBOWMAN@MYMAIL.COM'),
('MICHAEL','SMITH','1955-03-17','MICHAELSMITH@MYMAIL.COM'),
('FIONA','LUCK','1977-12-25','FIONALUCK@MYMAIL.COM'),
('MARK','FLEMMING','1948-05-04','MARKFLEMMING@MYMAIL.COM'),
('LUNA','BROOKFIELD','1955-02-18','LUNABROOKFIELD@MYMAIL.COM'),
('COLLEEN','BROOKER','1960-09-18','COLLEENBROOKER@MYMAIL.COM'),
('DAVID','ALLISON','1968-12-17','DAVIDALLISON@MYMAIL.COM'),
('ASHLEY','GREENLAND','1978-04-28','ASHLEYGREENLAND@MYMAIL.COM'),
('JASON','GUNNER','1973-03-22','JASONGUNNER@MYMAIL.COM'),
('JAMIE','HALLOCK','1968-07-29','JAMIEHALLOCK@MYMAIL.COM'),
('MARK','LOWEN','1956-12-20','MARKLOWEN@MYMAIL.COM'),
('TASHA','HOPKINS','1966-06-26','TASHAHOPKINS@MYMAIL.COM'),
('LYDIA','HUNTER','1970-08-21','LYDIAHUNTER@MYMAIL.COM'),
('KAYLA','HONOR','1990-04-09','KAYLAHONOR@MYMAIL.COM'),
('RYAN','HOLMES','1987-03-10','RYANHOLMES@MYMAIL.COM'),
('PATRICK','BLACK','1978-05-25','PATRICKBLACK@MYMAIL.COM'),
('HIDY','MCGINLEY','1960-08-26','HIDYMCGINLEY@MYMAIL.COM'),
('WILLIAM','MILLER','1978-12-26','WILLIAMMILLER@MYMAIL.COM');

INSERT INTO gw_customer_membership (sid, join_date, account_number)
VALUE
(2,'2008-09-10','20926554367280'),
(3,'2006-08-23','20926554389065'),
(2,'2006-01-29','20926554366582'),
(3,'2010-03-25','20926554354376'),
(1,'2009-11-03','20926554312423'),
(1,'2002-04-20','20926554398760'),
(1,'2012-12-03','20926554377868'),
(1,'2008-05-18','20926554335625'),
(1,'2007-08-06','20926554367564'),
(4,'2005-05-29','20926554366754'),
(3,'2011-07-17','20926554322438'),
(3,'2007-06-28','20926554333542'),
(1,'2006-02-15','20926554377689'),
(2,'2003-11-07','20926554366540'),
(2,'2007-06-16','20926554321265'),
(4,'2009-09-09','20926554323231'),
(3,'2002-07-16','20926554399089'),
(3,'2013-05-11','20926554377876'),
(2,'2011-07-13','20926554366786'),
(2,'2012-08-08','20926554388910'),
(2,'2011-06-09','20926554377671'),
(4,'2014-01-03','20926554366541'),
(3,'2011-03-27','20926554312342'),
(4,'2008-04-18','20926554344454'),
(3,'2009-02-09','20926554388610'),
(2,'2006-05-28','20926554377663'),
(1,'2009-07-26','20926554399894'),
(1,'2013-03-23','20926554368492'),
(2,'2013-07-14','20926554333432'),
(3,'2008-06-04','20926554370650'),
(2,'2010-10-09','20926554344545'),
(1,'2011-03-13','20926554301019'),
(4,'2012-12-05','20926554322887'),
(3,'2013-04-08','20926554300996'),
(4,'2013-07-07','20926554355220'),
(1,'2007-05-09','20926554321328'),
(3,'2009-06-30','20926554311178'),
(4,'2007-06-14','20926554333669'),
(1,'2012-03-19','20926554327677'),
(2,'2011-07-16','20926554365470');







INSERT INTO gw_products (name,supplier_id, unit_price,quantity_instock,expire_date,buy_price)
VALUE
('CARROT', 8,1.50, 1000, '2014-09-30', 0.80),
('BROCOLLI', 9, 1.75, 1000, '2014-09-10',0.75),
('CUCUMBER',2, 2.50, 500, '2014-09-02',0.80),
('LETTUCE',5, 3.20,500,'2014-09-10',1.00),
('ONION',4, 1.20,1000,'2014-10-01',0.75),
('PEPPER',8, 0.60,500,'2014-09-01',0.30),
('TOMATO',8, 0.80,1000,'2014-09-15',0.25),
('POTATO',8, 1.00,1000,'2014-10-30',0.15),
('CELERY',8, 2.00,400,'2014-10-15',0.65),
('ZUCCHINI',9, 2.50,400,'2014-11-15',0.70),
('APPLE',8, 0.50,800,'2014-09-30',0.25),
('ORANGE',8, 0.75,800,'2014-09-15',0.35),
('PEACH',9, 1.25,400,'2014-09-10',0.30),
('GRAPE',9, 2.00,400,'2014-09-25',0.40),
('CHERRIES',9, 2.50,600,'2014-09-30',0.75),
('WATERMELON',2, 7.00,200,'2014-09-30',2.00),
('KIWI',3, 1.90,300,'2014-09-25',0.80),
('STRAWBERRIES',4, 3.50,500,'2014-09-08',0.90),
('PEAR',1, 2,200,'2014-09-30',0.80),
('BLUEBERRIES',1, 3.00,200,'2014-09-30',1.2),
('HOT SAUCE',5, 4.00,150,'2014-12-30',1.50),
('SALT',7, 3.5,100,'2015-08-30',1.20),
('SUGAR',5, 3.5,100,'2015-06-30',1.10),
('SOY SAUCE',3, 4.00,300,'2015-12-30',1.50),
('SALAD DRESSING',6, 4.50,100,'2014-12-30',1.80),
('SALSA',7, 3.50,150,'2014-12-30',1.20),
('CRANBERRY JAM',8, 4.8,200,'2015-04-30',1.8),
('SYRUP',1, 6.00,150,'2015-04-30',2.00),
('BBQ SAUCE',2, 8.00,200,'2015-07-30',2.50),
('KETCHUP',3, 3.00,300,'2015-12-30',1.80),
('BEER',4, 12.00,200,'2015-08-30',5.00),
('JUICE',5, 6.00,300,'2015-04-30',2.50),
('CHAMPAGNE',5, 10.00,100,'2015-12-30',4.00),
('RUM',6, 15.00,100,'2015-09-30',5.00),
('MARGARITA',8, 8.00,150,'2015-03-31',4.00),
('COCA COLA',9, 2.00,800,'2015-02-15',1.00),
('ICED LEMON TEA',2, 2.00,800,'2015-06-30',0.80),
('DISTILLED WATER',3, 1.50,1500,'2015-06-30',0.40),
('INSTANT COFFEE',5, 4.00,500,'2014-12-30',1.50),
('GREEN TEA',4, 6.00,400,'2014-12-30',2.00),
('BUTTER',3, 4.00,500,'2014-10-30',1.50),
('CHEESE',8, 8.00,800,'2014-10-30',2.50),
('MILK',9, 5,500,'2014-09-01',2.5),
('SOUR CREAM',4, 5.00,300,'2014-12-30',2.00),
('YOGURT',7, 6.00,200,'2014-09-10',2.50),
('BUN',3, 2.00,100,'2014-09-10',0.5),
('DONUT',2, 2.50,100,'2014-09-02',1.00),
('SLICED BREAD',1, 4.50,100,'2014-09-10',2.00),
('CAKE',4, 10,50,'2014-09-15',4.00),
('BAGEL',6, 1.50,50,'2014-09-02',0.6),
('BACON',7, 4.00,300,'2014-12-30',2.00),
('SAUSAGE',7, 8.00,200,'2015-03-30',3.50),
('BEEF',9, 10,100,'2015-09-20',5.00),
('HAM',3, 5.00,150,'2014-12-30',2.50),
('PORK',5, 6.00,100,'2014-09-30',2.00),
('TUNA',4, 12.00,100,'2014-10-30',5.00),
('CRAB',4, 15,50,'2014-09-30',8.00),
('SHRIMP',6, 10,100,'2014-12-30',4.00),
('SALMON',2, 15,100,'2014-12-30',8.00),
('OYSTER',1, 15,50,'2014-10-30',10.00);

INSERT INTO gw_products (supplier_id)
VALUE
(8),
(8),
(8),
(8),
(8),
(8),
(8),
(8),
(8),
(8),
(9),
(9),
(9),
(9),
(9),
(9),
(9),
(9),
(9),
(9),
(2),
(5),
(5),
(7),
(7),
(3),
(1),
(1),
(4),
(6);


INSERT INTO gw_departments
VALUE
(1,'VEGETABLES'),
(2,'FRUITS'),
(3,'CONDIMENTS'),
(4,'BEVERAGES'),
(5,'DAIRY'),
(6,'BAKERY'),
(7,'MEAT'),
(8,'SEAFOOD')

INSERT INTO gw_products_supplier (name, contact_person, phonenumber)
VALUE
('NESTLE','NICK','2123336457'),
('HEINZ','BOB','6472567948'),
('TROPICANA','NICHOLE','6472886653'),
('GOOD HAVEN','KELLY','2125534452'),
('KRAFT','HEATHER','6472890732'),
('LUCERNE','JANE','6472568890'),
('WHOLESOME FOODS','RICHAEL','6473134590'),
('LOCAL','KEVIN','4032996567')
('FARMANDYOU','EMILY','2125037738');

INSERT INTO gw_employee_salary (emp_id, SSN, jobtitle,pay_type,salary)
VALUE
(1,'654356782','SALE REP','HOUR','10.00'),
(2,'677856453','SALE REP','HOUR','10.00'),
(3, '643223978','SALE REP','HOUR','10.00'),
(4, '622321456','SHIFT SUPERSIVOR','HOUR','12.00'),
(5,'678933435','MANAGER','YEAR','45000'),
(6,'699254388','SALE REP','HOUR','10.00'),
(7,'611234569','SALE REP','HOUR','10.00'),
(8,'688227227','SHIFT SUPERVISOR','HOUR','12.00'),
(9,'655234256','ASSOCIATE MANAGER','YEAR','35000'),
(10,'678923421','SALE REP','HOUR','10.00'),
(11,'656569228','SALE REP','HOUR','10.00'),
(12,'699989778','SALE REP','HOUR','10.00'),
(13,'622334456','ASSOCIATE MANAGER','YEAR','35000'),
(14,'688889922','SHIFT SUPERVISOR','HOUR','12.00'),
(15,'655553328','SALE REP','HOUR','10.00'),
(16,'688899901','MANAGER','YEAR','45000'),
(17,'677799902','SALE REP','HOUR','10.00'),
(18,'688997766','SHIFT SUPERVISOR','HOUR','12.00'),
(19,'622033556','SALE REP','HOUR','10.00'),
(20,'655554433','SALE REP','HOUR','10.00'),
(21,'678956342','SALE REP','HOUR','10.00'),
(22,'699998821','SALE REP','HOUR','10.00'),
(23,'655553324','ASSOCIATE MANAGER','YEAR','35000'),
(24,'611223399','SHIFT SUPERVISOR','HOUR','12.00'),
(25,'602156366','SHIFT SUPERVISOR','HOUR','12.00'),
(26,'677089092','SALE REP','HOUR','10.00'),
(27,'602348971','SALE REP','HOUR','10.00'),
(28,'655460988','SALE REP','HOUR','10.00'),
(29,'678787898','MANAGER','YEAR','45000'),
(30,'655555088','SALE REP','HOUR','10.00'),
(31,'622221110','SHIFT SUPERVISOR','HOUR','12.00'),
(32,'699099033','ASSOCIATE MANAGER','YEAR','35000'),
(33,'677707798','SALE REP','HOUR','10.00'),
(34,'600998822','SALE REP','HOUR','10.00'),
(35,'698980001','SALE REP','HOUR','10.00'),
(36,'656560111','SALE REP','HOUR','10.00'),
(37,'633333666','MANAGER','YEAR','45000'),
(38,'644443389','SALE REP','HOUR','10.00'),
(39,'666445678','SHIFT SUPERVISOR','HOUR','12.00'),
(40,'648809998','SALE REP','HOUR','10.00');






INSERT INTO gw_sales (store_id, sale_date, payby, subtotal)
VALUE
(1,'2010-12-12 10:20:30','VISA',23.28),
(1, '2010-12-20 16:30:28','CASH',18.2),
(2, '2012-05-09 13:27:38','MASTERCARD', 54.6),
(2, '2012-05-09 18:05:30','VISA', 34.2),
(3, '2013-04-28 12:15:20','VISA', 87.9),
(3, '2013-04-28 19:04:34','CASH', 55.67),
(3, '2013-04-29 9:04:14','CASH', 45.98),
(3, '2013-04-30 10:04:34','VISA', 55.2),
( 3, '2013-05-28 12:04:34','CASH', 20.4),
( 4, '2013-05-28 19:04:34','CASH', 12.3),
(4, '2013-05-30 15:04:34','MASTERCARD', 104.8),
( 1, '2013-04-28 19:50:34','CASH', 88.65),
( 1, '2014-03-28 19:04:34','CASH', 65.98),
( 1, '2014-04-28 19:04:34','CASH', 65.87),
(1, '2014-02-8 9:06:27','VISA', 78.2),
(2, '2011-03-28 19:04:34','CASH', 52.4),
(3, '2011-04-28 19:04:34','CASH', 38.55),
( 3, '2013-06-8 16:04:34','CASH', 10.05),
( 4, '2012-09-2 18:04:04','VISA', 8),
( 2, '2011-12-8 15:04:34','CASH', 3.25),
(4, '2011-01-8 15:33:34','CASH', 40.8),
( 2, '2013-08-30 9:25:34','CASH', 96.45),
( 3, '2013-04-28 19:04:34','CASH', 83.35);

INSERT INTO gw_sales_withemp (employee_id, customer_id, store_id, sale_date, payby, subtotal)
VALUE
(1,3, 10),
(2,3, 5),
(3,15, 20),
(4,18, 18),
(5,23, 25),
(6,23, 25),
(7,23, 25),
(8,23, 27),
(9,29, 21),
(10,33, 35),
(11,39, 35),
(12,4, 8),
(13,2, 5),
(14,2, 4),
(15,2, 8),
(14, 15, 2, '2011-03-28 19:04:34','CASH', 52.4),
(23, 25, 3, '2011-04-28 19:04:34','CASH', 38.55),
(24, 25, 3, '2013-06-8 16:04:34','CASH', 10.05),
(33, 39, 4, '2012-09-2 18:04:04','VISA', 8),
(13, 15, 2, '2011-12-8 15:04:34','CASH', 3.25),
(38, 35, 4, '2011-01-8 15:33:34','CASH', 40.8),
(18, 18, 2, '2013-08-30 9:25:34','CASH', 96.45),
(23, 25, 3, '2013-04-28 19:04:34','CASH', 83.35);


INSERT INTO gw_sales_details
VALUE
(1, 2, 3),
(1, 12, 10),
(1, 25, 2),
(2, 16, 2),
(2, 30, 1),
(3, 38, 10),
(3, 45, 6),
(4, 10, 5),
(4, 18, 5),
(5, 31, 4),
(5, 34, 4),
(6, 40, 10),
(6, 37, 5),
(7, 35, 4),
(7, 39, 1),
(7, 50, 2),
(8, 59, 2),
(8, 49, 1),
(9, 48, 4),
(9, 47, 1),
(10, 53, 1),
(11, 59, 3),
(11, 60, 3),
(11, 57, 2),
(12, 33, 3),
(12, 35, 4),
(13, 38, 20),
(13, 36, 40),
(14, 42, 4),
(14, 49, 4),
(15, 29, 4),
(15, 16, 4);




--select first_name, last_name from gw_customer who is belong to store branch new york and
--joined the store after 2010-05-01
SELECT cus.first_name, cus.last_name 
FROM gw_customer cus
INNER JOIN gw_customer_membership cusmem ON cusmem.cid = cus.customer_id 
INNER JOIN gw_stores stores ON stores.sid = cusmem.sid
WHERE stores.city = 'NEW YORK' AND cusmem.join_date > '2010-05-01';
--4 total


--select employees who are under supervision by GORDON MACLEEN
SELECT emp.first_name, emp.last_name
FROM gw_employees emp
WHERE emp.store_id IN (
SELECT stores.sid
FROM gw_stores stores
INNER JOIN gw_employees emp ON emp.emp_id = stores.manager_id
WHERE emp.first_name = 'GORDON' AND emp.last_name = 'MACLEEN');
-- 10total


--select all the products supplied by WHOLESOME FOODS and expire by 2014-10-30
SELECT prod.name 
FROM gw_products prod
INNER JOIN gw_products_supplier su ON su.supplier_id = prod.supply_company
WHERE su.name = 'WHOLESOME FOODS' AND prod.expire_date < '2014-10-30';
--4 total


--select all the employees who were hired before 2008-01-01 with an hourly salary 10.00 in branch TORONTO

SELECT gw_employees.first_name, gw_employees.last_name FROM gw_employees INNER JOIN gw_stores ON gw_stores.sid = gw_employees.store_id INNER JOIN gw_employee_salary ON gw_employee_salary.emp_id = gw_employees.emp_id WHERE gw_stores.city =  'TORONTO' AND gw_employee_salary.jobtitle = 'SALES REP' AND gw_employees.hire_date > '2008-01-01';



DELETE FROM `gw_products` WHERE `gw_products`.`product_id` = 105 LIMIT 1;

--insert into relationships

INSERT INTO gw_employees( store_id, first_name, last_name, birth_date, hire_date, email, phonenumber ) 
SELECT sid,  'EMMA',  'JOHNSON',  '1991-01-23',  '2009-08-09',  'EMMAJOHNSON@MYMAIL.COM',  '4163344552'
FROM gw_stores
WHERE city =  'TORONTO';

INSERT INTO gw_sales_details( sid, item_id, quantity ) 
SELECT 1 , product_id, 2
FROM gw_products
WHERE name =  'ZUCCHINI';

INSERT INTO gw_customer_membership( cid, sid, join_date ) 
SELECT customer_id, sid,  '2013-11-30'
FROM gw_customer, gw_stores
WHERE gw_stores.city =  'NEW YORK'
AND gw_customer.first_name =  'NICOLE'
AND gw_customer.last_name =  'DAVIDSON';

INSERT INTO gw_sales_details( sid, item_id, quantity ) 
SELECT sale_id, product_id, 4
FROM gw_sales, gw_products
WHERE gw_sales.sale_id =2
AND gw_products.name =  'CARROT';

INSERT INTO gw_sales_withemp( sale_id, employee_id, customer_id ) 
SELECT gw_employees.emp_id, gw_customer.customer_id, 2
FROM gw_employees, gw_customer
WHERE gw_employees.first_name =  'JACKY'
AND gw_employees.last_name =  'ANDERSON'
AND gw_customer.first_name =  'FIONA'
AND gw_customer.last_name =  'LUCK';

--delete from many-to-many table
DELETE FROM gw_sales_details WHERE gw_sales_details.sid = 1 AND gw_sales_details.item_id = 2 LIMIT 1;

DELETE FROM gw_sales_details WHERE gw_sales_details.item_id IN (
SELECT gw_products.product_id
FROM gw_products
WHERE gw_products.name =  'BROCOLLI'
)
AND gw_sales_details.sid =1
LIMIT 1;

--update many-to-many table
UPDATE  gw_sales_details SET  quantity =  4 WHERE  gw_sales_details.sid =1 AND  gw_sales_details.item_id =2 LIMIT 1 ;

UPDATE gw_sales_details SET quantity =3 WHERE gw_sales_details.item_id IN (
SELECT gw_products.product_id
FROM gw_products
WHERE gw_products.name =  'YOGURT'
)
AND gw_sales_details.sid =3
LIMIT 1

