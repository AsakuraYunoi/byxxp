#!/bin/bash

# 首先cd到脚本所在的文件夹
cd "$(dirname "$0")"

# 检查Python环境
if ! command -v python3 &> /dev/null
then
    echo "❌ 你的电脑不支持，请自行安装python3后重试！"
    exit
fi

# 检查是否安装了必要的Python库
REQUIRED_PACKAGES=("os" "re" "datetime" "chardet" "openpyxl" "pandas")
for package in "${REQUIRED_PACKAGES[@]}"
do
    python3 -c "
import pkg_resources
try:
    pkg_resources.get_distribution('${package}')
    print('${package} is installed')
except pkg_resources.DistributionNotFound:
    print('${package} is NOT installed')
"
done

# 提示用户正在安装组件
echo "⚠️ 组件安装中，请稍后！"

# 安装必要的Python库
pip3 install os re datetime chardet openpyxl pandas

# 运行Python脚本
python3 byxxp.py
