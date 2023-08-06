

def sparseFeature(feat_name, feat_num, embed_dim=4):
    """
    create dictionary for sparse feature
    :param feat_name: feature name
    :param feat_num: the total number of sparse features that do not repeat
    :param embed_dim: embedding dimension
    :return:
    """
    return {'feat_name': feat_name, 'feat_num': feat_num, 'embed_dim': embed_dim}