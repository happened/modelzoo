# MLFLOW 搭建


1. docker部署minio

    docker run -itd --name minio -p 9000:9000 -p 9001:9001  quay.io/minio/minio server /data --console-address ":9001"

2. docker部署mysql

   docker run -itd --name mysql -v /data2/mysql_data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 mysql

3. 启动mlflow ui

```bash
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin
export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:9000  #这个得是对应的api 的端口 minio制定的那个是console的端口
mlflow server --backend-store-uri mysql+pymysql://root:123456@localhost:3306/mlflow_test --host 127.0.0.1 \
  -p 5002 --default-artifact-root s3://mlflow  
```