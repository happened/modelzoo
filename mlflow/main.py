import os
from random import random, randint
from mlflow import log_metric, log_param, log_artifacts
import mlflow
if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5002")
    mlflow.set_experiment("test")
    # 设置生成的记录的run name
    mlflow.start_run(run_name="hello")
    mlflow.set_tag("addition","备注")
    print(mlflow.get_artifact_uri())
    log_param("Param1", randint(0, 100))
    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/test.txt", "w") as f:
        f.write("hello world!")
    log_artifacts("outputs")
