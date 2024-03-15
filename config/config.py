SEED = 42

BUCKET_NAME = 'yahoofinances-stockprice'

TRAIN_CSV_PATH = f's3://{BUCKET_NAME}/train/train.csv'
TEST_CSV_PATH = f's3://{BUCKET_NAME}/test/test.csv'

OUTPUT = f's3://{BUCKET_NAME}/output'

