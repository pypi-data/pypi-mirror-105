import torch
from torch import nn
from easyrec.models import Base
from easyrec.layers import Dense


class Wide(Base):
    def __init__(self, wide_feature_columns, feature_index):
        super(Wide, self).__init__(wide_feature_columns, linear=True, is_build_feature_index=False)
        self.dense_len = sum([feat.dimension for feat in self.dense_feature_columns])
        self.dense_fc = nn.Linear(self.dense_len, 1)
        self.feature_index = feature_index

    def forward(self, X):
        dense_list = []
        for feat in self.dense_feature_columns:
            start, end = self.feature_index[feat.name]
            dense_list.append(X[:, start:end])
        dense_concat = torch.cat(dense_list, dim=-1)
        dense_out = self.dense_fc(dense_concat)

        emb_list = []
        for feat in self.sparse_feature_columns:
            start, end = self.feature_index[feat.name]
            sparse_input = X[:, start:end].long()
            emb_list.append(self.embedding_layers_dict[feat.name](sparse_input))
        emb_out = torch.sum(torch.cat(emb_list, dim=-1), dim=-1).reshape(emb_list[0].shape[0], 1)
        out = dense_out + emb_out
        return out


class Deep(Base):
    def __init__(self, deep_feature_columns, hidden_units, activation, feature_index):
        super(Deep, self).__init__(deep_feature_columns, is_build_feature_index=False)
        self.concat_size = sum([feat.dimension for feat in self.dense_feature_columns]) + sum(
            [feat.embedding_dim for feat in self.sparse_feature_columns])
        self.dense_layer = Dense(self.concat_size, hidden_units=hidden_units, activation=activation)
        self.fc = nn.Linear(hidden_units[-1], 1)
        self.feature_index = feature_index

    def forward(self, X):
        dense_list = []
        for feat in self.dense_feature_columns:
            start, end = self.feature_index[feat.name]
            dense_list.append(X[:, start:end])
        dense_concat = torch.cat(dense_list, dim=-1)

        emb_list = []
        for feat in self.sparse_feature_columns:
            start, end = self.feature_index[feat.name]
            sparse_input = X[:, start:end].long()
            emb_list.append(self.embedding_layers_dict[feat.name](sparse_input))
        emb_concat = torch.cat(emb_list, dim=-1).squeeze()
        all_concat = torch.cat([dense_concat, emb_concat], dim=-1)
        dense_output = self.dense_layer(all_concat)
        out = self.fc(dense_output)
        return out


class WideDeep(Base):
    def __init__(self, wide_feature_columns, deep_feature_columns, hidden_units=(256, 128, 64), activation='relu',
                 dnn_dropout=0., l1=0, l2=0):
        super(WideDeep, self).__init__(wide_feature_columns + deep_feature_columns,
                                       is_build_embedding_layer=False, is_build_feature_index=True)
        self.wide = Wide(wide_feature_columns, self.feature_index)
        self.deep = Deep(deep_feature_columns, hidden_units, activation, self.feature_index)

    def forward(self, X):
        return torch.sigmoid(self.wide(X) + self.deep(X))
