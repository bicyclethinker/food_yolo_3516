#!/bin/sh

APP_DIR=/opt/food_ai

cd $APP_DIR || exit 1

mkdir -p $APP_DIR/output/output_dump
mkdir -p $APP_DIR/output/logs

export LD_LIBRARY_PATH=$APP_DIR/lib:$LD_LIBRARY_PATH

$APP_DIR/bin/food5_single_test \
  --model $APP_DIR/model/food5_yolov5s_best.om \
  --input $APP_DIR/data/test_input.bin \
  --labels $APP_DIR/model/food5_labels.txt \
  --output $APP_DIR/output/output_dump \
  > $APP_DIR/output/logs/single_test.log 2>&1

echo "single test finished."
echo "check output:"
ls -lh $APP_DIR/output/output_dump
