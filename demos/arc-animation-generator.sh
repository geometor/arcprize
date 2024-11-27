#!/bin/bash

# Set variables
INPUT_DIR="./training"
OUTPUT_FILE="arc_animation.mp4"
FPS=12
FRAME_DURATION=$(echo "scale=10; 1 / $FPS" | bc)  # Duration of a single frame

# Get the number of PNG files
NUM_FILES=$(ls -1 "$INPUT_DIR"/*.png | wc -l)

# Generate a temporary file with frame durations
FRAME_FILE="frames.txt"
rm -f "$FRAME_FILE"
touch "$FRAME_FILE"

frames_to_hold=24  # Start by holding each image for 24 frames (1 second)

for file in "$INPUT_DIR"/*.png; do
    echo "file '$file'" >> "$FRAME_FILE"
    duration=$(echo "scale=10; $frames_to_hold * $FRAME_DURATION" | bc)  
    # Prepend a zero if duration is less than 1
    if (( $(echo "$duration < 1" | bc -l) )); then
        duration="0$duration"
    fi
    echo "duration $duration" >> "$FRAME_FILE"
    
    # Decrease the number of frames to hold
    frames_to_hold=$((frames_to_hold - 1))
    if [ $frames_to_hold -lt 1 ]; then
        frames_to_hold=1
    fi
done

# Use ffmpeg to create the video
ffmpeg -f concat -safe 0 -i "$FRAME_FILE" -vf "fps=$FPS,format=yuv420p" -movflags +faststart "$OUTPUT_FILE"

# Clean up
# rm "$FRAME_FILE"

echo "Video created: $OUTPUT_FILE"
mpv $OUTPUT_FILE
# echo "Total frames: $total_frames"
# echo "Approx. duration: $(echo "scale=2; $total_frames / $FPS" | bc) seconds"
