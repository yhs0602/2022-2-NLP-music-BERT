export PYTHONPATH=`pwd`
export CUDA_VISIBLE_DEVICES=0

# python eval_xai.py --task xai_M2P --head_name xai_head --checkpoint_file checkpoints/freeze_base/checkpoint_best_xai_apex_M2P_1e-4_base_1000_300_nofreeze.pt.pt  --data_dir processed/xai_data_bin_apex_reg_cls/0

python eval_xai.py --task xai_M2P --head_name xai_head --checkpoint_file checkpoints/freeze_base/checkpoint_best_xai_apex_M2P_1e-4_base_1000_300_nofreeze$i.pt.pt  --data_dir processed/xai_data_bin_apex_reg_cls/0
for (( i=0; i<=11; i++))
do
    python eval_xai.py --task xai_M2P --head_name xai_head --checkpoint_file checkpoints/freeze_base/checkpoint_best_xai_apex_M2P_1e-4_base_1000_300_freeze$i.pt.pt  --data_dir processed/xai_data_bin_apex_reg_cls/0
done
python eval_xai.py --task xai_M2P --head_name xai_head --checkpoint_file checkpoints/freeze_base/checkpoint_best_xai_apex_M2P_1e-4_base_1000_300_freezeall$i.pt.pt  --data_dir processed/xai_data_bin_apex_reg_cls/0
