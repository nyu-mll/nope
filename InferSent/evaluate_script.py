from pragmatics_dataset.InferSent.models import NLINet
import torch
from data import get_nli, get_batch, build_vocab
import argparse
import numpy as np
import pandas as pd
import os

parser = argparse.ArgumentParser(description='NLI training')
# paths
parser.add_argument("--nlipath", type=str, default='dataset/SNLI/', help="NLI data path (SNLI or MultiNLI)")
parser.add_argument("--outputdir", type=str, default='savedir/', help="Output directory")
parser.add_argument("--word_emb_path", type=str, default="dataset/fastText/crawl-300d-2M.vec", help="word embedding file path")


params, _ = parser.parse_known_args()


def load_model(model_path):
    params_model = get_params(model_path)
    nli_net = NLINet(params_model)
    nli_net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    return nli_net, params_model


def get_params(model_path):

    # extract parameters from checkpoint name
    params = model_path.split(".")[0]
    params = params.split("/")[-1]
    params = {p.split("=")[0]: p.split("=")[1] for p in params.split(",")}

    # rename/type certain parameters
    params['bsize'] = int(params['batch_size'])
    params['fc_dim'] = int(params['fc_dim'])

    # add default values for required parameters
    params['nonlinear_fc'] = 0
    params['n_classes'] = 3
    params['dpout_fc'] = 0
    params['project_bow'] = 0
    params['word_emb_dim'] = 300

    # modify params dict depending on encoder type
    if "encoder_type" in params:    # i.e. if BOW was used
        params['enc_lstm_dim'] = 1
        for k in ['batch_size', 'jobname', 'n_restarts', 'seed']:
            params.pop(k)
    else:                           # i.e. if InferSent was used
        params['dpout_model'] = float(params['dpout_model'])
        params['enc_lstm_dim'] = int(params['enc_lstm_dim'])
    return params



# eval_model("savedir/jobname=bow_combined,encoder_type=BOW,batch_size=128,fc_dim=256,pool_type=mean,n_restarts=4,dataset=combined,seed=445.final.pkl")

def prepare_data(eval_data_path):
    df = pd.read_json(eval_data_path, orient="records", lines=True)
    word_vec = build_vocab(list(df["hypothesis"]) + list(df["premise"]), params.word_emb_path)
    bos, eos = ("<p>", "</p>")

    s1 = [[bos] +
          [word for word in sent.split() if word in word_vec] +
          [eos] for sent in df["premise"]]
    s2 = [[bos] +
          [word for word in sent.split() if word in word_vec] +
          [eos] for sent in df["hypothesis"]]
    labels = np.array(df["label"])
    return s1, s2, labels, word_vec


def evaluate_model(nli_net, s1, s2, labels, word_vec, batch_size, word_emb_dim=300):

    for stidx in range(0, len(s1), batch_size):
        s1_batch, s1_len = get_batch(s1[stidx:stidx + batch_size],
                                     word_vec, word_emb_dim)
        s2_batch, s2_len = get_batch(s2[stidx:stidx + batch_size],
                                     word_vec, word_emb_dim)

        output = nli_net((s1_batch, s1_len), (s2_batch, s2_len))
        pred = output.data.max(1)[1]
        pass


nli_net, params_model = load_model("savedir/jobname=bow_combined,encoder_type=BOW,batch_size=128,fc_dim=256,pool_type=mean,n_restarts=4,dataset=combined,seed=445.final.pkl")
s1, s2, labels, word_vec = prepare_data("dataset/combined/dev.jsonl")
evaluate_model(nli_net, s1, s2, labels, word_vec, params_model['bsize'])