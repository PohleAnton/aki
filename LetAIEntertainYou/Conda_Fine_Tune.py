'''funtioniert nur mit conda'''

#run
'''
conda create -n unsloth python=3.10 -y
conda activate unsloth
conda install -c conda-forge pytorch
pip install xformers
pip install xformers

linux only:
pip install huggingface_hub ipython "unsloth[colab] @ git+https://github.com/unslothai/unsloth.git" "unsloth[conda] @git+https://github.com/unslothai/unsloth.git"
win:
conda install -c conda-forge pytorch       
pip install xformers                                                
pip install huggingface_hub ipython
pip install git+https://github.com/unslothai/unsloth.git
pip install "unsloth[colab] @ git+https://github.com/unslothai/unsloth.git"
                  
has to run in linux/wsl
for me:
/home/meth/miniconda3/bin/python
-->
\\wsl$\Ubuntu\home\meth\minconda3\bin\python



'''