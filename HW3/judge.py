#!/usr/bin/env python3
import os
import sys

import special

def read(filename):
    with open(filename, 'rb') as fp: return fp.read()

def run(ifn):
    #c = 'python3 -B AC_Code.py'
    c = 'python -B AC_Code.py'
    #c = '1189.exe'
    return os.system("%s < %s > %s"%(c,ifn,'slave.out'))

def main():
    score = 0
    for subtask in eval(read('subtasks.py')):        
        for trial in subtask[1:]:
            ifn, ofn, tl, ml, ol, dfns, wdfns, thsd = trial
            ts_psnr, ts_ssim = thsd
            print('%s '%ifn, end='')
            res = run(ifn)
            ResStr = ''
            if res != 0:
                ResStr = 'RE 0'
            else:
                waLine = os.system('python ./special %s %s slave.out' % (ifn, ofn))
                if waLine != 0:
                    ResStr = "WA 0 QQ" 
                else:
                    cmpInfo = ''
                    waLinef = ''
                    for wdfn in wdfns:
                        try:
                            psnr = special.PSNR(wdfn[1],wdfn[0])
                            ssim = special.SSIM(wdfn[1],wdfn[0])
                        except Exception as e:
                            psnr = 0
                            ssim = 0
                            waLinef += "output file name is wrong! "
                        if psnr<ts_psnr:
                            waLinef += 'PSNR<%d '%(ts_psnr)
                        if ssim<ts_ssim:
                            waLinef += 'SSIM<%.2f '%(ts_ssim)
                        if(os.path.exists(wdfn[0])):
                            os.remove(wdfn[0])

                        cmpInfo += '\n\t'+wdfn[0]+" PSNR:"+str(psnr)+' '
                        cmpInfo += "SSIM:"+str(ssim)+' '
                        
                    if waLinef:
                        ResStr = "WA 0 " + waLinef + cmpInfo
                    else:
                        ResStr = "AC %d"%subtask[0] + " " + cmpInfo   
                        score += subtask[0]
            print(ResStr)
    print(score)


if __name__ == '__main__':
    main()
    input('press enter to continue...')
