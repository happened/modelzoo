
import torch
from first_tutorial import init_torch_model

model = init_torch_model()

# 导出模型
x=torch.randn(1,3,256,256)
with torch.no_grad():
    torch.onnx.export(model,x,"scrnn.onnx",
                      opset_version=11,
                      input_names=['input'],
                      output_names=['output'])

exit(0)