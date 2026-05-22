#!/bin/bash

BOARD_IP=192.168.1.168
BOARD_USER=root
BOARD_DIR=/opt/food_ai

echo "[deploy] create board dirs..."
ssh ${BOARD_USER}@${BOARD_IP} "mkdir -p \
  ${BOARD_DIR}/bin \
  ${BOARD_DIR}/model \
  ${BOARD_DIR}/config \
  ${BOARD_DIR}/data \
  ${BOARD_DIR}/web/assets \
  ${BOARD_DIR}/history \
  ${BOARD_DIR}/output/input_dump \
  ${BOARD_DIR}/output/output_dump \
  ${BOARD_DIR}/output/snapshots \
  ${BOARD_DIR}/output/logs \
  ${BOARD_DIR}/lib"

echo "[deploy] copy model..."
scp ../model/food5_yolov5s_best.om ${BOARD_USER}@${BOARD_IP}:${BOARD_DIR}/model/
scp ../model/food5_labels.txt ${BOARD_USER}@${BOARD_IP}:${BOARD_DIR}/model/

echo "[deploy] copy config and data..."
scp ../config/*.json ${BOARD_USER}@${BOARD_IP}:${BOARD_DIR}/config/
scp ../data/nutrition_db.json ${BOARD_USER}@${BOARD_IP}:${BOARD_DIR}/data/

echo "[deploy] copy web..."
scp -r ../web/* ${BOARD_USER}@${BOARD_IP}:${BOARD_DIR}/web/

echo "[deploy] copy bin..."
scp ../bin/* ${BOARD_USER}@${BOARD_IP}:${BOARD_DIR}/bin/

echo "[deploy] chmod..."
ssh ${BOARD_USER}@${BOARD_IP} "chmod +x ${BOARD_DIR}/bin/*.sh ${BOARD_DIR}/bin/food*"

echo "[deploy] done."
