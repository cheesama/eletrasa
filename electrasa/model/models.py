from transformers import ElectraModel, ElectraTokenizer
from torchcrf import CRF

import torch
import torch.nn as nn
import torch.nn.functional as F

class KoELECTRAFineTuner(nn.Module):
    def __init__(self, intent_class_num, entity_class_num, default_model_path='monologg/koelectra-small-v2-discriminator'):
        super(KoELECTRAFineTuner, self).__init__()

        self.intent_class_num = intent_class_num
        self.entity_class_num = entity_class_num
        self.backbone = ElectraModel.from_pretrained(default_model_path)
        self.intent_embedding = nn.Linear(self.backbone.config.hidden_size, self.intent_class_num)
        self.entity_embedding = nn.Linear(self.backbone.config.hidden_size, self.entity_class_num)
        self.entity_featurizer = CRF(self.entity_class_num, batch_first=True)
        self.pad_token_id = pad_token_id

    def forward(self, tokens, entity_labels=None):
        feature = self.backbone(tokens)[0]

        intent_pred = self.intent_embedding(feature[:,0,:]) #forward only first [CLS] token
        entity_feature = self.entity_embedding(feature[:,1:,:]) #except first [CLS] token
        entity_pred = self.entity_featurizer.decode(entity_feature)

        if entity_labels is not None:
            entity_loss = self.entity_featurizer(entity_feature, entity_labels, reduction='mean')
            return intent_pred, entity_pred, entity_loss

        return intent_pred, entity_pred

        

        
        




