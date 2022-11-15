import onnxruntime
import torch
import numpy as np
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
    def forward(self,x):
        return torch.asinh(x)

from torch.onnx.symbolic_registry import  register_op

def asinh_symbolic(g,input,*,out=None):
    return g.op("Asinh",input)

register_op('asinh',asinh_symbolic,'',9)

model=Model()
input=torch.randn(1,3,10,10)
#torch.onnx.export(model,input,'asinh.onnx',opset_version=9)
#exit()
torch_output = model(input).detach().numpy()

sess = onnxruntime.InferenceSession('asinh.onnx')
ort_output = sess.run(None, {'0': input.numpy()})[0]
print(ort_output)
assert np.allclose(torch_output, ort_output)