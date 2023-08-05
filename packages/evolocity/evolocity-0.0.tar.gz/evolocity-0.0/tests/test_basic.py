import evolocity as evo
import numpy as np

test_seqs = [
    'MKTVRQERLKSIVRILERSKEPV',
    'SGAQLAEELSVSRQVIVQDIA',
    'SGAQLAYNIVASRQVIVQDIA',
    'YLRSLGTPRGYVLAGG',
    'KALTARQQEVFDLIRDHISQTGMPPTRAEIAQRLGFRS',
    'KALTARQQEIFDLIRDHISQTGMPPIVRAEIAQRLGFRS',
    'PNAAEEHLKALARKGVIEIVSGASR',
    'GIRLLQEE',
]

def test_einsum():
    from evolocity.tools.utils import prod_sum_obs, prod_sum_var, norm

    Ms, Mu = np.random.rand(5, 4), np.random.rand(5, 4)
    assert np.allclose(prod_sum_obs(Ms, Mu), np.sum(Ms * Mu, 0))
    assert np.allclose(prod_sum_var(Ms, Mu), np.sum(Ms * Mu, 1))
    assert np.allclose(norm(Ms), np.linalg.norm(Ms, axis=1))


def test_pipeline():
    adata = evo.pp.featurize_seqs(test_seqs)
    evo.pp.neighbors(adata)

    evo.tl.velocity_graph(adata)
    evo.tl.velocity_embedding(adata)

    evo.pl.velocity_embedding(adata)

    evo.tl.onehot_msa(adata)
    evo.tl.residue_scores(adata)
    evo.pl.residue_scores(adata)

    assert(adata.X.shape[0] == len(test_seqs))
    assert('seq' in adata.obs)
    assert('seqs_msa' in adata.obs)

def test_pipeline_tape():
    adata = evo.pp.featurize_seqs(test_seqs)
    evo.pp.neighbors(adata)

    evo.tl.velocity_graph(adata, model_name='tape')
    evo.tl.velocity_embedding(adata)

    evo.pl.velocity_embedding(adata)

    assert(adata.X.shape[0] == len(test_seqs))
    assert('seq' in adata.obs)
    assert(adata.uns['model'].name_ == 'tape')
