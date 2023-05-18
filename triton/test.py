import numpy as np
import torch
import tritonclient.http as httpclient
from PIL import Image

if __name__ == '__main__':
    triton_client = httpclient.InferenceServerClient(url='127.0.0.1:18000')

    image = Image.open('../data/cat.jpg')
    image = image.resize((224, 224), Image.ANTIALIAS)
    image = np.asarray(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    image = np.transpose(image, axes=[0, 3, 1, 2])
    image = image.astype(np.float32)

    inputs = []
    inputs.append(httpclient.InferInput('INPUT_0', image.shape, "FP32"))
    inputs[0].set_data_from_numpy(image, binary_data=False)
    outputs = []
    outputs.append(httpclient.InferRequestedOutput(
        'OUTPUT_0', binary_data=False,class_count=3))

    results = triton_client.infer('resnet50_pytorch', inputs=inputs, outputs=outputs)
    output_data0 = results.as_numpy('OUTPUT_0')

    print(output_data0.shape)
    print(output_data0)
