#!/bin/bash

./config.sh --bindir ./bin/etalon/ ./configs/user_defined.json
make
./config.sh --bindir ./bin/markov_predictor_max/ ./configs/markov.json
make
./config.sh --bindir ./bin/markov_predictor_prop/ ./configs/markov.json
make CXXFLAGS='-DMARKOV_PREDICTOR_PROP_ENABLE'
./config.sh --bindir ./bin/fifo_cache/ ./configs/fifo.json
make

echo -e "\n\n================\nBuild successfully:"
find ./bin/ -name champsim
