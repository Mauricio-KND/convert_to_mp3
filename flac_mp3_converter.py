import os
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.mp3 import MP3


def convert_flac_to_mp3(input_file, output_file):
    # Load FLAC file with pydub
    audio = AudioSegment.from_file(input_file, format="flac")

    # Get metadata from file with mutagen
    flac_metadata = FLAC(input_file)

    # Convert audio to MP3 at 320 kbps
    audio.export(output_file, format="mp3", bitrate="320k", tags={"title": flac_metadata.get("title")[0],
                                                                  "artist": flac_metadata.get("artist")[0],
                                                                  "album": flac_metadata.get("album")[0],
                                                                  "year": flac_metadata.get("date")[0],
                                                                  "genre": flac_metadata.get("genre")[0],
                                                                  })


if __name__ == "__main__":
    input_folder = "file_to_convert"
    output_folder = "converted_file"

    for filename in os.listdir(input_folder):
        if filename.endswith(".flac"):
            input_file = os.path.join(input_folder, filename)

            # Generate new filename
            base_filename = os.path.splitext(filename)[0]
            output_file = os.path.join(output_folder, f"{base_filename}.mp3")

            convert_flac_to_mp3(input_file, output_file)

    print("Conversion completed successfully!")
