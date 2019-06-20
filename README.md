# pytorch-attn
draw_attn

注：暂时只能用于画基于Tenosr的attn权重，文本文件的attn之后更新

数据：

attn：用pytorch的torch.save把attn权重保存下

source_sentence:源端的句子，长度需要和attn中src大小一致

target_sentence:源端的句子，长度需要和attn中tgt大小一致


用法：
python draw_attn.py -attn_path $attn_path -save_dir $save_dir -source_file $source_file -target_file $target_file

-attn_path是attn文件的路径

-source_file是源端句子文件的路径

-target_file是目标端句子文件的路径

-save_dir是存储的文件夹路径

-plt_show是否在窗口输出attn图片，默认是输出，也可以设置为0，不输出

-cbar：是否显示attn图片右侧的bar
