

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
do
    python3 ./generator/input_generator.py -L 6 -N $1 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 1000
    while [ $? -ne 0 ]
    do
      python3 generator/input_generator.py -L 6 -N $1 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 1000
    done
    if [[ $? -eq 0 ]]; then
        java -jar ./target/sds-tp3-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./parsable_files/static.txt -df ./parsable_files/dynamic.txt -t 100
        python3 ./post/postprocess.py -t msds
        python3 ./post/postprocess.py -t msdb
    else
        echo 'Could not generate all particles'
    fi
done
