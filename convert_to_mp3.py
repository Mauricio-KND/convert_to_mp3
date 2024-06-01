import os
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, error

script_version = "1.0.1"

def attach_cover_art(mp3_file, image_file):
    mp3 = MP3(mp3_file, ID3=ID3)

    # add ID3 tag if it doesn't exist
    try:
        mp3.add_tags()
    except error:
        pass

    with open(image_file, 'rb') as img:
        mp3.tags.add(APIC(
            encoding=3,
            mime='image/jpeg' if image_file.endswith('.jpg') else 'image/png',
            type=3,
            desc='Cover',
            data=img.read()
        ))

    mp3.save()

def convert_to_mp3(input_file, output_file, input_extension, image_file=None):
    # Load audio with pydub
    audio = AudioSegment.from_file(input_file, format=input_extension)

    # Fetch metadata for FLAC files
    if input_extension == "flac":
        metadata = FLAC(input_file)
        tags = {
            "title": metadata.get("title", [None])[0],
            "artist": metadata.get("artist", [None])[0],
            "album": metadata.get("album", [None])[0],
            "year": metadata.get("date", [None])[0],
            "genre": metadata.get("genre", [None])[0],
        }
    else:  # Other file types might not have tags or handle them differently
        tags = {}

    # Get original sampling rate
    original_sampling_rate = audio.frame_rate

    # Convert audio to MP3 at 320 kbps and include metadata if available
    exported_audio = audio.export(output_file, format="mp3", bitrate="320k", tags=tags)

    # Fetch the exported MP3 sampling rate using mutagen
    exported_mp3 = MP3(output_file)
    output_sampling_rate = exported_mp3.info.sample_rate

    # Print the sampling rates of the files
    print(f"Original sampling rate: {original_sampling_rate} Hz")
    print(f"Output sampling rate: {output_sampling_rate} Hz")

    if exported_audio:
        exported_audio.close()  # Close the file if it was indeed opened

    # If there is an image, set the cover art
    if image_file:
        attach_cover_art(output_file, image_file)

if __name__ == "__main__":
    print(f"Audio file conversion script v{script_version}")
    input_folder = "file_to_convert"
    output_folder = "converted_file"

    # Make sure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("Converting audio files to mp3...")

    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)
        base_filename, _ = os.path.splitext(filename)

        # Check for image files with the same base name
        image_file = None
        for ext in ['.jpg', '.png']:
            potential_image = os.path.join(input_folder, base_filename + ext)
            if os.path.isfile(potential_image):
                image_file = potential_image
                break

        if filename.lower().endswith(".flac") or filename.lower().endswith(".wav"):
            input_extension = "flac" if filename.lower().endswith(".flac") else "wav"
            output_file = os.path.join(output_folder, f"{base_filename}.mp3")
            print(f"Converting {filename} to mp3...")

            # Perform the conversion and attach cover art if it exists
            convert_to_mp3(input_file, output_file, input_extension, image_file=image_file)

    print("Conversion completed successfully!")
