import pickle
from basicts.utils.adjacent_matrix_norm import *

def load_pkl(pickle_file):
    try:
        with open(pickle_file, 'rb') as f:
            pickle_data     = pickle.load(f)
    except UnicodeDecodeError as e:
        with open(pickle_file, 'rb') as f:
            pickle_data     = pickle.load(f, encoding='latin1')
    except Exception as e:
        print('Unable to load data ', pickle_file, ':', e)
        raise
    return pickle_data

def dump_pkl(obj, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def load_adj(file_path, adj_type):
    try:
        # METR and PEMS_BAY
        sensor_ids, sensor_id_to_ind, adj_mx = load_pkl(file_path)
    except:
        # PEMS04
        adj_mx = load_pkl(file_path)
    if adj_type == "scalap":
        adj = [calculate_scaled_laplacian(adj_mx).astype(np.float32).todense()]
    elif adj_type == "normlap":
        adj = [calculate_symmetric_normalized_laplacian(adj_mx).astype(np.float32).todense()]
    elif adj_type == "symnadj":
        adj = [symmetric_message_passing_adj(adj_mx).astype(np.float32).todense()]
    elif adj_type == "transition":
        adj = [transition_matrix(adj_mx).T]
    elif adj_type == "doubletransition":
        adj = [transition_matrix(adj_mx).T, transition_matrix(adj_mx.T).T]
    elif adj_type == "identity":
        adj = [np.diag(np.ones(adj_mx.shape[0])).astype(np.float32).todense()]
    elif adj_type == 'original':
        adj = adj_mx
    else:
        error = 0
        assert error, "adj type not defined"
    return adj, adj_mx