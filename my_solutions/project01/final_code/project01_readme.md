1. ноутбук train_notebook_project1.ipynb запустить из папки notebooks
2. должна быть создана папка models рядом с папкой notebooks
3. в скрипте нужно относительные пути заменить
4. выполнить команды
cp /data/home/vladislav.boyadzhi/content_bigdata10_proj1/notebooks/vb_project01_gender-age.py ~/project01_gender-age.py 
tail -n1000 /data/share/project01/gender_age_dataset.txt | /data/home/vladislav.boyadzhi/project01_gender-age.py > output.json