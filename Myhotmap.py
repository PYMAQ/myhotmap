# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:48:56 2019

@author: haixinabcd
"""

import cv2
from PIL import  Image
import numpy as np
import random

class myhotmap:
    imglist0=[]
    colorlist0=[]
    def _draw_circle_8(self, x, y, cindex):
        r=self.r
        imglist0=self.imglist0
        
        imglist0[r + x][r + y]=cindex 
        imglist0[r - x][r + y]=cindex
        imglist0[r + x][r - y]=cindex
        imglist0[r - x][r - y]=cindex
        
    
        imglist0[r + y][r + x]=cindex
        imglist0[r - y][r + x]=cindex 
        imglist0[r + y][r - x]=cindex
        imglist0[r - y][r - x]=cindex 
        
        
    

    def _draw_circle_tobuf(self,imglist,xc,yc,w,h):
        r=self.r
        imglist0=self.imglist0
        allx=xc-r
        ally=yc-r
        for y in range(0,r*2+1):
            for x in range(0,r*2+1):               
                cindex= imglist0[y][x]              
                if (cindex>0):
                    if ((allx+x)>=0  and  (allx+x)<w):
                        if ( (ally+y)>=0 and  (ally+y)<h):
                            oindex=imglist[ally+y][allx+x]
                            if (cindex>oindex):
                                oindex=int(oindex/2)   # 最小颜色 取一半的id 累加
                            else:
                                cindex=int(cindex/2)                          
                            imglist[ally+y][allx+x]=oindex+cindex
        return imglist
    
 

    def _draw_circle_tojpg(self,imglist,img,w,h):
        colorlist=self.colorlist0
        clen=len(colorlist)-1
        for y in range(0,h):
            for x in range(0,w):               
                cindex= imglist[y][x]
                if (cindex>0):                    
                    if (cindex>clen):
                        cindex=clen                    
                    color=colorlist[cindex]
                    img.putpixel((x,y), color)                   
        return img       
    
#Bresenham's circle algorithm
    def _draw_circle(self,newr,fill, cindex):

        x = 0
        y = newr
        yi=0
        d = 3 - 2 * newr
        
        
        if (fill) :
            #如果填充（画实心圆）
            while (x <= y) :
                for yi in range (x,y+1):
                    self._draw_circle_8(x, yi,cindex)
                if (d < 0) :
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - y) + 10
                    y =y-1            
                x=x+1
        else:
            #如果不填充（画空心圆）
            while (x <= y):
                self._draw_circle_8(x, y,cindex)
                if (d < 0):
                    d = d + 4 * x + 6
                else:
                    d = d + 4 * (x - y) + 10
                    y =y-1            
                x=x+1



    def _hotmap_color1(self):
        cR = [ 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240 ]
        cG = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255 ]
        cB = [ 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    
        print(len(cR))
        for c0 in range(len(cR)):
            cc=(cR[c0],cG[c0],cB[c0])
            self.colorlist0.append(cc)
        


 
    def _rgb2hsl(self,rgb):
        rgb_normal = [[[rgb[0] / 255, rgb[1] / 255, rgb[2] / 255]]]
        hls = cv2.cvtColor(np.array(rgb_normal, dtype=np.float32), cv2.COLOR_RGB2HLS)
        return hls[0][0][0], hls[0][0][2], hls[0][0][1]  # hls to hsl
 
 
# HSL颜色转换为RGB颜色
    def _hsl2rgb(self,hsl):
        hls = [[[hsl[0], hsl[2], hsl[1]]]]  # hsl to hls
        rgb_normal = cv2.cvtColor(np.array(hls, dtype=np.float32), cv2.COLOR_HLS2RGB)
        return int(rgb_normal[0][0][0] * 255), int(rgb_normal[0][0][1] * 255), int(rgb_normal[0][0][2] * 255)
     
     
# HSL渐变色
    def _get_multi_colors_by_hsl(self,begin_color, end_color, color_count):
        if color_count < 2:
            return []
 
        colors = []
        hsl1 = self._rgb2hsl(begin_color)
        hsl2 = self._rgb2hsl(end_color)
        steps = [(hsl2[i] - hsl1[i]) / (color_count - 1) for i in range(3)]
        for color_index in range(color_count):
            hsl = [hsl1[i] + steps[i] * color_index for i in range(3)]
            colors.append(self._hsl2rgb(hsl))
     
        return colors
 



    def _hotmap_color2(self):
        color_count=30
        begin_color=(255,0,0)
        end_color=(0,255,0)   
        colorlist0=self._get_multi_colors_by_hsl(begin_color, end_color, color_count)
        
        
        begin_color=(0,255,0)
        end_color=(0,0,255)    
        colorlist1=self._get_multi_colors_by_hsl(begin_color, end_color, color_count)    
        self.colorlist0=colorlist0+colorlist1
        
    
        


#半径的圆，渐变表  r 半径
    def __init__(self,r):
        id=0
        self.r=r
        self.imglist0 = [([0] * (r*2+1)) for i in range((r*2+1))]        
        for n in range(r,0,-1):              #圆的半径的差            
            self._draw_circle(n,1,id)
            id=id+3    #颜色的渐变差
            
        #self._hotmap_color1()  #渐变色值1
        self._hotmap_color2()   #渐变色值2
        
        
    
#img   图片
#data   中心坐标   x y  
    def hotmap(self,img,data):
        h,w=img.size
        imglist = [([0] * w) for i in range(h)] #ditu
        for idd in data:
            x,y=idd
            self._draw_circle_tobuf(imglist,x,y,w,h)       
        _img =self._draw_circle_tojpg(imglist,img,w,h)
        return _img



def get_random(low,high):
 return((high-low)*random.random()+low)
 

 
if __name__ == '__main__':

    data=[]
    r=10
    img = cv2.imread("tu4.jpg")
    hp=myhotmap(r)
    for n in range(0,1080):
        x = int(get_random(0,800))
        y = int(get_random(0,650)) 
        data.append([x,y])
        
    
    bimg=Image.fromarray(img)
    hit_img=hp.hotmap(bimg,data)    
    black_img=np.asarray(hit_img)
    cv2.imshow("black_img",black_img);
    cv2.waitKey()
    cv2.destroyAllWindows()
    
