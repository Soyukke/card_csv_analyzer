import numpy as np
import sys
import unicodedata


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

def add_space(text, length):
    """
    INPUT: text: 文字列, length: 期待する文字列長
    OUTPUT: 長さlengthになるように半角スペースが加えられた文字列
    """
    len_text = get_east_asian_width_count(text)
    for i in range(length-len_text):
        text += ' '
    return text

if __name__=='__main__':
    argvs = sys.argv
    filename = argvs[1]
    flag_format = 0
    if len(argvs)>=3 and argvs[2]=='1':
        flag_format = 4

    vshop = []
    vvalue = []
    vshop_uniq = []
    vvalue_uniq = []

    with open(file=filename, mode='r', encoding='shift_jis') as f:
        for line in f:
            # print(line)
            spline = line.split(',')
            # 要素1が日付であることを確認
            if len(spline[0].split('/')) == 3:
                vshop.append(spline[1])
                vvalue.append(int(spline[2+flag_format]))
        vshop_uniq = np.unique(vshop)
        vvalue_uniq = np.zeros(shape=len(vshop_uniq), dtype=np.int)
        for i in range(len(vshop)):
            idx = vshop_uniq.tolist().index(vshop[i])
            vvalue_uniq[idx] += vvalue[i]
        
    # 店名で最大長
    n_shop_length = max([ get_east_asian_width_count(shop) for shop in vshop_uniq])
    n_value_length = max([len(str(value)) for value in vvalue_uniq])
    line_format = '{0}\t{1:' + str(n_value_length) + 'd}'
    for i in range(len(vshop_uniq)):
        line = line_format.format(add_space(vshop_uniq[i], n_shop_length), vvalue_uniq[i])
        print(line)
