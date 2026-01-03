import re
import argparse
import os

def time_to_milliseconds(time_str):
    """Convert time string (HH:MM:SS,mmm) to milliseconds."""
    hours, minutes, seconds, milliseconds = map(int, re.split(':|,', time_str))
    return (hours * 60 * 60 * 1000) + (minutes * 60 * 1000) + (seconds * 1000) + milliseconds

def milliseconds_to_time(ms):
    """Convert milliseconds to time string (HH:MM:SS,mmm)."""
    hours = ms // (60 * 60 * 1000)
    minutes = (ms % (60 * 60 * 1000)) // (60 * 1000)
    seconds = (ms % (60 * 1000)) // 1000
    milliseconds = ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def process_srt_file(input_file, output_file):
    """Process the SRT file to remove time intervals between lines."""
    cut_point = 0

    with open(input_file, mode='r', encoding='utf-8') as srt_file, \
         open(output_file, mode='w', encoding='utf-8') as srt_cut_file:

        for line in srt_file:
            if '-->' in line:
                line = line.strip()
                start, end = line.split(' --> ')

                start_point = time_to_milliseconds(start)
                end_point = time_to_milliseconds(end)

                time_difference = start_point - cut_point
                start_point = cut_point
                end_point -= time_difference
                cut_point = end_point

                start = milliseconds_to_time(start_point)
                end = milliseconds_to_time(end_point)

                srt_cut_file.write(f"{start} --> {end}\n")
            else:
                srt_cut_file.write(line)

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Process SRT file to remove time intervals between subtitles.")
    parse.add_argument('--input', '-i', type=str, help='Input SRT file name (without extension)', required=True)
    args = parse.parse_args()

    input_file_path = f"{args.input}"
    output_file_path = os.path.splitext(input_file_path)[0] + "_cut.srt"

    try:
        process_srt_file(input_file_path, output_file_path)
        print(f"Processed file saved as: {output_file_path}")
    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")