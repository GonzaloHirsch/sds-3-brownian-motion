for i in 1 2 3 4 5 6 7 8 9 10
do
    python3 generator/input_generator.py -L 6 -N 60 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 400
    while [ $? -ne 0 ]
    do
      python3 generator/input_generator.py -L 6 -N 60 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 400
    done
    if [[ $? -eq 0 ]]; then
        java -jar ./target/sds-tp3-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./parsable_files/static.txt -df ./parsable_files/dynamic.txt -t 100
        python3 post/postprocess.py -t evp
        python3 post/postprocess.py -t evp0
    else
        echo 'Could not generate all particles'
    fi
done

for i in 1 2 3 4 5 6 7 8 9 10
do
    python3 generator/input_generator.py -L 6 -N 120 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 400
    while [ $? -ne 0 ]
    do
      python3 generator/input_generator.py -L 6 -N 120 -r 0.2 -m 0.9 -R 0.7 -M 2 -v 2 -retry 400
    done
    if [[ $? -eq 0 ]]; then
        java -jar ./target/sds-tp3-1.0-SNAPSHOT-jar-with-dependencies.jar -sf ./parsable_files/static.txt -df ./parsable_files/dynamic.txt -t 100
        python3 post/postprocess.py -t evp
        python3 post/postprocess.py -t evp0
    else
        echo 'Could not generate all particles'
    fi
done
