# Лабораторная работа №3

### Используйте приложенный url2domains.py чтобы отфильтровать данные. (не забудьте сделать его исполняемым chmod +x url2domains.py)

`hadoop fs -cat /labs/lab03data/* | ./url2domains.py > filtered`

### Загружаем его в HDFS

`hadoop fs -put filtered /user/${USER}/`

### Создаем таблицу в Hive (здесь и далее используем beeline)

```
DROP TABLE name_surname;

CREATE EXTERNAL TABLE name_surname(
    uid BIGINT, ts FLOAT, url_string STRING)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',';
```

### Загружаем данные в таблицу (внимание! При повторной загрузке надо сначала снова залить файл на HDFS (шаг 2)

`LOAD DATA INPATH '/user/name.surname/filtered' OVERWRITE INTO TABLE name_surname;`

### Мега запрос с выгрузкой итогового файла на Хадуп

```
WITH agg AS (
    SELECT uid, trim(url_string) as url_string, count(url_string) AS cnt
    FROM name_surname
    GROUP BY uid, url_string
    HAVING cnt > 9
), ungrouped AS (
    SELECT agg.uid,
        CASE WHEN agg.url_string IN ('cars.ru', 'avto-russia.ru', 'bmwclub.ru') THEN 1 ELSE 0 END AS auto_user,
        CASE WHEN agg.url_string IN ('zakon.kz', 'egov.kz', 'makler.md') THEN 1 ELSE 0 END AS business_user,
        CASE WHEN agg.url_string IN ('russianfood.com', 'psychologies.ru', 'gotovim.ru') THEN 1 ELSE 0 END AS home_user,
        CASE WHEN agg.url_string IN ('books.imhonet.ru', 'zhurnaly.biz', 'zvukobook.ru') THEN 1 ELSE 0 END AS book_user
    FROM agg
)
INSERT OVERWRITE DIRECTORY 'hdfs://master.cluster-lab.com:8020/user/name.surname/lab03result'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
SELECT uid, MAX(auto_user) AS user_cat1_flag, MAX(business_user) AS user_cat2_flag,
            MAX(home_user) AS user_cat3_flag, MAX(book_user) AS user_cat4_flag
FROM ungrouped
GROUP BY uid;
``` 

### Вроде бы есть способ фильтровать данные в хадупе. Проверьте сами, работает ли, и как. Может быть только если скрипт в HDFS, а может и вообще никак.

```
ADD FILE /data/home/name.surname/lab03/url2domains.py;
SELECT TRANSFORM(uid, ts, url_string)
    USING 'url2domains.py'
    AS uid, ts, url_string
FROM name_surname;
```

