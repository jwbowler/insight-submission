#!/usr/bin/env sh

mkdir -p tweet_output

python src/words_tweeted.py tweet_input/tweets.txt > tweet_output/ft1.txt &
python src/mincemeat.py localhost

python src/median_unique.py tweet_input/tweets.txt > tweet_output/ft2.txt
