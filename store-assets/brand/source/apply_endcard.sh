#!/bin/sh
# Replace a clip's last SECS seconds with the brand end card: a still from just before the old ending,
# blurred and darkened, with the card faded in over it. Keeps the original audio and length.
# Cuts 0.1 s early so no frame of an old baked-in end card survives. H.264 veryfast crf 20, 30 fps.
# usage: apply_endcard.sh IN.mp4 CARD.png OUT.mp4 [SECS=3]
set -e
in=$1; card=$2; out=$3; secs=${4:-3}
len=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
cut=$(python3 -c "print(round($len-$secs-0.1,3))")
tail=$(python3 -c "print(round($len-$cut,3))")
grab=$(python3 -c "print(round($cut-0.3,3))")
tmp=$(mktemp -d)
ffmpeg -v error -y -ss "$grab" -i "$in" -frames:v 1 "$tmp/still.png"
ffmpeg -y -v error -i "$in" -loop 1 -t "$tail" -i "$tmp/still.png" -loop 1 -t "$tail" -i "$card" -filter_complex "
[0:v]trim=0:$cut,setpts=PTS-STARTPTS,fps=30,format=yuv420p,setsar=1[a];
[1:v]fps=30,gblur=sigma=34,eq=brightness=-0.24:saturation=0.7[bg];
[2:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1,fps=30[c];
[bg][c]overlay=0:0:format=auto,format=yuv420p,setsar=1[b];
[a][b]concat=n=2:v=1:a=0[v]" -map "[v]" -map 0:a? -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -r 30 -c:a copy -movflags +faststart -shortest "$out"
rm -rf "$tmp"
