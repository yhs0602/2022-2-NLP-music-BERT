# data directory structure
# goal: midi -> whose
# augmentation: pitch shift, time shift, velocity shift, note shift
# output: whose_what_whichaug_amount

import argparse
import os
from argparse import ArgumentTypeError

from mido import MidiFile, MidiTrack
from mido.midifiles import second2tick, midifiles


# https://stackoverflow.com/a/6512463/8614565
def parseNumList(string):
    values = string.split("_")
    # ^ (or use .split('-'). anyway you like.)
    if len(values) != 3:
        raise ArgumentTypeError(
            "'" + string + "' is not. Expected start-end-step forms like '0-5-1'"
        )
    start = int(values[0], 10)
    end = int(values[1], 10)
    step = int(values[2], 10)
    return list(range(start, end + 1, step))


parser = argparse.ArgumentParser(
    description="Modify pitches, tempos, and velocities of midi files."
)
parser.add_argument("dir", type=str, help="directory of midi files")
parser.add_argument(
    "--pitch_change",
    type=int,
    default=0,
    help="pitch change amount (+- integer)",
    required=False,
)
parser.add_argument("--tempo", type=int, default=100, help="set tempo", required=False)
parser.add_argument(
    "--velocity", type=int, default=100, help="change velocity", required=False
)
parser.add_argument(
    "--pitch_range", type=parseNumList, help="pitch range for batch", required=False
)
parser.add_argument(
    "--tempo_range", type=parseNumList, help="tempo range for batch", required=False
)
parser.add_argument(
    "--velocity_range",
    type=parseNumList,
    help="velocity range for batch",
    required=False,
)


def augment_of_dir(dir, pitch_change, tempo_change, velocity_change):
    filename_suffix = (
        "_pitch_"
        + str(pitch_change)
        + "_tempo_"
        + str(tempo_change)
        + "_velocity_"
        + str(velocity_change)
        + ".mid"
    )
    print("filename_suffix: ", filename_suffix)
    augmented_dir = "_augmented/"
    os.makedirs(dir + augmented_dir, exist_ok=True)
    for file in os.listdir(dir):
        if not file.lower().endswith(".mid"):
            continue
        # player = int(file.split("-")[0].replace("p", ""))
        # part = file.split("-")[1].split(".")[0]
        # print("player: ", player, " part: ", part)
        augment_one_file(
            dir + file,
            dir + augmented_dir + file.split(".")[0] + filename_suffix,
            pitch_change,
            tempo_change,
            velocity_change,
        )


def augment_one_file(from_file, to_file, pitch_change, tempo_change, velocity_change):
    mid = MidiFile(from_file)
    out_mid = MidiFile()
    out_track = MidiTrack()
    out_mid.tracks.append(out_track)
    tempo = int(midifiles.DEFAULT_TEMPO * tempo_change / 100.0)
    for msg in mid:
        msg.time = int(second2tick(msg.time, mid.ticks_per_beat, tempo))
        if msg.type == "note_on" or msg.type == "note_off":
            msg.note += pitch_change
            msg.velocity = int(msg.velocity * velocity_change / 100.0)
            out_track.append(msg)
        else:
            out_track.append(msg)
    out_mid.save(to_file)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.pitch_range:
        for pitch in args.pitch_range:
            if args.tempo_range:
                for tempo in args.tempo_range:
                    if args.velocity_range:
                        for velocity in args.velocity_range:
                            augment_of_dir(args.dir, pitch, tempo, velocity)
                    else:
                        augment_of_dir(args.dir, pitch, tempo, args.velocity)
            else:
                augment_of_dir(args.dir, pitch, args.tempo, args.velocity)
    else:  # FIXME: this is not generalized
        augment_of_dir(
            args.dir,
            args.pitch_change,
            tempo_change=args.tempo,
            velocity_change=args.velocity,
        )
