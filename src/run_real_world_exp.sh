for k in 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90;
do python3 exp_real_world.py movielens noisy $k | tee movielens_noisy_$k.txt
done

for k in 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90;
do python3 exp_real_world.py lastfm noisy $k | tee lastfm_noisy_$k.txt
done

for k in 5 10 15 20 25;
do 
    for eps in 6 10 16;
    do
        for bf in 0.0001 0.0002 0.0003 0.001;
        do
            python3 exp_real_world.py movielens bucket $k $eps $bf | tee movielens_bucket_${k}_${eps}_${bf}.txt
        done;
    done;
done;

for k in 5 10 15 20 25;
do 
    for eps in 4;
    do
        for bf in 0.0001 0.0002 0.0003 0.001;
        do
            python3 exp_real_world.py movielens bucket $k $eps $bf | tee movielens_bucket_${k}_${eps}_${bf}.txt
        done;
    done;
done;

for k in 5 10 15 20 25;
do 
    for eps in 1 2 3;
    do
        for bf in 0.0001;
        do
            python3 exp_real_world.py movielens bucket $k $eps $bf | tee movielens_bucket_${k}_${eps}_${bf}.txt
        done;
    done;
done;

for k in 5 10 15 20;
do 
    for eps in 4 6 8 12;
    do
        for bf in 0.0001 0.0003 0.001;
        do
            python3 exp_real_world.py lastfm bucket $k $eps $bf | tee lastfm_bucket_${k}_${eps}_${bf}.txt
        done;
    done;
done;
