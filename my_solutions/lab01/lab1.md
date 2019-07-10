1. скачать в директорию /Users/antonina.goryacheva/Desktop/NewProLab/kk ключ npl.pem
2. поставить на него права 
**$ chmod 0600 npl.pem (если мы перешли в эту директорию, иначе - прописать полный путь)**
3. скопировать ключ на тачку master.cluster-lab.com
**$ scp ./npl.pem antonina.goryacheva@master.cluster-lab.com:~/npl.pem**
4. зайти на машину по ssh
**$ ssh -i /Users/antonina.goryacheva/Desktop/NewProLab/kk/npl.pem antonina.goryacheva@master.cluster-lab.com*

5. проверить, что ключ скопирован 
**$ cat ~/.ssh/npl.pem**
6. снова установить права 
**$ chmod 0600 npl.pem**


7. подключиться к машине
**$ ssh -i ~/.ssh/npl.pem ubuntu@ec2-54-171-222-80.eu-west-1.compute.amazonaws.com**
(после @ указать public DNS хоста из ЛК со статусом running)

8. Ставим Ambari на сервер-менеджер (все как в инструкции)
**$ sudo su**
**$ wget -O /etc/apt/sources.list.d/ambari.list http://public-repo-1.hortonworks.com/ambari/ubuntu16/2.x/updates/2.7.0.0/ambari.list**
**$ apt-key adv --recv-keys --keyserver keyserver.ubuntu.com B9733A7A07513CAD**
**$ apt-get update**
**$ apt-cache showpkg ambari-server**
**$ apt-cache showpkg ambari-agent**
**$ apt-cache showpkg ambari-metrics-assembly**


**$ apt-get install ambari-server** 
(тут была ошибка Unable to lock the administration directory (/var/lib/dpkg/), 
надо просто подождать - мне помогло)

9. Настройка Ambari

(не забываем, что все команды выполняются из-под пользователя root)

**$ ambari-server setup**
дальше все по умолчанию (жать enter)

**$ ambari-server start**
**$ ps -ef | grep Ambari**

Машина настроена, можно закрыть сессию:

**$ exit**
**$ exit**

9. Подключиться через Web-интерфейс к Ambari и собрать из остальных нод кластер
Тут все как в инструкции

10. Тестовое задание кластере
подключаемся
**$ ssh -i npl.pem ubuntu@ec2-34-250-13-236.eu-west-1.compute.amazonaws.com**
Проверяем, создан ли пользователь hdfs
**$ sudo cat /etc/passwd | grep hdfs**
Все дальнейшие действия выполняем под пользователем hdfs
**$ sudo su hdfs**	
Загружаем данные с сервера NPL:
**$ wget http://data.cluster-lab.com/public-newprolab-com/numbers.txt.lzma -O /tmp/numbers.txt.lzma**
Распаковываем
**$ lzma -d /tmp/numbers.txt.lzma**
Создаём директорию /users/numbers на HDFS
**$ hdfs dfs -mkdir -p /users/numbers**
И скидываем в неё наш файл
**$ hdfs dfs -put /tmp/numbers.txt /users/numbers/**

Обновляем mapreduce jar-файл
**$ hdfs dfs -ls /hdp/apps**
**$ hdfs dfs -rm /hdp/apps/3.0.1.0-187/mapreduce/mapreduce.tar.gz**
**$ hdfs dfs -put /usr/hdp/3.0.1.0-187/hadoop/mapreduce.tar.gz /hdp/apps/3.0.1.0-187/mapreduce/mapreduce.tar.gz** 

Запускаем MapReduce Job
**$ hadoop jar /usr/hdp/3.0.0.0-1634/hadoop-mapreduce/hadoop-streaming.jar 
		-D mapred.reduce.tasks=1 
		-input /users/numbers 
		-output /users/numbers/result 
		-mapper "cat" 
		-reducer "uniq -c"**

Если результат не устраивает, удаляем файл
**$ hdfs dfs -rm -r -f /users/ && hdfs dfs -mkdir -p /users/numbers**























