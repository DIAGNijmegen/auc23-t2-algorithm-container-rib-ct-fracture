#!/usr/bin/env bash

if ! [ "$1" ]; then
  echo "Expected input directory as argument, but no argument found. Aborting."
  exit 0
fi

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

./build.sh

docker volume create algorithm-output

# Run the algorithm on the input directory specified in the first argument, 
# emulating Grand Challenge environment.
# memory and memory-swap can be increased to 30g max.
MEMORY="16g"
docker run --rm --gpus all \
        --memory=$MEMORY --memory-swap=$MEMORY \
        --cap-drop=ALL --security-opt="no-new-privileges" \
        --network none --shm-size=128m --pids-limit 256 \
        -v $1:/input/ \
        -v algorithm-output:/output/ \
        algorithm

# Print all generated results
echo "The Algorithm generated the following results:"

docker run --rm \
    -v algorithm-output:/output/ \
    python:3.7-slim sh -c 'for f in /output/*.json; do echo $(basename $f):; cat $f | python -m json.tool; done'

echo "Please manually check if the output above is expected. For each interface, there should be a single probability for a binary task, and a list of probabilities for a multi-class task."

docker volume rm algorithm-output
