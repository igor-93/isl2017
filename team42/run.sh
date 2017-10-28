#!/bin/bash

n_workers=5
run_worker_command="python3 manage.py runworker"
run_daphne="daphne team42.asgi:channel_layer"
run_mongod="sudo service mongod start" 
nlp_command='cd ./nlp/lib & screen -m -d java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000' 
redis_command="screen -d -m redis-server"

#cmds=("${cmds[@]}" "$run_mongod" )
#cmds=("${cmds[@]}" "$nlp_command" )

for run in `seq 1 $n_workers`
do
	cmds=("${cmds[@]}" "$run_worker_command" )
done

#cmds=("${cmds[@]}" "$run_daphne" )


for each in "${cmds[@]}"
do
  echo "$each"
done



eval "$run_mongod"
eval "$redis_command"
eval "$nlp_command"
eval "$run_daphne"


for cmd in "${cmds[@]}"; do {
  echo "Process \"$cmd\" started";
  $cmd & pid=$!
  PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT
trap "killall screen" SIGINT
trap "sudo service mongod stop" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";