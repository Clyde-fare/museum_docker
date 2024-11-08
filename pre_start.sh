cd /workspace;
git clone https://github.com/xuebinqin/U-2-Net.git
git clone https://github.com/facebookresearch/sam2.git
cd sam2 && \
	pip install -e ".[notebooks]"
cd ..
cd sam2/checkpoints && \
	./download_ckpts.sh && \
cd ../..
mkdir /workspace/data;
mkdir /workspace/data/raw_data;

