docker run -it --name triton --net=host -v /home/work/project/modelzoo/triton/models/:/models nvcr.io/nvidia/tritonserver:22.11-py3 bash


docker run -itd --name triton_test --gpus=all -p18000:8000 -p18001:8001 -p18002:8002 -v E:\\pythonFile\\modelzoo\\triton\\models:/models nvcr.io/nvidia/tritonserver:22.11-py3 bash
./bin/tritonserver --model-store=/models  # 启动 triton
