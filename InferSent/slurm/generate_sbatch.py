import itertools
import random
import argparse

parser = argparse.ArgumentParser(description="Generate a sweep of sbatch scripts")

# paths
parser.add_argument("--nlipath", type=str, default=None, help="NLI data path")
parser.add_argument("--outputdir", type=str, default=None, help="Output directory")
parser.add_argument("--logdir", type=str, default=None, help="Logs directory")

parser.add_argument("--encoder_type", nargs='?', default=None, help="see list of encoders")
parser.add_argument("--batch_size", nargs='*', type=int, default=None)
parser.add_argument("--dpout_model", nargs='*', type=float, default=None)
parser.add_argument("--enc_lstm_dim", nargs='*', type=int, default=None)
parser.add_argument("--fc_dim", nargs='*', type=int, default=None)
parser.add_argument("--pool_type", nargs='*', type=str, default=None, help="max or mean or both")
parser.add_argument("--project_bow", nargs='*', type=int, default=None)


args = parser.parse_args()

args_dict = args.__dict__.copy()
# for k in ["nlipath", "outputdir", "logdir"]:
#     args_dict.pop(k)
sweep = {k: args_dict[k] for k in args_dict if args_dict[k] != None}
for k in sweep:
    if type(sweep[k]) != list:
        sweep[k] = [sweep[k]]
# sweep = {
#     "batch_size": [32, 64],
#     "dpout_model": [0, 0.1],
#     "enc_lstm_dim": [1024, 2048],
#     "fc_dim": [256, 512],
# }

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
    outputmodelname = ",".join(f"{hp[0]}={hp[1]}" for hp in experiment if hp[0] not in ["nlipath", "outputdir", "logdir"])
    args += f" --outputmodelname {outputmodelname}"
    script = header.format(args=args)
    with open(f"sbatch_scripts/train_infersent_{i}.slurm", "w") as f:
        f.write(script)


