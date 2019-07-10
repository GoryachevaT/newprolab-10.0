CREATE EXTERNAL TABLE antonina_goryacheva (
	uid string, 
	ts string, 
	url string) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t' 
STORED AS TEXTFILE 
location '/user/antonina.goryacheva/url_tab/';

load data inpath '/user/antonina.goryacheva/lab03data/' into table antonina_goryacheva;


create table tg as
with t0 as (
				select 
						cast(t.uid as float) uid, t.url,  
						case when url like '%cars.ru%' then 1 else 0 end cars, 
						case when url like '%avto-russia.ru%' then 1 else 0 end avto_russia, 
						case when url like '%bmwclub.ru%' then 1 else 0 end bmwclub, 
						case when url like '%zakon.kz%' then 1 else 0 end zakon, 
						case when url like '%egov.kz%' then 1 else 0 end egov, 
						case when url like '%makler.md%' then 1 else 0 end makler, 
						case when url like '%russianfood.com%' then 1 else 0 end russianfood, 
						case when url like '%psychologies.ru%' then 1 else 0 end psychologies, 
						case when url like  '%gotovim.ru%' then 1 else 0 end gotovim, 
						case when  url like '%books.imhonet.ru%' then 1 else 0 end books, 
						case when url like '%zhurnaly.biz%' then 1 else 0 end zhurnaly, 
						case when url like '%zvukobook.ru%' then 1 else 0 end zvukobook 
				from antonina_goryacheva t where t.uid is not NULL
		    ), 
  t1 as (
  			select 
  				uid, 
  				sum(cars) cars, sum(avto_russia) avto_russia, sum(bmwclub) bmwclub, 
  				sum(zakon) zakon, sum(egov) egov, sum(makler) makler, 
  				sum(russianfood) russianfood, sum(psychologies) psychologies, sum(gotovim) gotovim, 
  				sum(books) books, sum(zhurnaly) zhurnaly, sum(zvukobook) zvukobook 
  			from t0 group by uid
  		) 
select 
cast(uid as bigint) uid, 
case when cars >= 10 or avto_russia >= 10 or bmwclub >= 10 then 1 else 0 end user_cat1_flag, 
case when zakon >= 10 or egov >= 10 or makler >= 10 then 1 else 0 end user_cat2_flag, 
case when russianfood >= 10 or psychologies >= 10 or gotovim >= 10 then 1 else 0 end user_cat3_flag, 
case when books >= 10 or zhurnaly >= 10 or zvukobook >= 10 then 1 else 0 end user_cat4_flag  
from t1 order by uid;


INSERT OVERWRITE DIRECTORY 'hdfs://master.cluster-lab.com:8020/user/antonina.goryacheva/lab03result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select * from tg order by uid;

hadoop fs -getmerge /user/antonina.goryacheva/lab03result ~/lab03_users.txt

==============================================================================================================
CREATE EXTERNAL TABLE antonina_goryacheva (
	uid string, 
	ts string, 
	url string) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t' 
STORED AS TEXTFILE 
location '/user/antonina.goryacheva/url_tab/';

load data inpath '/user/antonina.goryacheva/lab03data_s/' into table antonina_goryacheva;

select count(1), count(distinct uid), count(distinct url) from antonina_goryacheva where uid is not NULL;
 count(1)  |   uid   |  url   |
+----------+---------+--------+
| 6572876  | 100000  | 17710  |



create table tg as
with t0 as (select 
				uid,
				trim(t.url), 
				case when trim(t.url) like 'cars.ru' then 1 else 0 end cars, 
				case when trim(t.url) like 'avto-russia.ru' then 1 else 0 end avto_russia, 
				case when trim(t.url) like 'bmwclub.ru' then 1 else 0 end bmwclub from antonina_goryacheva t), 
	t1 as (select 
				uid, 
				sum(cars) cars, 
				sum(avto_russia) avto_russia, 
				sum(bmwclub) bmwclub 
		   from t0 group by uid
		  ) 
select uid, case when cars >= 10 or avto_russia >= 10 or bmwclub >= 10 then 1 else 0 end user_cat1_flag 
from t1;


select count(1), count(distinct uid) from tg where uid is not NULL;
|   _c0   |   _c1   |
+---------+---------+
| 100000  | 100000  



create table tg_domains as select trim(t1.url) url, tg.user_cat1_flag auto_flag from antonina_goryacheva t1 left join tg on t1.uid = tg.uid;

select count(1), count(distinct url) from tg_domains;
  _c0      |  _c1   |
+----------+--------+
| 6572876  | 17710  


select count(1), sum(auto_flag) from tg_domains;
+----------+---------+
|   _c0    |   _c1   |
+----------+---------+
| 6572876  | 313556  |


create table tg_domains_v2 as
with t as (select trim(t1.url) url, tg.user_cat1_flag auto_flag from antonina_goryacheva t1 left join tg on t1.uid = tg.uid) 
,t0 as (select t.url, count(t.url) over (partition by t.url) url_cnt, t.auto_flag, sum(t.auto_flag) over (partition by t.url) sum_auto_flag from t), 
t1 as (select 
			url, 
			round(((sum_auto_flag/6572876)*(sum_auto_flag/6572876))/((url_cnt/6572876)*(313556/6572876)),20) k1 
	   from t0 group by url, url_cnt, sum_auto_flag
	) 
select * from t1 order by k1 desc, url LIMIT 200; 


INSERT OVERWRITE DIRECTORY 'hdfs://master.cluster-lab.com:8020/user/antonina.goryacheva/lab03result_s'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
select * from tg_domains_v2 order by k1 desc, url;

hadoop fs -getmerge /user/antonina.goryacheva/lab03result_s ~/lab03s_domains.txt