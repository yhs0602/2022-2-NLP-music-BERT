import argparse
import csv
import os
import zipfile

argparser = argparse.ArgumentParser(
    description="Generate total_augmented.csv and augmented_segmented_midi.zip file from total.csv and midi files in the augmented directory."
)
argparser.add_argument(
    "augmented_dir", type=str, help="directory of augmented midi files with a trailing slash"
)

if __name__ == "__main__":
    args = argparser.parse_args()
    file = open("./total.csv", encoding="utf-8")
    csvreader = csv.reader(file)
    outfile = open("./total_augmented.csv", encoding="utf-8", mode="w")
    csvwriter = csv.writer(outfile)
    header = next(csvreader)
    csvwriter.writerow(header)
    table = {}
    for row in csvreader:
        user = row[0]
        dataID = row[1]
        filename = row[2]
        misc = row[3:]
        table[filename] = row  # 'wav' does not matter
        csvwriter.writerow(row)
    # find max dataID
    max_dataID = 0
    for row in table.values():
        if int(row[1]) > max_dataID:
            max_dataID = int(row[1])
    max_dataID += 1
    print("max_dataID:", max_dataID)
    # iterate over the augmented files
    # Schubert_D960_mv2_8bars_1_08.wav
    # file paths should be flat
    # e.g. Schubert_D960_mv2_8bars_1_08_pitch_10_tempo_100_velocity_100.wav
    not_found = []
    for filename in os.listdir(args.augmented_dir):
        if not filename.lower().endswith(".mid"):
            continue
        # get the original file name
        original_filename = filename.split("_pitch_")[0] + ".wav"
        # get the original row
        original_row = table.get(original_filename)
        if original_row is None:
            print("original file not found:", original_filename)
            not_found.append(original_filename.replace(".wav", ".mid"))
            continue
        # create a new row
        new_row = original_row.copy()
        new_row[1] = str(max_dataID)
        new_row[2] = filename
        csvwriter.writerow(new_row)
        max_dataID += 1
    file.close()
    outfile.close()
    print("csv file generated")
    with zipfile.ZipFile('augmented_segmented_midi.zip', 'w') as myzip:
        with zipfile.ZipFile('segmented_midi.zip', 'r') as original_zip:
            for filename in original_zip.namelist():
                myzip.writestr(filename, original_zip.read(filename))
        for filename in os.listdir(args.augmented_dir):
            if not filename.lower().endswith(".mid"):
                continue
            if filename in not_found:
                print("Skipping not found:", filename)
                continue
            myzip.write(args.augmented_dir + filename, filename)
    print("zip file generated")
