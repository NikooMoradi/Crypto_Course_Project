#!/usr/bin/env sh
#SBATCH --partition=GPUampere
#SBATCH --time=02:00:00
#SBATCH --job-name=test
#SBATCH --output=test_%j.txt
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --mem=32G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4

CONDA_PREFIX=/homes/nmoradi/.conda/envs/temp

eval "$(conda shell.bash hook)"
conda activate temp
srun -N1 env | grep CONDA_PREFIX


# python3 /homes/nmoradi/test/codes/handle_NaN.py
# python3 /homes/nmoradi/test/codes/handle_NaN_mednext.py
#SBATCH --job-name=handle_NaN
#SBATCH --output=handle_NaN_506_fold4_%j.txt
# python3 /homes/nmoradi/test/codes/create_splits.py
python3 /homes/nmoradi/sut/main.py
# python3 /homes/nmoradi/test/codes/my_ensembling_nifti.py
# python3 /homes/nmoradi/test/codes/move_and_rename.py
# python3 /homes/nmoradi/test/codes/move_BraTS_files.py
# python3 /homes/nmoradi/test/codes/seperate_zeros.py
# python3 /homes/nmoradi/test/codes/copy_models.py
# python3 /homes/nmoradi/test/codes/Calculate_metrics.py
# python3 /homes/nmoradi/test/codes/convert_pkl_to_json.py


# python3 /homes/nmoradi/test/codes/ensembling_nnUNet.py -i /homes/nmoradi/test/evaluation/ensembled_prediction_preRT/nnUNet_predictions /homes/nmoradi/test/evaluation/ensembled_prediction_preRT/MedNext_predictions -o /homes/nmoradi/test/evaluation/ensembled_prediction_preRT/ensembled_predictions --save_npz

echo 'finished run'
