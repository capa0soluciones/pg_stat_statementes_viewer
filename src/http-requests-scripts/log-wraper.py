import os
import sys
import argparse
import json

def split_log(logfile, output_dir, length_threshold=None, filter_word=None, min_duration=None):
    with open(logfile, 'r') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        # Encontrar el índice donde comienza el JSON
        json_start_index = line.find('{')
        if json_start_index != -1:
            json_str = line[json_start_index:]
            try:
                log_data = json.loads(json_str)
                duration = float(log_data.get('duration', 0))
                if (length_threshold is None or len(line) > length_threshold) and \
                   (filter_word is None or filter_word in line) and \
                   (min_duration is None or duration > min_duration):
                    output_file_path = os.path.join(output_dir, f'log_line_{index + 1}.txt')
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(line.strip())
            except ValueError:
                # Ignore lines that are not in JSON format
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split log file based on line length and optionally filter by specific word and minimum duration.")
    parser.add_argument('-f', '--file', help="Log file to split", required=True)
    parser.add_argument('-o', '--output', help="Output directory", required=True)
    parser.add_argument('-l', '--length', type=int, help="Minimum line length threshold")
    parser.add_argument('-t', '--text', help="Filter lines by specific word")
    parser.add_argument('-d', '--duration', type=float, help="Minimum duration threshold")
    args = parser.parse_args()

    logfile = args.file
    output_dir = args.output
    length_threshold = args.length
    filter_word = args.text
    min_duration = args.duration

    if not os.path.isfile(logfile):
        print(f"Error: The file {logfile} does not exist.")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"Error: The directory {output_dir} does not exist.")
        sys.exit(1)

    split_log(logfile, output_dir, length_threshold, filter_word, min_duration)
