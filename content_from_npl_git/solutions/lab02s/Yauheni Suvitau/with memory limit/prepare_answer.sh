mkdir tmp_res
hdfs dfs -copyToLocal /user/evgeny.suvitov/lab2s/* tmp_res/
mkdir pred_res
for val in $(seq 0 7)
do
    cat tmp_res/part$val/part-00000 | sort -nk2 -r --numeric-sort | head -n 350 > pred_res/pred_res$val
    echo "done$val"
done

cat pred_res/* | sort -nk2 -r --numeric-sort | head -n 350 > top350.txt
cp top350.txt ~
rm -rf tmp_res/
rm -rf pred_res/
