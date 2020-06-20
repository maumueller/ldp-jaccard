PYTHON=python3
THREADS=6

mkdir -p ../results

for i in 50 100 200 500; do
    $PYTHON get_groundtruth.py movielens.dat $i;
done

$PYTHON get_groundtruth.py lastfm.dat 20

for e in buckets.yaml synthetic.yaml synthetic_small.yaml; do
    $PYTHON run_synthetic.py experiments/$e $THREADS;
done

$PYTHON run_realworld.py experiments/real_world.yaml $THREADS

$PYTHON compute_statistics.py real_world.results.pickle | tee ../results/real_world.csv

$PYTHON split_up_log.py buckets.csv --prefix ../results/buckets_
$PYTHON split_up_log.py synthetic.csv --prefix ../results/synthetic_
$PYTHON split_up_log.py synthetic_small.csv --prefix ../results/synthetic_ --append
