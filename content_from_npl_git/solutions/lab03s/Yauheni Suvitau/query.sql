create external table evgeny_3s
(uid string, url string)
row format delimited
fields terminated by '\t'
location '/user/evgeny.suvitov/lab03s_data';--data from mapper.py

create external table evgeny_categorized
(uid string, auto string, tmp1 string, tmp2 string, tmp3 string)
row format delimited
fields terminated by '\t'
location '/user/evgeny.suvitov/lab03_result'; --data from lab03

insert overwrite directory 'hdfs://master.cluster-lab.com:8020/user/evgeny.suvitov/lab03s_result'
row format delimited fields terminated by '\t' stored as textfile
select 
t4.url, 
t4.domain_auto_prob/(t4.domain_prob*t5.auto_prob) relevance 
from
(
	select
	t3.url url,
	count(t3.auto_flag) domain_prob,
	pow(sum(t3.auto_flag),2) domain_auto_prob
	from
	(
		select 
		nvl(t2.auto,0) auto_flag, 
		t1.url url 
		from 
		evgeny_3s t1 
		left join evgeny_categorized t2
		on t1.uid = t2.uid
	) t3
	group by t3.url
) t4,
(
	select 
	sum(case when auto_flag=1 then 1 else 0 end) auto_prob
	from
	(
		select 
		nvl(t2.auto,0) auto_flag,
		t1.url url 
		from evgeny_3s t1 
		left join evgeny_categorized t2 
		on t1.uid = t2.uid
	) t3
) t5
order by relevance desc, t4.url limit 200;