# data directory structure
# goal: midi -> whose
# augmentation: pitch shift, time shift, velocity shift, note shift
# output: whose_what_whichaug_amount

from mido import Message, MidiFile, MidiTrack
from mido.midifiles import second2tick, midifiles
import os


def augment_of_dir(dir, amount):
    target_dir = dir + '_pitch_' + str(amount) + '/'
    os.mkdir(target_dir)
    for file in os.listdir(dir):
        if not file.lower().endswith('.mid'):
            continue
        player = int(file.split('-')[0].replace('p', ''))
        part = file.split('-')[1].split('.')[0]
        print("player: ", player, " part: ", part)
        pitch_augmentation(dir + file, target_dir + file, amount)


def pitch_augmentation(from_file, to_file, amount):
    mid = MidiFile(from_file)
    out_mid = MidiFile()
    out_track = MidiTrack()
    out_mid.tracks.append(out_track)
    for msg in mid:
        print(msg.time)
        msg.time = int(second2tick(msg.time, mid.ticks_per_beat, midifiles.DEFAULT_TEMPO))
        print(msg.time)
        if msg.type == 'note_on' or msg.type == 'note_off':
            # print(msg)
            msg.note += amount
            out_track.append(msg)
        else:

            out_track.append(msg)
    out_mid.save(to_file)


if __name__ == '__main__':
    augment_of_dir('Data/D958/', 12)
