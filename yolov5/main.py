import time

from process import *

import openvino.runtime as ov


def infer():
    core = ov.Core()
    model = core.read_model("yolov5s.xml")
    compiled_model = core.compile_model(model, "CPU")

    rec_input_layer = next(iter(compiled_model.inputs))
    rec_output_layer = next(iter(compiled_model.outputs))

    infer_request = compiled_model.create_infer_request()
    start=time.time()
    infer_request.infer(inputs={"images": get_input_tensor()})
    det_results = infer_request.get_tensor(rec_output_layer).data

    end=time.time()
    print("cost ",end-start)

    get_result_classify(det_results[0])


infer()
