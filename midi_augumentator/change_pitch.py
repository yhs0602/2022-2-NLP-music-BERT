# data directory structure
# goal: midi -> whose
# augmentation: pitch shift, time shift, velocity shift, note shift
# output: whose_what_whichaug_amount

import argparse
import os

from mido import MidiFile, MidiTrack
from mido.midifiles import second2tick, midifiles

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


def augment_of_dir(dir, pitch_change, tempo_change, velocity_change):
    target_dir = (
        dir + "_pitch_" + str(pitch_change) + "_tempo_" + str(tempo_change) + "/"
    )
    os.mkdir(target_dir)
    for file in os.listdir(dir):
        if not file.lower().endswith(".mid"):
            continue
        player = int(file.split("-")[0].replace("p", ""))
        part = file.split("-")[1].split(".")[0]
        print("player: ", player, " part: ", part)
        augment_one_file(
            dir + file, target_dir + file, pitch_change, tempo_change, velocity_change
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
    augment_of_dir(
        args.dir,
        args.pitch_change,
        tempo_change=args.tempo,
        velocity_change=args.velocity,
    )
