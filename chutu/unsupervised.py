# -*- coding: utf-8 -*-
import sys
import train_sample
from pre import *
import supervised_methods
if __name__ == '__main__':
    # D:\\shapedata\\data\\2012-before....D:\\shapedata\\data\\2013-after....D:\\shapedata\\data\\diff.dat....D:\\shapedata\\data\\sample.dat
    #Img_fileName="d:\\shapedata\\orag1\\2016-spectral1.img"
    #Img_fileName2="d:\\shapedata\\orag1\\2017-spectral1.img"
    #fileName_choose3="d:\\shapedata\\result\\diff2.dat"
    #fileName_choose4="d:\\shapedata\\result\\sample2.dat"
    #save_path="d:\\shapedata\\result\\sampfsfsf.tif"
    Img_fileName=sys.argv[1]
    Img_fileName2=sys.argv[2]
    fileName_choose3=sys.argv[3]
    fileName_choose4=sys.argv[4]
    Save_path=sys.argv[5]
    print('--------- Hello World ----------')
    sys.stdout.flush()
    print('1')
    sys.stdout.flush()
    print('-- {},{},{},{} ------'.format(Img_fileName,Img_fileName2,fileName_choose3,fileName_choose4))
    sys.stdout.flush()
    print('---- difference Start ------')
    sys.stdout.flush()
    print('5')
    sys.stdout.flush()
    try:
        result = train_sample.difference(Img_fileName, Img_fileName2)
        print('---- difference End ------')
        sys.stdout.flush()
        print('25')
        sys.stdout.flush()
        print('---- saveimage Start ------')
        sys.stdout.flush()
        saveimage(result, fileName_choose3, Img_fileName)
        print('---- saveimage End ------')
        print('35')
        sys.stdout.flush()
        print('---- train_sample Start ------')
        sys.stdout.flush()
        result = train_sample.train_sample(Img_fileName, Img_fileName2)
        print('---- train_sample End ------')
        sys.stdout.flush()
        print('45')
        sys.stdout.flush()
        print('---- saveimage Start ------')
        sys.stdout.flush()
        saveimage(result, fileName_choose4, Img_fileName)
        print('---- saveimage End ------')
        sys.stdout.flush()
        print('55')
        sys.stdout.flush()
        print('---- Supervised_methods Start ------')
        sys.stdout.flush()
        cd_array = supervised_methods.Supervised_methods(fileName_choose3, fileName_choose4,'ELM')
        print('---- Supervised_methods End ------')
        sys.stdout.flush()
        print('65')
        sys.stdout.flush()
        print('---- saveimage Start ------')
        sys.stdout.flush()
        saveimage(cd_array, Save_path, fileName_choose3)
        print('---- saveimage End ------')
        sys.stdout.flush()
    except:
        pass
    print('70')
    sys.stdout.flush()