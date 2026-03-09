#!/bin/bash
source .venv/bin/activate
spotdl save \
  "https://open.spotify.com/playlist/2FfmyKKrgtJISTx3uNA3Bo" \
  --user-auth \
  --client-id "b3f7f9b52bb7488985f8ab16ecf8e27a" \
  --client-secret "77a681d1d04545ca90a741983d63085e" \
  --save-file /tmp/test.spotdl
