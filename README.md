# Music XAI Improvement

Author: 강성현, 양현서, Richard Novenius

## Fine Tuning
```
branch: ludrex
```
- method:
```shell
blah 
```
- Generated pitch = -6, -5, -4, -3, ..., +12
- Generated tempo = 60, 120, 180
- Generated velocity = 50, 90
- Generated file name example = `{original_filename}_{pitch}_-12_{tempo}_120_{velocity}_90.mid`
- Then run modified `python map_midi_to_label.py` to generate `midi_label_map_apex_reg_cls.json` file.
- Then run modified `python -u gen_xai.py xai` to generate `xai_data_raw_apex_reg_cls_augmented` folder.
- Then run modified `bash scripts/binarize_xai.sh xai` to generate `xai_data_bin_apex_reg_cls_augmented` folder.
- Then run modified `scripts/train_xai_base_small.sh` to train the model. 

## Data Augmentation
```
branch: attempt/augmentation
```
- method:
```shell
cd midi_augmentator
pip install -r requirements.txt # mido
python augmentation.py ../processed/segmented_midi/ --pitch_range=-6_12_1 --tempo_range 60_180_60 --velocity_range 50_90_40 
```
- Generated pitch = -6, -5, -4, -3, ..., +12
- Generated tempo = 60, 120, 180
- Generated velocity = 50, 90
- Generated file name example = `{original_filename}_{pitch}_-12_{tempo}_120_{velocity}_90.mid`
- Then run modified `python map_midi_to_label.py` to generate `midi_label_map_apex_reg_cls.json` file.
- Then run modified `python -u gen_xai.py xai` to generate `xai_data_raw_apex_reg_cls_augmented` folder.
- Then run modified `bash scripts/binarize_xai.sh xai` to generate `xai_data_bin_apex_reg_cls_augmented` folder.
- Then run modified `scripts/train_xai_base_small.sh` to train the model.