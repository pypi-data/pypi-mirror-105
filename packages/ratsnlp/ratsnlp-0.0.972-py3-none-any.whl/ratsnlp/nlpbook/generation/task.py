from transformers import PreTrainedModel
from transformers.optimization import AdamW
from pytorch_lightning import LightningModule
from ratsnlp.nlpbook.generation.arguments import GenerationTrainArguments
from torch.optim.lr_scheduler import ExponentialLR, CosineAnnealingWarmRestarts


class GenerationTask(LightningModule):

    def __init__(self,
                 model: PreTrainedModel,
                 args: GenerationTrainArguments,
    ):
        super().__init__()
        self.model = model
        self.args = args

    def configure_optimizers(self):
        if self.args.optimizer == 'AdamW':
            optimizer = AdamW(self.parameters(), lr=self.args.learning_rate)
        else:
            raise NotImplementedError('Only AdamW is Supported!')
        if self.args.lr_scheduler == 'cos':
            scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=1, T_mult=2)
        elif self.args.lr_scheduler == 'exp':
            scheduler = ExponentialLR(optimizer, gamma=0.5)
        else:
            raise NotImplementedError('Only cos and exp lr scheduler is Supported!')
        return {
            'optimizer': optimizer,
            'scheduler': scheduler,
        }

    def forward(self, **kwargs):
        return self.model(**kwargs)

    def step(self, inputs, mode="train"):
        loss, logits, _ = self.model(**inputs)
        self.log(f"{mode}_loss", loss, prog_bar=True, logger=True, on_step=True, on_epoch=True)
        return loss

    def training_step(self, inputs, batch_idx):
        return self.step(inputs, mode="train")

    def validation_step(self, inputs, batch_idx):
        return self.step(inputs, mode="val")

    def test_step(self, inputs, batch_idx):
        return self.step(inputs, mode="test")
