import alsaaudio

def set_audio_levels(output_volume, input_volume):
    try:
        # Set output (playback) volume
        output_mixer = alsaaudio.Mixer('Master')
        output_mixer.setvolume(output_volume)
        
        # Set input (capture) volume
        input_mixer = alsaaudio.Mixer('Capture')
        input_mixer.setvolume(input_volume)
        
        print(f"Output volume set to {output_volume}%")
        print(f"Input volume set to {input_volume}%")
    except alsaaudio.ALSAAudioError as e:
        print(f"Error setting audio levels: {e}")

if __name__ == "__main__":
    # Set output volume to 80% and input volume to 70%
    set_audio_levels(80, 70)
