import torch
from second_tutorial import init_torch_model

model = init_torch_model()
x = torch.randn(1, 3, 256, 256)
# 直接修改模型无法达到我们想要的目的，实现动态的
with torch.no_grad():
    torch.onnx.export(model, (x, torch.tensor(3)),
                      "scrnn2.onnx",
                      opset_version=11,
                      input_names=['input', 'factor'],
                      output_names=['output'])
