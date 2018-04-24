#!/bin/bash

echo "------------- Current Cuda Version -------------"
nvcc --version
NVCC_VER="$(nvcc --version)"
NVCC_VER_D=$(echo $NVCC_VER | cut -d',' -f 3,4)
echo ""
echo "Cuda ="$NVCC_VER_D

V91="V9.1"
V90="V9.0"
V80="V8.0"

current_ver = ""

if [[ $NVCC_VER_D == *"$V90"* ]]; then
    read -p "Switch to (8.0 / 9.1) ? " tar_cuda_ver
    current_ver="9.0"
elif [[ $NVCC_VER_D == *"$V80"* ]]; then
    read -p "Switch to (9.0 / 9.1) ? " tar_cuda_ver
    current_ver="8.0"
elif [[ $NVCC_VER_D == *"$V91"* ]]; then
    read -p "Switch to (8.0 / 9.0) ? " tar_cuda_ver
    current_ver="9.1"
fi

#echo "Switch to Cuda V" $tar_cuda_ver " ..."

CUDA_PATH="/usr/local/cuda-"$tar_cuda_ver
if [ -d $CUDA_PATH ]; then
    full_tar_ver=V$tar_cuda_ver
    if [[ $NVCC_VER_D == *"$full_tar_ver"* ]]; then
        echo "You are already in use of Cuda"$NVCC_VER_D
    else
        echo "Switching to Cuda "$full_tar_ver" ..."
	sudo ln -sfn $CUDA_PATH /usr/local/cuda
        echo "Switch to Cuda" $tar_cuda_ver " Success !!"
    fi
else
    echo "Incorrect Cuda Version "$tar_cuda_ver
fi

echo ""
echo "------------- Current Cuda Version -------------"
nvcc --version
