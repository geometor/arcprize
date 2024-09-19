#!/bin/bash

# Set variables
INPUT_DIR="./training"
ORIGINAL_OUTPUT="arc_animation_original.mp4"
HD_OUTPUT="arc_animation_720p.mp4"
FPS=24
FRAME_DURATION=$(echo "scale=10; 1 / $FPS" | bc)  # Duration of a single frame
RESOLUTION="1280:720"  # 720p resolution

# Get the number of PNG files
NUM_FILES=$(ls -1 "$INPUT_DIR"/*.png | wc -l)

# Generate a temporary file with frame durations
FRAME_FILE="frames.txt"
rm -f "$FRAME_FILE"
touch "$FRAME_FILE"

frames_to_hold=24  # Start by holding each image for 24 frames (1 second)

for file in "$INPUT_DIR"/*.png; do
    echo "file '$file'" >> "$FRAME_FILE"
    duration=$(echo "scale=10; $frames_to_hold * $FRAME_DURATION" | bc)  # Duration of a single frame
    
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

# Use ffmpeg to create the original video
ffmpeg -f concat -safe 0 -i "$FRAME_FILE" -vf "fps=$FPS,format=yuv420p" -movflags +faststart "$ORIGINAL_OUTPUT"

echo "Original video created: $ORIGINAL_OUTPUT"

# Convert the original video to 720p
ffmpeg -i "$ORIGINAL_OUTPUT" -vf "scale=$RESOLUTION:force_original_aspect_ratio=decrease,pad=$RESOLUTION:-1:-1:color=black" -c:a copy "$HD_OUTPUT"

echo "720p version created: $HD_OUTPUT"

# Clean up
# rm "$FRAME_FILE"

echo "Total frames: $NUM_FILES"
echo "Approx. duration: $(echo "scale=2; $NUM_FILES / $FPS" | bc) seconds"
