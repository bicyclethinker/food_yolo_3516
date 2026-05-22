#!/bin/sh

APP_DIR=/opt/food_ai
WEB_PORT=8080

cd $APP_DIR || exit 1

mkdir -p $APP_DIR/output/logs
mkdir -p $APP_DIR/output/output_dump
mkdir -p $APP_DIR/history

export LD_LIBRARY_PATH=$APP_DIR/lib:$LD_LIBRARY_PATH

echo "[food_ai] start web server..."
busybox httpd -f -p $WEB_PORT -h $APP_DIR/web > $APP_DIR/output/logs/httpd.log 2>&1 &

echo "[food_ai] start main app..."
$APP_DIR/bin/food_ai_app \
  --config $APP_DIR/config/food_ai_config.json \
  > $APP_DIR/output/logs/food_ai.log 2>&1
