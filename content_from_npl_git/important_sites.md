## Важные сайты и URL

| назначение | URL | comments |
|---|---|---|
| ЛК | lk.newprolab.com | персональная информация по лабам, ssh ключ |
| master | master.cluster-lab.com:22 | главный линукс-сервер |
| class marker | classmarker.com | для тестов |
| Ambari | master.cluster-lab.com:8080 | панель мониторинга кластера |
| Hadoop | http://master.cluster-lab.com:8088/cluster | мониторинг хадупа :warning: через прокси! |
| jupyter-hub | master.cluster-lab.com:80 | для запуска тетрадок с кодом |
| proxy | master.cluster-lab.com:22 | `ssh username@master.cluster-lab.com  -D localhost:1080 -N`|
| HBase | - |`hbase_endpoint = 'master.cluster-lab.com'`| 
| Hive  | node1.cluster-lab.com:10000 |`beeline -u jdbc:hive2://node1.cluster-lab.com:10000 -n name.surname` |

