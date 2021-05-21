import itertools
import random

sweep = {
    "batch_size": [32, 64, 128],
    "dpout_model": [0, 0.1],
    "nonlinear_fc": [0, 1],
    "enc_lstm_dim": [1024, 2048],
    "n_enc_layers": [1, 3, 5],
    "fc_dim": [128, 512]
}

header = """#!/bin/bash
#SBATCH --job-name=infersent
#SBATCH --open-mode=append
#SBATCH --output=./%j_%x.out
#SBATCH --error=./%j_%x.err
#SBATCH --export=ALL
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=64G
#SBATCH -c 4

singularity exec --nv --overlay $SCRATCH/overlay-50G-10M.ext3:ro /scratch/work/public/singularity/cuda10.1-cudnn7-devel-ubuntu18.04-20201207.sif /bin/bash -c "

source /ext3/env.sh
conda activate

cd ../..
python train_nli.py {args}
"
"""

hps = []
for hp in sweep:
    hps.append([(hp, val) for val in sweep[hp]])

hp_settings = [list(x) for x in itertools.product(*hps)]
for i, experiment in enumerate(hp_settings):
    experiment.append(("seed", random.randint(0, 9999)))
    args = " ".join(f"--{hp[0]} {hp[1]}" for hp in experiment)
    outputmodelname = ",".join(f"{hp[0]}={hp[1]}" for hp in experiment)
    args += f" --outputmodelname {outputmodelname}"
    script = header.format(args=args)
    with open(f"sbatch_scripts/train_infersent_{i}.slurm", "w") as f:
        f.write(script)


