# -*- coding:utf-8 -*-



import matplotlib as mpl
import seaborn as sns
# mpl.use('TkAgg')
import matplotlib.pyplot as plt
sns.set_context(context="talk")
mpl.rcParams["font.sans-serif"] = ["SimHei"]

import torch
import argparse

def parser():
       parser = argparse.ArgumentParser(description="draw_attn_pic")
       parser.add_argument("-attn_path",type=str, default="E:\contrastive-attn-all\\checkpoint41_attn_layer_0")
       parser.add_argument("-save_dir",type=str, default="E:\contrastive-attn-all\\attn_pic\\")
       parser.add_argument("-source_file",type=str, default="D:\leetcode\draw\draw_attn\source_sentence")
       parser.add_argument("-target_file",type=str, default="D:\leetcode\draw\draw_attn\\target_sentence")
       parser.add_argument("-num_sentence", type=int, default=1 )
       parser.add_argument("-isTensor",type=int ,default=1)
       parser.add_argument("-cbar", type=int, default=1)
       parser.add_argument("-plt_show", type=int, default=1)
       return parser



def draw(args,ndata, xticklabels, yticklabels, ax):
    sns.heatmap(ndata,vmax=1,vmin=0,square=True,ax=ax,xticklabels=xticklabels, yticklabels=yticklabels,cbar=args.cbar)

def read_sentence(file_name,num_sentence):
    all_sentence =[]
    max_length = -1
    fp = open(file_name,encoding="utf-8")
    for line in fp.readlines():
        sentence = []
        length = 0
        for word in line.strip().split(" "):
            sentence.append(word)
            length+=1
        if max_length<length:
            max_length = length
        # print(max_length)
        if len(all_sentence)<num_sentence:
            all_sentence.append(sentence)
        else:
            break
    fp.close()
    return all_sentence,max_length


def draw_attn_pic(args,attn_path,save_dir, source_filename, target_filename, num_sentence):
    source_sentence, source_length = read_sentence(file_name=source_filename, num_sentence=num_sentence)
    target_sentence, target_length = read_sentence(file_name=target_filename, num_sentence=num_sentence)
    if args.isTensor:
        attn = torch.load(attn_path)
        if attn.dim() == 3:
            batch, tgt, src = attn.size()
            print("attn size:batch{}*tgt{}*src{}".format(batch, tgt, src))
            attn_numpy = attn.detach().numpy()
            for index in range(0, num_sentence):
                tmp_data = attn_numpy[index, :, :]
                fig, ax = plt.subplots(figsize=(15, 8))
                draw(args,tmp_data, xticklabels=source_sentence[index][:], yticklabels=target_sentence[index][:], ax=ax)
                if args.plt_show:
                    plt.show()
                fig.savefig(save_dir + "pic_index{}.jpg".format(index))
        elif attn.dim() == 4:
            batch, head, tgt, src = attn.size()
            print("attn size:batch{}*head{}*tgt{}*src{}".format(batch, head, tgt, src))
            attn_numpy = attn.detach().numpy()
            for index in range(0, num_sentence):
                for head_i in range(attn.size(1)):
                    tmp_data = attn_numpy[index, head_i, :, :]
                    fig, ax = plt.subplots(figsize=(15, 8))
                    draw(args,tmp_data, xticklabels=source_sentence[index][:], yticklabels=target_sentence[index][:], ax=ax)
                    if args.plt_show:
                        plt.show()
                    fig.savefig(save_dir + "pic_index{}_head{}.jpg".format(index+1, head_i))
        else:
            print("the size of attn is wrong")
            exit()

    else:
        print("I will add this part if I have time")
        exit()

def main(args):
    draw_attn_pic(args, args.attn_path, args.save_dir, args.source_filename,args.target_filename,args.num_sentence)


if __name__ == '__main__':
    parser = parser()
    args = parser.parse_args()
    main(args)

