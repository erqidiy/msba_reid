#!/usr/bin/env bash
GPUS='0'

CUDA_VISIBLE_DEVICES=$GPUS python3 tools/self_train.py -cfg='configs/softmax_triplet.yml' \
DATASETS.NAMES '("competition1910",)'  \
DATASETS.TEST_NAMES 'competition1910' \
INPUT.SIZE_TRAIN '[256, 128]' \
INPUT.SIZE_TEST '[256, 128]' \
SOLVER.IMS_PER_BATCH '78' \
MODEL.NAME 'resnet101' \
MODEL.WITH_IBN 'True' \
MODEL.BACKBONE 'resnet101' \
MODEL.VERSION 'resnet101_ibn_bs63' \
SOLVER.OPT 'adam' \
SOLVER.LOSSTYPE '("softmax", "triplet")' \
MODEL.PRETRAIN_PATH '/media/tomheaven/MacOS/Users/tomheaven/.cache/torch/checkpoints/resnet101_ibn_a.pth.tar' \
TEST.WEIGHT 'logs/competition1910/resnet101_ibn_bs63/ckpts/model_best.pth'