import os
from easydict import EasyDict
import torch
# architecture 
from basicts.archs.MTGNN_arch import MTGNN_arch
# runner
from basicts.runners.MTGNN_runner import MTGNNRunner
from basicts.data.base_dataset import BaseDataset
from basicts.metrics.mae import masked_mae
from basicts.metrics.mape import masked_mape
from basicts.metrics.rmse import masked_rmse
from basicts.losses.losses import maksed_l1_loss
from basicts.utils.serialization import load_adj

CFG = EasyDict()

# ================= general ================= #
CFG.DESCRIPTION = 'MTGNN model configuration'
CFG.RUNNER  = MTGNNRunner
CFG.DATASET_CLS   = BaseDataset
CFG.DATASET_NAME  = "PEMS08"
CFG.DATASET_TYPE  = 'Traffic flow'
CFG.GPU_NUM = 1
CFG.SEED    = 1
CFG.CUDNN_ENABLED = True
CFG.METRICS = {
    "MAE": masked_mae,
    "RMSE": masked_rmse,
    "MAPE": masked_mape
}

# ================= model ================= #
CFG.MODEL = EasyDict()
CFG.MODEL.NAME  = 'MTGNN'
CFG.MODEL.ARCH  = MTGNN_arch
_, adj_mx = load_adj("datasets/" + CFG.DATASET_NAME + "/adj_mx.pkl", "doubletransition")
num_nodes = 170
adj_mx = torch.tensor(adj_mx)-torch.eye(num_nodes)
CFG.MODEL.PARAM = {
    "gcn_true"  : True, 
    "buildA_true": True,
    "gcn_depth": 2,
    "num_nodes": num_nodes,
    "predefined_A":adj_mx,
    "dropout":0.3,
    "subgraph_size":20,
    "node_dim":40,
    "dilation_exponential":1,
    "conv_channels":32,
    "residual_channels":32,
    "skip_channels":64,
    "end_channels":128,
    "seq_length":12,
    "in_dim":2,
    "out_dim":12,
    "layers":3,
    "propalpha":0.05,
    "tanhalpha":3,
    "layer_norm_affline":True
}
CFG.MODEL.FROWARD_FEATURES = [0, 1]            # traffic speed, time in day
CFG.MODEL.TARGET_FEATURES  = [0]                # traffic speed

# ================= optim ================= #
CFG.TRAIN = EasyDict()
CFG.TRAIN.LOSS = maksed_l1_loss
CFG.TRAIN.OPTIM = EasyDict()
CFG.TRAIN.OPTIM.TYPE = "Adam"
CFG.TRAIN.OPTIM.PARAM= {
    "lr":0.001,
    "weight_decay":0.0001,
}

# ================= train ================= #
CFG.TRAIN.CUSTOM            = EasyDict()          # MTGNN custom training args
CFG.TRAIN.CUSTOM.STEP_SIZE  = 100
CFG.TRAIN.CUSTOM.NUM_NODES  = num_nodes
CFG.TRAIN.CUSTOM.NUM_SPLIT  = 1

CFG.TRAIN.CLIP       = 5
CFG.TRAIN.NUM_EPOCHS = 100
CFG.TRAIN.CKPT_SAVE_DIR = os.path.join(
    'checkpoints',
    '_'.join([CFG.MODEL.NAME, str(CFG.TRAIN.NUM_EPOCHS)])
)
# train data
CFG.TRAIN.DATA          = EasyDict()
CFG.TRAIN.NULL_VAL      = 0.0
## read data
CFG.TRAIN.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.TRAIN.DATA.BATCH_SIZE   = 32
CFG.TRAIN.DATA.PREFETCH     = False
CFG.TRAIN.DATA.SHUFFLE      = True
CFG.TRAIN.DATA.NUM_WORKERS  = 2
CFG.TRAIN.DATA.PIN_MEMORY   = False
## curriculum learning
CFG.TRAIN.CL    = EasyDict()
CFG.TRAIN.CL.WARM_EPOCHS    = 0
CFG.TRAIN.CL.CL_EPOCHS      = 3
CFG.TRAIN.CL.PREDICTION_LENGTH  = 12


# ================= validate ================= #
CFG.VAL = EasyDict()
CFG.VAL.INTERVAL = 1
# validating data
CFG.VAL.DATA = EasyDict()
## read data
CFG.VAL.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.VAL.DATA.BATCH_SIZE     = 32
CFG.VAL.DATA.PREFETCH       = False
CFG.VAL.DATA.SHUFFLE        = False
CFG.VAL.DATA.NUM_WORKERS    = 2
CFG.VAL.DATA.PIN_MEMORY     = False

# ================= test ================= #
CFG.TEST = EasyDict()
CFG.TEST.INTERVAL = 1
# validating data
CFG.TEST.DATA = EasyDict()
## read data
CFG.TEST.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.TEST.DATA.BATCH_SIZE    = 32
CFG.TEST.DATA.PREFETCH      = False
CFG.TEST.DATA.SHUFFLE       = False
CFG.TEST.DATA.NUM_WORKERS   = 2
CFG.TEST.DATA.PIN_MEMORY    = False
