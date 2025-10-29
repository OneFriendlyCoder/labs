#!/bin/bash

NOISE_PROFILE=""
VIDEO="$1"

# Validate noise profile
if [ ! -f "$NOISE_PROFILE" ]; then
    echo "ERROR: Noise profile not found at:"
    echo "   $NOISE_PROFILE"
    exit 1
fi

# Validate video file
if [ -z "$VIDEO" ] || [ ! -f "$VIDEO" ]; then
    echo "ERROR: Valid video file not provided."
    echo "Usage:"
    echo "    ./noise.sh /path/to/video.mp4"
    exit 1
fi

echo "Using noise profile: $NOISE_PROFILE"
echo "Processing: $VIDEO"
echo

base="${VIDEO%.*}"
raw_audio="${base}-raw_audio.wav"
clean_audio="${base}-clean.wav"
output_video="${base}-clean.mp4"

echo " → Extracting raw audio..."
ffmpeg -y -i "$VIDEO" -vn "$raw_audio" >/dev/null 2>&1

echo " → Reducing noise..."
sox "$raw_audio" "$clean_audio" noisered "$NOISE_PROFILE" 0.21

echo " → Merging cleaned audio with video..."
ffmpeg -y -i "$VIDEO" -i "$clean_audio" -c:v copy -map 0:v:0 -map 1:a:0 "$output_video" >/dev/null 2>&1

echo " → Removing temporary files..."
rm -f "$raw_audio" "$clean_audio"

echo
echo " ✅ DONE → $output_video"
echo "----------------------------------------"
