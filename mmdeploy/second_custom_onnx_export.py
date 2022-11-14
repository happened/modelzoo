import torch
from second_custom_op import init_torch_model

model = init_torch_model()
x = torch.randn(1, 3, 256, 256)
factor = torch.tensor([1, 1, 3, 3], dtype=torch.float)

with torch.no_grad():
    torch.onnx.export(model, (x, factor),
                      "srcnn3.onnx",
                      opset_version=11,
                      input_names=['input', 'factor'],
                      output_names=['output'])