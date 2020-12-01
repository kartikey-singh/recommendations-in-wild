#!/bin/sh

cd resources/music/

if [ -d "$1_outputs" ]
then
	rm -rf  "$1_outputs"
fi

mkdir "$1_outputs"

ffmpeg -i $1 -f segment -segment_time 30 -c copy "$1_outputs"/out%03d.mp3

# source /home/kartikeysingh/anaconda3/etc/profile.d/conda.sh
eval "$(conda shell.bash hook)"
conda activate spleeter

for filename in "$1_outputs"/out*
do
	spleeter separate -i $filename -p spleeter:2stems -o "$1_outputs"/spleeter
done	