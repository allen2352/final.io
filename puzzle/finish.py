from pygame import init,display,image,event,QUIT,quit,MOUSEBUTTONDOWN,MOUSEMOTION,KEYDOWN,mouse,transform,draw,font,key,K_w,K_v,K_a,K_d,K_j,Surface,K_s,K_i,K_p,K_x,K_z,K_u,K_k,K_o,K_l,K_c,K_b,mixer,K_UP,K_DOWN,K_LEFT,K_RIGHT,K_SPACE,time as py_time
from os import environ,_exit,listdir,path,rename,remove,getcwd,mkdir
from pygame.locals import RESIZABLE,FULLSCREEN
from math import sin,cos,pi,acos,atan,asin
from time import time,sleep,localtime
from random import random
from threading import Thread
from requests import get as requests_get
def Github_Download(filepath,save_path=None):
    url=f'https://github.com/allen2352/python/raw/master/{filepath}'
    r = requests_get(url)
    if r.status_code==200:
        if save_path!=None:
            open(save_path,'wb').write(r.content)
            return
        return r.content
    print(url)
    raise Exception('resources.py   filepath download error')
def create_dir(dir_name):
    if not path.isdir(dir_name):
        mkdir(dir_name)
def get_home_path():             #獲取類似 C:/Users/allen 之類的路徑
    return '/'.join(getcwd().replace('\\','/').split('/')[:3])
download_dir=get_home_path()+'/puzzle/'
create_dir(download_dir)
work_dir=download_dir+'resources/'
def puzzle_download(process_func):
    def process():
        now=0
        while n>0:
            now_process=i+min(1,(time()-st)/interval)
            now+=(now_process-now)/5
            process_func(now,n)
            sleep(0.1)
        process_func(n,n)
    def unzip_object(content_bytes,folderpath=''):
        ptr,n=0,len(content_bytes)
        while ptr<n:
            k=content_bytes.index(b'*',ptr)
            content_length=int(content_bytes[ptr:k])
            object_type=int(bytes([content_bytes[k+1]]))
            k2=content_bytes.index(b'*',k+1)
            filename_length=int(content_bytes[k+2:k2])
            filename=content_bytes[k2+1:k2+1+filename_length].decode('utf-8')
            ptr=k+2+content_length
            content=content_bytes[k2+1+filename_length:ptr]
            #-------------------------------------------------------
            filepath=f'{folderpath}{filename}'
           # print(f'-o {filepath}')
            if object_type==0:  #為資料夾
                if not path.isdir(filepath):
                    mkdir(filepath)
                unzip_object(content,filepath+'/')
            elif object_type==1:     #為檔案
                #print(filepath)
                f=open(filepath,'wb')
                f.write(content)
                f.close()
        if ptr!=n:
            print(f'解壓縮出現問題:ptr={ptr},n={n}')
    contents_list=[]
    i,n=0,10
    interval=10      #追上下一次進度需要的秒數
    st = time()
    Thread(target=process).start()
    for i in range(n):
        st = time()
        contents_list.append(Github_Download(f'puzzle/encapsulation{i+1}.puz'))
        interval=time()-st
        wait_tap()
    n=0
    unzip_object(b''.join(contents_list),download_dir)
def check_resources():
    if not path.isfile(work_dir+'ok.txt'):
        def download_text(text,c,d):
            screen.blit(download_font.render(text, True, c),d)
        screen=display.set_mode((1280, 720), FULLSCREEN)
        Github_Download('puzzle/download.jpg',download_dir+'download.jpg')
        Github_Download('puzzle/download.mp3', download_dir + 'download.mp3')
        Github_Download('puzzle/download.ttc', download_dir + 'download.ttc')
        download_font = font.Font(download_dir + 'download.ttc', 25)
        screen.blit(transform.scale(image.load(download_dir+'download.jpg').convert(), (1280, 720)), (0, 0))
        mixer.music.stop(), mixer.music.load(download_dir + 'download.mp3'), mixer.music.play(-1)
        def process_func(k,n):
            draw.rect(screen, (50, 50, 50), [0, 620, 1280, 100]), download_text(f'正在下載檔案... {round(100*k/n,1)}%', (255, 255, 255), (15, 630))
            draw.rect(screen, (150, 150, 150), [30, 675, 1220, 12], 1)
            draw.rect(screen, (0,200,0), [30, 676,int(1280*k/n), 10])
            display.update()
        puzzle_download(process_func)
        open(work_dir+'ok.txt','wb').close()
        #清空存檔
        for i in listdir(f'{work_dir}data'):
            if 'save ' == i[:5]: remove(f'{work_dir}data/{i}')
        #還原設定:
        open(f'{work_dir}data/setting.txt','w',encoding='utf-8').write(
            "{'bgm': 0.7, 'sound': 0.7, 'mode': 0, 'operate': 0, 'last_file':0, 'ending': {'end1':False, 'end2':False, 'end3': False, 'end4': False}}"
        )

def readlist(txt):
    content, k, p, trans = txt[1:-1], 0, 0, []  # 計[],計初始,結果
    for i in range(len(content)):
        if content[i] in ['[', '{', '(']:
            k += 1
        if content[i] in [']', '}', ')']:
            k -= 1
        if (content[i] == ',' and k == 0) or i == len(content) - 1:
            if i == len(content) - 1:
                part = content[p:]
            else:
                part, p = content[p:i], i + 1
            while part[0] == ' ':
                part = part[1:]
            while part[-1] == ' ':
                part = part[:-1]
            if part == 'True':
                trans += [True]
            elif part == 'False':
                trans += [False]
            elif part == 'None':
                trans += [None]
            elif part[0] == '[' and part[-1] == ']':
                trans += [readlist(part)]
            elif part[0] == '(' and part[-1] == ')':
                part1,part2=readlist(f'[{part[1:-1]}]'),()
                for j in part1:
                    part2+=(j,)
                trans+=[part2]
            elif part[0] == '{' and part[-1] == '}':
                e, c = {}, part[1:-1].split(',')
                for j in c:
                    c1 = j.split(':')
                    while c1[1][0] == ' ':
                        c1[1] = c1[1][1:]
                    while c1[1][-1] == ' ':
                        c1[1] = c1[1][:-1]
                    try:
                        c1[1] = int(c1[1])
                    except:
                        c1[1] = c1[1][1:-1]
                    e[int(c1[0])] = c1[1]
                trans += [e]
            elif part[0] == part[-1] == "'" or part[0] == part[-1] == '"':
                trans += [part[1:-1]]
            else:
                try:
                    trans += [int(part)]
                except:
                    if part[0]=='<' and part[-1]=='>':
                        trans+=[None]
                    else:
                        try:
                            trans += [float(part)]
                        except:trans += [part]
    return trans
#-----------------------------------------------------------角色分肢
class limb:
    def copy(self):
        l=limb()
        l.surfbox=self.surfbox
        l.interface=self.interface
        l.parent=self.parent
    def __init__(self):
        self.surfbox=[]
        self.surfn=0
        self.interface=[]
        self.p=(0,0)
        self.angle=0
        self.parent=0
        self.layer=100
        self.id=None
        self.screenpos=[0,0,0,0,Surface((10,10))]
        self.displaylock=0
        self.bring_f=[]
        self.bring_h = []
        self.flip=False
#-------------------------------------------------------------------主要
class body:
    def __init__(self):
        self.name=''
        self.mainlimb=[]
        self.acts=[]
        self.seriesacts=[]
        self.p=[0,0]
        self.posek=0
        self.posekn=0
        self.sleep=0
        self.pos=[650,330]
        self.displaylock=0
        self.flip=False
        self.rotate=0
        self.temangle=0
        self.sign=1
        self.pickfix=True
    def getparts(self):
        def breakdownpart(part):
            parts = [part]
            for i in part.interface:
                for j in i[-1]:
                    parts += breakdownpart(j)
            return parts
        parts=[]
        for part in self.mainlimb:
            parts+=breakdownpart(part)
        return parts
    def rotatepos(self,pos, angle,flip=False):
        if flip:return (int(-cos(angle * pi / 180) * pos[0] + sin(angle * pi / 180) * pos[1]),int(sin(angle * pi / 180) * pos[0] + cos(angle * pi / 180) * pos[1]))
        return (int(cos(angle * pi / 180) * pos[0] + sin(angle * pi / 180) * pos[1]),int(-sin(angle * pi / 180) * pos[0] + cos(angle * pi / 180) * pos[1]))
    def linkshow(self,i, p,box=0,rect=None):
        pos= i.surfbox[i.surfn]
        if self.rotate!=None:i.angle += self.rotate
        else:self.rotate=0
        angle=-i.angle if self.flip else i.angle
        r = [self.rotatepos(pos[1][0],angle,self.flip), self.rotatepos(pos[1][1], angle,self.flip), self.rotatepos(pos[1][2], angle,self.flip),self.rotatepos(pos[1][3], angle,self.flip)]
        x, y = min(r[0][0], r[1][0], r[2][0], r[3][0]), min(r[0][1], r[1][1], r[2][1], r[3][1])
        if rect==None:
            i.p=p
            if box==1 and i.displaylock==0:
                if p[0]+x<self.box[0]:
                    self.box[0]=p[0]+x
                if p[1]+y<self.box[1]:
                    self.box[1]=p[1]+y
                surf=transform.rotate(pos[0],angle).get_rect()
                if p[0]+x+surf[2]>self.box[2]:
                    self.box[2]=p[0]+x+surf[2]
                if p[1]+y+surf[3]>self.box[3]:
                    self.box[3]=p[1]+y+surf[3]
            else:
                self.blititem += [[i.layer, pos[0],i.angle, p[0] + x, p[1] + y,i,angle,i.displaylock == 0]]
            for j in i.interface:
                for m in j[1]:
                    np = self.rotatepos(j[0],angle,self.flip)
                    self.linkshow(m, (p[0] + np[0], p[1] + np[1]),box=box)
        else:draw.rect(screen,(255,0,255),[i.p[0]+x,i.p[1]+y]+transform.rotate(pos[0],angle).get_rect()[2:],2)
        i.angle -= self.rotate
    def get_rect(self):
        self.box=[100000,100000,-100000,-100000]
        for j in self.mainlimb:
            self.linkshow(j,(self.pos[0]+self.p[0],self.pos[1]+self.p[1]),box=1)
        return [self.box[0],self.box[1],self.box[2]-self.box[0],self.box[3]-self.box[1]]
    def show(self,standardpos=None,surf=None,rotate=None):
        if rotate!=None:
            self.rotate+=rotate
            self.temangle=rotate
        if self.displaylock==0:
            self.blititem, layer = [], 0
            if standardpos==None:
                standardpos=self.pos
            for j in self.mainlimb:
                self.linkshow(j,(standardpos[0]+self.p[0],standardpos[1]+self.p[1]))
            while layer < 200:
                for i in self.blititem:
                    if i[0] == layer:
                        angle = -i[6] if i[5].flip else i[6]
                        for j in i[5].bring_h:
                            if type(j.hide)==bool and j.visible:
                                j.Show((i[5].p[0] + i[5].interface[0][0][0] * cos(angle / 180 * pi) -j.role.p[0], i[5].p[1] + abs(i[5].interface[0][0][1] * sin(angle / 180 * pi)) - j.role.p[1]), rotate=angle)
                        if i[7]:(screen if surf == None else surf).blit(
                            transform.flip(transform.rotate(i[1], i[2]), self.flip, False), (i[3], i[4]))
                        for j in i[5].bring_f:
                            if type(j.hide) == bool and j.visible:
                                j.Show((i[5].p[0] + i[5].interface[0][0][0] * cos(angle / 180 * pi) -j.role.p[0], i[5].p[1] + abs(i[5].interface[0][0][1] * sin(angle / 180 * pi)) - j.role.p[1]), rotate=angle)
                layer += 1
        if rotate != None: self.rotate -= rotate
    def updateparts(self):
        self.parts=self.getparts()
    def getpose(self):
        box,dolist=self.getparts(),[]
        for i in box:
            dolist+=[[i.id,i.angle,i.surfn,i.displaylock]]
        return dolist
    def loadpose(self,n,speed=None):
        if n<len(self.acts):self.setpose(self.acts[n],speed)
    def setpose(self, command,speed=None):
        if type(command)==list:
            if speed==None:
                speed=command[1]
            self.posekn, dolist = int(1000 / speed),command[-1]
            for i in self.parts:
                i.temangle, i.plusa, i.ch, i.lock = i.angle, 0, i.surfn, 1
                for j in dolist:
                    if j[0] == i.id:
                        i.temangle, i.plusa, i.ch, i.lock = i.angle, (j[1] - i.angle) / self.posekn, j[2], j[3]
            self.tempos, self.plus,self.posehk,self.posek= self.p, ((command[2][0]-self.p[0] )/ self.posekn,(command[2][1]-self.p[1])/self.posekn),int(self.posekn/2+1),0
        else:
            self.sleep=command
            self.posek,self.posekn=0,1
    def runpose(self,pos=None,surf=None,rotate=None):
        if self.sleep > 0:
            self.show(pos,surf=surf)
            sleep(self.sleep)
            self.sleep = 0
        elif self.posek<self.posekn:
            self.posek+=1
            for j in self.parts:
                j.angle = int(j.temangle + j.plusa * (self.posek))
                if j.ch != j.surfn and self.posek == self.posehk:
                    j.surfn = j.ch
                if j.displaylock != j.lock and self.posek ==self.posehk:
                    j.displaylock = j.lock
            self.p = [int(self.tempos[0] + self.plus[0] * (self.posek)), int(self.tempos[1] + self.plus[1] * (self.posek))]
            self.show(pos,surf=surf)
        elif rotate!=None:self.show(pos,surf=surf,rotate=rotate)
def readrole(rolename,size=1):
    if '/' in rolename:
        info = open(f'{work_dir}{rolename}/info.txt', 'r').read().split('\n')
        role, folderpath = body(),work_dir+rolename
    else:
        info=open(f'{work_dir}package/role/{rolename}/info.txt','r').read().split('\n')
        role,folderpath=body(),f'{work_dir}package/role/{rolename}'
    for i in range(3):
        info[i]=readlist(info[i])
    role.name=rolename.split('/')[-1]
    allpart=[]
    for infom in info[0]:
        mainpart = []
        for i in infom:
            part=limb()
            part.id, part.surfn, part.p, part.angle, part.layer, part.displaylock=i[0]
            for j in i[1]:
                if folderpath+f'/s{j[0]}.png' not in terminal.limb_ed:terminal.limb_ed[folderpath+f'/s{j[0]}.png']=image.load(folderpath+f'/s{j[0]}.png')
                part.surfbox+=[[terminal.limb_ed[folderpath+f'/s{j[0]}.png'],j[1]]]
            part.interface=i[2]
            mainpart+=[part]
        for i in mainpart:
            for j in i.interface:
                for m in range(len(j[-1])):
                    for n in mainpart:
                        if n.id==j[-1][m]:
                            j[-1][m]=n
                            n.parent=j[-1]
                            break
        role.mainlimb+=[mainpart[0]]
        allpart+=mainpart
    role.acts,role.seriesacts=info[1:3]
    for i in role.acts:
        for j in i[-1]:
            for m in allpart:
                if m.id==j[-1]:
                    j[-1]=m
                    break
    role.updateparts()
    for part in role.parts:
        for i in part.surfbox:
            i[0]=transform.scale(i[0],(int(i[0].get_rect()[2]*size),int(i[0].get_rect()[3]*size)))
            for k in range(len(i[1])):
                i[1][k] = (int(i[1][k][0] * size), int(i[1][k][1] * size))
        for i in part.interface:
            i[0]=(int(i[0][0]*size),int(i[0][1]*size))
    for act in role.acts:
        act[2]=[int(act[2][0]*size),int(act[2][1]*size)]
    return role
def Split_Character(chr,limb_name):
    def remove_part(limb,part,rel_pos):
        for j in limb.interface:
            pos=(rel_pos[0]+j[0][0],rel_pos[1]+j[0][1])
            for i in j[1]:
                if i == part:
                    j[1].remove(i)
                    i.rel_pos,i.parent,i.cut_pos=pos,limb,j[0]
                else:remove_part(i, part,pos)
    try:
        part,void_body,rel_pos=chr.GetLimb(limb_name),body(),chr.role.p
        chr.parts.remove(part)
        for i in chr.role.mainlimb:
            if i==part:
                chr.mainlimb.remove(part)
                chr.rel_pos=rel_pos
            else:remove_part(i,part,rel_pos)
        void_body.mainlimb+=[part]
        void_body.acts += [[0,20,[0,0], []]]
        void_body.parts,void_body.name=void_body.getparts(),chr.name
        for i in void_body.parts:
            void_body.acts[-1][-1] += [[i.id, i.angle, i.surfn, i.displaylock, i]]
        cut_chr,cut_chr.parent,cut_chr.cut_pos,cut_chr.id=Character(void_body,chr.size,(int(chr.pos[0]+part.rel_pos[0]),int(chr.pos[1]+part.rel_pos[1]))),part.parent,part.cut_pos,chr.id
        cut_chr.Flip(chr.flip)
        return cut_chr
    except:return None
class Character:
    def __init__(self,role_folder,size,pos=None,attributes={}):
        self.zoom=1
        if type(role_folder)==str:
            self.role_folder=work_dir+role_folder
        self.role=readrole(role_folder,size) if type(role_folder)==str else role_folder
        self.size=size
        if pos!=None:self.role.pos=[pos[0],pos[1]]
        self.pos=self.role.pos
        self.name=self.role.name
        self.pose_finish=False
        self.posen=0         #目前是第幾個pos
        self.in_action=[]
        self.bring=[]   #
        self.live=1
        self.tapfloor=False
        self.flip=self.role.flip
        self.rotate=0
        self.hide=False
        self.speed=[0,0,0]
        self.modify_move=[0,0,0]   #(n,x,y)
        self.parent=None
        self.state=0       #0:normal,1:ladder,2:stairs
        self.eventing=False
        self.visible = True
        self.st=0
        self.value=0
        self.nowaction=''
        self.limb_dictory={}
        self.motion_dictory={}
        self.events = {'auto': [], 'pickup': [], 'throw': [],'use':[]}
        self.extra=[]
        if type(role_folder)==str and 'event.txt' in listdir(self.role_folder):
            info = open(f'{self.role_folder}/event.txt','r').read().split('\n\n\n\n')
            basic=info[0].split('\n')
            self.id = basic[0]
            self.fix = basic[1]=='True'
            self.rigid = basic[2]=='True'
            self.reversible=basic[3]=='True'
            for i in info[1].split('\n\n\n'):
                c = i.split('\n')
                self.events[c[0]]=readlist(c[1])
        else:
            self.id =self.name
            self.fix = False  # 定點不動
            self.rigid = False  # 是否不可穿越
            self.reversible = True  #是否可翻轉
        self.insertpart =None
        self.change_attributes(attributes)
        if type(role_folder)==str and 'control.ini' in listdir(self.role_folder):
            f,g=open(f'{self.role_folder}/control.ini','r').read().split('\n#------------------------\n')
            for i in f.split('\n'):
                c=i.split('=>')
                self.limb_dictory[c[0]]=int(c[1])         #hand(部位名稱)=>10(部位id)
            for i in g.split('\n'):
                c=i.split('=>')
                self.motion_dictory[c[0]]=int(c[1])         #w(鍵盤str)=>5(動作序號)
        self.parts=self.role.getparts()
        self.calculate_rects()
        self.role.loadpose(0,1000)
        self.tem_cold=0
        self.do_event=None
        self.control=True
        self.lock=False
        self.freeze=0
        self.blood=0
        self.nowdo=[]
    def calculate_rects(self):
        self.rects,posen= [],self.posen
        for i in range(len(self.role.acts)):
            self.role.loadpose(i, 1000)
            self.role.runpose()
            self.rects += [self.get_rect()]
        self.posen=posen
        self.role.loadpose(self.posen, 1000)
    def change_attributes(self,attributes):
        for attribute in attributes:
            if attribute == 'flip':  #
                self.Flip(attributes[attribute])
            elif attribute == 'live':
                self.live = attributes[attribute]
            elif attribute == 'name':
                self.name = attributes[attribute]
            elif attribute == 'rigid':
                self.rigid = attributes[attribute]
            elif attribute == 'fix':
                self.fix = attributes[attribute]
            elif attribute == 'state':
                self.state = attributes[attribute]
            elif attribute == 'visible':
                self.visible, self.pose_finish = attributes[attribute], True
            elif attribute == 'rotate':
                self.rotate = self.role.rotate = attributes[attribute]
            elif attribute == 'insert':
                for part in attributes[attribute]:
                    if type(part)==str:
                        self.Insert(part, command_to_character(attributes[attribute][part]))
                        self.extra += [self.GetLimb(part).bring_f[-1]]
                    elif type(part)==list:
                        self.Insert(part[0],command_to_character(part[1]))
                        self.extra += [self.GetLimb(part[0]).bring_f[-1]]
            elif attribute == 'value':
                self.value = attributes[attribute]
            elif attribute == 'hide':
                self.hide = attributes[attribute]
            elif attribute=='insertpart':
                self.insertpart=attributes[attribute]
    def Insert(self,partname,obj,visible=True):
        obj.parentname=partname
        self.GetLimb(partname).bring_f += [obj]
        self.GetLimb(partname).bring_f[-1].visible, self.GetLimb(partname).bring_f[-1].pos[0]= visible, -1000
    def get_rect(self):
        rect = self.role.get_rect()
        return [rect[0]-self.pos[0],rect[1]-self.pos[1],rect[0]-self.pos[0]+rect[2],rect[1]-self.pos[1]+rect[3]]
    def Flip(self,flip=None):
        if self.reversible:
            if flip!=None and self.role.flip==flip:return
            else:self.role.flip=self.flip=not self.role.flip
            for i in self.parts:
                i.flip=not i.flip
                for j in i.bring_h:j.Flip()
                for j in i.bring_f: j.Flip()
    def GetLimb(self,name):
        try:return self.parts[self.limb_dictory[name]]
        except:
            if name=='':
                try:return self.parts[-1]
                except:pass
            return None
    def DoPose(self,pose_name,speed=None):
        if pose_name in self.motion_dictory or (type(pose_name)==int and pose_name<len(self.rects)):
            self.pose_finish=False
            self.posen=pose_name if type(pose_name)==int else self.motion_dictory[pose_name]
            self.role.loadpose(self.posen,speed)
    def DoAction(self,action_name):
        for action in self.role.seriesacts:
            if action[0]==action_name:
                box=[]
                for i in action[-1]:
                    box+=[[]+i]
                    box[-1][2]=[int(i[2][0]*self.size),int(i[2][1]*self.size)]
                self.in_action,self.pose_finish,self.nowaction=[box,0,len(action[-1])],False,action_name
                break
    def Inserted_item(self):
        parts,box=self.role.getparts(),[]
        for part in parts:
            for i in part.bring_f+part.bring_h:box+=[i]
        return box
    def Throw(self,limbname=None,objectid=None,fix_item_pos=False):
        for i in self.limb_dictory:
            if i==limbname or limbname==None:
                part = self.GetLimb(i)
                if part==None:return
                try:h,f=part.bring_h,part.bring_f
                except:part.bring_h,part.bring_f=[],[]
                j=0
                while j<len(part.bring_h):
                    if type(part.bring_h[j].hide)==bool and (part.bring_h[j].id==objectid or objectid==None):
                        part.bring_h[j].pos,part.bring_h[j].parentname= [self.pos[0]+part.p[0] - self.role.mainlimb[0].p[0],self.pos[1]+part.p[1] - self.role.mainlimb[0].p[1]],i
                        if not fix_item_pos:
                            part.bring_h[j].hide,part.bring_h[j].state,part.bring_h[j].visible= False,0,True
                            part.bring_h[j].rotate = part.bring_h[j].role.rotate = 0
                            del part.bring_h[j]
                        else:return part.bring_h[j]
                    j+=1
                j=0
                while j<len(part.bring_f):
                    if type(part.bring_f[j].hide)==bool and (part.bring_f[j].id == objectid or objectid == None):
                        part.bring_f[j].pos,part.bring_f[j].parentname= [self.pos[0]+part.p[0] - self.role.mainlimb[0].p[0],self.pos[1]+part.p[1] - self.role.mainlimb[0].p[1]],i
                        if not fix_item_pos:
                            part.bring_f[j].hide,part.bring_f[j].state,part.bring_f[j].visible= False,0,True
                            part.bring_f[j].rotate=part.bring_f[j].role.rotate=0
                            del part.bring_f[j]
                        else:return part.bring_f[j]
                    j+=1
    def DoEvent(self,eventname,world):
        if eventname in self.events and not self.eventing:
            for info in self.events[eventname]:#[物件id,觸發座標,誤差座標,events]
                for chr in world['object']:
                    if chr.id in info[0] and type(chr.hide)==bool and ((not chr.hide and type(info[1][0])!=str and abs(self.pos[1]-chr.pos[1]-info[1][1])<info[2][1]*self.zoom) or (chr.hide and (chr in terminal.world.itemlist or self.id!='player') and info[1][0]=='bring')):
                        if (not chr.hide and abs(self.pos[0]-chr.pos[0]-info[1][0])<info[2][0]*self.zoom) or (info[1][0]=='bring' and self.flip==info[1][1]):
                            if (not chr.hide and abs(self.pos[0]-chr.pos[0]-info[1][0])<info[2][0]):self.modify_move=[30,(chr.pos[0]+info[1][0]-self.pos[0])/30,(chr.pos[1]+info[1][1]-self.pos[1])/30]
                            self.eventing,self.role.pickfix=True,False
                            self.do_event=[0,0,chr,info[3]]   #進度(fps),進度(event),物件,events
                            return chr
                        if ((not chr.hide and abs(chr.pos[0]-self.pos[0]-info[1][0])<info[2][0]*self.zoom) or (info[1][0]=='bring' and self.flip==(not info[1][1]))) and not chr.fix:
                            if (not chr.hide and abs(chr.pos[0]-self.pos[0]-info[1][0])<info[2][0]):self.modify_move = [30, (-self.pos[0] - info[1][0] + chr.pos[0]) / 30,(chr.pos[1] + info[1][1] - self.pos[1]) / 30]
                            self.eventing,box,self.role.pickfix=True,[],False
                            for i in info[3]:
                                if i[1]==4:box+=[[i[0],4,[1,0,3,2][i[2]]]]
                                elif i[1] == 5:box += [[i[0],5,[-i[2][0],i[2][1]],i[3]]]
                                elif i[1] == 8:box += [[i[0],8,[-i[2][0], i[2][1]]]]
                                else:box+=[i]
                            self.do_event=[0,0,chr,box]   #進度(fps),進度(event),物件,events
                            return chr
    def touch(self,other):
        if self.pos[0]+self.rects[self.posen][2]>other.pos[0]+other.rects[other.posen][0] and self.pos[1]+self.rects[self.posen][3]>other.pos[1]+other.rects[other.posen][1] and self.pos[0]+self.rects[self.posen][0]<other.pos[0]+other.rects[other.posen][2] and self.pos[1]+self.rects[self.posen][1]<other.pos[1]+other.rects[other.posen][3]:return True
        return False
    def calculate(self,world,g=0.1):
        if not self.fix:
            if self.speed[1] < -5*self.zoom: self.speed[1] = -5*self.zoom
            elif self.pos[1] + self.rects[self.posen][3] < world['floor'] and self.state==0:    #如果離地
                self.tapfloor = False
                if self.speed[0] != 0 and (self.pos[0]+self.rects[self.posen][2]>world['background'][2][0] or self.pos[0]+self.rects[self.posen][0]<0):self.speed[0]=0
                for i in world['object']:
                    if i.rigid and not i.hide and self.touch(i) and i!=self:                           #如果踩到東西
                        if self.speed[0]!=0 and i.rects[i.posen][1]<self.pos[1]-i.pos[1]<i.rects[i.posen][3]:      #撞到
                            self.speed[0]=0
                        elif self.pos[1]<i.pos[1]+i.rects[i.posen][1] and self.speed[1]>=0:                     #採到
                            self.tapfloor,self.speed[1]=True,0
                        #break
                if not self.tapfloor: self.speed[1] += g*self.zoom
            elif not self.tapfloor and self.speed[1]>=0:self.tapfloor,self.speed[1]=True,0
            elif self.state>0 and self.speed[1]!=0:self.speed[1]=0
            elif self.tapfloor and self.speed[0]!=0:
                if self.speed[0]>0.05:self.speed[0]*=0.95
                else:self.speed[0]=0
                if self.speed[2] != 0:self.speed[2]=0
            if self.speed[2] != 0:
                self.speed[2]*=0.95
                if abs(self.speed[2])<0.05:self.speed[2]=0
            self.pos[0]+=self.speed[0]
            self.pos[1]+=self.speed[1]
            if self.pos[1] + self.rects[self.posen][3] >world['floor'] and not self.lock:self.pos[1]=world['floor']-self.rects[self.posen][3]
            if self.speed[2]!=0:
                self.rotate+=self.speed[2]
                self.role.rotate=self.rotate
            if self.live==0 and self.hide:                                        #物理計算
                change_limb_angle(self.role,0)
    def Show(self,pos=None,surf=None,rotate=None,runpose=True):
        if self.eventing and self.do_event!=None:
            if self.modify_move[0]>0:
                self.modify_move[0]-=1
                self.pos[0]+=self.modify_move[1]
                self.pos[1] += self.modify_move[2]
            if self.do_event[1]<len(self.do_event[3]) and self.do_event[0]>=self.do_event[3][self.do_event[1]][0]:
                if self.do_event[3][self.do_event[1]][1]==0:self.DoPose(self.do_event[3][self.do_event[1]][2])
                if self.do_event[3][self.do_event[1]][1]==1:self.do_event[2].DoPose(self.do_event[3][self.do_event[1]][2])
                if self.do_event[3][self.do_event[1]][1] == 2:
                    if self.do_event[3][self.do_event[1]][3]==0:self.role.rotate+=self.do_event[3][self.do_event[1]][2]
                    elif self.do_event[3][self.do_event[1]][3]==1:self.do_event[2].role.rotate+=self.do_event[3][self.do_event[1]][2]
                if self.do_event[3][self.do_event[1]][1]==3:
                    if self.do_event[3][self.do_event[1]][3]==0:self.GetLimb(self.do_event[3][self.do_event[1]][2]).bring_h += [self.do_event[2]]
                    elif self.do_event[3][self.do_event[1]][3]==1:self.GetLimb(self.do_event[3][self.do_event[1]][2]).bring_f += [self.do_event[2]]
                    self.do_event[2].hide,self.do_event[2].state,self.do_event[2].insertpart= True,0,self.do_event[3][self.do_event[1]][2]
                if self.do_event[3][self.do_event[1]][1] == 4:
                    [self,self.do_event[2]][self.do_event[3][self.do_event[1]][2]//2].Flip(self.do_event[3][self.do_event[1]][2]%2==0)
                if self.do_event[3][self.do_event[1]][1] == 5:
                    if self.do_event[3][self.do_event[1]][3]==0:
                        self.pos[0]+=self.do_event[3][self.do_event[1]][2][0]*self.zoom
                        if self.do_event[3][self.do_event[1]][2][1]>0:self.pos[1] += self.do_event[3][self.do_event[1]][2][1]*self.zoom
                        elif self.state==0:
                            self.speed[1]+=self.do_event[3][self.do_event[1]][2][1]*self.zoom
                            self.tapfloor=False
                        else:
                            self.pos[1] += self.do_event[3][self.do_event[1]][2][1]*self.zoom
                    elif self.do_event[3][self.do_event[1]][3]==1:
                        self.do_event[2].pos[0]+=self.do_event[3][self.do_event[1]][2][0]*self.zoom
                        self.do_event[2].pos[1] += self.do_event[3][self.do_event[1]][2][1]*self.zoom
                if self.do_event[3][self.do_event[1]][1] == 6:                       #丟掉物件
                    self.Throw(objectid=self.do_event[3][self.do_event[1]][2])
                if self.do_event[3][self.do_event[1]][1] == 7:                        #角色狀態
                    self.state=self.do_event[3][self.do_event[1]][2]
                if self.do_event[3][self.do_event[1]][1] == 8:                          #物件速度增量
                    self.do_event[2].speed[0] += self.do_event[3][self.do_event[1]][2][0]*self.zoom
                    self.do_event[2].speed[1] += self.do_event[3][self.do_event[1]][2][1]*self.zoom
                    if self.do_event[3][self.do_event[1]][2][1]<0:self.do_event[2].tapfloor = False
                if self.do_event[3][self.do_event[1]][1] == -1:self.eventing,self.role.pickfix=False,True
                self.do_event[1]+=1
            self.do_event[0]+=1
        if (self.role.posek<self.role.posekn or self.role.sleep>0) and runpose:
            self.role.runpose(pos,surf,rotate)
        elif len(self.in_action)>0:
            self.role.setpose(self.in_action[0][self.in_action[1]])
            self.in_action[1]+=1
            if self.in_action[1]>=self.in_action[2]:self.in_action=[]
            self.role.show(pos,surf,rotate)
        else:
            self.role.show(pos,surf,rotate)
            if not self.pose_finish:self.pose_finish=True
def change_limb_angle(body,angle):
    def cla(limb,angle):
        if len(limb.interface)==1:
            if limb.interface[0][0][1] < 0:angle += 180
            limb.angle+=(angle-limb.angle-body.rotate-body.temangle)
        for i in limb.interface:
            for j in i[1]:
                cla(j,angle)
    for i in body.mainlimb:
        cla(i,angle)
def size_level(chr):
    size,k=(chr.rects[chr.posen][2]-chr.rects[chr.posen][0])*(chr.rects[chr.posen][3]-chr.rects[chr.posen][1])/((terminal.zoom)**2),1
    while size>50*(1.5**(k-1)):k+=1
    return k
def rect_zoom(rect,rate):
    return [int(rect[0]*rate),int(rect[1]*rate),int(rect[2]*rate),int(rect[3]*rate)]
background = (253, 129, 173)
class newsurface:
    def __init__(self,surf):
        self.surf=surf
        self.speed=[0,0,0]   #x,y,旋轉角度
        self.angle=0
        self.x=0
        self.y=0
        self.p=[0,0]
        self.effect=-1
    def setstart(self):
        self.p=[self.x+self.surf.get_rect()[2]/2,self.y+self.surf.get_rect()[3]/2]
        self.w=int(self.surf.get_rect()[2]/2)
        self.h=int(self.surf.get_rect()[3]/2)
    def show(self,pos,surf=None):
        self.p[0]+=self.speed[0]
        self.p[1]+=self.speed[1]
        self.angle+=self.speed[2]
        img=transform.rotate(self.surf,self.angle)
        img.set_colorkey(background)
        (screen if surf==None else surf).blit(img,(int(self.p[0]+pos[0]),int(self.p[1]+pos[1])))
def splitimage(surf,n):
    w,h=surf.get_rect()[2:]
    p1,p2=(int(w/3+w/3*random()),0),(int(w/3+w/3*random()),h)
    img1,img2=surf.subsurface([0,0,max(p1[0],p2[0]),h]).copy(),surf.subsurface([min(p1[0],p2[0]),0,w-min(p1[0],p2[0]),h]).copy()
    draw.polygon(img1,background,[p1,p2,(max(p1[0],p2[0]),0 if p2[0]>p1[0] else h)]),draw.polygon(img2,background,[(0,0),(0,h),(abs(p1[0]-p2[0]),0 if p2[0]<p1[0] else h)])
    img1.set_colorkey(background),img2.set_colorkey(background)
    img1,img2=newsurface(img1),newsurface(img2)
    img1.x,img1.y,img2.x,img2.y=0,0,min(p1[0],p2[0]),0
    if n>0:
        box1,box2=splitimage(transform.rotate(img1.surf,-90),n-1),splitimage(transform.rotate(img2.surf,-90),n-1)
        for i in box1:
            i.x,i.y,i.surf=i.y,h-i.x-i.surf.get_rect()[2],transform.rotate(i.surf,90)
        for i in box2:
            i.x,i.y,i.surf=i.y+min(p1[0],p2[0]),h-i.x-i.surf.get_rect()[2],transform.rotate(i.surf,90)
        return box1+box2
    return [img1,img2]
class button:
    def __init__(self,t,p,b=30,ftc=(255,255,255),bgc=(150,150,150)):
        if type(p)==tuple:p=[p[0],p[1]]
        self.surf=self.buttonsurface(t,b,ftc,bgc)
        self.a=self.surf
        p1=self.surf.get_rect()
        self.p=p+p1[2:4]
        self.cond=0
        self.initbox=[t,p,b,ftc,bgc]
    def buttonsurface(self,t, b, c1, c2):
        text=font.Font(f'{work_dir}data/msjh.ttc', b).render(t, True, c1)
        backc = Surface(text.get_rect()[2:4])
        backc.fill(c2),backc.blit(text,(0,0))
        return backc
    def setsurface(self,t,b=None,c1=None,c2=None):
        box=[b,c1,c2]
        for i in range(3):
            if box[i]==None:
                box[i]=self.initbox[i+2]
        self.surf = self.buttonsurface(t,box[0],box[1],box[2])
        self.p=self.p[:2]+self.surf.get_rect()[2:4]
    def tap(self,x,y):
        return 0<x-self.p[0]<self.p[2] and 0<y-self.p[1]<self.p[3]
    def show(self):
        screen.blit(self.surf,self.p[:2])
class Check_box:
    def __init__(self,pos,bool=False):
        self.pos=pos
        self.is_check=bool
    def tap(self,mouse_pos):
        if 0<mouse_pos[0]-self.pos[0]<50 and 0<mouse_pos[1]-self.pos[1]<30:self.is_check=[1,0][self.is_check]
    def Show(self):
        draw.rect(screen,(0,200,0),[self.pos[0],self.pos[1],25,30]),draw.rect(screen, (100, 100, 100), [self.pos[0],self.pos[1],50,30], 4)
        draw.rect(screen, (130, 130, 130),[self.pos[0]+2 + (23 if self.is_check else 0),self.pos[1]+2, 23,26])
class Input_box:
    def __init__(self,pos,size,font,ftc=(0,0,0),bgc=(255,255,255),border_color=(0,0,0),limit=None):
        self.pos=pos
        self.size=size
        self.force=False
        self.font=font
        self.surf=Surface(size)
        if bgc!=None:self.surf.fill(bgc)
        else:self.surf.fill(background),self.surf.set_colorkey(background)
        draw.rect(self.surf,border_color,[0,0,size[0],size[1]],3)
        self.point=0
        self.ftc=ftc
        self.word_box=[]
        self.limit=limit
        self.input_t=0
        self.Value=''
        self.warn=0
    def SetLimit(self,limit):self.limit=limit
    def input(self,event):
        if self.force and event!=None:
#            print(event.unicode)
            if event.key == 1073741904 and self.point > 0:
                self.point-=1
            elif event.key == 1073741903 and self.point < len(self.word_box):
                self.point += 1
            elif (event.unicode == '\x08' or event.key==8) and self.point > 0:
                del self.word_box[self.point - 1]
                self.point -= 1
            elif event.unicode == '\x7f' and self.point < len(self.word_box):
                del self.word_box[self.point]
            else:self.AddText(event.unicode)
            self.input_t=time()
    def AddText(self,text):
        for i in text:
            if (self.limit==None or i in self.limit) and i != '':
                self.word_box=self.word_box[:self.point]+[[self.font.render(i, True,self.ftc),i]]+self.word_box[self.point:]
                self.point+=1
    def tap(self,mouse_pos):
        if 0 < mouse_pos[0]-self.pos[0] <self.size[0] and 0 < mouse_pos[1]-self.pos[1] < self.size[1]:
            self.force,self.input_t=True,time()
            w, self.point = 0, len(self.word_box)
            for i in range(len(self.word_box)):
                if mouse_pos[0] < self.pos[0]+5 + w:
                    self.point = i
                    break
                w += self.word_box[i][0].get_rect()[2] + 1
        else:self.force=False
    def Show(self):
        w,p,self.Value= 0, 0,''
        screen.blit(self.surf,self.pos)
        for j in range(len(self.word_box)):
            if 10+ w+self.word_box[j][0].get_rect()[2]<self.size[0]:
                screen.blit(self.word_box[j][0], (self.pos[0]+5 + w,self.pos[1]))
                w += self.word_box[j][0].get_rect()[2] + 1
                self.Value+=self.word_box[j][1]
                if j == self.point - 1: p = w
            else:
                self.warn=time()
                self.word_box,self.point=self.word_box[:j],min(self.point,j)
                break
        if time()-self.warn<0.5:draw.rect(screen,(255,0,0),[self.pos[0],self.pos[1],self.size[0],self.size[1]],3)
        elif self.force and (time()-self.input_t)%2/2< 0.5:
            draw.line(screen,self.ftc, (self.pos[0]+5 + p,self.pos[1]+3),(self.pos[0]+5 + p,self.pos[1]+self.size[1]-3),1)
def copy_variable(variable):
    if type(variable)==list:item=[]
    elif type(variable)==dict:item={}
    else:return variable
    for i in variable:
        if type(item)==list:item+=[copy_variable(i)]
        elif type(item) == dict:item[i]=copy_variable(variable[i])
    return item
def ashow(t,b,c,d):
    screen.blit(font.Font(f'{work_dir}data/msjh.ttc', b).render(t, True, c),d)
def systeminput(t,input='',num_only=False,int_only=False):
    x,y,abc,lock=550,160,1,1
    def up(t):
        draw.rect(screen,(50,50,50),[x-50,y-30,350,100]),draw.rect(screen, (255, 255, 255), [x-30, y, 310,30]),ashow(t,20, (255, 255, 255), (x - 45, y-30))
        ashow('  ' + input,20, (0, 0, 0), (x - 20, y)),draw.rect(screen, (0, 200, 0), [x +150, y+32, 50, 30]),draw.rect(screen, (255,0, 0), [x, y + 32, 50, 30])
        ashow('確定',20, (255, 255, 0), (x+150, y+32)),ashow('取消', 20, (255, 255, 0), (x, y + 32))
        display.update()
    up(t)
    while abc==1:
        for event2 in event.get():
            if event2.type == MOUSEBUTTONDOWN:
                pos= mouse.get_pos()
                if 150<pos[0]-x<200 and 32<pos[1]-y<62:
                    abc=0
                if 0<pos[0]-x<50 and 32<pos[1]-y<62:
                    return False
                up(t)
            if event2.type == KEYDOWN:
                if event2.key==8:
                    input=input[:-1]
                elif event2.key ==13:
                    abc=0
                else:
                    get_input=event2.unicode
                    if (not num_only and not int_only) or get_input in '0123456789'+('.' if num_only else ''):
                        input+=get_input
                up(t)
            if event2.type==QUIT:
                return False
        sleep(0.1)
    try:
        if num_only:
            input=float(input)
        if int_only:
            input = int(input)
    except:
        systemhint('input error!!!')
        return False
    return input
def str_convert(string):
    def converting(k):
        result=None
        while string[k]==' ':k+=1
        if string[k]=='{':
            result={}
            k+=1
            while string[k] == ' ': k += 1
            if string[k]!='}':k-=1
            while string[k]!='}':
                key,k=converting(k+1)
                while string[k]!=':':k+=1
                result[key],k=converting(k+1)
                while string[k] not in ',}': k += 1
        elif string[k]=='[':
            result=[]
            k += 1
            while string[k] == ' ': k += 1
            if string[k] != ']':k -= 1
            while string[k] != ']':
                item,k = converting(k + 1)
                result+=[item]
                while string[k] not in ',]': k += 1
        elif string[k]=='(':
            result=()
            k += 1
            while string[k] == ' ': k += 1
            k -= 1
            while string[k] != ')':
                item,k = converting(k + 1)
                result+=(item,)
                while string[k] not in ',)': k += 1
        elif string[k] in ['"',"'"]:
            k, p = k + 1, k
            while string[k] != string[p]: k += 1
            result = string[p + 1:k]
        elif string[k] in '-0123456789':
            p=k
            while string[k] in '-0123456789.': k += 1
            result=float(string[p:k]) if '.' in string[p:k] else int(string[p:k])
            k-=1
        elif string[k:k+4]=='True':result,k=True,k+3
        elif string[k:k + 4] == 'None':result, k = None, k + 3
        elif string[k:k + 5]== 'False':result, k =False, k + 4
        return result,k+1
    return converting(0)[0]
class Game_set:
    def __init__(self,pos):
        self.pos=pos
        self.blank=Surface((600,400))
        self.blank.fill((255,255,255)),self.blank.blit(transform.scale(terminal.image['gear'],(50,50)),(540,310))
        text_render(self.blank,'BGM:',40,(0,0,0),(20,20)),text_render(self.blank, '音效:', 40, (0, 0, 0), (20,90)),text_render(self.blank, '縮放:', 40, (0, 0, 0), (20,160)),
        text_render(self.blank, '畫面:      全螢幕      視窗', 40, (0, 0, 0), (20,230)),text_render(self.blank, '操作:      鍵盤      觸控式', 40, (0, 0, 0), (20,300))
        draw.rect(self.blank,(50,50,50),[150,45,400,10]),draw.rect(self.blank,(50,50,50),[150,115,400,10]),draw.rect(self.blank,(50,50,50),[150,185,400,10])
        self.blank.set_alpha(180)
    def display(self,update=True):
        screen.blit(self.blank,self.pos)
        draw.rect(screen,(130,130,130),[self.pos[0]+140+int(400*terminal.bgm_vol),self.pos[1]+30,20,40])
        draw.rect(screen, (130, 130, 130), [self.pos[0] + 140 + int(400 * terminal.sound_vol), self.pos[1] + 100, 20, 40])
        draw.rect(screen, (130, 130, 130), [self.pos[0] + 140 + int(100 *(terminal.zoom-1)), self.pos[1] + 170, 20, 40])
        draw.rect(screen,(0,0,0),[self.pos[0]+160+180*terminal.view_mode,self.pos[1]+230,[140,100][terminal.view_mode],52],2)
        draw.rect(screen, (0, 0, 0),[self.pos[0] + 160 + 140 * terminal.operate_mode, self.pos[1] + 300, [100, 140][terminal.operate_mode], 52],2)
        if update:display.update()
    def mainloop(self,tap_pos):
        global screen
        needsave,zoom=False,terminal.zoom
        if 150<tap_pos[0]-self.pos[0]<550 and 35<tap_pos[1]-self.pos[1]<75:
            terminal.bgm_vol,needsave=(tap_pos[0]-self.pos[0]-150)/400,True
            mixer.music.set_volume(terminal.bgm_vol)
        if 150 < tap_pos[0] - self.pos[0] < 550 and 105 < tap_pos[1] - self.pos[1] < 145:
            terminal.sound_vol,needsave= (tap_pos[0] -self.pos[0] - 150) / 400,True
            terminal.adjust_sound()
        if 150 < tap_pos[0] - self.pos[0] < 550 and 175 < tap_pos[1] - self.pos[1] < 215:
            terminal.zoom,needsave=round((tap_pos[0] -self.pos[0] - 150)/100,2)+1,True
        if 0 < tap_pos[0] - self.pos[0]-160 <140 and 0< tap_pos[1] - self.pos[1]-230<52:
            terminal.view_mode,needsave=0,True
            screen= display.set_mode((1280, 720),FULLSCREEN)
        if 0 < tap_pos[0] - self.pos[0] -340 < 100 and 0 < tap_pos[1] - self.pos[1] - 230 < 52:
            terminal.view_mode,needsave= 1,True
            screen = display.set_mode((1280, 720))
        if 0 < tap_pos[0] - self.pos[0] -160 < 100 and 0 < tap_pos[1] - self.pos[1] - 300 < 52:
            terminal.sound['button4'].play()
            terminal.operate_mode, needsave = 0, True
        if 0 < tap_pos[0] - self.pos[0] -300 < 140 and 0 < tap_pos[1] - self.pos[1] - 300 < 52:
            terminal.sound['button4'].play()
            terminal.operate_mode,needsave= 1,True
        if key.get_pressed()[K_s] and 0 < tap_pos[0] - self.pos[0] -540 < 50 and 0 < tap_pos[1] - self.pos[1] - 310 < 50:
            def Developers_tool():
                draw.rect(screen,(200,200,200),[self.pos[0],self.pos[1],600,400])
                o,o2,o3,check_box,abc,allcheck=['物件','移動','劇情','監視防盜','武器防盜','飛行','無敵','電腦登錄'],['電梯卡','萬能鑰匙','可視化','控制','手機滿電'],['阻隔','潛地','跌倒'],[],1,[terminal.world.computer_setting['power_room']['anti-system'],terminal.world.computer_setting['power_room']['anti-weapon'],terminal.player_setting['fly'],terminal.player_setting['invincible'],terminal.world.computer_setting['power_room']['login']]
                for i in range(len(o)):text_render(screen,o[i],25,(0,0,0),(self.pos[0]+5,self.pos[1]+10+i*45))
                for i in range(len(o2)): text_render(screen, o2[i], 25, (0, 0, 0),(self.pos[0] + 215, self.pos[1] + 145 + i * 45))
                for i in range(5):check_box+=[Check_box((self.pos[0]+130,self.pos[1]+150+i*45),allcheck[i])]
                check_box2,check_box3=[Check_box((self.pos[0]+330,self.pos[1]+150),'elevator_card' in terminal.world.props),Check_box((self.pos[0]+330,self.pos[1]+195),'keys' in terminal.world.props),Check_box((self.pos[0]+330,self.pos[1]+240),terminal.world.role.visible),Check_box((self.pos[0]+330,self.pos[1]+285),terminal.world.role.control),Check_box((self.pos[0]+330,self.pos[1]+330),terminal.world.phone_setting['power']==100)],[]
                for i in range(len(o3)):
                    text_render(screen, o3[i], 25, (0, 0, 0),(self.pos[0] + 425, self.pos[1] + 145 + i * 45))
                    check_box3+=[Check_box((self.pos[0]+530,self.pos[1]+150+i*45),terminal.player_setting[['block','latent','fall'][i]])]
                bg=screen.copy()
                def up():
                    screen.blit(bg,(0,0))
                    itemname.Show(),get_btn.show(),roomname.Show(),plot_progress.Show(),clear_police.show()
                    delete_btn.show(), clear_btn.show(),roommove_btn.show()
                    for i in check_box+check_box2+check_box3:i.Show()
                    display.update()
                itemname,get_btn,delete_btn,clear_btn=Input_box((self.pos[0]+100,self.pos[1]+10),(250, 35), font_dict2[25], bgc=None),button(' get ',(self.pos[0]+380,self.pos[1]+10),25,bgc=(0,0,0)),button(' delete ',(self.pos[0]+439,self.pos[1]+10),25,bgc=(0,0,0)),button(' clear ',(self.pos[0]+530,self.pos[1]+10),25,bgc=(0,0,0))
                roomname,roommove_btn,plot_progress,clear_police=Input_box((self.pos[0]+100,self.pos[1]+55),(250, 35), font_dict2[25], bgc=None),button(' move ',(self.pos[0]+380,self.pos[1]+55),25,bgc=(0,0,0)),Input_box((self.pos[0]+100,self.pos[1]+100),(70, 35), font_dict2[25], bgc=None,limit='0123456789.'),button(' 清除警察&警報 ',(self.pos[0]+380,self.pos[1]+100),25,bgc=(0,0,0))
                plot_progress.AddText(str(terminal.world.plot['man1']))
                while abc==1:
                    for event2 in event.get():
                        if event2.type == QUIT:abc=0
                        if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                            x, y = mouse.get_pos()
                            itemname.tap((x, y)),plot_progress.tap((x,y)),roomname.tap((x,y))
                            if get_btn.tap(x,y):
                                name=itemname.Value
                                for room in map:
                                    if name!='':
                                        for cmd in map[room]['object']:
                                            if cmd[0]==name:
                                                cmd[2]=(terminal.world.role.pos[0],terminal.world.role.pos[1])
                                                terminal.world.world['object']+=[command_to_character(cmd)]
                                                itemname.word_box,name=[],''
                                                break
                            if delete_btn.tap(x,y):
                                for item in terminal.world.world['object']:
                                    if item.name==itemname.Value:
                                        terminal.world.world['object'].remove(item)
                                        itemname.word_box=[]
                                        break
                            if clear_btn.tap(x,y):
                                k,itemname.word_box=0,[]
                                while k<len(terminal.world.world['object']):
                                    if not terminal.world.world['object'][k].hide:del terminal.world.world['object'][k]
                                    else:k+=1
                                systemhint('已清空')
                            if roommove_btn.tap(x,y):
                                if roomname.Value in terminal.world.map:teleport([roomname.Value,[300,300]])
                                else:systemhint('房間不存在')
                                roomname.word_box=[]
                            if clear_police.tap(x,y):
                                k,terminal.world.policebox,terminal.world.alarm=0,[],False
                                for room in terminal.world.map:
                                    terminal.world.map[room]['warn']=False
                                while k<len(terminal.world.world['object']):
                                    if terminal.world.world['object'][k].name in ['mpolice','wpolice','specialforce','specialforce2']:del terminal.world.world['object'][k]
                                    else:k+=1
                                systemhint('已清空')
                            for i in check_box+check_box2+check_box3:i.tap((x,y))
                            if not (0<x-self.pos[0]<600 and 0<y-self.pos[1]<400):abc=0
                        if event2.type == KEYDOWN:
                            itemname.input(event2),plot_progress.input(event2),roomname.input(event2)
                    up()
                    sleep(0.1)
                terminal.world.plot['man1']=float(plot_progress.Value) if '.' in plot_progress.Value else int(plot_progress.Value)
                terminal.world.computer_setting['power_room']['anti-system']=check_box[0].is_check
                terminal.world.computer_setting['power_room']['anti-weapon'] = check_box[1].is_check
                terminal.player_setting['fly']=check_box[2].is_check
                terminal.player_setting['invincible']=check_box[3].is_check
                terminal.world.computer_setting['power_room']['login']=check_box[4].is_check
                if 'elevator_card' in terminal.world.props and not check_box2[0].is_check:terminal.world.props.remove('elevator_card')
                elif 'elevator_card' not in terminal.world.props and check_box2[0].is_check:terminal.world.props+=['elevator_card']
                if 'keys' in terminal.world.props and not check_box2[1].is_check:terminal.world.props.remove('keys')
                elif 'keys' not in terminal.world.props and check_box2[1].is_check:terminal.world.props+=['keys']
                terminal.world.role.visible=check_box2[2].is_check
                terminal.world.role.control = check_box2[3].is_check
                if check_box2[4].is_check:terminal.world.phone_setting['power']=100
                for i in range(len(o3)):terminal.player_setting[['block','latent','fall'][i]]=check_box3[i].is_check
            try:Developers_tool()
            except:pass
        if needsave:
            terminal.save_setting()
            if terminal.zoom!=zoom:terminal.re_assign='resize'
def display_thank():
    x,y,allbox,k,blank,pic,pk=0,820,[[transform.scale(terminal.blank.copy(),(500,100)),[100,720]]],0,transform.scale(terminal.blank.copy(),(550,120)),[],[0,0,180]#第幾張,alpha,cold
    if terminal.world.clearance==3:
        for i in range(26):
            pic+=[transform.scale(image.load(f'{work_dir}data/picture/{i}.png'),(480,269))]
    elif terminal.world.clearance==4:
        for i in range(13):pic+=[transform.scale(image.load(f'{work_dir}data/picture/{i}.png'),(480,269))]
        for i in (13,14,17,18,19,21,22):pic+=[transform.scale(image.load(f'{work_dir}data/picture/{i}.png'),(480,269))]
        for i in range(7): pic += [transform.scale(image.load(f'{work_dir}data/picture/{26+i}.png'), (480, 269))]
    screen.fill((0,0,0)),display.update()
    mixer.music.stop(),text_render(allbox[0][0],'特別感謝',50,(240,240,0),(0,0),1)
    mixer.music.load(f'{work_dir}bgm/ending.mp3')
    mixer.music.play()
    t=time()
    for name in terminal.world.guide2:
        if name in Item_dictory and name in terminal.info:
            for posen in terminal.world.guide2[name]:
                img=blank.copy()
                img.blit(transform.scale(terminal.info[name][posen][0],(100,100)),(0,0))
                text_render(img, f"{Item_dictory[name][0]}", 30, (240,240, 0), (120, 5))
                text_render(img,f"演出次數:{terminal.world.guide2[name][posen]['display']}",30,(255,255,255),(350,5))
                text_render(img, f"使用次數:{terminal.world.guide2[name][posen]['used']}", 30, (255,255,255), (350, 35))
                if name in People:text_render(img,f"死亡次數:{terminal.world.guide2[name][posen]['died']}",30,(255,255,255),(350,65))
                allbox+=[[img,[[100,700][x],y]]]
                y+=120
                k+=1
                if k%67==0:x=[1,0][x]
    while time()-t<3:sleep(0.3)
    t=time()+109
    while allbox[-1][1][1]>0:
        screen.fill((0,0,0))
        change=allbox[-1][1][1]>(t-time())*122
        for i in allbox:
            if -100 < i[1][1] < 820:
                screen.blit(i[0], i[1])
            if change:i[1][1]-=2.5
        if (allbox[int(len(allbox)/2)][1][1]>-650 or allbox[int(len(allbox)/2)][1][1]<-1000) and pk[0]<len(pic):
            draw.rect(screen,(0,0,0),[700 if allbox[int(len(allbox)/2)][1][1]>-650 else 50,250,480,269])
            pic[pk[0]].set_alpha(min(max(pk[1],0),255))
            screen.blit(pic[pk[0]],(700 if allbox[int(len(allbox)/2)][1][1]>-650 else 50,250))
            if change:
                if pk[2]>0:
                    if pk[1]<255:pk[1]+=20
                    else:pk[2]-=1
                else:
                    pk[1]-=20
                    if pk[1]<=0:
                        pk[0]+=1
                        pk[2]=180
        elif pk[1]>0:pk=[pk[0],0,100]
        display.update()
        get=wait_tap()
        if type(get)==bool:
            mixer.music.pause()
            if yesno('確定要跳過嗎?','感謝者名單'):return
            mixer.music.unpause()
def random_order(order):
    norder=[]
    while len(order)>0:
        get=order[int(len(order)*random())]
        norder+=[get]
        order.remove(get)
    return norder
class Virtual_key:
    def __init__(self,unicode='',key=0):
        self.unicode=unicode
        self.key=key
class Virtual_keyboard:
    def __init__(self,pos,size,hide=False):
        self.pos=pos
        self.size=size
        self.board=Surface(size)
        self.board_shift=Surface(size)
        self.shift=False
        self.hide=hide
        keyfont=font.Font(f'{work_dir}data/arial.ttf',20)
        keys=[
            '12345','67890','[]\\/=',[';',':',"'",'Back'],
            'abcde','fghij','klmno','pqrst',
            'uvwxy',['z','.','-','shift']
        ]
        keys2 = [
            '!@#$%', '^&*()','{}|?+',['<','>','"','Delete'],
            'ABCDE','FGHIJ', 'KLMNO', 'PQRST',
            'UVWXY',['Z', ',', '_', 'shift']
        ]
        x,y,width,h=5,5,int(size[0]/5-6),int((size[1])/len(keys)-len(keys)+5)
        self.tapbox=[]
        key_color=(150,150,150)
        key_color2=(120,120,120)
        key_color3=(100,100,100)
        def drawbutton(surf,text,rect):
            x,y,w,h=rect
            draw.rect(surf, key_color,rect), draw.polygon(surf,key_color2,[(x + w, y), (x + w + 2, y + 2), (x + w + 2, y + h + 2), (x + w, y + h)]), draw.polygon(
            surf, key_color3, [(x, y + h), (x + w, y + h), (x + w + 2, y + h + 2), (x + 2, y + h + 2)])
            word=keyfont.render(text,True,(255,255,0) if text=='shift' and surf is self.board_shift else (0,0,0))
            surf.blit(word,(x+int(w/2-word.get_rect()[2]/2),y+int(h/2-word.get_rect()[3]/2)))
        for i in range(len(keys)):
            for j in range(len(keys[i])):
                if x > size[0] - 5: x, y = 5, y + h + 5
                w=width if j<len(keys[i])-1 else (size[0]-x-5)
                drawbutton(self.board,keys[i][j],[x,y,w,h]),drawbutton(self.board_shift,keys2[i][j],[x,y,w,h])
                self.tapbox+=[[(pos[0]+x,pos[1]+y,w,h),keys[i][j],keys2[i][j]]]
                x+=w+5
    def tap(self,pos):
        if self.hide:return None
        if not (0<pos[0]-self.pos[0]<self.size[0] and 0<pos[1]-self.pos[1]<self.size[1]):return None
        for i in self.tapbox:
            if 0<pos[0]-i[0][0]<i[0][2] and 0<pos[1]-i[0][1]<i[0][3]:
                if i[1]=='shift':self.shift=not self.shift
                else:
                    keyword=i[2] if self.shift else i[1]
                    if keyword=='Back':return Virtual_key('\x08')
                    elif keyword=='Delete':return Virtual_key('\x7f')
                    else:return Virtual_key(keyword)
        return Virtual_key()
    def Show(self):
        if not self.hide:screen.blit(self.board_shift if self.shift else self.board,self.pos)
def alpha_blit(surface,surface2,pos,col):
    w,h=surface.get_rect()[2:4]
    for x in range(surface2.get_rect()[2]):
        for y in range(surface2.get_rect()[3]):
            if 0<pos[0]+x<w and 0<pos[1]+y<h and surface2.get_at((x,y))[3]!=0:
                c=surface.get_at((pos[0]+x,pos[1]+y))
                if c[3]!=0:
                    surface.set_at((pos[0]+x,pos[1]+y),(max(min(c[0]+col[0],255),0),max(min(c[1]+col[1],255),0),max(min(c[2]+col[2],255),0)))
def sword_chop(who,direct,target):
    terminal.sound['swing'].play()
    attack_range =  [who.pos[0] + (-220 if direct else 50),who.pos[1] + who.rects[who.posen][1]-100, 170 * terminal.zoom,who.rects[who.posen][3] - who.rects[who.posen][1]]
    box = []
    for chr in terminal.world.world['object']:
        if not chr.hide and chr.name in target and rect_touch(attack_range, chr):
            if chr.name == 'girl' and who.id in ('player','girl'):
                chr.state = 0
                chr.rotate = chr.role.rotate = 0
                terminal.world.world['object'].remove(chr)
                terminal.world.world['object']+=[chr]
                if terminal.world.scenes_name=='c_lab' and chr not in terminal.world.followbox:
                    terminal.world.Add_follow(chr)
                continue
            elif chr.name=='sickbed':
                girl=terminal.world.search('girl',inroom=True)
                if girl!=None:girl.state=0
            elif chr.name=='aircraft':
                chr.blood+=10
                continue
            cut_order = random_order(['left_sh', 'left_arm', 'left_leg', 'head', 'body', 'right_sh', 'right_arm', 'right_leg'])
            for cut_part in cut_order + ['']:
                k = Split_Character(chr, cut_part)
                if k != None:
                    terminal.sound['chop'].play()
                    if chr.live == 1 and chr.name not in ('hyena','mpolice','wpolice','specialforce'): terminal.world.Talk(chr, ['啊~~~', '救命啊!', '厄啊~'][int(3 * random())])
                    if chr.live==1:
                        for rect in chr.rects: rect[3] -= 120
                    chr.live, chr.speed, chr.state = 0.8, [-2 if direct else 2, -1, 0], 0
                    if chr.name == 'hyena': terminal.world.busy = False
                    if chr.id == 'scientist': chr.DoPose(18 + chr.posen // 3)
                    k.surf_copy = [k.parent.surfbox[k.parent.surfn][0].copy(),k.role.mainlimb[0].surfbox[k.role.mainlimb[0].surfn][0].copy()]
                    k.speed, k.live = [(-1 if direct else 1) * int(2 + 2 * random()), -2 - int(3 * random()),50 * random()], 'blood'
                    k.parent.surfbox[k.parent.surfn][0].blit(transform.scale(terminal.image['bld1'], (100, 100)),(-30, 20))
                    k.role.mainlimb[0].surfbox[k.role.mainlimb[0].surfn][0].blit(transform.scale(terminal.image['bld1'], (50, 50)), (-10, -10))
                    # k.rects[k.posen][3]-=100
                    box += [k]
                    break
    explosion(None, attack_range, target=Cuttable_obj, blood=False, power=2, effect=None, fragments=0,sound='fragmentation')
    terminal.world.world['object'] += box
class rollboard:
    def __init__(self,p,panel,buttonlist,checkonly=False):#p:rect(x,y,w,h),panel:surf,buttonlist:[[surf,(x,y),func,arg]]
        self.p=p  #rect
        self.y=0
        self.buttonlist=buttonlist
        self.surf=panel
        self.size=panel.get_rect()[2:]
        self.rol=None
        self.temsurf=panel.copy()
        self.checkonly=checkonly
        for i in buttonlist:
            self.temsurf.blit(i[0],i[1])
        self.rollrect=[self.p[0]+self.p[2]+7,self.p[1]+int(self.p[3]*self.y/self.size[1]),8,int(self.p[3]*self.p[3]/self.size[1])]
        self.taproll=False
        self.temy=0
        self.maxy=self.size[1]-self.p[3]
        self.fix=self.size[1]/self.p[3]
    def show(self):
        screen.blit(self.temsurf,self.p[:2],[0,self.y,self.p[2],self.p[3]])
        if self.p[3]<self.size[0] or self.y>=0:
            draw.rect(screen,(200,200,200),[self.p[0]+self.p[2]+5,self.p[1],10,self.p[3]],2)
            draw.rect(screen,(230,230,230) if self.taproll else (200,200,200),self.rollrect)
    def roll(self,y=0):
        self.y += y * self.fix
        self.y = max(0, min(self.y, self.maxy))
        self.rollrect[1] = self.p[1] + int(self.p[3] * self.y / self.size[1])
    def rolling(self):
        if mouse.get_pressed()[0]:
            x,y=mouse.get_pos()
            if (0<x-self.rollrect[0]<self.rollrect[2] and 0<y-self.rollrect[1]<self.rollrect[3]) or self.taproll:
                if self.taproll:
                    self.roll(y - self.temy)
                else:self.taproll=True
                self.temy=y
            return True
        elif self.taproll:
            self.taproll=False
            return True
        return False
    def contain(self,pos):
        return 0<pos[0]-self.p[0]<self.p[2]+20 and 0<pos[1]-self.p[1]<self.p[3]
    def tap(self,pos):
        for i in self.buttonlist:
            if 0<pos[0]-self.p[0]-i[1][0]<i[0].get_rect()[2] and 0<pos[1]-self.p[1]-i[1][1]+self.y<i[0].get_rect()[3]:
                if i[2]!=None:i[2](i[3])
                break
class FPS:
    def __init__(self,interval=0.01):
        self.start_time=0
        self.time=0
        self.max=0
        self.now=0
        self.interval=interval
    def update(self):
        self.max = (time() - self.start_time) / self.interval
        if time()>self.start_time+100 or self.max>self.now+5:
            self.start_time=time()
            self.max=1
            self.now=0
        if self.now>self.max:
            sleep(0.01)
        self.now += 1
        display.update()
map={
     'Initial room':{'background':[16,[0,0],[1510,720],[]],                    #[bgcode,[角色相對背景位置],[bg_w,bg_y],[bg_object]]
                    'floor':660,                                                   #相對於背景(0,0)的位置
                    'trigger':[[[1500,500,200,300],['B2',(850,487)]],[[1130,520,112,98],'charge','z',['charge1','charge2','charge3']],[[30,585,540,80],'shattered','z',['shattered2'],{'variable':'small room'}]],
                    'back':[],
                    'object':[['crackhole',1,(289,754),0,{'visible':False}],['kirito',0.4,(-500,500),0],['exptable',1,(800,533)],['microscope',0.4,(620,478),0],['note',0.5,(680,516),0,{'value':'實驗編號:#1093|負責人員:CUTHBERT|藥物:CHLORPHENIRAMINE'}],['testtube',0.15,(950,487),1],['potion',0.2,(800,495),0],['potion',0.2,(850,495),1],['sickbed',0.5,(300,555)]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #名稱,初始,結尾(-1:最後),增量,rect,播放次數(-1:無限),前後(0:後,1:前),計算禎
                    },
            'Ward':{'background':[16,[0,0],[1510,720],[]],
                    'floor':660,
                    'trigger':[[[1500,500,200,300],['B2',(250,487)]],[[1130,520,112,98],'charge','z',['charge1','charge2','charge3']]],#'shattered','z',['shattered2']  #'enterhole','space',[]
                    'back':[],
                    'object':[['exptable',1,(800,533)],['microscope',0.4,(620,478),1],['note',0.5,(680,516),0,{'value':'實驗編號:#1088|負責人員:HERBERT|藥物:AMINOPHYLLINE'}],
                              ['testtube',0.15,(950,487),1],['potion',0.2,(800,495),8],['potion',0.2,(850,495),7],['sickbed',0.5,(240,575),0],
                              ['girl',0.18,(240,440),4,{'flip':True,'state':1,'rotate':10}]],
                    'front':[],
                    'effect':[],
                    },
          'B2_lab':{'background':[3,[0,0],[3010,720],[]],
                    'floor':660,
                    'trigger':[[[3000,500,200,300],['B2',(1450,487)]],[[2150,70,97,58],'Destroy_the_monitor','auto',['monitor3','monitor3'],{'rotate':-15,'flip':True,'variable':[2500,200,500,400]}]],
                    'back':[['lab1',(1700,430,172,204)],['lab5',(2000,300,208,168)],['lab3',(20,400,142,240)]],
                    'object':[['wbox',0.7,(300,590),6,{'flip':True}],['wbox',0.6,(450,600),6,{'flip':True}],['car_key',0.1,(380,630)],['exptable',1,(800,533)],['exptable',1,(1350,533)],['microscope',0.4,(1460,478),1],['microscope',0.4,(1320,478),0],['testtube',0.15,(1200,487),1],['potion',0.2,(600,495),4],['potion',0.2,(650,485),5],['potion',0.2,(700,495),0],['potion',0.2,(750,495),1],['potion',0.2,(1400,495),2],['potion',0.2,(850,495),3],['beaker',0.2,(920,496)],['beaker',0.2,(1020,440)],['tripod',0.15,(1020,490)],['alcohol',0.2,(1020,505)],
                              ['scientist',1,(800,350),0,{'insert':[['righthand',['potion',0.2,(0,0),9,{'rotate':-40}]],['lefthand',['potion',0.2,(800,495),1]]]}],['scientist',1,(1386,350),3,{'flip':True}],['scientist',1,(1830,345),12,{'state':1}]],
                    'front':[],
                    'effect':[],
                    },
          'Sweep room':{'background':[1,[0,0],[1410,720],[]],
                    'floor':660,
                    'trigger':[[[1099,246,143,301],['Storeroom',(550,551)],'space']],
                    'back':[],
                    'object':[['rake',0.5,(400,633)],['broom',0.5,(700,529)],['wbox',0.3,(900,607),0],['ladder',1,(800,655)]],
                    'front':[],
                    'effect':[],
                    },
       'Storeroom':{'background':[16,[0,0],[1860,720],[]],
                    'floor':660,
                    'trigger':[[[1850,500,200,300],['B2',(2150,487)]],[[500,287,143,301],['Sweep room',(1200,551)],'space',['door6']],[[50,470,140,190],'unlock_coffer','z',[],{'variable':'QSPd9d8','variable2':['note',0.5,(80,600),0,{'value':'hint$player$0'}]}]],
                    'back':[],
                    'object':[['sword',0.3,(1020,550)],['wbox',0.3,(400,605),0],['wbox',0.3,(730,583),1],['wbox',0.3,(530,490),0],['wbox',0.3,(600,590),1],['bucket',0.4,(920,578),0],['bucket',0.4,(1030,580),0],['bucket',0.4,(1230,588),7],['bucket',0.4,(1350,588),7],['bucket',0.4,(500,580),2],['coffer',0.4,(120,565),0]],
                    'front':[],
                    'effect':[],
                    },
       'restroom':{'background':[71,[0,0],[1280,720],[]],
                    'floor':660,
                    'trigger':[[[0,100,10,500],['B2',(2650,487)]]],
                    'back':[],
                    'object':[['phone',0.1,(176,420),1,{'state':1}]],
                    'front':[],
                    'effect':[],
                    },
              'B2':{'background':[13,[0,0],[3200,720],[]],
                    'floor':600,
                    'trigger':[[[300,285,200,300],['Ward',(1400,561)],'space',['iron door']],[[900,285,200,300],['Initial room',(1400,561)],'space',['iron door']],[[1500,285,200,300],['B2_lab',(2900,561)],'space',['iron door2']],[[2100,285,200,300],['Storeroom',(1750,561)],'space',['iron door']],[[2699,285,200,300],['restroom',(100,561)],'space',['iron door2']],[[3190,300,50,400],['staircase',(350,4165)]]],
                    'back':[['restroom',(2900,320,40,40)]],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        'time_lab':{'background':[46,[0,0],[1280,720],[]],
                    'floor':600,
                    'trigger':[[[0,100,10,600],['small room',(150,426)]]],
                    'back':[],
                    'object':[['c4',0.5,(1000,580)],['c4',0.5,(1100,580)],['c4',0.5,(1170,580)]],
                    'front':[],
                    'effect':[],
                    },
        'small room':{'background':[6,[0,0],[1280,720],[]],
                    'floor':539,
                    'trigger':[[[700,100,200,300],['B3',(950,509)],'space'],[[0,0,250,500],['time_lab',(100,491)],'space'],[[400,-230,200,30],'outhole','touch',[],{'variable':'small room'}]],
                    'back':[],
                    'object':[['ladder',1,(200,400),1],['ladder',1,(300,500),1]],
                    'front':[],
                    'effect':[],
                    },
        'power room':{'background':[67,[0,0],[1280,720],[]],
                    'floor':660,
                    'trigger':[[[0,100,10,600],['B3',(350,509)]],[[1050,320,109,78],'use_computer','z',['computer']],[[300,0,45,42],'Destroy_the_monitor','auto',['monitor4','monitor4'],{'flip':True,'variable':[700,100,500,600]}]],
                    'back':[['wire',(500,540,208,132)],['wire',(650,540,208,132)],['wire',(800,540,208,132)]],
                    'object':[['charge',0.1,(700,656)]],
                    'front':[],
                    'effect':[],
                    },
       'treasure2':{'background':[40,[0,0],[2010,720],[]],
                    'floor':660,
                    'trigger':[[[0,100,10,600],['B3',(1550,509)]],[[2000,100,10,600],['treasure',(100,551)]]],
                    'back':[['chair',(400,450,148,180)],['password',(1400,400)]],
                    'object':[['lighttool',0.5,(1000,506),0,{'flip':True,'state':1}],['lighttool',0.5,(800,495),1],['lighttool',0.5,(300,482),2,{'flip':True}],
                              ['camera',0.5,(700,518),0],['mircophone',0.5,(1200,585),0,{'flip':True}],['rope',0.5,(1700,370),0,{'fix':False,'state':1}],
                              ['note',0.5,(1493,651),0,{'state':1,'value':'檔板很大，但很脆弱，請勿弄壞'}],
                              ['wbox',0.5,(150,622),5],['wbox',0.5,(230,622),5],['wbox',0.5,(1800,595),3],['wbox',0.5,(1900,608),4],['aircraft',0.1,(1050,400)]],
                    'front':[],
                    'effect':[],
                    },
        'treasure':{'background':[41,[0,0],[2010,720],[]],
                    'floor':660,
                    'trigger':[[[2000,100,100,600],['B3',(2150,509)]],[[0,0,10,600],['treasure2',(1900,551)]],
                               [[460,66,71,33],'Destroy_the_monitor','auto',['monitor2','monitor2'],{'rotate':-20,'variable':[810,200,400,500]}],[[1480,66,71,33],'Destroy_the_monitor','auto',['monitor2','monitor2'],{'rotate':20,'flip':True,'variable':[810,200,400,500]}],
                               [[650,500,20,51],'c4_boom','touch',['c4','c4']],[[1350,500,20,51],'c4_boom','touch',['c4','c4'],{'flip':True}],
                               [[781,519,20,51],'c4_boom','touch',['c4','c4']],[[1218,519,20,51],'c4_boom','touch',['c4','c4'],{'flip':True}]],
                    'back':[],
                    'object':[['gem',0.2,(1030,450),10,{'state':1}],['floor',0.45,(1010,520),1,{'visible':False}],
                               ['wbox',0.7,(150,590),6,{'flip':True}],['wbox',0.6,(350,600),6,{'flip':True}]],
                    'front':[],
                    'effect':[],
                    },
     'mortal room':{'background':[11,[0,0],[2600,720],[]],
                    'floor':660,
                    'trigger':[[[2610,100,100,600],['B3',(2800,509)]]],
                    'back':[['bld7',(200,100)],['bld2',(800,630)],['bld3',(150,570)],['bld3',(500,600)],['bld7',(600,300)],['bld7',(700,200)],['bld8',(250,500,26,42)],['bld5',(1000,200)],
                            ['bld7',(300,300)],['bld8',(450,450,26,42)]],
                    'object':[['c4',0.5,(50,628)],['c4',0.5,(120,628)],['patient',0.8,(200,625),0,{'live':0}],['patient',0.8,(550,615),3,{'live':0,'rotate':50}],
                              ['patient',0.8,(300,615),3,{'live':0,'rotate':130}],['patient',0.8,(700,615),3,{'live':0,'rotate':165,'flip':True}],
                              ['patient',0.8,(400,625),0,{'live':0,'rotate':190}],['patient',0.8,(600,625),0,{'live':0,'rotate':35,'flip':True}],
                              ['gun',1,(1280,620),0,{'flip':True,'state':1}]],
                    'front':[],
                    'effect':[],
                    },
               'B3':{'background':[23,[0,0],[3200,720],[]],
                    'floor':620,
                    'trigger':[[[900,255,230,330],['small room',(765,441)],'space',['door3']],[[300,255,230,330],['power room',(100,561)],'space',['door3']],[[1500,255,230,330],['treasure2',(100,551)],'space',['door3']],[[2100,255,230,330],['treasure',(1900,551)],'space',['door3']],[[2699,305,150,280],['mortal room',(2500,551)],'space',['door5']],[[3190,300,50,400],['staircase',(350,4803)]]],
                    'back':[],
                    'object':[['wblock',0.4,(2780,440),1,{'state':1}]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
               'B1':{'background':[80,[0,0],[5000,720],[]],
                    'floor':660,
                    'trigger':[[[250,500,20,51],'c4_boom','touch',['c4','c4'],{'flip':True}],[[1090,246,199,382],['staircase',(350,3537)],'space',['emergency exit']],[[2800,500,636,160],'car_inspect','z',['limousine','limousine'],{'flip':True}],[[1900,460,55,180],'notice_board','space',['notice board'],{'variable':'媒體工作者快捷電梯|(此電梯僅限媒體工|作者搭乘，非相關人|員請搭乘一般電梯)','variable2':5}],[[1600,325,250,300],'take_elevator2','space',['elevator']],[[4760,500,242,219],'block','touch',['block3','block3']],
                               [[4980,100,20,600],'display_end','touch',[],{'variable':'end1'}],[[3670,332,200,300],['security_room',(100,585)],'space',['iron door2']],[[3550,460,55,180],'notice_board','space',['notice board'],{'variable':'保全室|入內請出示身分','variable2':8}]],
                    'back':[['transformer box',(50,450,260,202)]],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
      'security_room':{'background':[14,[0,0],[1280,720],[]],
                    'floor':685,
                    'trigger':[[[0,246,20,382],['B1',(3750,560)]],[[870,100,97,58],'Destroy_the_monitor','auto',['monitor3','monitor3'],{'rotate':15,'variable':[0,150,1200,600]}],
                               [[100,430,55,180],'notice_board','space',['notice board'],{'variable':'保全室|入內請出示身分','variable2':8}]],
                    'back':[['table2',(1025,540),{'flip':True}],['chair2',(1190,620,50,50)],['badge',(1000,150,236,182)],['computer2',(1078,500,116,92)]],
                    'object':[['preservation',0.65,(1200,490),4,{'flip':True,'state':1}],
                              ['super_gun',0.5,(750,570),0,{'state':1,'rotate':90}],['super_gun',0.5,(650,570),0,{'state':1,'rotate':90}],['super_gun',0.5,(850,570),0,{'state':1,'rotate':90}]
                              ],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
              '1F':{'background':[10,[0,0],[5200,1000],[]],
                    'floor':900,
                    'trigger':[[[3790,550,295,345],['staircase',(350,2917)],'space',['door2']],[[4130,720,55,180],'notice_board','space',['notice board'],{'variable':'一般電梯|樓梯間','variable2':10}],[[4400,585,250,300],'take_elevator2','space',['elevator']],[[4700,720,55,180],'notice_board','space',['notice board'],{'variable':'媒體工作者快捷電梯|(此電梯僅限媒體工|作者搭乘，非相關人|員請搭乘一般電梯)','variable2':5}],[[5190,500,50,500],['1F_outside',(100,491)]]],
                    'back':[['lab1',(2000,710,172,204)],['lab3',(1700,660,142,240)],['lab4',(1400,685,190,230)],['lab5',(2300,600,208,168)],['lab6',(730,790,102,120)],['lab7',(2800,710)],['lab1',(3450,710,172,204)]],
                    'object':[['scientist',1,(1200,630),0,{'insert':[['righthand',['potion',0.2,(0,0),9,{'rotate':-40}]],['lefthand',['potion',0.2,(800,495),1]]]}],['scientist',1,(2800,630),3,{'flip':True}],['scientist',1,(2130,620),6],['scientist',1,(3578,620),6],['scientist',1,(870,630),9],['scientist',1,(1875,630),9],['scientist',1,(1455,595),12,{'flip':True}],['scientist',1,(3386,630),15,{'insert':[['righthand',['potion',0.2,(800,495),9]]]}]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]_
                    },
      '1F_outside':{'background':[62,[0,0],[3547,720],[]],
                    'floor':620,
                    'trigger':[[[0,300,20,700],['1F',(5100,791)]],[[900,410,152,193],'block','none',['block']],[[1300,0,300,720],'missile_protection','touch'],
                               [[300,235,300,300],'alarm','touch',[],{'variable':20}],[[3525,100,20,600],'display_end','touch',[],{'variable':'end2'}]],
                    'back':[],
                    'object':[['mpolice',0.45,(600,482),0],['wpolice',0.65,(700,437),0]],#['sword',0.3,(1020,550)],['gun',1,(400,620)],['super_gun',0.5,(300,520)],['c4',0.5,(600,520)],['shield',0.5,(800,420)],['specialforce',0.5,(1300,482),0,{'flip':True}]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        '2F_canteen':{'background':[32,[0,0],[1280,720],[]],
                    'floor':680,
                    'trigger':[[[1290,100,20,600],['2F',(300,491)]]],
                    'back':[],
                    'object':[['lettuce',0.2,(200,480),2,{'state':1}],['lettuce',0.2,(280,480),2,{'state':1}],['wbox',2,(550,600),7,{'state':1}],
                              ['rice',0.2,(355,480),0,{'state':1}],['rice',0.2,(415,480),0,{'state':1}],['rice',0.2,(470,480),1,{'state':1}],['floor',0.5,(305,516),1,{'visible':False}]],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
      '2F_kitchen':{'background':[35,[0,0],[1280,720],[]],
                    'floor':620,
                    'trigger':[[[-10,100,20,600],['2F_kitchen2',(1580,521)]],[[1290,100,20,600],['2F',(900,491)]]],
                    'back':[],
                    'object':[['spatula',0.2,(480,309),0,{'state':1}],['spatula',0.2,(505,309),1,{'state':1}],['spatula',0.2,(555,309),2,{'state':1}],
                              ['pan',0.2,(810,372),0,{'state':1}],['pan',0.2,(1140,402),0,{'state':1}],['lettuce',0.2,(960,395),1,{'state':1}],['lettuce',0.2,(920,395),1,{'state':1}],
                              ['knife',0.2,(450,392),1,{'state':1,'rotate':-55}],['knife',0.2,(360,392),2,{'state':1,'rotate':-40}],['wbox',2,(350,570),7]],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
      '2F_kitchen2':{'background':[52,[0,0],[1680,720],[]],
                    'floor':650,
                    'trigger':[[[1680,100,20,600],['2F_kitchen',(100,491)]],[[725,450,85,35],'cooking','z'],[[890,450,85,35],'cooking','z']],
                    'back':[],
                    'object':[['lettuce',0.2,(160,459),0,{'state':1}],['lettuce',0.2,(220,459),0,{'state':1}],['lettuce',0.2,(280,459),0,{'state':1}],
                              ['meat',0.2,(100,520),0,{'state':1}],['meat',0.2,(160,520),0,{'state':1}],
                              ['spoon',0.2,(590,467),0,{'state':1,'rotate':100}],['spoon',0.2,(550,465),0,{'state':1,'rotate':100}],
                              ['pan',0.25,(1210,472),1,{'state':1}],['knife',0.2,(1090,462),0,{'state':1,'rotate':-60}],
                              ['pot',0.3,(770,422),0,{'state':1}],['steamer',0.2,(930,428),0,{'state':1}],
                              ['wineglass',0.2,(1420,459),1,{'state':1}],['liquor',0.2,(1460,435),0,{'state':1}],['liquor',0.2,(1520,440),1,{'state':1}],
                              ],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
      '2F_coldroom':{'background':[91,[0,0],[1415,720],[]],
                    'floor':700,
                    'trigger':[[[1405,100,20,600],['2F',(1500,491)]]],
                    'back':[],
                    'object':[['pig',0.6,(250,425),1,{'state':1}],['pig',0.6,(250,523),1,{'state':1}],['pig',0.6,(820,570),1,{'state':1}],
                              ['fish',0.2,(520,513),0,{'state':1}],['fish',0.2,(630,513),0,{'state':1}],
                              ['meat',0.2,(193,625),0,{'state':1}],['meat',0.2,(260,615),0,{'state':1}],['meat',0.2,(362,610),1,{'state':1}],
                              ],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
    '2F_reception':{'background':[31,[0,0],[1280,720],[]],
                    'floor':650,
                    'trigger':[[[0,100,20,600],['2F',(2100,491)]]],
                    'back':[],
                    'object':[['wineglass',0.2,(570,450),0,{'state':1}],['wineglass',0.2,(450,480),0,{'state':1}],['wineglass',0.2,(680,450),0,{'state':1}],['wineglass',0.2,(800,480),0,{'state':1}],
                              ['liquor',0.2,(650,460),2,{'state':1}],['liquor',0.2,(630,480),2,{'state':1}],['liquor',0.2,(670,480),2,{'state':1}],['floor',0.5,(645,516),1,{'visible':False}]],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
       'restroom2':{'background':[71,[0,0],[1280,720],[]],
                    'floor':660,
                    'trigger':[[[0,100,10,500],['2F',(2690,487)]]],
                    'back':[],
                    'object':[],
                    'front':[],
                    'effect':[],
                    },
              '2F':{'background':[54,[0,0],[3200,720],[]],
                    'floor':600,
                    'trigger':[[[300,285,140,280],['2F_canteen',(1180,551)],'space',['door0']],[[900,285,140,280],['2F_kitchen',(1180,491)],'space',['door0']],[[1500,285,140,280],['2F_coldroom',(1315,600)],'space',['door0']],[[2100,285,140,280],['2F_reception',(100,551)],'space',['door0']],[[2699,285,140,280],['restroom2',(100,551)],'space',['door0']],[[3190,300,50,400],['staircase',(350,2293)]]],
                    'back':[['restroom',(2880,320,40,40)]],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
              '3F':{'background':[77,[0,0],[3600,720],[]],
                    'floor':600,
                    'trigger':[[[3590,300,50,400],['staircase',(350,1673)]],[[690,400,40,46],'master_key_lock','z',['sensor','sensor2']],[[280,0,100,720],'block']],
                    'back':[],
                    'object':[['hyena',0.2,(700,550),0],['hyena',0.2,(800,550),0],['hyena',0.2,(1000,550),0],['hyena',0.2,(1200,550),0],
                              ['hyena',0.2,(1400,550),0],['hyena',0.2,(1500,550),0],['hyena',0.2,(2000,550),0],['hyena',0.2,(2200,550),0]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        '3F_keyroom':{'background':[42,[0,0],[1280,720],[]],
                    'floor':650,
                    'trigger':[[[1260,100,20,600],['3F',(500,431)]],[[480,0,320,138],'outhole','touch',[],{'variable':'4F_keyroom'}]],
                    'back':[],
                    'object':[['ironbox',0.2,(130,590),0,{'value':[1,2,3]}],['ironbox',0.2,(130,520),0,{'value':[1,2,3]}],
                              ['ironbox',0.3,(1100,550),1,{'state':1,'value':[1,2,3]}]],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        '4F_keyroom':{'background':[61,[0,0],[1976,720],[]],
                    'floor':630,
                    'trigger':[[[-10,100,20,600],['4F_hide_room',(2100,431)]],[[1370,550,300,100],'enterhole','space',[],{'variable':'3F_keyroom'}]],
                    'back':[],
                    'object':[['crackhole',1,(1480,720),0,{'visible':False}],
                              ['ironbox',0.8,(1900,560),2,{'value':['1','2','3'],'flip':True}]],#
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
       '4F_hide_room':{'background':[60,[0,0],[2280,720],[]],
                    'floor':560,
                    'trigger':[[[2260,100,20,600],['4F_keyroom',(100,521)]],[[200,385,40,170],'sensor_door','z',['sensor3'],{'flip':True}],
                               [[0,500,10,100],'export_exit'],
                               [[281,360,20,51],'c4_boom','auto',['c4','c4']],[[281,220,20,51],'c4_boom','auto',['c4','c4']],
                               [[281,430,20,51],'c4_boom','auto',['c4','c4']],[[281,290,20,51],'c4_boom','auto',['c4','c4']],
                               [[0,175,63,366],'block','touch',['auto-door','auto-door']],[[0,0,238,130],'block','touch']
                               ],
                    'back':[],
                    'object':[['keys',0.1,(1228,346),0,{'state':1}],#,
                              ['ironbox',0.2,(390,450),0,{'state':1,'value':[0,1,9]}],['ironbox',0.2,(510,450),0,{'state':1,'value':[3,4,6,9]}],['ironbox',0.2,(645,450),0,{'state':1,'value':[7,8,12]}],
                              ['ironbox',0.3,(1810,450),1,{'state':1,'value':[2,5,6]}],['ironbox',0.3,(1950,450),1,{'state':1,'value':[12,13,14,15,10]}],
                              ['treasure',0.15,(-10000,0),0]#,['floor',0.4,(1226,380),0,{'visible':False}]
                              ],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
         '4F_exit':{'background':[34,[0,0],[1280,720],[]],
                    'floor':620,
                    'trigger':[[[-10,100,20,600],['4F',(200,431)]]],
                    'back':[],
                    'object':[],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
       'news_room':{'background':[37,[0,0],[2405,720],[]],
                    'floor':620,
                    'trigger':[[[0,100,10,600],['4F',(2620,431)]],[[1800,295,250,300],'take_elevator2','space',['elevator']],[[1650,430,55,180],'notice_board','space',['notice board'],{'variable':'媒體工作者快捷電梯|(此電梯僅限媒體工|作者搭乘，非相關人|員請搭乘一般電梯)','variable2':5}]],
                    'back':[],
                    'object':[],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
     'weapon_room1':{'background':[82,[0,0],[1280,720],[]],
                    'floor':620,
                    'trigger':[[[1269,300,50,400],['4F',(1360,431)]],[[0,300,10,400],['weapon_room2',(2300,565)]]],
                    'back':[],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
     'weapon_room2':{'background':[83,[0,0],[2490,720],[]],
                    'floor':670,
                    'trigger':[[[2200,345,175,320],['weapon_room1',(100,507)],'space',['door9']],[[1350,300,100,300],'plot','auto',[],{'variable':False,'variable2':'man1'}],[[120,500,950,150],'smash_obj','auto',[],{'variable':[[0,[]],[0,[]]],'variable2':0}]],#,[[1350,0,50,650],'block']],
                    'back':[],
                    'object':[['gun',1,(280,200),0,{'state':1}],['sword',0.3,(700,400),4,{'state':1}],
                              ['flame_gun',0.45,(300,300),0,{'state':1}],['sword',0.3,(700,200),1,{'state':1}],
                              ['super_gun',0.5,(300,370),0,{'state':1}],['sword',0.3,(700,300),2,{'state':1}],
                              ['flame_gun',0.45,(280,500),1,{'state':1,'name':'socket'}],['sword',0.3,(700,500),3,{'state':1}],
                              ['shield',0.5,(900,250),1,{'state':1}],['shield',0.5,(900,470),0,{'state':1}],
                              ['man1',1.1,(1200,535),4,{'insert':{'gun':['gun',1,(0,0)]}}],['wbox',0.2,(1260,635),0]],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
              '4F':{'background':[39,[0,0],[3676,720],[]],
                    'floor':530,
                    'trigger':[[[70,100,300,400],['4F_exit',(100,521)],'space'],[[400,350,55,180],'notice_board','space',['notice board'],{'variable':'禁止進入','variable2':10}],
                               [[1260,100,300,400],['weapon_room1',(1180,513)],'space'],[[1590,350,55,180],'notice_board','space',['notice board'],{'variable':'武器存放室|僅有經會長許可之人|才能進入，違反規定|人員經查獲將被嚴厲|懲處。','variable2':5}],
                               [[2470,100,300,400],['news_room',(100,508)],'space'],[[2800,350,55,180],'notice_board','space',['notice board'],{'variable':'新聞播放室|僅限新聞工作者進入|，非相關人員請勿進|入。','variable2':5}],[[3666,300,50,400],['staircase',(350,1053)]]],
                    'back':[],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
    'president room':{'background':[86,[0,0],[1280,720],[]],
                    'floor':550,
                    'trigger':[[[1170,250,100,300],['5F',(100,513)],'space'],[[800,500,170,30],'enterhole','space',[],{'variable':'4F_hide_room'}]],
                    'back':[],
                    'object':[['crackhole',1,(860,650),0,{'visible':False}],['flammable',0.3,(100,515),1,{'rigid':True}],['flammable',0.3,(190,515),1,{'rigid':True}],['flammable',0.3,(145,450),1,{'rigid':True}],
                              ['desk',0.5,(500,412)],['cabinet',0.5,(920,485)],['card',0.5,(348,322),1,{'state':1}]],
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
              '5F':{'background':[49,[0,0],[3882,720],[]],
                    'floor':620,
                    'trigger':[[[3872,300,50,400],['staircase',(350,433)]],[[0,300,100,400],['president room',(1180,442)],'space'],[[1750,300,50,300],'prison_5F','touch']],#[[500,300,20,300],'plot','auto',['door0'],{'variable':False,'variable2':'man1'}]],
                    'back':[],
                    'object':[['mpolice',0.45,(1500,482),0],['wpolice',0.65,(2000,437),0],['mpolice',0.45,(1600,482),0],['wpolice',0.65,(100,437),0],
                              ['specialforce',0.5,(1300,422),3,{'insert':{'gun':['super_gun',0.5,(0,0)]}}],['specialforce',0.5,(1600,392),7,{'insert':{'shield':['shield',0.5,(0,0)]}}]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
       'staircase':{'background':[20,[0,0],[1471,4917],[]],
                    'floor':4900,
                    'trigger':[[[100,4473,360,418],['B3',(3100,491)],'space',['safety door2']],[[1375,4269,55,25],'Destroy_the_monitor','auto',['monitor','monitor'],{'flip':True,'variable':[500,4500,1400,1000]}],
                               [[1440,4314,30,280],'block','touch',['pillar','pillar']],[[1370,4425,40,170],'sensor_door2','z',['sensor3']],
                               [[150,3922,295,345],['B2',(3100,491)],'space',['door2']],[[550,3967,250,300],'take_elevator','space',['elevator']],
                               [[100,3302,199,338],['B1',(1090,531)],'space',['emergency exit']],[[550,3345,250,300],'take_elevator','space',['elevator']],[[753,3100,45,42],'Destroy_the_monitor','auto',['monitor4','monitor4'],{'variable':[0,3300,400,500]}],
                               [[100,2675,295,345],['1F',(3900,791)],'space',['door']],[[550,2721,250,300],'take_elevator','space',['elevator']]
                               ,[[150,2053,295,345],['2F',(3100,491)],'space',['door2']],[[550,2096,250,300],'take_elevator','space',['elevator']]
                               ,[[150,1432,295,345],['3F',(3500,491)],'space',['door2']],[[550,1475,250,300],'take_elevator','space',['elevator']]
                               ,[[150,810,295,345],['4F',(3576,470)],'space',['door2']],[[550,855,250,300],'take_elevator','space',['elevator']]
                               ,[[130,190,350,345],['5F',(3782,491)],'space',['door10']],[[550,235,250,300],'take_elevator','space',['elevator']],[[100,235,900,300],'alarm','touch',[],{'variable':0}]],
                    'back':[],
                    'object':[['floor',0.8,(1150,4790),0,{'visible':False}],['floor',0.8,(980,4490),0,{'visible':False}],['stairs',0.8,(1132,4730),0,{'visible':False}],['floor',1,(1312,4620),0,{'visible':False}],['stairs2',0.8,(985,4435),0,{'visible':False}],['floor',1,(488,4303),1,{'visible':False}],
                              ['floor',0.8,(1150,4167),0,{'visible':False}],['floor',0.8,(980,3867),0,{'visible':False}],['stairs',0.8,(1132,4107),0,{'visible':False}],['floor',1,(1312,3997),0,{'visible':False}],['stairs2',0.8,(985,3812),0,{'visible':False}],['floor',1,(488,3680),1,{'visible':False}],
                              ['floor',0.8,(1150,3545),0,{'visible':False}],['floor',0.8,(980,3245),0,{'visible':False}],['stairs',0.8,(1132,3485),0,{'visible':False}],['floor',1,(1312,3375),0,{'visible':False}],['stairs2',0.8,(985,3189),0,{'visible':False}],['floor',1,(488,3057),1,{'visible':False}],
                              ['floor',1,(488,2434),1,{'visible':False}],
                              ['floor',0.8,(1150,2300),0,{'visible':False}],['stairs',0.8,(1132,2240),0,{'visible':False}],['floor',1,(1312,2140),0,{'visible':False}],['floor',1,(488,1810),1,{'visible':False}],
                              ['floor',0.8,(1150,1685),0,{'visible':False}],['floor',0.8,(980,1385),0,{'visible':False}],['stairs',0.8,(1132,1625),0,{'visible':False}],['floor',1,(1312,1520),0,{'visible':False}],['stairs2',0.8,(985,1320),0,{'visible':False}],['floor',1,(488,1188),1,{'visible':False}],
                              ['specialforce',0.5,(430,422),3,{'insert':{'gun':['super_gun',0.5,(0,0)]}}],['specialforce',0.5,(130,392),7,{'insert':{'shield':['shield',0.5,(0,0)]}}],['floor',1,(1312,895),0,{'visible':False}],['stairs2',0.8,(985,700),0,{'visible':False}],['floor',1,(468,585),1,{'visible':False}],],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    'text':[['5F',80,(255,255,255),(630,65)],['4F',80,(255,255,255),(630,685)],['3F',80,(255,255,255),(630,1308)],['2F',80,(255,255,255),(630,1930)],
                            ['1F',80,(255,255,255),(630,2555)],['B1',80,(255,255,255),(630,3177)],['B2',80,(255,255,255),(630,3800)]]
                    },
        'top floor':{'background':[88,[0,0],[1800,2140],[]],
                    'floor':1950,
                    'trigger':[[[1269,300,50,400],['4F',(1360,431)]],[[0,300,10,400],['weapon_room2',(2300,565)]],[[320,1625,250,300],'take_elevator','space',['elevator']],[[750,1535,1107,397],'helicopter','auto',['helicopter','helicopter']]],
                    'back':[['top floor',(0,1500)]],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        'not exist':{'background':[19,[0,0],[1280,720],[]],
                    'floor':620,
                    'trigger':[],
                    'back':[],
                    'object':[['boss',0.4,(0,0)],['keys',0.1,(0,0)]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
               'nb':{'background':[18,[0,0],[1600,720],[]],
                    'floor':660,
                    'trigger':[[[1240,330,140,280],['nb2',(540,1200)],'space',['door0']]],
                    'back':[],
                    'object':[['Eln', 0.2, (1200, 550)]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
              'nb2':{'background':[18,[0,0],[3200,1440],[]],
                    'floor':1300,
                    'trigger':[[[550,943,140,280],['nb',(1240,560)],'space',['door0']],[[1500,376,140,280],['nb3',(100,771)],'space',['door0']],
                               [[2480,923,250,300],['nb4',(100,521)],'space',['door8']]],
                    'back':[],
                    'object':[['floor',0.8,(520,530),1],['floor',0.8,(2800,400),0],['floor',0.8,(1800,680),1],
                              ['ladder',1,(300,1265)],['sword',0.3,(2920,368),2],
                              ['wblock',0.7,(2600,1060),0,{'state':1}],['cabinet',0.5,(1020,1230)]
                              ],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
              'nb3':{'background':[24,[0,0],[1280,971],[]],
                    'floor':870,
                    'trigger':[[[0,100,20,800],['nb2',(1500,500)]]],
                    'back':[],
                    'object':[['ladder',1,(700,870)]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
             'nb4':{'background':[7,[0,0],[1440,720],[]],
                    'floor':620,
                    'trigger':[[[0,330,20,280],['nb2',(2480,1200)]],[[750,330,30,100],['nb2',(2480,1200)],'hide'],
                               [[600,0,97,58],'Destroy_the_monitor','auto',['monitor3','monitor3'],{'rotate':-15,'flip':True,'variable':[950,200,500,400]}]],
                    'back':[],
                    'object':[['rake',0.5,(650,633)],['gem',0.2,(1240,630),10]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
             'nb_ex':{'background':[79,[0,0],[1701,720],[]],
                    'floor':620,
                    'trigger':[],
                    'back':[],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        'c_corridor':{'background':[12,[0,0],[2350,720],[]],
                    'floor':650,
                    'trigger':[[[0,100,20,600],['staircase',(1370,4455)]],[[1000,285,246,345],['c_lab',(100,581)],'none',['door4']],[[1460,285,246,345],['c_Storeroom',(100,581)],'none',['door11']],
                               [[1900,285,350,345],['c_staircase',(250,245)],'none',['door10']],[[0,0,10,10],'inspect_aircraft_die','auto']],
                    'back':[],
                    'object':[['aircraft',0.1,(1050,300)],['aircraft',0.1,(1150,400)],['aircraft',0.1,(1200,320)]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
            'c_lab':{'background':[26,[0,0],[2030,720],[]],
                    'floor':680,
                    'trigger':[[[0,100,20,600],['c_corridor',(1050,550)]]],
                    'back':[],
                    'object':[['girl',0.18,(1585,355),4,{'state':1,'rotate':75}],['lab_tube',1,(1524,445),0,{'state':1}]],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        'c_Storeroom':{'background':[8,[0,0],[1280,720],[]],
                    'floor':680,
                    'trigger':[[[0,100,20,600],['c_corridor',(1550,550)]]],
                    'back':[],
                    'object':[['floor',0.6,(620,575),1,{'visible':False}],['sword',0.3,(500,550),0,{'state':1}],['sword',0.3,(680,540),1,{'state':1}],
                              ['sword',0.3,(620,540),4,{'state':1}],['sword',0.3,(670,530),3,{'state':1}],['sword',0.3,(870,560),2,{'state':1}],
                              ['gun', 1, (980, 630), 0,{'rotate':-30,'state':1}],['gun', 1, (1050, 630), 0,{'rotate':-30,'state':1}],['gun', 1, (1120, 630), 0,{'rotate':-30,'state':1}],
                              ['flame_gun', 0.45, (730, 550), 0, {'state': 1}],['shield',0.5,(180,510),0,{'state':1}],['shield',0.5,(222,510),0,{'state':1}],['shield',0.5,(265,510),0,{'state':1}],
                              ['super_gun', 0.5, (930, 570), 0, {'rotate':90,'state':1}],['super_gun', 0.5, (1000, 570), 0, {'rotate':90,'state':1}],['super_gun', 0.5, (1070, 570), 0, {'rotate':90,'state':1}]
                              ],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        'c_staircase':{'background':[2,[0,0],[1280,1580],[]],
                    'floor':1570,
                    'trigger':[[[230,480,200,500],'block','touch'],[[40,1060,200,500],'block','touch'],[[150,10,350,345],['c_corridor',(1950,550)],'space',['door10']],
                               [[460,1232,175,320],['c_battle',(150,570)],'space',['door9']],
                               #[[460,1232,175,320],['c_boomhole',(100,2165)],'space',['door9']],
                               ],
                    'back':[],
                    'object':[['floor',0.8,(965,1490),0,{'visible':False}],['floor',0.8,(804,1160),0,{'visible':False}],
                              ['stairs',0.8,(956,1405),0,{'visible':False}],['floor',1,(1136,1310),0,{'visible':False}],
                              ['stairs2',0.8,(815,1115),0,{'visible':False}],['floor',1,(312,993),1,{'visible':False}],
                              ['floor',0.8,(972,867),0,{'visible':False}],['floor',0.8,(804,567),0,{'visible':False}],
                              ['stairs',0.8,(956,810),0,{'visible':False}],['floor',1,(1136,687),0,{'visible':False}],
                              ['stairs2',0.8,(809,512),0,{'visible':False}],['floor',1,(312,380),1,{'visible':False}],
                              #['sword', 0.3, (500, 250), 0, {'state': 1}],
                              #['super_gun', 0.5, (1000, 260), 0, {'state': 1}],
                              #['shield', 0.5, (180, 210), 0, {'state': 1}]
                              ],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
           'c_battle':{'background':[4,[0,0],[10000,720],[]],
                    'floor':670,
                    'trigger':[[[0,100,20,600],['c_staircase',(550,1470)]],[[9980,100,20,600],['c_nuclear',(100,570)]],[[0,0,10,10],'end_battle','auto'],
                               [[9600,450,40,60],'puzzle_square','auto',['sensor','sensor']],[[9890,-30,120,720],'block','touch',['c_door','c_door']]],
                    'back':[],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
        'c_nuclear':{'background':[5,[0,0],[1988,720],[]],
                    'floor':670,
                    'trigger':[[[0,100,20,600],['c_battle',(9900,570)]]],
                    'back':[],
                    'object':[['boom',0.2,(1470,550),3,{'state':1,'rotate':-30}],['boom',0.2,(1570,490),3,{'state':1,'rotate':-30}],
                              ['boom',0.2,(1650,530),3,{'state':1,'rotate':60}],['boom',0.2,(1630,560),3,{'state':1,'rotate':-30}],['boom',0.2,(1570,550),3,{'state':1,'rotate':-30}],['boom',0.2,(1530,520),3,{'state':1,'rotate':-30}],
                              ['ironbox',0.3,(1940,580),1,{'state':1,'value':[12,13,14,15,10]}],
                              ['bucket',0.4,(420,558),6,{'state':1}],['bucket',0.4,(560,558),6,{'state':1}],['bucket',0.4,(620,578),2,{'state':1}],
                              ['bucket',0.4,(720,578),1,{'state':1}],['bucket',0.4,(920,558),6,{'state':1}],
                    ],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
         'c_boomhole':{'background':[15,[0,0],[10000,2315],[]],
                    'floor':2265,
                    'trigger':[[[0,1700,20,600],['c_staircase',(550,1470)]]],#,[[0,0,10,10],'end_battle','auto']],
                    'back':[],
                    'object':[],    #[Chatacters[:3],posen]
                    'front':[],
                    'effect':[],                                                   #[[code,x,y,n,maxn,plus,循環],.....]
                    },
}
message={
    'Initial':[
        ['科技學會會長_165日前', '恭喜研究員GAVIN MORIN發表的「Engineering bacteria to search for specific concentrations of molecules by a systematic synthetic biology design method」論文獲獎，請各位多多和這位同仁學習請教。'],
        ['大樓管理員_159日前', '3樓毒氣室毒氣外洩，多位研究員昏迷，請各位勿往3樓移動。'],
        ['藥品批發有限公司_147日前', '您訂購的藥品\nCHLORPHENIRAMINE*3\nJENAC*2\nSIBELIUM*5\n已到貨，請查收。'],
        ['SCI器材中心_146日前', '您訂購的顯微鏡3組已到貨，請查收。'],
        ['黑旗集團_121日前','新實驗用人體10組已送至門口，請與大樓管理員查收。'],
        ['JAXON RANDOLPH_106日前', '聽說最近科技學會會長偷偷利用協會的錢買了一顆鑽石，你知道這個消息是不是真的嗎?'],
        ['藥品批發有限公司_105日前', '您訂購的藥品\nSILYMARIN*10\nVALISIN*3\nTRIAMCINOLONE*15\n已到貨，請查收。'],
        ['科技學會會長_103日前','研究員JAXON RANDOLPH違反研究員規定擅自進入一般研究員禁止進入的大樓B3，誤觸防盜系統死亡，請各位懷念他。'],
        ['藥品批發有限公司_93日前', '您訂購的藥品\nAMINOPHYLLINE*2\nCINNARIZINE*1\nSULFATRIM*6\n已到貨，請查收。'],
        ['SCI器材中心_80日前', '您訂購的酒精燒杯試管組合已到貨，請查收。'],
        ['科技學會會長_71日前', '近日經濟不景氣，多位研究員離職，請各位努力堅持住。'],
        ['藥品批發有限公司_64日前', '您訂購的藥品\nHUSTOSEL*7\nMETHYLEPHEDRINE*3\nSEDONIN*3\n已到貨，請查收。'],
        ['大樓管理員_56日前','4樓實驗室發生爆炸引發火災，造成多位研究員不幸離世，請各位懷念他們。'],
        ['科技學會會長_36日前','恭喜研究員JAIDEN DUFFY發表的「The effects of hepatitis C virus NS5A protein on ASPM phosphorylation and mitotic progression」論文獲獎，請各位多多和這位同仁學習請教。'],
        ['EMERY BANKS_19日前','科技學會會長用協會的錢買了大量的黃金收為己用。'],
        ['黑旗集團_18日前', '新實驗用人體10組已送至門口，請與大樓管理員查收。'],
        ['科技學會會長_15日前','最近有許多有關我挪用公款買私人物品的醜聞，此為不實的誹謗，造謠者EMERY BANKS已被懲處並逐出協會，請各位誤信造謠信息。'],
        ['大樓管理員_6日前','大樓內部電梯故障，工作人員緊急搶修中，請搶修期間所有研究員多多善用樓梯移動。'],
        ['大樓管理員_5日前','今日凌晨一樓樓梯間發稱大爆炸，整層樓梯被炸毀，事件起因被懷疑為人為所致，警方目前正調查中。'],
        ['大樓管理員_3日前','故障的電梯已搶修完畢，請各位同仁可安心使用。'],
        ['大樓管理員_2日前','今日清晨二、四樓樓梯間發稱爆炸，有多位深夜研究人員遭受波及造成死傷，目前警方懷疑事件與前幾天爆炸做案犯人相同，目前二樓以上禁止任何人進入。'],
        ['科技學會會長_2日前','近期事故頻繁，請各位同仁上班期間多加小心，警方目前已加強附近巡邏，大樓監控系統已大幅升級，不須擔心再有任合可疑人物進入。'],
        ['匿名帳號_1日前','會長在哪?']
    ]
}
notes=[
    ['工作資料','負責實驗編號:#1088\n實驗藥物:AMINOPHYLLINE'],
    ['帳號密碼','帳號:名子+@researcher.com \n密碼:130909495'],
    ['藥水配方','$potion_0$+$potion_1$=爆炸\n$potion_2$+$potion_4$+$potion_5$=火焰\n$potion_8$+$potion_9$=冰凍\n$potion_7$+$potion_11$=毒氣']
]
bullet_dictory={'gun':{'num':30,'cold':50,'bullet':'bullet1','size':(20,9),'speed':15,'shot_pos':(0,-25),'shot_pos2':(0,-25)},
                'aircraft':{'num':10000,'cold':50,'bullet':'bullet7','size':(62,8),'speed':10,'shot_pos':(40,-10),'shot_pos2':(40,-10)},
                'flame_gun':{'num':90,'cold':70,'bullet':'bullet3','size':(48,10),'speed':10,'shot_pos':(70,-25),'shot_pos2':(0,-25)},
                'super_gun':{'num':300,'cold':10,'bullet':'bullet2','size':(20,17),'speed':15,'shot_pos':(120,7),'shot_pos2':(120,-30)},
                'shield':{'num':100,'cold':10,'bullet':'bullet2','size':(20,17),'speed':20,'shot_pos':(120,7),'shot_pos2':(120,0)},
                'socket':{'num':30,'cold':70,'bullet':'bullet5','size':(80,20),'speed':10,'shot_pos':(40,-25),'shot_pos2':(0,-25)}
}
boom_effect_dictory={'fancy boom':[563,520],
             None:[0,0]
}
People=['player','scientist','patient','mpolice','wpolice','boss','an','kirito','specialforce','specialforce2','hyena','girl','preservation','aircraft']
Moveable_obj=['bucket','cabinet','sickbed','desk']
Cuttable_obj=['bucket','wbox','sickbed','wblock','lab_tube','aircraft']
Cookware=['pan','pot','steamer']
Meat=['scientist','patient','mpolice','wpolice','boss','meat','fish','pig','kirito']
Game_setting={
    'computer_setting':{'power_room':{'login':False,'anti-system':True,'anti-missile':True,'anti-weapon':True},'account':'HERBERT@researcher.com','password':'130909495','missile-password':'missile123','weapon-password':'038fhn3if'},
    'phone_setting':{'link':False,'flymode':True,'gps':True,'power':0},
    'police':{'mpolice':{'num':10,'size':0.45,'insert':{'gun':['flame_gun',0.45,(0,0)]}},
              'wpolice':{'num':10,'size':0.65,'insert':{'gun':['gun',1,(0,0)]}},
              'specialforce':{'num':1,'size':0.5,'insert':{'gun':['super_gun',0.5,(0,0)]}},
              'specialforce2':{'num':5,'size':0.5,'insert':{'shield':['shield',0.5,(0,0)]}}},
    'plot':{'man1':0,'Eln':0,'girl':0},
    'watch':{'man1':False,'Eln':True,'girl':True,'player':False,'kirito':False,
             'preservation':False,'boss':True,'scientist':True},       #角色看向右方時的flip
    'boom trigger':{'treasure2':False},
    'master_key_password':'op666',
    'people_talk':{'girl':['Initial room','B2_lab','B2','Sweep room','Storeroom','staircase','time_lab','small room','power room','treasure','treasure2','mortal room','B3','B1','1F','1F_outside','c_lab','c_Storeroom','c_corridor','c_nuclear','c_boomhole'],
                   'man1':['power room','staircase','3F','4F_hide_room','3F_keyroom','c_lab','c_Storeroom','c_nuclear','c_staircase','c_corridor']},
    'item_talk':{'girl':['gun','phone','c4','elevator_card'],
                 'man1':['ironbox']},
    'info':{'Initial room':'房間地板的裂縫似乎可以通往別處...','coffer':'在儲藏室的保險箱裡應該有什麼祕密','power room':'發現一台電腦，但旁邊有監視器','computer':'電腦需要登入的帳號資訊',
            'phone':'一台沒電的手機','elevator':'有一個電梯'},
    'hint':{'Initial room':['裂縫','如果有鑿子之類的應該可以鑿開吧?'],'coffer':['保險箱','密碼感覺會隱藏在某個地方...但藏在哪裡我也想不到...'],'power room':['監視器','如果能用什麼工具破壞掉就好了...'],
            'computer':['電腦','如果能從手機或筆記之類的應該能找到帳號密碼吧...'],'phone':['手機','需要充電器...'],'elevator':['電梯','應該能在哪裡找到電梯卡吧...']},
    'ending':{
        'end1':['tragedy end','在開車逃離大樓後，樓內警報不斷作響，在一陣混亂之中，保全們紛紛開車出動追擊，你則全速的逃離現場','不幸的是，由於你所開的車上裝有自動衛星定位系統，因此位置一下子就曝光了',
                '碰，一聲巨大的聲響，一起嚴重的交通事故發生在高架橋上，一輛黑色的長車從橋上墜落至下方，無法承受撞擊的力道摔成了碎片，橋上幾個人默默地看著橋的下方，拿起了對講機:','「確認目標物已排除---」'],
        'end2':['bad end','呼，呼，呼，你終於逃離了大樓，跑了一大段路後，你意識到你處於一個陌生的城市','由於身體已經一段時間沒有進食，在身無分文的情況下，你請求了警方的協助，請求幫忙聯絡家庭',
                '「好的，馬上幫你聯絡」眼前和藹的警察如此說道，你狼吞虎嚥的吃著他為你準備的食物，一邊靜靜的等待聯絡的結果','................','「是有點...想睡了呢...」累積多日的睡意迫使你閉上了雙眼','當你再次睜開雙眼，看到的是熟悉的研究室天花板，你又回到了原本所待的大樓研究室',
                '「我...被那個警察騙了嗎..」強烈的睏意侵蝕著你的大腦，你永遠沉睡了......'],
        'end3':['normal end','轟隆隆---轟隆隆---伴隨著大樓倒塌的聲音，你搭乘著直升機離開了那個拘束你多日的地方','「辛苦你了呢」在直升機駕駛座位的EMERY BANKS這樣對你說道，「這之後就不會有人受苦了呢...」多日的疲憊向你襲來，你看著那個男人的背影，進入了夢鄉',
                '睜開眼後，看見的是自己房間熟悉的天花板，旁邊是熟悉的家人面孔','「歡迎回家-------」'],
        'end4':['True end','炸出天坑過了不久，附近的居民趕來察看，不少警備人員也來進行搜救','被救出後，EMERY BANKS忙著處理後續的相關事宜，身為倖存者之一也是公司的前員工，被纏問了許多與公司相關的事，持續提供證言',
                '而受試者女孩則回到調查會進行資料和證據的提供，調查會也從公司的遺物中搜出不少機密檔案','而我，也回到那熟悉溫暖的家'],
    },
    'achieve':{'支援者殺手':'主動使支援角色死亡',
               '和平':'成功逃脫且無人受傷',
               '討厭科學':'一場遊戲中殺死5名以上科學家',
               '獵人':'擊敗3F所有敵人'
               }
}
dialogue={               #[n]:DoPose(n),string:說出string,(n):跳到選項n
      'player':{0:['給看見這張紙的任何頭腦清醒的人，這間公司已經完蛋了，理事長將公司的所有秘密藏在他的房間，萬能鑰匙就在3F進入機密門後的閣樓裡，機密門的密碼是op666，去行動吧'],
                1:['嗯......','......','......','這個地方是哪裡?'],
                2:['嗯......','先來看看周遭好了'],
                3:['.......','感覺是個實驗室','我被抓來做實驗了嗎!?','得快點逃']
                },
      'Eln':{0:[('resize',2),[3],'哈囉!歡迎你來到\nSkyscraper Escape','這個空間是新手教學教室，這裡的場景與劇情和遊戲內容完全無關~',[4],'那你現在準備好要開始接受教學了嗎?',[(2.5,'好了!'),(1,'還沒'),(2,'妳是誰啊?'),(100,'我要跳過教學')]],
             1:['嗯，好吧','......','......',[3],'那你現在準備好了嗎?',[(2.5,'好了!'),(1.5,'還沒有欸，再等我一下'),(2,'妳是誰?'),(100,'我要跳過教學')]],
             1.5:[[4],'嗯...',[3],'不管，我不等你了','我要直接開始教學',(3,0)],
             2:[[3],'我是新手教學輔導者，Elaina，是遊戲精靈',[4],[(2.5,'了解，請教學吧'),(1.5,'嗯，讓我思考一下')]],
             2.5:['好!那我們開始吧~',(3,0)],
             2.8:[[3],'嗯，好吧','先用鍵盤上↑下↓左←右→隨便移動吧',('resize',0.5),(3.5,0)],
             3:[[3],'請先用鍵盤上↑下↓左←右→移動試試看~~',('resize',0.5),(3.5,0)],
             4:[[4],'好!移動已經會了','那接下來我們移動到另一個房間吧','你跟著我走，按空白鍵可以進入門裡面!',[1],(4.5,0)],
             5:[('resize',1.6),[3],'這裡是教學的第二部分，道具篇~','麻煩你按z將旁邊的道具拿起來試試看',(5.5,0)],
             6:[[3],'好，那我這邊說明一下~','道具在持有後，會顯示在左下方的道具欄中，按a或用滑鼠點擊可以切換道具欄，按x則可放下當前的道具',[4],'試著把道具裝備在第三個道具欄看看~~',(6.5,0)],
             7:['good!','另外，z除了撿道具之外，還有使用道具和拖洩物品的作用喔','接下來請和我來~',('resize',0.625),(7.5,0)],
             8:['好了，就是這裡',[3],'現在這裡有一扇被木板釘住的門，試著去尋找並使用道具破壞它吧!',(8.5,0)],
             9:['Excellent!!!','太棒了，我們到門的另一端吧~',(9.5,0)],
             10:[[True],['point'],'你看，這裡的前方有一顆鑽石','為了防止這顆鑽石被小偷偷走，因此架設了監視器監視著,只要有人走到它的監視範圍內，就會警鈴大作，使警察出現',[3],[False],'注意，若被警察攻擊後就會死亡喔','監視器下方那支釘耙可以破壞監視器，請試著在不被警察追的情況下把鑽石拿給我吧~',[4],[(10.1,'如果死亡會怎麼樣?'),(10.2,'了解了!')]],
             10.1:['死亡的話遊戲會從被警察通緝前的存檔點開始，遊戲都是自動存檔',[(10.2,'了解了')]],
             10.2:['好!開始行動!',(10.5,0)],
             10.7:['Wow!你完成了呢!',(10.8,0)],
             11:[('resize',2),[3],'你已經把遊戲操作的都學會了!可以開始遊戲了!',[4],'要開始遊戲嗎?',[(15,'開始遊戲'),(12,' 這個遊戲的故事背景是什麼? ')]],
             12:['嗯，這個遊戲的故事設定是有一名受害者，它被送進一間公司當成實驗人體','本來應該不久就會死掉，但他在實驗過程中醒來，要逃離那間公司',[(15,'好!我要開始遊戲!'),(13,'有什麼遊戲提示嗎'),(14,'妳是不是遊戲的boss?')]],
             13:[[3],'遊戲中大多數的物品都單純是遊戲背景物件，是沒有作用的','不要浪費時間在研究那些物件上',[4],'按暫停後查看道具欄就能知道哪些是有用哪些是無用的道具了',[(100,'好!我要開始遊戲!'),(14,'妳是不是遊戲的boss?')]],
             14:['才不是，我看起來像是壞人嗎',[(15,'的確不像'),(16,'像是')]],
             15:[[6],'嗯!那就開始遊戲吧~',(100,0)],
             16:[['shock1'],'乾，屁啦哪裡像',[(15,'對不起，讓我開始遊戲吧')]],
             90:['想問關於遊戲操作的?',(90.5,0)],
             90.5:[[(91,'如何移動和進入門'),(92,'如何撿起和使用道具'),(93,'如何丟棄道具'),(94,'如何切換道具欄'),(95,'如何拖拉物品'),(96,'沒有要問的了')]],
             91:['按上↑下↓左←右→就可以移動了','進入門的話使用空白鍵','之後要進入電梯或洞穴的地方也可以用空白鍵進入~',(90.5,0)],
             92:['按Z可以撿起道具放入道具欄或使用當前道具欄的道具喔!',(90.5,0)],
             93:['用X可以把當前道具欄的道具棄下', (90.5,0)],
             94:['按A或用滑鼠點擊切換道具欄', (90.5,0)],
             95:['按Z可以抓住，按住Z左右←→移動可以拖移物品','但遊戲中並不是所有物品都能拖移喔，有些是固定住的', (90.5, 0)],
             96:['好，加油吧!',(97,0)],
             100:[[7],'如果想回顧教學的話，按暫停看遊戲說明就好囉!',('resize',0.5),'Good luck!',(101,0)]
             },
      'girl':{0.5:[('resize',1.6),[[0]],{'player':['嗯......','這個人也是和我一樣被抓來做實驗的嗎','這裡有幾個被實驗者呢']},('resize',0.625),(0.8,0)],
              1:[('resize',2),[4,1000],'嗶嗶嗶---','.......',[5],'正在初始化數據......','......','......',[6],'檢查四周......',[0],'發現一個受實驗者',[(2,'你是?')]],#,'哇!對了，我要買XISJ商店的限定商品啊',('resize',0.5),(2,0)],
              2:[[3],'啊',[8],'好，我先自我介紹',[3],'我是科學聯邦調查會製作的生化人','來這裡的目的是要查出這個地方的不法行為，因此偽裝成受實驗用人體混入','你身上沒有工作人員專用工作服及標誌，因此判定你為受實驗者',
                 [0],'這個地方很危險，趕快逃出去吧',[(3,'好，掰掰'),(4,'我逃不出去'),(5,'那妳要留在這裡幹嘛')]],
              3:[[0],'嗯路上小心',('resize',0.5),[0,1000],(3.5,0)],
              3.5:'stay',
              3.6:[[(3.7,'你在這裡做什麼'),(3.5,'離開')]],
              3.7:[[21],{'player':['watch_girl']},'watch_player','喔!','我現在在嘗試突破這棟大樓系統的防火牆，看能不能對外連線',[22],'你不趕快逃嗎?',[(4,'我逃不出去'),(3.8,'沒事，只是來問問')]],
              3.8:[[21],'嗯，快走吧!',(3.5,0)],
              4:[[8],'嗯......',[0],'說的也是，這裡應該有很多監控和守衛，還蠻難離開的',[8],'系統呼叫塔台，系統呼叫塔台','......',[0],'訊號被干擾----','......',
                 [3],'不然這樣吧，你告訴我目前你找到的線索，我可以來想逃出去的方法',[0],[(6,'告訴她這裡的事')]],
              5:[[8],'我要留在這裡尋找這間公司犯罪的證據',[0],'有了證據後就能合法逮捕這間公司的人員',[3],'但這間公司警備很嚴，因此用正常進入是不太可能的，只好偽裝成受實驗用人體進入',[0],
                 '你也趕快離開這個危險的地方吧',[(3,'好，掰掰'),(4,'我逃不出去')]],
              6:'talk_thing',
              7:[[3],'哦....原來如此...',[8],'嗯......',[3],'我身上除了有要找到這間公司犯罪證據的任務外，還有要確定所有受實驗者安全的職責',[0],'我和你一起尋找出口吧，我也可以順便調查',[(8,'好'),(3,'我自己找就好')]],
              8:['請多多指教了',('resize',0.5),[0,1000],(8.5,0)],
              8.5:'girl_follow',
              9:[[(10,'討論線索'),(12,'幫我一下'),(13.5,'關於生化人'),(14,'沒事了')]],
              10:'talk_information',
              12:[[0],'要幫你什麼?',[(15,'拿東西'),(16,'站著不動就好'),(14,'沒事算了')]],
              13:[[0],[(17,'妳要怎麼紀錄證據'),(18,'妳能打倒守衛嗎'),(19,'妳能與外部連線嗎'),(14,'沒事了')]],
              13.5:[[3],'?',(13,0)],
              14:[(14.5)],
              15:'girl_take_item',
              16:'stand',
              17: [[0], '嗯...', [3], '我是生化人，我的大腦有改造過', [8], '只要看過的東西都不會忘記，能夠紀錄在腦裡', [0],'需要時我可以把看過的東西畫出來，因此我可以算是一台人體相機', (13, 0)],
              18:['......','應該沒辦法',[0],'我的潛入設定是普通人，所以我的開發者製造我時力量設定和普通人一樣',[3],'但和普通人不同的是，我即便流很多血大腦也不會休克','也會使用武器',(13,0)],
              19:[[0],'可以，我的腦內有通訊器',[8],'但為了在混入實驗人體不被檢查發現，因此通訊器做的很小，功能並不完備',[3],'來這裡後我發現這裡有訊號干擾器，我無法傳遞訊息','情況有些不樂觀',[0],
                  '但在我被送入前，已經有約定過如果我在2天內沒有出來，他們將直接派人進入搜索',(13,0)],
              20:[[3],[[0]],'咦!怎麼會有手機','裡面有線索嗎?',[(21,'給她看'),(22,'手機沒有電')]],
              21:['notalk',[[5]],{'player':['給妳看']},'......','沒電了啊...','如果有充電器就好了'],
              22:['這樣啊...','如果有充電器就好了......',(22.5,0)],
              23:[[3],[[0]],'咦!手機充好了嗎?','我想看一下',[(25,'給她看'),(25.5,'取消')]],
              24:[[3],[[0]],'咦!怎麼會有手機','裡面有線索嗎?',[(25,'給她看'),(26,'有線索')]],
              25:['notalk',[[5]],{'player':['給妳看']},'......','原來如此...',[0],'這棟大樓最近發生好多事...','通往上層的方法現在只有電梯嗎...','如果要逃脫還是先看能不能從一樓就逃走好了......',(25.5,0)],
              26:['那我要看',[(25,'給她看')]],
              30:['啊!是電梯卡','我們趕快搭電梯逃走',(30.5,0)],
              31:[[0],'等一下',[[0]],'我突然想到，就算我們搭電梯逃生也沒辦法逃很久的','無論搭到哪個樓層他們都會追上來',{'player':'那怎麼辦'},'我來當誘餌，你先搭電梯逃走吧',[(32,'好'),(33,'我拒絕')]],
              32:['嗯，逃到高一點的樓層吧',(32.5,0)],
              32.5:'take_elevator_escape',
              33:['好吧，那一起趕快逃',(33.5,0)],
              40:[{'man1':['watch_girl',[0]],'player':['watch_girl']},[[0]],'嗶嗶嗶---','......','......',[5],'正在初始化數據......','......',[6],'檢查四周......',[3],'watch_man1','啊!你是EMERY BANKS',{'man1':['對!協助者妳好']},[8],'唔....',[3],'我睡了多久啊?',[(41,'將這期間發生的事告訴她')]],
              41:'talk_thing3',
              42:[[3],'watch_player',{'man1':['watch_girl']},'哦!原來如此',[8],'......',[3],'所以現在有辦法能逃出去嗎?','出口被堵住了','watch_man1',{'player':['watch_man1'],'man1':[[4],'......','我其實也對這個地方不熟，不知道哪裡有路可以出去',[0],'就我所知，這裡只有三個房間:研究室、儲藏室、還有一個機密房間']},'watch_player',
                  [(43,'這裡是研究室嗎'),(44,'儲藏間是儲存什麼?'),(44.5,'機密門裡有什麼?')]],
              43:['watch_man1',{'man1':['watch_player','對，這裡是研究室'],'player':['watch_man1']},'watch_man1',[3],'哦，那儲藏室裡有什麼?',[0],{'man1':['watch_girl','儲藏室平常是當擺設藥品的倉庫，沒甚麼重要的東西...','我們唯一的逃生希望就是裡頭的機密門了']},
                  'watch_player',[(45,'機密門裡面有甚麼嗎')]],
              44:['watch_man1',{'player':['watch_man1'],'man1':['watch_player','儲藏室平常是當擺設藥品的倉庫，沒甚麼重要的東西...','我們唯一的逃生希望就是裡頭的機密門了']},'這樣啊......','watch_player',[(45,'機密門裡面有甚麼嗎')]],
              44.5:['watch_man1',{'player':['watch_man1'],'man1':['watch_player','機密門裡我也不知道有什麼','聽說是理事長秘密研發的東西，所以裡面有許多守衛，蠻難進入的','但研究室和儲藏室是確定沒有任何其他進出口的','就期待機密門裡面真的有逃生路了']},[0],'這樣啊...',[3],'那好吧!我也覺得可以試試',(46,0)],
              45:['watch_man1',{'player':['watch_man1'],'man1':['watch_player','機密門裡我也不知道有什麼','聽說是理事長秘密研發的東西，所以裡面有許多守衛，蠻難進入的','就期待裡面真的有逃生路了']},'嗯，我也覺得可以試試',(46,0)],
              46:['watch_player',{'player':['watch_girl']},[(47,'同意'),(47,'我覺得可以'),(48,'我覺得不行')]],
              47:[[3],'好!那就去看看吧',(49,0)],
              48:['......','哪裡不行呢...',[(47,'沒事，可以')]],
              50:[[3],[[0]],{'man1':[[0],'這...威力太驚人了'],'player':['!!!'],},[3],'嗚哇......',('resize',0.33),[(-1500,0)],'這些炸彈威力好誇張',(51,0),{'man1':[[4],'嗯，好吧，既然坑炸出來了...我們要怎麼上去呢']},
                  [8],'......','哦!',{'man1':['怎麼了嗎?']},'watch_man1','我連接到外部的訊號了!','我可以發出求救訊號請他們過來',{'man1':['什麼!也太方便了吧','我回去之後也要自己做一台改造人']},
                  '要花很多錢的喔',{'man1':['哈哈哈']},(51,0)],
              },
      'man1':{0:[[(-1000,0)],[3],[False],[[0]],[['hollowness']],'不准動!!!','......','...你是...受實驗者?',[(1,'對'),(2,'不，我是來抓你的')]],
              1:['......','嗯......','那你是怎麼逃出來的?',[(1.5,'自己醒來，沒人在'),(2.1,'有協助者'),(3,'躲開監視器，關掉保全系統')]],
              1.5:['騙人，監視器那麼多，你是怎麼過的?',[(2.1,'有協助者幫助'),(3,'躲開監視器，關掉保全系統')]],
              2:[[3],'那你就死吧',(2.5,0)],
              2.1:['!','有協助者?','是誰?',[(2.2,'科技董事會的人員'),(2.3,'聯邦調查會的人員'),(2.2,'科學協會的人員'),(2.4,'我忘了')]],
              2.2:['......','沒聽過這個單位','不過為了保險起見，你還是死吧',(2.5,0)],
              2.3:['!',[4],'哦，原來如此',[0],'我確實有請求聯邦調查會的幫助','他們已經潛入到這裡來了啊...','好吧，我信任你','你趕快離開這危險的地方吧',[(3.7,'離開'),(4.5,'我找不到離開的方法'),(5,'你在這裡幹嘛?')]],
              2.4:['......',(2.5,0)],
              2.5:'shot',
              3:['!?','啥，這麼容易?',[4],'......',[3],'我不相信','這棟大樓的樓梯毀了，沒有電梯卡你也沒辦法上來的','你在騙我',[(2.1,'有協助者幫助'),(2,'對，我在騙你')]],
              3.5:[[(-1000,0)],[[0]],[(3.6,'可以再說一次密碼嗎'),(3.9,'再說一次我該怎麼逃'),(6,'你在這裡幹嘛?'),(4,'離開')]],
              3.6:['missile123',(3.5,0)],
              3.7:'leave2',
              3.8:[[(-1000,0)],[0],[[0]],[(3.7,'離開'),(4.5,'我找不到離開的方法'),(5,'你在這裡幹嘛?')]],
              3.9:['到監控室找到你們關掉監視器的電腦','飛彈防禦系統的解除密碼是missile123，去輸入就能解除','之後再幹掉門口的警衛就能逃離',(3.5,0)],
              4:'leave',
              4.5:[[[0]],'?','不是有協助者嗎',[(4.6,'告訴他之前發生的事')]],
              4.6:'talk_thing2',
              4.7:['......',[4],'原來如此，剛剛的警報就是你們搞出來的啊...',[0],'不過你那位協助者應該是不要緊的','她有流很多血但不死的體質，現在應該被人員抓到機密研究室研究',[(4.8,'那你能帶我逃脫嗎'),(4.9,'那你能救她嗎')]],
              4.8:['逃脫?','這簡單','這棟大樓1F設有飛彈防護系統，它會透過臉部辨識去偵測離開或接近這棟大樓的陌生人並攻擊','你們不是找到監控室的電腦嗎?','飛彈防禦系統的解除密碼是missile123，去輸入就能解除','之後再幹掉門口的警衛就能逃離',(3.5,0)],
              4.9:['......','我也許能','如果有機會的話',[(4.8,'那你能帶我逃脫嗎'),(5,'你要怎麼救')]],
              5:[[[0]],'......','...干你屁事，你趕快離開這裡吧',[(3.7,'離開'),(4.8,'我找不到逃脫的方法')]],
              6:['我不要告訴你，你趕快離開',[(4,'離開'),(6.1,'不要，因為我很好奇')]],
              6.1:['乾',[3],'不可以，你再不離開我就送你離開',[(4,'離開'),(2.4,'那你送我離開吧'),(6.6,'我有能力能幫你')]],
              6.6:['......','你有能力幫我?','......',[5],'哈哈哈有意思，那好吧',[0],'這棟大樓的某處藏著一顆鑽石，你若能找到那顆鑽石給我，那就證明你的能力',[(7.5,'好，我去找'),(7,'對不起，我沒能力')]],
              7:['那就快離開!',(3.5,0)],
              7.5:'Inspect_gem',
              8:[[(-1000,0)],[[0]],'......','你真的找到鑽石了呢','好吧，我就承認你的能力','既然你要幫我，我就把我的計畫告訴你','我叫EMERY BANKS，原本是這間公司的員工，剛開始我進入公司時，對公司所做的事還不知情','但有一天，我的朋友JAXON RANDOLPH告訴我和其他人，會長偷用公司的錢購買私人財物，結果隔天他就死亡了',
                 '於是我開始進行調查，發現了我朋友死亡的秘密','是被會長的身邊警衛抓走害死的!!','於是我離職，開始計畫對會長進行復仇','就在今晚!','如何?你要加入嗎?',[(9,'加入'),(10,'不要')]],
              9:[[0],'好，我現在先來說明一下我的計畫',[(0,0)],[True],'你看，這裡是公司的武器室，這裡擺滿了昂貴的武器','我們現在要奪取的武器是「火箭筒」，就在武器庫左下角的位置','如果沒有「火箭筒」，就無法擊敗5F會長室前的保全和會長身邊的警衛','但我們無法直接拿，因為這個武器庫設有自動保全系統',['pickup'],[True],
                 '只要一有東西進入',['use'],150,'就會被燒盡，因此我們無法進入',[0],'但是這個保全裝置有個開關，他就在監視器保全系統電腦的設定中','我們得去保全系統室操作電腦將這項設定關掉',[(-1000,0)],[False],'密碼是038fhn3if，很複雜，怕你忘記，我和你一起去好了','等到保全系統關閉，我們就可以拿火箭筒了',(11,0)],
              10:['不行，你已經聽了我今晚要復仇的事了，現在你只能答應我',[(9,'加入'),(2,'不要')]],
              11:'man1_follow',
              12:[[[0]],'太好了，我來說明接下來的行動',(12.5,0)],
              12.5:'man1_take_shield',
              13:[[[0]],{'player':['watch_man1']},100,'watch_player','我們等一下先想辦法到5F','不要坐電梯，會被門口的保全發現','當我們到5F時，你馬上用火箭筒偷襲5F門口兩個保全，這時警報器會大響','我們就抓緊時間，趕快衝進去，打敗路上的警衛到會長室中','然後把他轟掉!','在戰鬥過程中，你負責攻擊，我負責抵擋','這樣懂了嗎',[(14,'懂了'),(13,'再說一次')]],
              14:['好，開始行動!',(15,0)],
              15:'man1_to_5F',
              16:'end',
              17:'man1_walk_to_prison',
              18:[[[0]],[0],'什麼?',[True],[(-700,0)],(19,0)],
              19:'boss_walk',
              20:[{'boss':[[0],[['guffaw']],'哼哼~哈哈哈哈~','該死的老鼠，被我抓到了']},'可惡','你這個混帳傢伙，快放我們出去!把JAXON RANDOLPH的命還來!',{'boss':['哼，這個裝置是無法從內部破壞的!你們是不可能逃出這個機關的，就在這等死吧','等一下我的另一批部隊就來了，祝你們好運啦~']},[(21,'使用萬能鑰匙')]],
              21:'choose_prison_key',
              22:[{'boss':['什麼!怎麼可能!','居然被解開了']},[True],[5],'哈哈哈!報應啊!受死吧!',(23,0)],
              23:'boss_escape',
              24:[300,'耶!太棒了，打倒他了!','嗚呼~~',(25,0)],
              25:'Building_collapsed',
              26:[[[0]],[['alarm']],{'system':[['大樓系統通知--------封鎖系統已啟動，所有樓層鐵門已關閉，請各位同仁不要慌張，請在原處等待']]},[4],'這是...','不妙，大樓封鎖系統啟動了，要是一直待在這，我們會被抓到的',[0],'我的直升機停在頂樓，這棟大樓密道很多，我們趕快到頂樓逃出去',[0],
                  {'system':['shock']},'什麼?又怎麼了!?',[['alarm']],{'system':[['大樓警報!大樓警報!請所有員工同仁注意!!!',(255,0,0)],['大樓自毀系統已啟動，建築將於100秒後崩塌，請各位同仁趕緊疏散至大樓外!',(255,0,0)]]},[['earthquake']],'可惡的死東西...會長想將所有員工一起與他陪葬!',[0],'我們快逃!!',(26.5,0)],
              26.5:'Building_collapsed_savefile',
              28:[[0],'來，跟著我上來',(29,0)],
              29:'drive_helicopter',
              35:[{'player':['watch_man1',[0]]},'watch_player',[4],'......',[0],'你是要救協助者才放棄去頂樓，來這個地方的吧',[(36,'對'),(37,'不是'),(37,'我只是單純走錯路')]],
              36:['唉，雖然在你靠近這裡時就有想過，但還是和你過來了','這裡保存很多機密資料，建材非常堅固，不會倒塌的','就在這裡看看有什麼逃脫方法吧'],
              37:['......','算了',(36,0)],
              40:[[[0]],[0],'哦，她就是你之前說的那個協助者啊?',[(41,'對啊'),(42,'不是'),(41,'確實')]],
              41:[[0],'嗯......',[4],'如果有工具可以破壞儀器就好了...',(41.5)],
              42:[[0],'......','不!她是協助者沒錯，我認識她','她就是之前我請求聯邦調查會和我聯絡的人',[4],'如果有工具可以破壞儀器就好了...',(41.5,0)],
              43:[[[0]],{'girl':[[0],[False]]},'......',[4],'......','這間應該是藥品的儲藏室吧，之前我來這裡時應該是存放藥品沒錯',[0],'看來機密研究室在不對研究員開放期間會把要販賣的武器暫存在這個房間',{'girl':[[0],[True]]},(43.5,0)],
              43.5:'man1_take_gun',
              45:[{'player':['watch_man1'],'girl':['watch_man1']},[True],[4],'這...這是啥......',{'girl':['是要輸入密碼之類的嗎']},[4],'不是....感覺像要解題...',[5],'理事長平常都在搞些啥啊',(46,0)],
              50:[[(-720,0)],[0],'......',[4],'這些是...',[(51,'是炸彈'),(52,'是核彈吧'),(51,'!!!')]],
              51:['watch_girl',{'player':['watch_girl'],'girl':['好多...']},[4],[False],'嗯......這些炸彈上面有核能的標誌，該不會是核彈吧',(53,0)],
              52: [{'player':['watch_man1']},[4],'嗯...看起來挺像',(53,0)],
              53: [{'girl':['watch_man1','真的嗎?',[True],[8],'......','......',[3],'我想應該不是',[0]],'player':['watch_girl']},'watch_girl','!','什麼?為什麼',{'player':['watch_girl'],'girl':[[8],'因為',[3],'我感受不到核反應']},
                   {'player':['watch_man1'],'girl':['watch_player']},[0],'哦，你連這個都感受的出來嗎?','改造人真是方便',[4],'不過如果是這樣的話，這些假核彈的目的是......',[(54,'拿來以假亂真販賣吧'),(54,'想研發卻沒技術?'),(54,'拿來恐嚇?')]],
              54: ['watch_player',[4],{'girl':['watch_player',[3],'哦，有這個可能欸',[0],'watch_man1']},'嗯...的確是','我想一下','......','......',{'girl':[[True],'但總覺得奇怪...']},'......',[0],'欸，等等...不對','管理事長想拿這些來做甚麼，反正現在他也死了',{'girl':['watch_man1','!!']},[0],'我們現在應該要想怎麼逃出去才對',[(55,'拿炸彈炸出洞吧'),(56,'你有想法嗎?'),(57,'來探索房間有無密道好了')]],
              55: [[5],'哈哈，有道理',(58,0)],
              56: ['我在想能不能直接用這些炸彈炸出洞','哈哈',(58,0)],
              57:['哦，也是啦',{'girl':['watch_player','哦那我也來幫忙']},'就來探索一下吧','不過要小心一下這些炸彈就是了',(59,0)],
              58:['但挺危險的呢',[0],'如果它們的威力大到能幫我們炸出穿到地面的洞，那爆炸時我們一定要離的夠遠呢',{'girl':['watch_man1','不過的確可以試試呢','watch_player']},'watch_player','算了，反正就試試吧，也只能死馬當活馬醫了',(59,0)],
              59.5:['......','爆炸應該...結束了吧','去看一下好了',{'girl':['嗯好!']},(59.7,0)],
              60:[[0],[(60.5,'現在要做什麼'),(60.2,'離開一下'),(61,'關於這棟大樓'),(75,'沒事了')]],
              60.2:'tem_leave',
              60.5:'talk_now_do',
              61:['有什麼問題?',(61.2,0)],
              61.2:[[0],[(61.3,'關於樓層'),(65.7,'關於警備系統'),(70,'關於研究'),(75,'取消')]],
              61.3:['你想問幾樓?',(61.5,0)],
              61.5:[[0],[(65.5,'5F'),(65,'4F'),(64.5,'3F'),(64,'2F'),(63.5,'1F'),(63,'B1'),(62.5,'B2'),(62,'B3'),(75,'取消')]],
              62:['那是被禁止進入的樓層','只有理事長和它的一些親信可以去而已','監視器挺多的，之前JAXON RANDOLPH就是去那裏之後失蹤了，我為了調查是好不容易才潛下去沒被發現','但現在既然監視器都失效了，下去也變簡單了',(61.5,0)],
              62.5:['一般的研究員樓層，裡面還有儲藏室和廁所',(61.5,0)],
              63:['地下停車場，裏頭還有一間保全室',(61.5,0)],
              63.5:['一般研究員的工作地方',(61.5,0)],
              64:['會客室吧?','裡面還有食堂、廚房、冷凍庫',(61.5,0)],
              64.5:['......','在3F之上基本上研究員是無法去的','理事長養了好幾隻看門狗在3樓去看守裡面的一個房間，狗很兇殘和嗜血，之前有研究員去結果就沒再回來了','至於裡面的房間有什麼我也不知道','應該是一些機密文件和理事長偷偷貪的錢吧',(61.5,0)],
              65:['有一個新聞台，是我們公司在發布科學界新聞稿用的','還有一個武器室，除了警備人員以外都不准進入','第三個房間應該室緊急逃生口，但那個逃生門從沒有打開過.....','可能要發生什麼緊急狀況才會打開?',(61.5,0)],
              65.5:['理事長房間的所在地，裡面有很多警衛',(61.5,0)],
              65.7:['哪部分?',(66,0)],
              66:[[0],[(67,'監視器'),(68,'武器'),(69,'警衛'),(69.5,'陷阱'),(75,'沒事了')]],
              67:['監視器都是用機器自動辨識人臉抓入侵者的，基本上不會有真人看管','所以即便監視器壞了也不會有人發現',(66,0)],
              68:['這間公司有向海外購買大量違法武器，大多數是用來交易用途','只有理事長和高階長官知道',[4],'至於部分武器可能會留來自衛和肅清競爭對手的吧',(66,0)],
              69:['警備分為普通警察、保全、機械守衛三種','普通警察就很一般','保全身上有防彈衣，一般武器傷害不了他們，同時也持有較強的武器','啊順帶一提，我現在穿的也是防彈衣','另外，機械守衛是最難纏的傢伙，子彈要打好幾發才會壞，我來這裡前已經消除大半路上的機械守衛了',(66,0)],
              69.5:['你是說炸彈的部分嗎',[4],'嗯，感應式炸彈的確很麻煩',[0],'但只要小心避開就好了',(66,0)],
              70:['這間公司主要做生物基因改造、藥品製造，和物種研究','其他還有販賣毒品和武器交易作為收入來源，但多數的研究員都不知道','在表面上的研究多數都是合法的，但也有些違法的人體研究會在地下室進行',
                  '其中更為機密的研究室會在機密研究室進行','機密研究室在B2和B3之間，要特別的感應卡才能進入',[(71,'我是被拿來做甚麼研究?'),(72,'機密研究室裡有什麼'),(75,'了解了')]],
              71:[[4],'......',[0],'應該是新藥物研發吧','查看藥物在人體的反應之類的',[(72,'機密研究室裡有什麼'),(75,'了解了')]],
              72:['機密研究室只有在特別的時期才會讓研究員進入，平時不開放','但根據我之前進入的經驗，裡面有幾個高階儀器，還有大型人體試管，總之是連我也覺得很神祕的地方','據說為了保護機密文件，建材使用的極其堅固，能防大規模的地震',[(75,'了解了')]],
             }
}
Item_hint={
    'alcohol':['一瓶酒精燈',0,'感覺可以用來加熱東西'],
    'beaker':['這個杯子應該可以裝東西吧',0,'不過應該沒有用'],
    'book':['可以看一下書裡有甚麼線索'],
    'boom':['好危險...'],
    'broom':['這個掃把感覺可以用來掃地',0,'如果哪裡有灰塵應該可以清理一下吧','可能有東西會被灰塵蓋住'],
    'c4':['感覺很危險','到不得已的時候再使用好了','現在使用聲音可能會招來警衛'],
    'camera':[0,'......',3,'這應該是一個播電影的吧','我不知道有什麼用...'],
    'card':['可以用來通過一些感應器吧?'],
    'car_key':['應該是某台車的鑰匙','去找找看的話可能車裡有什麼秘密呢',0,'或許可以開車逃出去...'],
    'charge':['是手機充電線!','手機可以充電了!'],
    'fish': [0,'嗯...','肚子餓可以吃?','還是魚身體裡有藏督西需要解剖一下'],
    'flame_gun':['火焰槍'],
    'flammable':['箱子','易燃燒，可投擲'],
    'floor':['平台','可以站立在此上面'],
    'gem':['這是在博覽會被盜的鑽石!','如果能逃脫的話就帶回去歸還吧'],
    'aircraft':[0,'......',3,'會不會爆炸呀'],
    'gun':['帶著可以防身',0,'或是能擊碎某些東西吧...','這間公司非法持有武器......'],
    'hyena':['感覺好噁心'],
    'ironbox': ['某種高科技的箱子','無法被破壞'],
    'keys':['萬能鑰匙','能輕鬆打開各種鎖'],
    'kirito':['玩家','就是你'],
    'ladder':['還蠻好用的'],
    'lettuce':['生菜','富含纖維素'],
    'lighttool':['燈光設備','就是燈光設備'],
    'liquor':['喝了應該會醉'],
    'meat':['餓了可以吃?','......','我想不到其他的'],
    'microscope':['一台顯微鏡','應該用不到吧?'],
    'mircophone':['可以把聲音放大?',8,'......',0,'會不會把守衛引來呀'],
    'mpolice':[0,'......'],
    'note':['裡面應該會記錄一些重要資訊'],
    'pan': ['平底鍋', '能用來炒東西'],
    'patient':[0,'......','可憐的受害者'],
    'phone':['裡面應該有什麼重大情報'],
    'pig': ['一隻豬'],
    'pot': ['一個鍋子'],
    'potion':['一瓶藥水',0,'.......','不知道...我不懂化學...'],
    'rake':['釘耙','......','咦欸?','這能不能把監視器耙下來呀?','......'],
    'rice': ['飯'],
    'scientist':[0,'......','要搜他身嗎...'],
    'shield':['可以擋子彈'],
    'socket':['危險的武器'],
    'spatula': ['鍋鏟', '能用來炒東西'],
    'specialforce':[0,'......','那麼大隻你怎麼拿得動'],
    'spoon': ['湯勺', '能用來盛湯'],
    'steamer':['蒸籠','可以蒸東西'],
    'super_gun':['看起來是加特林，可以快速連續的發射子彈'],
    'sword':['嗯...','應該可以防身用和切一些東西',0,'......','是說這間公司為什麼會有劍'],
    'table':['桌子','能用來放置物品，可以被移動'],
    'testtube':['試管','實驗用品之一'],
    'treasure':['寶石','價值不斐'],
    'tripod':['一個三腳架','應該沒甚麼用吧'],
    'wbox':['墊腳箱','乾決鰻方便的'],
    'wineglass':['喝飲料用的杯子'],
    'wpolice':[0,'.......','警察的屍體']
}
Item_dictory={
    'alcohol':['酒精','實驗用品之一'],
    'beaker':['燒杯','實驗用品之一'],
    'wblock': ['木釘板', '可以釘住門'],
    'book':['書本','裡面可能會記錄一些重要資訊'],
    'boom': ['強力炸彈', '威力極大'],
    'boss':['科技學會會長','敵人角色'],
    'box':['隱形箱',''],
    'broom':['掃帚','可以用來清潔灰塵'],
    'bucket':['桶子','有各種顏色或材質，可以被移動',{7:['垃圾桶','可以被移動']}],
    'c4':['c4炸彈','使用拋擲會引發爆炸，請勿靠近'],
    'cabinet':['櫥櫃','能夠容納許多東西，可以被移動'],
    'camera':['電影播放器?','無法撥放影片，但似乎能以不同的視角看見世界'],
    'card':['卡片','可以用來感應感應器'],
    'car_key':['車鑰匙','某台車的鑰匙'],
    'charge':['充電線','手機用充電線'],
    'coffer':['保險箱','需要密碼才能開啟'],
    'crackhole':['裂洞','通往下方的洞'],
    'Eln':['Elaina','遊戲精靈，新手教學輔導者'],
    'desk':['桌子','能用來放置物品，可以被移動'],
    'exptable':['實驗桌','能用來放置物品，不可以被移動'],
    'fish': ['魚', '魚肉，料理後很好吃'],
    'flame_gun':['火焰槍','射出的子彈會爆炸',{1:['火箭筒','射出的子彈極具威力']}],
    'flammable':['箱子','易燃燒，可投擲',{2:['垃圾袋']}],
    'floor':['平台','可以站立在此上面'],
    'gem':['鑽石','極其珍貴'],
    'girl': ['???', '受實驗者之一'],
    'aircraft':['守衛機器人','會飛行並會對入侵者投射高能量光束'],
    'gun':['一般手槍','能發射子彈'],
    'hyena':['鬣狗','不要被他抓到'],
    'ironbox': ['某種高科技的箱子','無法被破壞',{2:['鐵箱','可以站立']}],
    'keys':['萬能鑰匙','能輕鬆打開各種鎖'],
    'kirito':['玩家','就是你'],
    'knife': ['菜刀', '做菜用具，也能切肉'],
    'lab_tube':['管蓋','固定管中的內容物'],
    'ladder':['梯子','可以攀爬'],
    'lettuce':['生菜','富含纖維素',{2:['生菜沙拉','用生菜做的沙拉']}],
    'lighttool':['燈光設備','就是燈光設備'],
    'liquor':['酒','喝了會醉',{2:['香檳','一種白葡萄氣泡酒']}],
    'man1':['EMERY BANKS','這間公司的前員工'],
    'meat':['肉','富含蛋白質'],
    'microscope':['顯微鏡','實驗用品之一'],
    'mircophone':['麥克風','可以用來唱歌'],
    'mpolice':['男警察','敵人角色，武器為火焰槍'],
    'note':['便條紙','裡面可能會記錄一些重要資訊'],
    'pan': ['平底鍋', '能用來炒東西'],
    'patient':['受實驗者','???'],
    'phone':['手機','能拍照、做紀錄、傳訊息'],
    'pig': ['豬', '豬肉的來源'],
    'pot': ['百寶鍋', '能裝入比本身大兩倍的物品，最多裝5個'],
    'potion':['藥水','實驗用品之一，一個瓶子能裝大量的藥水'],
    'preservation':['保全','管理地下室鐵門'],
    'rake':['釘耙','能擊碎脆弱的大地，或破壞上方的物品(如監視器之類)'],
    'rice': ['飯', '富含醣類'],
    'rope':['繩索','拉了不知道有什麼事會發生'],
    'scientist':['科學家','這間公司的員工'],
    'shield':['盾牌','能夠抵擋子彈'],
    'sickbed':['病床','受實驗者躺的床，可以被移動'],
    'socket':['火箭筒','射出的子彈極具威力'],
    'spatula': ['鍋鏟', '能用來炒東西'],
    'specialforce':['保全','敵人角色，身穿防彈衣，手持類武器也無法造成傷害，裝備為連續機關槍或盾牌'],
    'spoon': ['湯勺', '能用來盛湯'],
    'stairs':['樓梯(右)','可以攀爬'],
    'stairs2':['樓梯(左)','可以攀爬'],
    'steamer':['蒸籠','可以蒸東西'],
    'super_gun':['連續機關槍','可以快速且連續的發射子彈'],
    'sword':['劍','可用來砍東西'],
    'table':['桌子','能用來放置物品，可以被移動'],
    'testtube':['試管','實驗用品之一'],
    'treasure':['寶石','價值不斐',{9:['金塊','以純金打造'],10:['金塊堆','4個金塊堆成'],11:['金塊塔','10個金塊堆成']}],
    'tripod':['三腳架','實驗用品之一'],
    'wbox':['木箱','可用來墊腳',{3:['包包'],4:['包包'],5:['包包'],6:['包包']}],
    'wineglass':['酒杯','喝酒用的杯子'],
    'wpolice':['女警察','敵人角色，武器為一般手槍']
}
    #--------------------------------------------------------
Eevent_dictory={
    'block':['阻礙物','你無法由此通過'],
    'c4_boom':['感應式炸彈','一觸碰就會爆炸，同時觸發警報'],
    'monitor':['監視器','當大樓自動監視保全系統開啟時，被它拍攝到會觸發警報'],
    'use_computer':['電腦','可以控管大樓保全設備'],
    'notice_board':['告示板','通常是針對某個場所或設備的描述'],
    'car_inspect':['豪華禮車','某個人的，請勿嘗試駕駛'],
    'helicopter':['直升機','某個人的，請勿嘗試駕駛']
}
Game_instructions=[['↑','跳躍、攀爬(上)'],['← →','左右移動'],['↓','趴下、攀爬(下)'],['空白鍵','進入(門、通道、交通工具)、開啟、查看'],['A','切換道具'],['Z','撿起、使用、拖(道具、儀器)、輸入(密碼)'],['X','放下持有中的物品']]

def teleport(self,must=False):
    if terminal.door_lock or terminal.world.role.live!=1 or (not terminal.world.role.visible and self.key=='space') and not must:return
    if not terminal.world.alarm:terminal.savefile()
    if type(self)==list:functionkey=self
    else:
        for i in terminal.world.world['object']:  # 如果門被擋住，就無法傳送
            if i.name == 'wblock' and self.Touch(i): return
        functionkey=self.functionkey
        for flw in terminal.world.followbox:
            if flw.name == 'man1' and functionkey[0] in ('1F', 'B2_lab'):
                if len(self.world.talkbox)==0:self.world.Talk(flw, '別去那裡，我會被我的前同事看到')
                return
        if len(self.picturename) > 0 and 'door' in self.picturename[self.posen]: terminal.sound['door'].play()
    movebox, k = [], 0
    while k < len(terminal.world.world['object']):
        if terminal.world.world['object'][k].hide:
            terminal.world.world['object'][k].pos[0]-=10000
            movebox += [terminal.world.world['object'][k]]
            del terminal.world.world['object'][k]
        else:k += 1
    terminal.world.role.pos = [functionkey[1][0], functionkey[1][1]]
    terminal.world.change_scenes(functionkey[0])
    for follower in terminal.world.followbox:follower.pos=[terminal.world.role.pos[0],terminal.world.role.pos[1]]
    terminal.world.world['object'] += movebox
    for chr in terminal.world.world['object']:
        if chr.name=='hyena' and chr.live==1:
            try:
                chr.pos,chr.value=[chr.orig_pos[0],chr.orig_pos[1]],-3
                chr.role.loadpose(1,1000)
            except:chr.orig_pos=[chr.pos[0],chr.pos[1]]
def take_elevator(self):
    if 'elevator_card' not in terminal.world.props:
        terminal.world.Talk(terminal.world.role,'需要電梯卡')
        return
    if not self.islaunch:
        for flw in self.world.followbox:flw.tem_cold=1
        terminal.sound['elevator'].play()
        self.islaunch, n = True, 250
        self.world.world['back'] += [[terminal.image['elevator2'], self.rect[:2]]]
        terminal.tem = [n, self.rect[0], self.rect[1]]
        def open_elevator():
            if terminal.tem[0] > 0:
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 22 + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1],int(105 * terminal.tem[0] / n), 269])
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 232 - int(105 * terminal.tem[0] / n) + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1], int(105 * terminal.tem[0] / n),269])
                terminal.tem[0] -= 2
        def close_elevator():
            if terminal.tem[0] > 0 or terminal.world.busy:
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 22 + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1],105 - int(105 * terminal.tem[0] / n), 269])
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 126 + int(105 * terminal.tem[0] / n) + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1],105 - int(105 * terminal.tem[0] / n), 269])
                if terminal.tem[0] > 0: terminal.tem[0] -= 2
        def wait_select():
            self.world.busy = True
            self.world.paint_back = open_elevator
            while terminal.tem[0] > 0: sleep(0.03)
            self.world.Select(['Top', '5F', '4F', '3F', '2F', '1F', 'B1', 'B2', 'cancel'])
            while self.world.select == None:
                sleep(0.2)
                if not self.Touch(self.world.role): break
            self.world.selecting, self.world.paint_back, terminal.tem[0] = False, self.world.void, n
            if self.world.select not in [None, 'cancel']:
                self.world.role.pos, self.world.role.state = [self.rect[0] + 125, self.rect[1] + 185], 1
                self.world.paint_front = close_elevator
                for follower in self.world.followbox:
                    follower.pos=[self.world.role.pos[0]-30+int(60*random()),self.world.role.pos[1]-20]
                    follower.tem_cold=1
            else:
                self.world.paint_back = close_elevator
            while terminal.tem[0] > 1: sleep(0.2)
            if self.world.select not in [None, 'cancel']:
                pos = {'Top':[445, 1810],'5F': [675, 420], '4F': [675, 1042], '3F': [675, 1660], '2F': [675, 2281], '1F': [675, 2906],
                       'B1': [675, 3530], 'B2': [675, 4152]}[self.world.select]
                for i in self.world.events_box:
                    i[2]-=int(abs(pos[1]-self.world.role.pos[1])/240)
                    i[2]=max(i[2],time()+1)
                #if self.world.select=='Top':pos=None
                self.world.map['top floor']['floor']=10000
                self.world.role.pos, self.world.role.visible, terminal.world.role.control = pos, False, False
                for follower in self.world.followbox: follower.visible,follower.chroom= False,0
                if self.world.select=='Top':
                    self.functionkey = ['top floor', [445, 1810]]
                    teleport(self,must=True)
                elif self.world.select!='Top' and self.world.scenes_name=='top floor':
                    self.functionkey = ['staircase', pos]
                    teleport(self,must=True)
                    self.world.world['background'][1][0],self.world.world['background'][1][1]=0,-self.world.role.pos[1]+400
                else:
                    self.world.modify_speed = int(abs(pos[1] - self.world.role.pos[1]) / 3) + 40
                    if abs(pos[1]-self.world.role.pos[1])>300:
                        while self.world.modify_y[0] == 0: sleep(0.1)
                        while self.world.modify_y[0] > 0:sleep(0.2)
                for follower in self.world.followbox:follower.visible,follower.pos= True,[self.world.role.pos[0] - 30 + int(60 * random()), self.world.role.pos[1]]
                self.world.world['back'] += [[terminal.image['elevator2'], [self.world.role.pos[0] - 125, self.world.role.pos[1] - 185]]]
                self.world.paint_front, terminal.tem, self.world.role.visible = open_elevator, [n,self.world.role.pos[0] - 125,self.world.role.pos[1] - 185], True
                terminal.sound['elevator'].play(),sleep(0.2)
                self.world.map['top floor']['floor'] = 1950
                while terminal.tem[0] > 1: sleep(0.2)
                terminal.tem[0], self.world.paint_back, self.world.role.state, self.world.paint_front, self.world.modify_speed = n, close_elevator, 0, self.world.void, 40
                while terminal.tem[0] > 1: sleep(0.2)
            self.world.world['back'],self.world.role.control= [],True
            self.world.busy, self.world.paint_front, self.world.paint_back = False, self.world.void, self.world.void
            self.islaunch = False
        Thread(target=wait_select).start()
def take_elevator2(self):
    if 'elevator_card' not in terminal.world.props:
        terminal.world.Talk(terminal.world.role,'需要電梯卡')
        return
    if self.world.plot['girl'] == 32.5:
        girl=self.world.search2('girl')
        if girl==None:
            if len(self.world.talkbox)==0:self.world.Talk(self.world.role,'現在回去會被抓到...先躲到警報停...')
            return
    if not self.islaunch:
        for flw in self.world.followbox: flw.tem_cold = 1
        terminal.sound['elevator'].play()
        self.islaunch, n = True, 250
        self.world.world['back'] += [[terminal.image['elevator2'], self.rect[:2]]]
        terminal.tem = [n, self.rect[0], self.rect[1]]
        def open_elevator():
            if terminal.tem[0] > 0:
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 22 + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1],int(105 * terminal.tem[0] / n), 269])
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 232 - int(105 * terminal.tem[0] / n) + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1], int(105 * terminal.tem[0] / n),269])
                terminal.tem[0] -= 2
        def close_elevator():
            if terminal.tem[0] > 0 or terminal.world.busy:
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 22 + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1],105 - int(105 * terminal.tem[0] / n), 269])
                draw.rect(screen, (88, 88, 88), [terminal.tem[1] + 126 + int(105 * terminal.tem[0] / n) + terminal.world.world['background'][1][0],terminal.tem[2] + 32 + terminal.world.world['background'][1][1],105 - int(105 * terminal.tem[0] / n), 269])
                if terminal.tem[0] > 0: terminal.tem[0] -= 2
        def wait_select():
            self.world.busy = True
            self.world.paint_back = open_elevator
            while terminal.tem[0] > 0: sleep(0.03)
            self.world.Select(['4F','1F','B1','cancel'])
            while self.world.select == None:
                sleep(0.2)
                if not self.Touch(self.world.role): break
            self.world.selecting, self.world.paint_back, terminal.tem[0] = False, self.world.void, n
            if self.world.select not in [None, 'cancel']:
                self.world.role.pos, self.world.role.state = [self.rect[0] + 125, self.rect[1] + 185], 2
                self.world.paint_front = close_elevator
                for follower in self.world.followbox:
                    follower.pos=[self.world.role.pos[0]-30+int(60*random()),self.world.role.pos[1]-20]
                    follower.tem_cold = 1
            else:
                self.world.paint_back = close_elevator
            while terminal.tem[0] > 1: sleep(0.2)
            if self.world.select not in [None, 'cancel']:
                room={'4F':'news_room'}[self.world.select] if self.world.select in ['4F'] else self.world.select
                roomfloor={'news_room':4,'1F':1,'B1':0}
                for i in self.world.events_box:
                    i[2] -=2*abs(roomfloor[self.world.scenes_name]-roomfloor[room])
                    i[2] = max(i[2], time() + 1)
                for trigger in terminal.world.map[room]['trigger']:
                    if trigger.function != None and trigger.function.__name__ == 'take_elevator2':
                        self.functionkey = [room, [trigger.rect[0] + 125, trigger.rect[1] + 185]]
                if self.world.plot['girl']==32.5:
                    def stop_alarm():
                        sleep(8)
                        for i in range(200):
                            mixer.music.set_volume(bgm_vol*(200-i)/200),sleep(0.1)
                        self.world.play_bgm('hollowness'),mixer.music.set_volume(bgm_vol)
                        self.world.plot['girl']=32.6
                    terminal.door_lock,terminal.world.policebox,terminal.world.alarm,bgm_vol=False,[],False,terminal.bgm_vol
                    Thread(target=stop_alarm).start()
                    for obj in self.world.world['object']:
                        if obj.name=='girl':
                            self.world.nowbg.blit(transform.scale(terminal.image['bld1'],(300,60)),(obj.pos[0]-100,620))
                            self.world.world['object'].remove(obj)
                            for i in range(30):
                                self.world.nowbg.blit(transform.rotate(terminal.image['bullet1'],int(45+90*random())),(obj.pos[0]-500+int(1000*random()), 620))
                for follower in self.world.followbox:follower.chroom=0
                teleport(self)
                self.world.role.visible, self.world.role.control = False, False
                for follower in self.world.followbox:
                    follower.pos= [self.world.role.pos[0] - 30 + int(60 * random()), self.world.role.pos[1]]
                self.world.world['back'] += [[terminal.image['elevator2'], [self.world.role.pos[0] - 125, self.world.role.pos[1] - 185]]]
                self.world.paint_front, terminal.tem, self.world.role.visible = open_elevator, [n,self.world.role.pos[0] - 125,self.world.role.pos[1] - 185], True
                terminal.sound['elevator'].play()
                while terminal.tem[0] > 1: sleep(0.2)
                terminal.tem[0], self.world.paint_back, self.world.role.state, self.world.paint_front, self.world.modify_speed = n, close_elevator, 0, self.world.void, 40
                while terminal.tem[0] > 1: sleep(0.2)
            self.world.world['back'],self.world.role.control= [],True
            self.world.busy, self.world.paint_front, self.world.paint_back = False, self.world.void, self.world.void
            self.islaunch = False
        Thread(target=wait_select).start()
def shattered(self):
    def waiting_motion():
        self.world.busy = True
        try:
            while self.world.role.do_event[0]<80: sleep(0.1)
        except:pass
        terminal.sound['shield'].play()
        if self.life < 1:
            self.key, self.function = 'space', enterhole
            self.world.world['background'][0] = 22
            terminal.sound['collapse'].play()
            self.world.nowbg = self.world.allbackground['Initial room'] = transform.scale(image.load(f'{work_dir}scenes/22.png'),(1510, 720)).convert()
            for i in self.world.world['object']:
                if i.fix: i.Show(surf=self.world.allbackground['Initial room'])
            self.picturename,self.rect=['shattered3','shattered3'],[22,587,460,129]
            sleep(1)
        girl=self.world.search2('girl')
        if girl!=None and girl.state==0:
            self.world.talkbox=[]
            girl.DoPose(3),self.world.Talk(girl,['哇!開了!','...','能鑿開嗎?'][self.life])
            if self.life==0 and 'Initial room' in self.world.information:self.world.information.remove('Initial room')
        self.world.busy = False
    key = False
    for i in self.world.world['object']:
        if i.hide and type(i.hide)==bool and i.name == 'rake':
            key = True
            self.life -= 1
    if key:Thread(target=waiting_motion).start()
def hole_paint_back():
    terminal.world.role.Show((terminal.world.role.pos[0] + terminal.world.world['background'][1][0],terminal.world.role.pos[1] + terminal.world.world['background'][1][1]))
    screen.blit(terminal.image['shattered'+str(terminal.hole_back[0])],(terminal.hole_back[1][0]+terminal.world.world['background'][1][0],terminal.hole_back[1][1]+ terminal.world.world['background'][1][1]))
def enterhole(self):
    for obj in self.world.world['object']:
        if obj.name=='cabinet' and rect_touch(self.rect,obj):return
    item,terminal.hole_back= None,{'small room':[4,(0,624)],'4F_hide_room':[5,(722,501)],'3F_keyroom':[6,(1334,640)]}[self.variable]
    for i in self.world.world['object']:
        if i.hide and type(i.hide)==bool and i.visible and i in self.world.itemlist: item = i
    if item != None:
        def waiting_throw():
            def back_count():
                item.Show((item.pos[0] + self.world.world['background'][1][0],
                           item.pos[1] + self.world.world['background'][1][1]))
                if item.pos[1] + item.rects[item.posen][1] < 900:
                    item.pos[1] += self.sp
                    self.sp += 0.1
                screen.blit(terminal.image['shattered'+str(terminal.hole_back[0])],
                            (terminal.hole_back[1][0]+self.world.world['background'][1][0],terminal.hole_back[1][1] + self.world.world['background'][1][1]))
            self.world.role.control, self.world.busy, self.sp = False, True, 0
            self.world.role.DoEvent('throw', self.world.world)
            while self.world.role.eventing: sleep(0.1)
            self.world.role.Throw()
            self.world.paint_back, item.visible = back_count, False
            if item.name == 'ladder':
                item.DoPose(1, 1000)
            elif item.name == 'rake':
                item.rotate = item.role.rotate = 120
            elif item.name == 'broom':
                item.rotate = item.role.rotate = 90
            self.world.world['object'].remove(item)
            while item.pos[1] + item.rects[item.posen][1] < 720: sleep(0.2)
            self.world.role.control, self.world.busy, item.state, self.world.paint_back, item.visible, item.pos = True, False, 0, self.world.void, True, [1200 if self.variable=='4F_hide_room' else 600, -90]
            if item.name in ['rake', 'broom']: item.rotate = item.role.rotate = 120
            self.world.map[self.variable]['object'] += [item]
            self.world.calculate(self.variable)
        Thread(target=waiting_throw).start()
    else:
        self.world.role.DoEvent('enterhole', self.world.world)
        if self.world.role.eventing:
            self.world.role.lock = True
            def waiting_motion():
                while self.world.role.eventing: sleep(0.2)
                self.functionkey, self.world.paint_back = [self.variable,{'small room':(600,-90),'4F_hide_room':(1200,101),'3F_keyroom':(600,300)}[self.variable]], self.world.void
                self.world.busy, self.world.role.visible = False, True
                teleport(self)
                self.world.role.lock = False
            self.world.busy, self.world.paint_back, self.world.role.visible = True, hole_paint_back,False
            Thread(target=waiting_motion).start()
def outhole(self):
    def waiting_motion():
        if self.world.role.state!=0:self.world.role.state=0
        while self.world.role.eventing: sleep(0.1)
        if self.variable == '4F_keyroom':self.world.role.speed[1] = -10
        while self.world.role.speed[1]<0:sleep(0.1)
        self.world.role.visible, self.world.busy= True, False
        terminal.world.role.lock, terminal.world.role.control= True,True
    terminal.world.role.lock,terminal.world.role.control,terminal.world.role.speed[1],terminal.world.role.state=True,False,0,0
    self.functionkey,terminal.hole_back={'small room':['Initial room', (252, 898)],'4F_keyroom':['4F_keyroom',(1503,730)]}[self.variable],{'small room':[4,(0,624)],'4F_keyroom':[6,(1334,640)]}[self.variable]
    teleport(self)
    self.world.paint_back, self.world.role.visible= hole_paint_back,False
    self.world.role.DoEvent('enterhole', self.world.world)
    self.world.busy = True
    Thread(target=waiting_motion).start()
def sensor_door(self):
    for item in terminal.world.world['object']:
        if item.hide and type(item.hide)==bool and item.name=='card':
            terminal.sound['card'].play(),terminal.world.role.DoPose('use')
            for j in terminal.world.world['trigger']:
                if j.function!=None and j.function.__name__=='block':
                    self.functionkey,terminal.world.world['front']='None',[[transform.scale(terminal.image['auto-door-back'],(228,175)),(0,0)]]
                    for k in range(315):
                        j.rect[1]-=1
                        terminal.world.display()
                    terminal.world.world['trigger'].remove(j)
                    terminal.world.world['front'] =[]
                    break
            break
def sensor_door2(self):
    for item in terminal.world.world['object']:
        if item.hide and type(item.hide)==bool and item.name=='card':
            terminal.sound['card'].play(),terminal.world.role.DoPose('use')
            for j in terminal.world.world['trigger']:
                if j.function!=None and j.function.__name__=='block':
                    self.functionkey,pic='None',j.picturebox[0]
                    for k in range(280):
                        j.picturebox[0]=transform.scale(pic,(j.rect[2],j.rect[3]-k))
                        terminal.world.display()
                    j.function,j.functionkey=teleport,['c_corridor',(100,550)]
                    j.rect[0]+=20
                    break
            break
def GetPicture(self, pos, direct=0, scenesname=''):  # 0:全景照,1:側視照(向右),2:側視照(向左)
    if scenesname == '': scenesname = self.scenes_name
    all, x_pos = self.map[scenesname]['object'] + [self.role], pos[0]
    if direct in [1, 2]:
        surf, picturebox = transform.scale(self.picturebg, (self.map[scenesname]['background'][2][1], self.map[scenesname]['background'][2][1])).copy(), []
        while len(all) > 0:
            k, n, far = 0, 0, x_pos + [0, 1, -1][direct]
            while k < len(all):
                if (direct == 1 and all[k].pos[0] >= far > x_pos) or (direct == 2 and all[k].pos[0] <= far < x_pos):
                    far, n = all[k].pos[0], k
                elif (direct == 1 and all[k].pos[0] <= x_pos) or (direct == 2 and all[k].pos[0] >= x_pos):
                    del all[k]
                    continue
                k += 1
            if n < len(all):
                picturebox += [all[n]]  # 最遠的
                del all[n]
        box = []
        for chr in picturebox:  # 由遠而近
            rect, rate = chr.role.get_rect(), 360 / abs(chr.pos[0] - x_pos)
            img = transform.scale(terminal.blank.copy(), (int(rect[2]) + 20, int(rect[3]) + 20))
            chr.Show((chr.pos[0] - rect[0] + 10, chr.pos[1] - rect[1] + 10), surf=img)
            w, h, onfloor = int(rect[2] * 360 / abs(chr.pos[0] - x_pos)), int(rect[3] * 360 / abs(chr.pos[0] - x_pos)), \
                            rect[1] + rect[3] + 100 > self.map[scenesname]['floor'] - 50
            x, y = 360 + (int(
                ((rect[1] + rect[3] - self.map[scenesname]['floor']) / (720 - self.map[scenesname]['floor'])) * h) * (
                              1 if direct == 1 else -1) if onfloor else -int(w / 2)), rect[1] + rect[3] - h - int(
                (pos[1] - rect[1]) * rate / 2) * (1 if onfloor else 0) - 360 + int(360 * rate)
            if not chr.fix and chr.visible:
                box += [[chr.pos[0], transform.flip(transform.scale(img, (w, h)), direct == 2, False), (x, y)]]
        self.picture_render(box, x_pos, direct)
        for i in box:
            surf.blit(i[1], i[2])
        return surf
def command_to_character(command):
    command=copy_variable(command)
    command[0] = f'role/{command[0]}'
    info = command[3:]
    role = Character(*command[:3])
    if len(info) > 0:
        role.posen = info[0]
        role.role.loadpose(info[0], 1000)
        if len(info) == 2:
            role.change_attributes(info[1])
    else:role.role.loadpose(0, 1000)
    role.pose_finish=True
    return role
def charge(self):
    def wait_select():
        while terminal.world.select==None:
            sleep(0.1)
            if not self.Touch(self.world.role):
                break
        terminal.world.selecting = False
        if terminal.world.select!=None:
            if self.variable==0:
                self.posen,self.variable=1,['charge',0.1,self.rect[:2]]
                self.world.role.Throw()
                for i in terminal.world.world['object']:
                    if i.name=='charge':terminal.world.world['object'].remove(i)
            elif self.posen==1:
                if self.world.select=='拔充電線':
                    self.variable,self.posen=0,0
                    terminal.world.world['object']+=[command_to_character(['charge',0.1,[self.rect[0]+60,self.rect[1]+40]])]
                elif self.world.select=='手機充電' :
                    self.posen,self.variable2=2,time()
                    self.world.role.Throw()
                    for i in terminal.world.world['object']:
                        if i.name == 'phone':
                            terminal.world.world['object'].remove(i)
                    for i in range(len(self.world.itemlist)):
                        if self.world.itemlist[i]!=None and self.world.itemlist[i].name=='phone':self.world.itemlist[i]=None
            elif self.posen == 2:
                self.world.phone_setting['power']+=min(int((time()-self.variable2)*1.5),100-terminal.world.phone_setting['power'])
                self.variable2=time()
                if self.world.select == '拔除手機':
                    self.posen = 1
                    terminal.world.world['object'] += [command_to_character(['phone',0.1,[self.rect[0]+40,self.rect[1]+40],1])]
                else:self.world.Talk(self.world.role,str(int(self.world.phone_setting['power']))+'%')
            self.world.select=None
            self.world.display()
    if self.cold<time():
        if self.variable==0:
            get=role_item('charge')
            if get!=None:
                terminal.world.Select(['插入插座'])
        elif self.posen==1:
            get = role_item('phone')
            terminal.world.Select(['拔充電線']+(['手機充電'] if get!=None else []))
        elif self.posen == 2:
            terminal.world.Select(['拔除手機','查看電量'])
        Thread(target=wait_select).start()
        self.cold=time()+1
def cooking(self):
    def wait_select():
        while terminal.world.select==None:
            sleep(0.2)
            if not self.Touch(self.world.role):
                break
        terminal.world.selecting = False
        if terminal.world.select!=None:
            self.world.role.Throw(),get.Flip(False)
            fixpos,sound={'pot':[40,-35],'pan':[-10,-35],'steamer':[45,-22]}[get.name],{'pot':'stew','pan':'fry','steamer':'stew'}[get.name]
            get.pos,get.state,get.rotate=[self.rect[0]+fixpos[0],self.rect[1]+fixpos[1]],1,0
            terminal.sound[sound].play()
            if get.name=='pot':
                terminal.world.world['effect'] += [['fume', 120, -1,0.4,[self.rect[0],self.rect[1]-260,self.rect[2],200],2,1, 0]]
                terminal.world.world['effect'] += [['wide fire', 12, -1,0.7,[self.rect[0],self.rect[1]-45,self.rect[2],50],3,1, 0]]
            elif get.name=='pan':terminal.world.world['effect'] += [['wide fire', 12, -1,1,[self.rect[0],self.rect[1]-45,self.rect[2],50],8,1, 0]]
            elif get.name == 'steamer':terminal.world.world['effect'] += [['fume', 120, -1,0.4,[self.rect[0]-30,self.rect[1]-220,self.rect[2]+60,200],2,1, 0]]
            box=get.Inserted_item()
            for obj in box:
                try:obj.parent.surfbox[obj.parent.surfn][0],obj.role.mainlimb[0].surfbox[obj.role.mainlimb[0].surfn][0]=obj.surf_copy
                except:pass
                for part in obj.role.getparts():
                    img=part.surfbox[part.surfn][0]
                    L, H = img.get_size()
                    for l in range(L):
                        for h in range(H):
                            c = img.get_at((l, h))
                            if c[3] != 0:
                                if get.name=='steamer':
                                    m=min(max(c[0],c[1],c[2])+20,255)
                                    img.set_at((l, h),(c[0]+int((m-c[0])/2),c[1]+int((m-c[1])/2),c[2]+int((m-c[2])/2)))
                                else:img.set_at((l, h), (min(c[0] + 5, 255),min(max(c[1] + int((min(c[0] + 10, 255) - c[1] - 70) / 10 * 5), 0),255), min(max(int(c[2] / (max(5 // 2, 1))), 0), 255)))
                                #img.set_at((l, h), (min(c[0] + 5, 255),min(max(c[1] + int((min(c[0] + 10, 255) - c[1] - 70) / 10 * 5), 0),255), min(max(int(c[2] / (max(5 // 2, 1))), 0), 255)))
            self.world.select,self.world.role.control,self.world.busy=None,False,True
            while len(self.world.world['effect'])>0:sleep(0.2)
            terminal.sound[sound].stop()
            self.world.role.control,self.world.busy=True,False
    if self.cold<time():
        if self.variable==0:
            get=terminal.world.role.Throw(fix_item_pos=True)
            if get!=None and get.name in Cookware:
                self.world.useitem=None
                terminal.world.Select([{'pot':'燉一下','pan':'炒一下','steamer':'蒸一下'}[get.name]])
                Thread(target=wait_select).start()
        self.cold=time()+1
def car_inspect(self):
    def preservation_action():
        sleep(2)
        p_room = self.world.search('preservation', room_info=True)
        if p_room != None and self.world.scenes_name=='B1':
            preservation, preservation.pos = self.world.search('preservation'), [3670, 520]
            if preservation.live==1:
                self.world.map[p_room]['object'].remove(preservation)
                self.world.world['object'] += [preservation]
                self.world.Talk(preservation, '嘿!你在對那台車做甚麼'), preservation.DoPose(3,1000)
                self.world.play_bgm('nervous')
                self.world.alarm=True
                for police in terminal.world.policebox:
                    police.chroom += 500
                while preservation.live==1 and len(self.world.talkbox)>0:sleep(1)
                if preservation.live==1:
                    self.world.Talk(preservation, '警衛!警衛!快來!'),preservation.Flip(),preservation.DoPose(0)
                    while preservation.live == 1 and len(self.world.talkbox)>0: sleep(1)
                    if preservation.live==1:
                        self.world.world['object'].remove(preservation),preservation.DoPose(4,1000),preservation.Flip()
                        self.world.map['security_room']['object']+=[preservation]
                        preservation.pos,preservation.state=[1200,490],1
    for obj in self.world.world['object']:
        if obj.name=='car_key' and type(obj.hide)==bool and obj.hide:
            if yesno('是否要開鎖?','汽車鎖'):
                terminal.sound['unlock'].play(),terminal.world.display(),sleep(1),terminal.sound['anti_theft'].play()
                self.function,self.world.selecting= car_inspect2,False
                terminal.world.Select(['檢查車內', '開車']),Thread(target=wait_car_inspect).start()
                if not self.world.alarm:Thread(target=preservation_action).start()
            break
def wait_car_inspect():
    self=terminal.world.search_trigger('car_inspect2')
    if self!=None:
        while terminal.world.select == None:
            sleep(0.2)
            if not self.Touch(self.world.role):
                break
        self.world.selecting=False
        if terminal.world.select == '檢查車內':
            def inspect_car():
                def car_inside():
                    draw.rect(screen, (255, 255, 255), [238, 70, 805, 580]), screen.blit(transform.scale(image.load(f'{work_dir}scenes/81.jfif'), (795, 570)), (243, 75))
                    draw.rect(screen, (255, 0, 0), [1045, 75, 30, 30]), text_render(screen, 'X', 30, (255, 255, 255),(1050, 70))
                    if 'elevator_card' not in terminal.world.props: screen.blit(transform.scale(terminal.image['elevator_card'], (28, 52)), (660, 480))
                    display.update()
                def take_card():
                    if yesno('要拿走電梯卡嗎?'):
                        terminal.world.props += ['elevator_card']
                        systemhint('獲得道具:「電梯卡」')
                    car_inside()
                car_inside()
                terminal.Operation_panel([[[1045, 75, 30, 30], 'QUIT'], [[660, 480, 28, 52], take_card]])
                terminal.world.paint_front, terminal.world.busy = terminal.world.void, False
                terminal.world.display()
            terminal.world.paint_front, terminal.world.busy = inspect_car, True
        elif terminal.world.select == '開車':
            def render_car():
                x,flip,rect=self.world.role.pos[0]+self.world.world['background'][1][0]-300,1 if self.world.role.flip else -1,(self.world.role.pos[0]-300,450,636,210)
                screen.blit(transform.flip(car,flip==1,False),(x,500))
                tire_img=transform.rotate(tire['img'],2800-self.world.role.pos[0])
                fix=int(tire_img.get_rect()[2]/2)
                screen.blit(tire_img,(x+tire[flip][0]+37-fix,625-fix)),screen.blit(tire_img,(x+tire[flip][1]+37-fix,625-fix))
                if self.world.role.pos[0]>4600:
                    for trigger in self.world.world['trigger']:
                        if trigger.function!=None and trigger.function.__name__=='block':
                            terminal.world.world['trigger'].remove(trigger),terminal.sound['fall'].play()
                            explosion(trigger.picturebox[0],trigger.rect,target=['flammable'],blood=False,effect=None,fragments=3)
                            break
                if self.world.role.pos[0]<500:
                    for trigger in self.world.world['trigger']:
                        if trigger.function!=None and trigger.function.__name__=='c4_boom':
                            for flw in self.world.followbox:
                                if flw.name=='girl':
                                    flw.pos[0]=self.world.role.pos[0]
                                    self.world.world['object']+=[flw]
                            trigger.function(trigger,boom=True),explosion(transform.flip(car,flip==1,False),rect, blood=False, fragments=4)
                            self.world.paint_front=self.world.void
                            break
                for chr in self.world.world['object']:
                    if chr.name in People and chr.visible and chr.live==1 and rect_touch(rect,chr):
                        chr.live, chr.speed = 0.8, [-4*(1 if self.world.role.pos[0]>chr.pos[0] else -1), -3, 0]
                        if chr.id == 'scientist': chr.DoPose(18 + chr.posen // 3)
                        chr.rects[chr.posen][3] -= 120
                        terminal.sound['hitted'].play()
                for i in self.world.bullet:
                    if rect_touch2(rect,i[1]) and i[3][3]==1:i[3][3]=2
            tire={1:[49,490],-1:[75,514],'angle':0,'img':transform.scale(terminal.image['tire'],(74,74))}
            self.world.role.visible,self.world.role.pos[0],car=False,3100,transform.flip(transform.scale(terminal.image['limousine'],(636,160)),True,False)
            girl = self.world.search2('girl')
            if girl != None:
                if girl in self.world.world['object'] and girl in self.world.followbox: self.world.world['object'].remove(girl)
            self.world.paint_front=render_car
            if self in self.world.world['trigger']:self.world.world['trigger'].remove(self)
            terminal.sound['car_door'].play(),sleep(0.5),terminal.sound['car_engine'].play()
def car_inspect2(self):
    if not terminal.world.selecting:
        terminal.world.Select(['檢查車內', '開車'])
        Thread(target=wait_car_inspect).start()
def Destroy_the_monitor(self):
    try:monitor(self)
    except:pass
    key, terminal.world.usemode = 0, 'use'
    if abs(terminal.world.role.pos[0]-self.rect[0])<200*terminal.zoom and terminal.world.role.pos[1]-300*terminal.zoom<self.rect[1]:
        for i in terminal.world.world['object']:
            if i.hide and type(i.hide)==bool and i.name=='rake':
                terminal.world.usemode,key='use2',i
    if (key!=0 and terminal.world.role.eventing and terminal.world.role.do_event[0]>70 and terminal.world.role.do_event[2]==key) or self.variable==1:
        if self.variable==0:terminal.sound['shield'].play()
        self.variable,terminal.world.busy=1,True
        self.rect[1]+=6
        tapfloor=self.rect[1]>terminal.world.world['floor']
        if not tapfloor:
            for i in self.world.world['object']:
                if i.name=='floor' and rect_touch(self.rect,i):tapfloor=True
        if tapfloor:
            terminal.sound['fragmentation'].play()
            terminal.world.usemode='use'
            box,move,terminal.world.busy=splitimage(self.picturebox[self.posen],1),[(-15,-10),(15,-10),(-30,10),(30,10)],False
            for i in range(4):
                box[i].angle=random()*30
                box[i].setstart(),box[i].show(pos=(self.rect[0]+move[i][0],self.rect[1]+move[i][1]),surf=terminal.world.nowbg)
            terminal.world.world['trigger'].remove(self),terminal.world.display()
            if self.world.scenes_name=='power room':
                girl=self.world.search2('girl')
                if girl!=None:
                    self.world.Talk(girl,'哇!太好了!去看看電腦')
                    if 'power room' in self.world.information:self.world.information.remove('power room')
def export_exit(self):
    bg=Surface((1280,720))
    bg.blit(transform.scale(self.world.nowbg,(960,540)),(160,90)),bg.blit(transform.scale(image.load(f'{work_dir}scenes/85.png'),(1280,720)),(0,0))
    self.world.allbackground['4F_exit']=bg
    self.function=teleport
    self.functionkey=['4F_exit',(640,491)]
    self.world.map['4F_exit']['trigger']+=[Trigger([280,125,700,425],['4F_hide_room',(100,491)],self.world,key='space')]
def block(self):
    if terminal.player_setting['block']:
        if terminal.world.role.pos[1] > self.rect[1] + self.rect[3] and terminal.world.role.speed[1]<0:
            terminal.world.role.speed[1],terminal.world.role.pose_finish= 0,True
            #terminal.world.role.pos[1] = self.rect[1] + self.rect[3]
        else:
            if len(self.world.talkbox)==0 and 45>self.world.plot['man1']>=26 and self.world.scenes_name[-1]=='F':
                for chr in self.world.world['object']:
                    if chr.name=='man1':self.world.Talk(chr,'不行，這裡被封鎖了')
            if terminal.world.role.pos[0]>self.rect[0]+self.rect[2]/2:
                terminal.world.role.pos[0]=self.rect[0]+self.rect[2]-terminal.world.role.rects[terminal.world.role.posen][0]
            else:terminal.world.role.pos[0]=self.rect[0]-terminal.world.role.rects[terminal.world.role.posen][2]
        if terminal.world.role.pos[0] + terminal.world.world['background'][1][0] < 360 and terminal.world.world['background'][1][0]<0 and self.rect[0]+self.rect[2]>self.world.role.pos[0]:terminal.world.world['background'][1][0] = max(360 - terminal.world.role.pos[0],-terminal.world.world['background'][2][0]+1280)
def inspect_aircraft_die(self):
    k=0
    for i in self.world.world['object']:
        if i.name=='aircraft' and i.live==1:k+=1
    if k==0:
        for trigger in terminal.world.world['trigger']:
            if trigger.function != None and trigger.function.__name__ == 'teleport' and trigger.functionkey[0] == 'staircase':
                trigger.function = collapse_block
        terminal.world.alarm = False
        if self in self.world.world['trigger']:self.world.world['trigger'].remove(self)
def zoom_rect(rect,zoom):
    nrect=[]
    for i in rect:nrect+=[int(i*zoom)]
    return nrect
def monitor(self):
    if terminal.world.computer_setting['power_room']['anti-system'] and self.variable!=False and rect_touch(zoom_rect(self.variable,terminal.zoom),terminal.world.role) and not terminal.world.alarm:
        terminal.sound['alarm'].play()
        terminal.world.alarm,self.variable=True,False
        self.world.play_bgm('nervous')
def notice_board(self):
    terminal.world.Talk(terminal.world.role,self.variable.replace('|','\n'))
def plot(self):
    touch=rect_touch(self.rect,terminal.world.role)
    if self.variable and not touch:
        self.variable=False
        self.cold = time() + 1
    if not self.variable and touch and self.cold<time():
        self.variable=True
        terminal.world.loading_story(self.variable2)
        self.cold = time() + 1
def smash_obj(self):#名稱,初始,結尾(-1:最後),增量,rect[x,y,w,h,{rotate:0,flip:False,alpha=255}],播放次數(-1:無限),前後(0:後,1:前),計算禎
    if terminal.world.computer_setting['power_room']['anti-weapon']:
        for chr in self.world.world['object']+[self.world.role]:
            if chr.state==0:
                if rect_touch([self.rect[0],self.rect[1],self.rect[2]/2,self.rect[3]],chr) and self.variable[0][0]<1:
                    terminal.sound['fire'].play()
                    self.world.world['effect'] += [['spitfire',0, -1,1,[self.rect[0]-90,self.rect[1]-450,765,650,{'alpha':150}],1,1,0]]
                    self.variable[0][0]=140
                elif rect_touch([self.rect[0]+self.rect[2]/2,self.rect[1],self.rect[2]/2,self.rect[3]],chr) and self.variable[1][0]<1:
                    terminal.sound['fire'].play()
                    self.world.world['effect'] += [['spitfire',0, -1,1,[self.rect[0]-190+self.rect[2]/2,self.rect[1]-450,765,650,{'flip':True,'alpha':150}],1,1,0]]
                    self.variable[1][0]=140
                if rect_touch(self.rect,chr) and chr.name!='gem':
                    #chr.role.mainlimb[0].surfbox[chr.role.mainlimb[0].surfn][0]
                    for i in chr.role.getparts():
                        i.surfbox[i.surfn][0].blit(transform.scale(terminal.black2,i.surfbox[i.surfn][0].get_size()),(0,0))
                        i.surfbox[i.surfn][0].set_colorkey((0,0,0))
                        i.surfbox[i.surfn][0]=i.surfbox[i.surfn][0].convert_alpha()
                    if chr.id=='player':
                        if chr.live>0:chr.live-=0.02
                        else:chr.live=0
        if 0<self.variable[0][0]<10 or 0<self.variable[1][0]<10:
            for chr in self.world.world['object']:
                if rect_touch(self.rect, chr) and chr.state==0:
                    self.world.world['object'].remove(chr)
        self.variable[0][0]-=1
        self.variable[1][0]-=1
def alarm(self):
    for police in terminal.world.police:terminal.world.police[police]=self.variable
    if not terminal.world.alarm:
        terminal.sound['alarm'].play(),self.world.play_bgm('nervous')
    terminal.world.alarm=True
    terminal.world.world['trigger'].remove(self)
def puzzle_square(self):
    if type(self.variable)!=list:
        blank=[]
        for i in range(5):
            blank+=[[]]
            for j in range(5):blank[-1]+=[0]
    else:blank=self.variable
    bg=Surface((400,600))
    bg.fill((0,100,100)),text_render(bg,'Turn all white',50,(255,255,255),(50,25)),draw.circle(bg,(100,100,100),(200,545),40)
    text_render(bg, 'reset', 25, (255, 255, 255),(170,525))
    def up(update=True):
        for i in range(len(blank)):
            for j in range(len(blank[i])):
                draw.rect(bg,(255,255,255) if blank[i][j]==1 else (0,0,0),[14+75*j,120+75*i,72,72])
        self.picturebox[0] = transform.scale(bg, self.rect[2:])
        self.world.display(False),screen.blit(bg, (420, 60))
        if update:display.update()
    abc = 1
    if self.key == 'auto':
        abc, self.key = 0, 'none'
        up(False)
    else:up()
    while abc == 1:
        for event2 in event.get():
            if event2.type == QUIT:raise Error
            if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                x, y = mouse.get_pos()
                for i in range(len(blank)):
                    for j in range(len(blank[i])):
                        if 0<x-432-75*j<72 and 0<y-170-75*i<72:
                            terminal.sound['button2'].play()
                            for i2,j2 in [(0,-1),(1,0),(0,1),(-1,0),(0,0)]:
                                if 0<=i+i2<len(blank) and 0<=j+j2<len(blank[i]):
                                    blank[i+i2][j+j2]=[1,0][blank[i+i2][j+j2]]
                if ((x-620)**2+(y-600)**2)**0.5<40:
                    for i in blank:
                        for j in range(len(i)):i[j]=0
                    terminal.sound['button5'].play()
                if not (420<x<820 and 60<y<660):abc=0
                up()
                key=True
                for i in blank:
                    for j in i:
                        if j==0:key=False
                if key:
                    terminal.sound['hint'].play(),sleep(1),terminal.sound['auto-door'].play(),self.world.role.Flip(False),self.world.role.DoPose(0)
                    man1,girl=self.world.search2('man1'),self.world.search2('girl')
                    door,abc=terminal.world.search_trigger('block'),0
                    for chr in (man1,girl):
                        if chr!=None:
                            chr.eventing=True
                            self.world.Talk(chr,'哇!開了' if chr.name=='man1' else '窩嗚'), chr.Flip(chr.name=='girl')
                    for i in range(250):
                        door.rect[1]-=1
                        self.world.display(), wait_tap(),sleep(0.03)
                    self.key='none'
                    if man1!=None:self.world.Talk(man1, '進去看看吧')
                    for chr in (man1,girl):
                        if chr!=None:chr.eventing=False
        sleep(0.1)
    self.variable=blank
def end_battle(self):
    def add_aircraft(x,n,y=-100):
        for i in range(n):self.world.world['object']+=[command_to_character(['aircraft',0.1,(x-400+int(800*random()),y+int(600*random()))])]
    def all_aircraft(radius=10000):
        k,s=0,0
        while s<len(self.world.map['c_battle']['object']):
            if self.world.map['c_battle']['object'][s].name=='aircraft' and abs(self.world.map['c_battle']['object'][s].pos[0]-self.world.role.pos[0])<radius:k+=1
            if 0<self.world.map['c_battle']['object'][s].pos[0]<terminal.world.map['c_battle']['background'][2][0] or self.world.map['c_battle']['object'][s].name!='aircraft':s+=1
            else:del self.world.map['c_battle']['object'][s]
        return k
    def big_aircraft_exist():
        exist = False
        for obj in self.world.world['object']:
            if obj.name == 'aircraft' and obj.size == 0.3: exist = True
        return exist
    if not terminal.world.alarm:terminal.world.alarm=True
    if terminal.world.selecting:terminal.world.selecting=False
    if terminal.world.paint_front != terminal.world.void and not big_aircraft_exist():
        terminal.world.paint_front= terminal.world.void
    if self.variable==0:
        for police in terminal.world.police:
            terminal.world.police[police] = 0
        for i in range(8):
            add_aircraft(1000 * (i + 1), 3 + i,200)
        self.variable=1
    elif self.variable==1 and self.world.role.pos[0]>3000:
        for i in range(5):
            add_aircraft(self.world.role.pos[0] - 1000, 3)
        if not big_aircraft_exist():
            self.world.world['object'] += [command_to_character(['aircraft', 0.3, (self.world.role.pos[0] + 1200, 400), 0, {'value': 2}])]
            self.world.world['object'][-1].blood = -100
        man1, girl,self.variable= self.world.search2('man1'), self.world.search2('girl'),2
        if girl != None: self.world.Talk(girl, '什麼!')
        if man1 != None: self.world.Talk(man1, '可惡，竟然從後面包抄')
    elif self.variable == 2 and self.world.role.pos[0]>7000:
        for i in range(6):
            add_aircraft(self.world.role.pos[0] + int(1000 + 500 * random()) * (1 if random() < 0.5 else -1), 3, -600)
        self.world.world['object'] += [command_to_character(['aircraft', 0.3, (self.world.role.pos[0] + 1500, 500), 0, {'value': 2}])]
        self.world.world['object'][-1].blood = -100
        man1, girl,self.variable= self.world.search2('man1'), self.world.search2('girl'),3
        if girl != None: self.world.Talk(girl, '天啊')
        if man1 != None: self.world.Talk(man1, '竟然又從天花板出現')
    elif self.variable == 3 and all_aircraft(2000) == 0:
        self.world.people_talk['man1'] += ['c_battle']
        skk = 0
        while skk < len(self.world.world['object']):
            if self.world.world['object'][skk].name == 'aircraft':
                self.world.world['object'][skk].live = 0
                del self.world.world['object'][skk]
            else:skk += 1
        terminal.world.alarm = False
        terminal.world.world['trigger'].remove(self)
man1_walk=['走走走，快點去系統控制室','你在幹嘛，快走','快快快~去監視器保全系統電腦的設定做更改','先生，快沒時間了哦','密碼是038fhn3if，給我記好']
def talk_now_do(e):
    wait_talk_end(terminal.world.role,'現在要做什麼?')
    print(terminal.world.plot['man1'])
    if e.pl<15:
        if e.room == 'power room':
            wait_talk_end(e,'去解除武器庫的警報，密碼是038fhn3if' if terminal.world.computer_setting['power_room']['anti-weapon'] else '趕快去拿火箭筒')
        elif e.room == 'weapon_room2' and not terminal.world.computer_setting['power_room']['anti-weapon'] and e.tapfloor:
            wait_talk_end(e,'火箭筒在武器庫左下角，快去拿')
        else:wait_talk_end(e,'去監控室電腦關閉武器庫警報，密碼是038fhn3if')
    elif e.pl < 22:wait_talk_end(e,'去5樓進攻啦!')
    elif e.pl < 45:
        if terminal.world.plot['girl']<40:wait_talk_end(e, '找協助者!')
        else:wait_talk_end(e, '到機密門裡看一下')
def tem_leave(e):
    wait_talk_end(terminal.world.role, '我先暫時離開一下')
    if terminal.world.scenes_name[:2]!='c_':
        wait_talk_end(e,'好，快去快回')
        while e in terminal.world.followbox:terminal.world.followbox.remove(e)
        e.DoPose(0)
        terminal.world.world['trigger']+=[Trigger([e.pos[0]+e.rects[e.posen][0],e.pos[1]+e.rects[e.posen][1],e.rects[e.posen][2]-e.rects[e.posen][0],e.rects[e.posen][3]-e.rects[e.posen][1]],'wait_role','auto')]
    else:wait_talk_end(e,'不可以，現在隨便亂走會有危險')
def wait_role(self):
    if terminal.world.alarm:
        man1=terminal.world.search2('man1')
        if man1!=None:terminal.world.world['object'].remove(man1)
        terminal.world.world['trigger'].remove(self)
    elif self.Touch(terminal.world.role):
        if terminal.world.select == '繼續任務':
            man1 = terminal.world.search2('man1')
            if man1 != None and man1 not in terminal.world.followbox: terminal.world.Add_follow(man1)
            terminal.world.world['trigger'].remove(self)
        elif terminal.world.select == '!':terminal.world.Select(['繼續任務', '取消'])
        elif not terminal.world.selecting:terminal.world.Select(['!'])
    elif terminal.world.selecting and terminal.world.selectbox[0][2] in ('!','繼續任務'):terminal.world.selecting=False
def get_attack_angle(who, target, pose_ed):
    x, y = target.pos[0] - who.pos[0], target.pos[1] - who.pos[1] + 40
    z = (x ** 2 + y ** 2) ** 0.5
    angle, s = acos(abs(x) / z) / pi * 180 * (1 if y < 0 else -1), 0
    for i in pose_ed:
        if angle > i: return pose_ed[i], (x, y, z)
        s = i
    return pose_ed[s], (x, y, z)
def gun_attack(gun, shotpos):
    terminal.sound['missile' if gun.name=='socket' else 'shot'].play()
    terminal.world.bullet += [[bullet_dictory[gun.name]['bullet'], [
        gun.pos[0] + int(bullet_dictory[gun.name]['shot_pos2'][0] * (-1 if gun.flip else 1)),
        gun.pos[1] + int(bullet_dictory[gun.name]['shot_pos2'][1]), bullet_dictory[gun.name]['size'][0],
        bullet_dictory[gun.name]['size'][1]],
                               [int(bullet_dictory[gun.name]['speed'] * shotpos[0] / shotpos[2]),
                                int(bullet_dictory[gun.name]['speed'] * shotpos[1] / shotpos[2]), 0],
                               [gun.flip, acos(shotpos[0] / shotpos[2]) / pi * 180, False, 0]]]
def find_closed(who,name,x=True,y=True):
    m=[20000,None]
    for obj in terminal.world.world['object']:
        if obj.name==name and obj.live==1:
            w=(who.pos[0]-obj.pos[0])**2 if x else 0
            h=(who.pos[1]-obj.pos[1])**2 if y else 0
            d=(w+h)**0.5
            if d<m[0]:m=[d,obj]
    return m[1]
def man1_action(man1,world):
    def near(x,radius):
        return abs(man1.pos[0]-x)<radius
    def easy_talk(R,talk=0,remove=True,mode='room_event'):
        if type(R)==str:R=[[0,R]]
        man1.DoPose(R[man1.freeze][0])
        world.Talk(man1,R[man1.freeze][1])
        man1.freeze+=1
        if man1.freeze>=len(R):
            if remove:
                if mode=='room_event':world.people_talk['man1'].remove(world.scenes_name)
                else:world.item_talk['man1'].remove(mode)
            if talk==True:man1.freeze='talk'
            else:man1.freeze=talk
    def select_inspect(text='!'):
        if world.select == text:
            world.select,world.selecting = None, False
            if abs(world.role.pos[0] - man1.pos[0]) < 90:
                man1.pos[0] = min(world.role.pos[0] + 90 * (1 if world.role.pos[0] < man1.pos[0] else -1),world.world['background'][2][0] - 100)
                world.role.pos[0] = man1.pos[0] - 90 * (1 if world.role.pos[0] < man1.pos[0] else -1)
            man1.pl=world.plot['man1']
            face_to_face(),world.loading_story('man1',60)
            man1.tem_cold,world.plot['man1']=1,man1.pl
        elif not world.selecting and len(world.talkbox) == 0 and man1.tem_cold < 1 and not world.instory:world.Select([text])
    def face_to_face(both=True):
        man1.Flip(world.role.pos[0] < man1.pos[0]),man1.DoPose(0)
        if both:world.role.Flip(world.role.pos[0]>man1.pos[0]),world.role.DoPose('normal')
    def moveto(pos,radius,speed=2):
        if abs(pos[0]-man1.pos[0])>radius:
            if man1.pose_finish:
                man1.Flip(man1.pos[0]>pos[0])
                man1.DoPose(f'walk{man1.posen%2+1}')
            man1.pos[0]+=speed*(-1 if man1.flip else 1)*terminal.zoom
            man1.eventing=True
            return True
        man1.eventing = False
        return False
    if len(man1.nowdo)>0:
        if 'escape_boom' in man1.nowdo:
            if not moveto((-100,0),100,7.5):
                if world.scenes_name=='c_battle':
                    world.followbox.remove(man1),world.world['object'].remove(man1),man1.nowdo.remove('escape_boom'),man1.DoPose(0,1000)
                    world.map['c_staircase']['object']+=[man1]
                    man1.pos=[700,1470]
                elif world.scenes_name=='c_nuclear'==man1.room:
                    world.world['object'].remove(man1)
                    man1.chroom,man1.room=60000,'c_battle'
                    world.map['c_battle']['object']+=[man1]
                    man1.pos=[9990,570]
            elif world.scenes_name == 'c_nuclear' and man1.room == 'c_battle':man1.pos[0] -= 8
            if len(world.talkbox)==0:world.Talk(man1,'快!跑的越遠越好')
        return
    if not world.alarm and len(world.talkbox)==0:
        if world.scenes_name in world.people_talk['man1']:
            if world.scenes_name == '3F': easy_talk([[0, '喂!這裡很危險，不要來這裡']])
            elif world.scenes_name == 'staircase': easy_talk([[0, '從現在開始要小心一點了...']])
            elif world.scenes_name == 'power room': easy_talk([[0, '密碼是038fhn3if，快去輸入!']])
            elif world.scenes_name == '4F_hide_room': easy_talk([[4, '......'],[0,'大樓裡竟然還有這種房間']])
            #elif world.scenes_name == '4F_keyroom': easy_talk([[0, '密碼是038fhn3if，快去輸入!']])
            elif world.scenes_name == '3F_keyroom': easy_talk([[0,'第一次來這裡...']])
            elif world.scenes_name == 'c_corridor':
                k=0
                for i in world.map['c_corridor']['object']:
                    if i.name=='aircraft' and i.live==1:k+=1
                if k==0:
                    world.people_talk['man1'].remove('c_corridor')
                    world.loading_story('man1',35)
                    for trigger in world.world['trigger']:
                        if trigger.function != None and trigger.function.__name__ == 'teleport':
                            trigger.key='space'
            elif world.scenes_name == 'c_lab':
                girl=world.search2('girl')
                if girl.state==0 or girl==None:world.people_talk['man1'].remove('c_lab')
                elif near(girl.pos[0],200):
                    world.people_talk['man1'].remove('c_lab'),face_to_face(),world.loading_story('man1',40)
            elif world.scenes_name == 'c_Storeroom' and man1 in world.world['object'] and near(300,100):
                world.people_talk['man1'].remove('c_Storeroom'), world.loading_story('man1',43)
            elif world.scenes_name=='c_staircase':easy_talk([[0,'從現在開始現在要小心一點了']])
            elif world.scenes_name == 'c_battle' and world.role.pos[0]>9500:
                girl=world.search2('girl')
                if girl!=None and girl.tapfloor:
                    girl.DoPose(0),world.people_talk['man1'].remove('c_battle'),world.role.DoPose(0)
                    while moveto((9700,0),30,3):
                        world.display(),wait_tap()
                    world.loading_story('man1',45)
                    trigger,man1.eventing=world.search_trigger('puzzle_square'),False
                    if trigger!=None:trigger.key='z'
            elif world.scenes_name == 'c_nuclear' and world.role.pos[0]>1200:
                world.role.DoPose(0),world.people_talk['man1'].remove('c_nuclear')
                girl = world.search2('girl')
                while man1.pos[0]<800 or girl.pos[0]<920:
                    world.display(),wait_tap()
                girl.pos[0],man1.pos[0]=920,800
                girl.DoPose(0),world.loading_story('man1',50)
                world.world['trigger']+=[Trigger([0,0,10,10],'nuclear_boom',world,'auto',[],{})]
                terminal.savefile()
        elif abs(man1.pos[0] - world.role.pos[0]) < 100 and not man1.eventing and not world.alarm:select_inspect()
        elif man1.tem_cold > 0:man1.tem_cold -= 1
        elif world.selecting and world.selectbox[0][2] == '!':world.selecting = False
        if len(world.talkbox)==0:
            for item in world.world['object']:
                if item.name in world.item_talk['man1']:
                    if not item.hide and abs(item.pos[0]-man1.pos[0])<100:
                        if item.name=='ironbox' and item.posen<2:
                            easy_talk([[4,'寶箱?'],[0,'那傢伙到底貪了多少錢啊']], mode=item.name)
    try:e = man1.shotbox
    except:man1.shotbox = [None, 0, (0, 0, 0)]
    if world.scenes_name in ('3F','c_battle','c_corridor'):
        weapon=man1.Throw(fix_item_pos=True)
        if weapon!=None:
            if weapon.name=='shield':
                for obj in world.world['object']:
                    if obj.name=='hyena' and obj.pos[0]>man1.pos[0]-100 and obj.live==1:
                        if man1.posen!=3:man1.DoPose(3,50),world.Talk(man1,'這些狗很危險啊!')
                        man1.Flip(True)
                        obj.pos[0] = man1.pos[0] - 100
            elif weapon.name in ('gun','flame_gun','super_gun','socket'):          #man1.shotbox=[target,time,(x,y,z)]
                t=time()
                if man1.shotbox[0]!=None:
                    if t>man1.shotbox[1]:
                        if man1.shotbox[0].live!=1:man1.shotbox[0],man1.eventing=None,False
                        elif man1.pose_finish:
                            posen,man1.shotbox[2]=get_attack_angle(man1,man1.shotbox[0],{60:12,20:11,0:3,-30:10})
                            if posen==man1.posen:
                                gun_attack(weapon,man1.shotbox[2])
                                man1.shotbox[1]=t+bullet_dictory[weapon.name]['cold']/40
                            else:man1.DoPose(posen,50),man1.Flip(man1.pos[0]>man1.shotbox[0].pos[0])
                else:
                    for obj in world.world['object']:
                        if obj.name in ('hyena','aircraft') and abs(obj.pos[0]-man1.pos[0])<1200 and obj.live==1:
                            man1.shotbox[0],man1.eventing=find_closed(man1,obj.name),True
                            break
    elif man1.shotbox[0] != None:man1.eventing,man1.shotbox[0] = False, None
    if world.plot['man1']<15:
        if not world.alarm and len(world.talkbox)==0:
            if man1.room=='weapon_room2' and not terminal.world.computer_setting['power_room']['anti-weapon'] and man1.tapfloor:
                if not world.role.eventing and world.role.tapfloor:
                    for item in world.world['object']:
                        if item.name=='socket' and item.hide:
                            world.followbox.remove(man1)
                            world.loading_story('man1',12)
    elif world.plot['man1']<22:
        if man1.room == '5F':
            man1.follow_speed=6
            if man1.pos[0]>3500:
                man1.pos[0]-=3
            if abs(man1.pos[0]-world.role.pos[0])<300 and world.police_comespeed>0:
                for i in world.bullet:
                    try:
                        if rect_touch(i[1],man1.shield) and not i[3][2] and i[3][3]==1:
                            if i[0] == 'bullet3':
                                world.world['effect'] += [['boom', 0, -1, 0.3, [i[1][0] - 50, i[1][1] - 50, 100, 100], 1, 1, 0]]
                                world.bullet.remove(i)
                            elif i[0] == 'bullet5':
                                world.world['effect'] += [['fancy boom', 0, -1, 1, [i[1][0] - 640, i[1][1] - 360, 1280, 720], 1, 1, 0]]
                                explosion(None, i[1], target=People[1:] + ['specialforce'])
                                if i in world.bullet: world.bullet.remove(i)
                            else:
                                i[2], i[3][2] = [-i[2][0] / (3 + random() * 2), -abs(i[2][0] / 3) - random() * 3,i[2][0] / 2], True
                    except:
                        man1.shield=man1.Throw(fix_item_pos=True)
                if not man1.eventing:man1.Throw(fix_item_pos=True),man1.DoEvent('use',world.world)
            man1.Flip(True)
    elif world.plot['man1']==23:
        if man1.room == '5F':
            boss_live=False
            for chr in world.world['object']:
                if chr.name=='boss' and chr.live==1:
                    boss_live=True
            if not boss_live:
                terminal.world.loading_story('man1',24)
        else:man1.follow_speed=3
    elif world.plot['man1']==26.5:
        world.play_bgm('earthquake')
        Building_collapsed(man1,story=False)
        world.plot['man1'] = 26
def unlock_coffer(self):
    t=systeminput('輸入密碼')
    if t!=False:
        if t==self.variable:
            for chr in self.world.world['object']:
                if chr.name=='coffer' and rect_touch(self.rect,chr):
                    chr.DoPose(1,speed=1000)
                    self.world.world['object']+=[command_to_character(self.variable2)]
            self.world.world['trigger'].remove(self)
            girl=self.world.search2('girl')
            if girl!=None:girl.DoPose(3),self.world.Talk(girl,'哇!打開了')
            if 'coffer' in self.world.information:self.world.information.remove('coffer')
        else:systemhint('密碼錯誤')
def prison_5F(self):
    terminal.world.world['trigger'].remove(self)
    terminal.world.plot['man1'] = 17
    terminal.world.loading_story('man1')
def helicopter(self):
    if self.variable=='wait':return
    if self.variable=='end':
        display_end(Trigger([0, 0, 10, 10], 'display_end', self.world, 'touch', [], {'variable': 'end3'}))
        if self in self.world.world['trigger']:self.world.world['trigger'].remove(self)
        self.world.clearance = 3
    elif terminal.world.plot['man1']==26 and len(terminal.world.events_box)>0 and terminal.world.events_box[0][2]>time()+8:
        man1=terminal.world.search2('man1')
        if man1!=None:terminal.world.loading_story('man1',28)
    elif key.get_pressed()[K_SPACE] and rect_touch(self.rect,self.world.role) and len(self.world.talkbox)==0:
        if terminal.world.plot['man1'] == 29:
            def paint_front():
                screen.blit(transform.flip(helicopter_surf,set[1],False),(self.world.role.pos[0]+self.world.world['background'][1][0]-500,self.world.role.pos[1]+self.world.world['background'][1][1]))
                screen.blit(transform.scale(transform.rotate(propeller,set[0]),(918,200)), (self.world.role.pos[0]+self.world.world['background'][1][0]+(200 if set[1] else 0)-500,self.world.role.pos[1]+self.world.world['background'][1][1]))
                set[0]+=20
            def move_helicopter():
                sleep(2)
                for i in range(50):
                    self.world.role.pos[1]-=10
                    self.world.role.pos[0] -= 3
                    sleep(0.05)
                set[1],self.world.role.pos[0]=True,838
                for i in range(100):
                    self.world.role.pos[1]-=10
                    self.world.role.pos[0]+=1
                    sleep(0.05)
                for i in range(80):
                    self.world.role.pos[0]+=30
                    sleep(0.05)
                hel.stop()
                self.variable='end'
            hel=terminal.sound['helicopter']
            hel.play()
            self.world.role.state,self.world.role.control,self.world.role.visible,self.world.role.pos=2,False,False,[1250,1535]
            helicopter_surf,propeller,set=transform.scale(terminal.image['helicopter2'],(1107,397)),transform.scale(terminal.image['propeller'],(918,918)),[0,False]#angle,direct
            self.picturebox=[]
            Thread(target=move_helicopter).start()
            self.world.paint_front,self.variable=paint_front,'wait'
        else:terminal.world.Talk(self.world.role,'我不會開')
#-----------------------------------------------
def shot(e):
    terminal.sound['shot'].play()
    terminal.world.role.freeze=100
    gun=e.Throw(fix_item_pos=True)
    terminal.world.bullet += [[bullet_dictory[gun.name]['bullet'], [gun.pos[0] + bullet_dictory[gun.name]['shot_pos2'][0] * (-1 if gun.flip else 1),gun.pos[1],bullet_dictory[gun.name]['size'][0], bullet_dictory[gun.name]['size'][1]],[bullet_dictory[gun.name]['speed'] * (-1 if gun.flip else 1), 0,0], [gun.flip, 0, False, 1]]]
def leave(e):
    terminal.world.plot['man1']=3.5
    e.DoPose(0)
def leave2(e):
    terminal.world.plot['man1']=3.8
    e.DoPose(0)
def Inspect_gem(e):
    for i in terminal.world.world['object']:
        if i.name=='gem' and i.hide and type(i.hide)==bool:
            terminal.world.loading_story('man1',8)
    if terminal.world.plot['man1']==7.5:
        terminal.world.Talk(e,'快去找鑽石吧')
        while len(terminal.world.talkbox) > 0:
            terminal.Wait(False),terminal.world.display()
        terminal.Wait()
    get=terminal.world.search('gem',room_info=True)
    if get==None:
        terminal.world.map['treasure']['object']+=[command_to_character(['gem',0.2,(1030,450),10,{'state':1}])]
def man1_follow(e):
    for trigger in terminal.world.world['trigger']:
        if trigger.function!=None and trigger.function.__name__=='plot':
            terminal.world.world['trigger'].remove(trigger)
    terminal.world.Add_follow(e)
    if 'elevator_card' not in terminal.world.props:terminal.world.props+=['elevator_card']
def man1_take_shield(e):
    target,terminal.world.computer_setting['power_room']['anti-weapon']=0,False
    for chr in terminal.world.world['object']:
        if chr.name=='shield' and chr.posen==0:
            target=chr.pos[0]
    e.Flip(e.pos[0]>target)
    while abs(e.pos[0]-target)>10:
        if e.pose_finish:
            e.DoPose([1,2][e.posen%2])
        e.pos[0]+=3 if target>e.pos[0] else -3
        terminal.world.calculate(thread=False,times=1),terminal.world.display(),terminal.Wait(False)
    e.Throw(),e.DoEvent('pickup',terminal.world.world)
    e.Flip(e.pos[0] >terminal.world.role.pos[0])
    terminal.world.loading_story('man1',13)
    e.shield=e.Throw(fix_item_pos=True)
def man1_take_gun(e):
    target=terminal.world.search2('gun')
    if target!=None:
        e.eventing=True
        while abs(e.pos[0] - target.pos[0]) > 10:
            if e.pose_finish:
                e.DoPose([1, 2][e.posen % 2])
            e.pos[0] += 3 if target.pos[0] > e.pos[0] else -3
            terminal.world.calculate(thread=False, times=1), terminal.world.display(), terminal.Wait(False)
        e.Throw(),e.DoPose(6)
        while not e.pose_finish:
            terminal.world.calculate(thread=False, times=1), terminal.world.display(), terminal.Wait(False)
        e.Insert('gun',target),wait_talk_end(e,'拿一個來用好了')
        target.rotate = target.role.rotate = 0
        e.eventing=False
def man1_to_5F(e):
    for police in terminal.world.police:
        terminal.world.police[police] = 0
    terminal.world.Add_follow(e)
    terminal.world.plot['man1'] = 16
def man1_walk_to_prison(e):
    def paint_front():
        screen.blit(prison,(1550+terminal.world.world['background'][1][0],y+terminal.world.world['background'][1][1]))
    prison, y = transform.scale(terminal.image['prison'], (420, 780)), -780
    terminal.world.paint_front = paint_front
    target,down=1750,49
    terminal.world.role.DoPose('normal')
    terminal.sound['heavy fall'].play()
    while abs(e.pos[0]-target)>10:
        if e.pose_finish:
            e.DoPose([1,2][e.posen%2])
        e.pos[0]+=12 if target>e.pos[0] else -12
        terminal.world.calculate(thread=False,times=1),terminal.world.display(),terminal.Wait(False)
        if down>0:
            y+=13
            down-=1
    for i in range(down):
        y+=13
        terminal.world.calculate(thread=False, times=1), terminal.world.display(), terminal.Wait(False)
    terminal.world.loading_story('man1',18)
    #terminal.world.Add_follow(e)
def drive_helicopter(e):
    terminal.world.followbox.remove(e)
    e.Flip(False)
    target = 1100
    while abs(e.pos[0] - target) > 10:
        if e.pose_finish:
            e.DoPose([1, 2][e.posen % 2])
        e.pos[0] += 3 if target > e.pos[0] else -3
        terminal.world.calculate(thread=False, times=1), terminal.world.display(), terminal.Wait(False)
    e.visible,e.state=False,1
def boss_walk(e):
    terminal.world.world['warn']=False
    terminal.world.world['object']+=[command_to_character(['boss',0.4,(500,495)])]
    terminal.world.world['trigger']+=[Trigger([1350,0,200,720],'block',terminal.world,key='touch'),
                                      Trigger([1550,45,420,330],'block',terminal.world,key='touch'),
                                      Trigger([1970,0,200,720],'block',terminal.world,key='touch')]
    target,boss= 1350,terminal.world.world['object'][-1]
    boss.Flip(True)
    while abs(boss.pos[0] - target) > 10:
        if boss.pose_finish:
            boss.DoPose([3, 4][boss.posen % 2])
        boss.pos[0] += 4 if target > boss.pos[0] else -4
        terminal.world.calculate(thread=False, times=1), terminal.world.display(), terminal.Wait(False)
    terminal.world.loading_story('man1',20)
def choose_prison_key(e):
    if 'keys' in terminal.world.props:
        removebox=[]
        for i in terminal.world.world['trigger']:
            if i.function!=None and i.function.__name__=='block':
                removebox+=[i]
        for i in removebox:terminal.world.world['trigger'].remove(i)
        terminal.world.nowbg.blit(transform.scale(terminal.image['prison'],(420,780)),(1550,-143))
        terminal.world.paint_front= terminal.world.void
        terminal.world.followbox.remove(e)
        terminal.world.loading_story('man1',22)
        terminal.world.world['warn']=True
        terminal.world.Add_follow(e)
    else:
        def enemy_come():
            terminal.world.alarm,terminal.world.followbox=True,[]
            for police in terminal.world.police:
                terminal.world.police[police] = 5
                terminal.world.police_comespeed=0
        target,boss,terminal.world.max_enemy=400,find_chr('boss'),5
        terminal.world.Talk(terminal.world.role,'沒有萬能鑰匙')
        boss.Flip(False)#,e.Throw()
        while abs(boss.pos[0] - target) > 10:
            if boss.pose_finish:
                boss.DoPose([3, 4][boss.posen % 2])
            boss.pos[0] += 4 if target > boss.pos[0] else -4
            terminal.world.calculate(thread=False, times=1), terminal.world.display(), terminal.Wait(False)
        terminal.world.Bind('警衛部隊', 10,enemy_come)
def Building_collapsed(e,story=True):
    def collapse():
        def helicopter_fall():
            target=None
            for i in terminal.world.world['trigger']:
                if i.function!=None and i.function.__name__=='helicopter':
                    target=i
            if target!=None:
                target.d=terminal.world.role.pos[1]
                while terminal.world.role.pos[1]<3000:
                    target.rect[1]+=terminal.world.role.pos[1]-target.d
                    target.d = terminal.world.role.pos[1]
                    sleep(0.05)
        terminal.world.shock[0] = False
        terminal.sound['collapse'].play()
        if terminal.world.scenes_name[:2]!='c_':
            #terminal.world.paint_front,terminal.world.paint_back=terminal.world.void,terminal.world.void
            terminal.world.role.control,terminal.world.world['floor'],terminal.world.role.eventing,terminal.world.role.state=False,10000,False,[0,0,2,3,4][terminal.world.role.state]
            if terminal.world.scenes_name=='top floor':
                terminal.world.nowbg,blank= transform.scale(image.load(f'{work_dir}scenes/88.jpg'),terminal.world.world['background'][2]),transform.scale(terminal.blank,(1280,720))
                blank.blit(terminal.image['top floor'],(terminal.world.world['background'][1][0],1500+terminal.world.world['background'][1][1])),blank.blit(terminal.image['elevator'],(320+terminal.world.world['background'][1][0],1625+terminal.world.world['background'][1][1]))
                box = splitimage(blank, 3)
                Thread(target=helicopter_fall).start()
            else:
                try:cbg=terminal.world.nowbg.subsurface([-terminal.world.world['background'][1][0],-terminal.world.world['background'][1][1],min(1280,terminal.world.nowbg.get_rect()[2]+terminal.world.world['background'][1][0]),min(720,terminal.world.nowbg.get_rect()[3]+terminal.world.world['background'][1][1])])
                except:cbg=screen.copy()
                terminal.world.nowbg,box=Surface(terminal.world.world['background'][2]),splitimage(cbg,4)
            for i in box:
                i.setstart()
                i.speed = [-1 + int(3 * random()), -2, -0.5 + random()]
                i.p[0] -= terminal.world.world['background'][1][0] + 200
                i.p[1] -= terminal.world.world['background'][1][1] + 130
            if terminal.world.plot['man1']<29 or terminal.world.role.state==0:terminal.world.role.live=0
            terminal.world.fragments += box
            def no_elevator():
                t=time()+3
                while t>time():
                    try:
                        if terminal.tem[0] > 1:terminal.tem[0]=0
                        sleep(0.1)
                    except:break
            Thread(target=no_elevator).start()
            k=0
            while k<len(terminal.world.world['object']):
                if terminal.world.world['object'][k].hide or not terminal.world.world['object'][k].visible:del terminal.world.world['object'][k]
                else:
                    terminal.world.world['object'][k].rigid,terminal.world.world['object'][k].fix,terminal.world.world['object'][k].state=False,False,0
                    k+=1
        else:
            terminal.world.play_bgm('fantasy')
            terminal.world.shock[0]=False
    if e in terminal.world.followbox:terminal.world.followbox.remove(e)
    e.Throw()
    if story:terminal.world.loading_story('man1',26)
    else:terminal.world.Add_follow(e)
    terminal.world.Bind('大樓崩毀',100,collapse)
    for chr in terminal.world.map['1F']['object']:
        if chr.name=='scientist' and chr.live:
            chr.pos[0]=4800
    for i in range(5):
        world=terminal.world.map[f'{i + 1}F']
        x,y,w,h=world['background'][2][0]-350,0,150,world['background'][2][1]-100
        terminal.world.allbackground[f'{i+1}F'].blit(transform.scale(terminal.image['prison2'],(w,h)),(x,y))
        world['trigger']+=[Trigger([x,y,w,h],'block',terminal.world,key='touch',picturebox=['prison2'])]
    terminal.world.SetShock(60,5)
def collapse_block(self):
    if len(self.world.talkbox)==0:
        self.world.Talk(self.world.role,'被土石擋住了')
def nuclear_boom(self):
    def nu_boom():
        def paint_front():
            if self.cold<255:white.set_alpha(self.cold)
            elif self.cold>755:
                self.world.paint_front=self.world.void
                self.world.busy,self.world.alarm=False,False
                self.world.play_bgm('fantasy'),mixer.music.set_volume(bgm_vol)
                self.world.loading_story('man1',59.5)
                man1, girl,self.world.role.control= self.world.search2('man1'), self.world.search2('girl'),True
                if girl != None: self.world.Add_follow(girl)
                if man1 != None:self.world.Add_follow(man1)
                for trigger in self.world.world['trigger']:
                    if trigger.function!=None and trigger.function.__name__=='teleport' and trigger.functionkey[0]=='c_battle':
                        trigger.functionkey=['c_boomhole',(100,2165)]
                self.world.selecting=False
            elif self.cold>500:
                white.set_alpha(755-self.cold)
                mixer.music.set_volume(bgm_vol * (755-self.cold)/255)
            screen.blit(white, (0, 0))
            self.cold += 1
        white,self.world.busy,bgm_vol=Surface((1280,720)),True,terminal.bgm_vol
        white.fill((255,255,255))
        if self.world.scenes_name in ('c_battle', 'c_nuclear'):
            self.world.role.Throw(),explosion(None,[0,0,self.world.world['background'][2][0],self.world.world['background'][2][1]], target='All', blood=False, power=6,effect=None, fragments=6, sound='boom')
            for i in self.world.fragments:
                i.speed[0]-=10
                i.speed[1]/=2
        self.world.paint_front=paint_front
        terminal.sound['big_boom2'].play()
        self.world.role.control=False
    if self.variable==0:
        girl, role=self.world.search2('girl'),self.world.role
        if girl != None:
            boomlist = (role.Throw(fix_item_pos=True), girl.Throw(fix_item_pos=True))
            for i in range(len(boomlist)):
                if type(boomlist[i]) == Character and boomlist[i].name == 'boom':
                    self.variable,self.cold = 1, i
    elif self.variable==1:
        man1, girl, self.variable = self.world.search2('man1'), self.world.search2('girl'), None
        for i in range(20):self.world.display(),wait_tap()
        terminal.sound['timer'].play()
        for i in range(20): self.world.display(), wait_tap()
        sleep(1),self.world.play_bgm('nervous')
        self.variable, self.world.alarm = 2, True
        if girl != None: wait_talk_end(girl, '什麼聲音!')
        if man1!=None:wait_talk_end(man1,'完蛋!這是定時炸彈!')
    elif self.variable==2 and len(self.world.talkbox)==0:
        if self in self.world.world['trigger']: self.world.world['trigger'].remove(self)
        man1, girl, self.variable,self.key= self.world.search2('man1'), self.world.search2('girl'),3,'none'
        if girl != None:
            girl.nowdo+=['escape_boom']
            self.world.Talk(girl, '天啊')
        if man1 != None:
            man1.nowdo+=['escape_boom']
            self.world.Talk(man1,'不知道威力多大，趕快丟掉，快逃!')
        if self.cold==1 and girl!=None:girl.Throw()
        terminal.world.Bind('定時炸彈',22,nu_boom)
def Building_collapsed_savefile(e):
    if e not in terminal.world.followbox:terminal.world.Add_follow(e)
    terminal.savefile()
    terminal.world.plot['man1']=26
def boss_escape(e):
    terminal.sound['scream_m1'].play()
def master_key_lock(self):
    if self.posen==0:
        t=systeminput('請輸入密碼')
        if t!='' and t!=False:
            if t==Game_setting['master_key_password']:
                self.posen=1
                terminal.world.Talk(terminal.world.role,'解鎖了!'),terminal.sound['hint'].play()
                terminal.world.world['trigger']+=[Trigger([200,205,287,333],['3F_keyroom',(1160,535)],terminal.world,'space')]
            else:terminal.world.Talk(terminal.world.role,'密碼不正確')
def missile_protection(self):
    def missile_start():
        cd,role=time()+1,self.world.role
        while role.live==1 and self.world.computer_setting['power_room']['anti-missile']:
            if self.world.scenes_name=='1F_outside':
                if time()>cd and role.pos[0]>800:
                    if role.pos[0]>2400:
                        self.world.bullet += [['bullet6', [2500+int(190*random()),-200,250,86],[12,12, 0],[False,-45,False,0]]] # 名稱,[x,y,w,h],[spx,spy,spr],[flip,rotate,gravity,0:我方,1:敵方]
                    if len(self.world.bullet)<4:
                        self.world.bullet += [['bullet6', [role.pos[0]-1000+int(600*random()),-200, 250,86], [12,12, 0],[False,-45, False,0]]]
                    cd=time()+round(0.8+random()*0.4,2)
            sleep(0.2)
    if self.Touch(self.world.role):
        self.world.world['trigger'].remove(self)
        Thread(target=missile_start).start()
def deity_teleportation(scenery,pos,ex=[]):
    bg=screen.copy()
    w,h=bg.get_rect()[2:4]
    n,box,s=30,[],10
    for chr in ex:
        chr.deity_pos=(chr.pos[0]-terminal.world.role.pos[0],chr.pos[1]-terminal.world.role.pos[1])
        terminal.world.world['object'].remove(chr)
        terminal.world.map[scenery]['object']+=[chr]
    fix = (terminal.world.role.pos[0] + terminal.world.world['background'][1][0],terminal.world.role.pos[1] + terminal.world.world['background'][1][1])
    wn,hn,sp=int(w/n) if w/n==int(w/n) else int(w/n+1),int(h/n) if h/n==int(h/n) else int(h/n+1),(int((terminal.world.world['background'][1][0]+pos[0])/n),int((terminal.world.world['background'][1][1]+pos[1])/n))
    teleport([scenery, fix])
    for chr in ex:
        chr.pos=[terminal.world.role.pos[0]+chr.deity_pos[0],terminal.world.role.pos[1]+chr.deity_pos[1]]
    terminal.world.world['background'][1]=[fix[0]-terminal.world.role.pos[0],fix[1]-terminal.world.role.pos[1]]
    terminal.world.display(False)
    bg2 = screen.copy()
    for j in range(hn):
        box+=[[]]
        for i in range(wn):
            box[-1]+=[[bg2.subsurface([n*i,n*j,min(n,w-n*i),min(n,h-n*j)]).convert_alpha(),0,True]]
    has_finish,all,k,radius=0,wn*hn,0,1
    terminal.sound['teleportation'].play()
    while has_finish<all:
        screen.blit(bg,(0,0))
        for times in range(2):
            for i in range(radius-times):
                for j in range(radius-times):
                    x,y=sp[0]-i+j,sp[1]-radius+1+j+i+times
                    if -1<y<len(box) and -1<x<len(box[y]) and box[y][x][2]:
                        box[y][x][0].set_alpha(box[y][x][1])
                        box[y][x][1]+=s
                        if box[y][x][1]>255:
                            box[y][x][0].set_alpha(255)
                            has_finish+=1
                            box[y][x][2]=False
                            bg.blit(box[y][x][0],(n*x,n*y))
                        screen.blit(box[y][x][0],(n*x,n*y))
        display.update()
        #sleep(0.1)
        radius+=1
        for event2 in event.get():
            if event2.type == QUIT:
                return
        k=0
def teaching(chr,world):
    def in_radius(pos1,pos2,radius):
        return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5<radius
    def drawtext(textlist,zoom_rate):#[(t,b,c,d)]
        for i in textlist:
            world.allbackground[world.scenes_name].blit(font.Font(f'{work_dir}data/msjh.ttc',i[1]).render(i[0],True,i[2]),i[3])
            world.nowbg.blit(font.Font(f'{work_dir}data/msjh.ttc',int(i[1]*zoom_rate)).render(i[0],True,i[2]),(int(i[3][0]*zoom_rate),int(i[3][1]*zoom_rate)))
    def moveto(pos,radius,speed=3):
        if abs(pos[0]-chr.pos[0])>radius:
            if chr.pose_finish:
                chr.Flip(chr.pos[0]<pos[0])
                chr.DoPose(f'walk{chr.posen%2+1}')
            chr.pos[0]+=speed*(1 if chr.flip else -1)*terminal.zoom
            return True
        return False
    def changeto(sceneryname,pos,flip,spl):
        world.world['object'].remove(chr)
        world.map[sceneryname]['object'] += [chr]
        world.plot['Eln'], world.busy, chr.pos =spl, False, [pos[0],pos[1]]
        chr.Flip(flip),chr.DoPose('normal')
    def face_to_face(both=True):
        chr.Flip(role.pos[0] > chr.pos[0]),chr.DoPose('normal')
        if both:role.Flip(role.pos[0]>chr.pos[0]),role.DoPose('normal')
    def tostory(n):face_to_face(), world.loading_story('Eln', n)
    pl,role=world.plot['Eln'],terminal.world.role
    if chr==0:
        terminal.teaching_mode,terminal.door_lock= True,False
        world.plot['Eln']= 'start'
        for i in world.map['nb']['object']:
            if i.name=='Eln':world.map['nb']['object'].remove(i)
        deity_teleportation('nb',role.pos)
        world.world['object'] += [command_to_character(['Eln', 0.2*terminal.zoom, (1200*terminal.zoom, 550*terminal.zoom)])]
    elif pl=='start':
        world.busy=True
        if not moveto(role.pos,300):
            world.busy,terminal.door_lock=False,True
            tostory(0)                                                    #進入教學
            if world.plot['Eln']==101:
                pl,terminal.door_lock=101,False
            else:
                drawtext([('↑↓←→移動',50,(0,0,0),(300,200))],1)
    elif pl==3.5:
        world.tem=[time()+1,5,(role.pos[0],role.pos[1])]                     #設定移動
        world.plot['Eln'] = 3.7
    elif pl==3.7:
        face_to_face(False)
        if time()>world.tem[0] and ((role.pos[0]!=world.tem[2][0] or role.pos[1]!=world.tem[2][1]) or world.tem[1]<1) and role.tapfloor:
            if world.tem[1]<1:
                world.busy=True
                role.control=False
                role.DoPose('normal')
                world.plot['Eln'] =3.8
            else:
                world.tem[1] -= 1
                world.tem[0] = time() + 1
                if not chr.pose_finish: chr.pose_finish = True
    elif pl==3.8:
        if not moveto(role.pos, 300):
            world.busy, role.control = False, True
            drawtext([('[空白鍵] 進入門', 50, (0, 0, 0), (800, 200))], 1)
            tostory(4)
    elif pl==4.5:                                              #進到第二個房間
        world.busy=True
        if not moveto((1310,470),50):
            changeto('nb2', (777, 1200),True,4.7)
            terminal.door_lock=False
    elif pl ==4.7:
        tostory(5)
        drawtext([('[z] 拿道具', 33, (0, 0, 0), (300,980))],1.6)
        world.world['background'][2][0],terminal.tem_wall,terminal.door_lock=-world.world['background'][1][0]+1280,world.world['background'][2][0],True
    elif pl==5.5:                                                     #檢測梯子被拿取
        face_to_face(False)
        if not chr.pose_finish:chr.pose_finish=True
        if role.pose_finish:
            for item in world.world['object']:
                if item.name=='ladder' and item.hide:
                    tostory(6)
                    drawtext([('[a] 切換道具欄', 33, (0, 0, 0), (300, 1070)),('[x] 丟棄道具', 33, (0, 0, 0), (300, 1120))], 1.6)
                    chr.pose_finish,world.tem=True,time()+8
    elif pl==6.5:
        face_to_face(False)
        if not chr.pose_finish: chr.pose_finish = True
        if time()>world.tem and len(world.talkbox)==0:
            world.Talk(chr,'試著把道具裝備在第三個道具欄看看~~')
            world.tem=time()+8
        if world.itemlist[2]!=None and role.pose_finish:
            world.world['background'][2][0],terminal.door_lock= terminal.tem_wall,False
            tostory(7)
            drawtext([('、拖物', 33, (0, 0, 0), (446,980)),('、使用道具', 33, (0, 0, 0), (350, 1020))],1)
    elif pl==7.5:
        world.busy = moveto((2480,923), 50)
        if not world.busy:
            if in_radius(role.pos,chr.pos,300):
                role.pos[0]=chr.pos[0]+250*(1 if role.pos[0]>chr.pos[0] else -1)
                tostory(8)                                                                       #指派碎門任務
            elif len(world.talkbox)==0 and random()<0.1:world.Talk(chr,'快過來!'),face_to_face(False)
    elif pl == 8.5:
        key=True
        face_to_face(False)
        if chr.touch(role):
            if world.select=='任務說明':
                world.Talk(chr,'想辦法去找尋、利用道具把門上的木頭釘板擊碎吧~')
                world.select,world.selecting=None,False
            elif world.select=='遊戲方法':
                world.select, world.selecting = None, False
                role.pos[0]=chr.pos[0]-250
                face_to_face(),world.loading_story('Eln',90)
                world.plot['Eln'] = 8.5
            elif not world.selecting and len(world.talkbox)==0:
                world.Select(['任務說明','遊戲方法'])
        elif world.selecting:world.selecting=False
        elif not chr.pose_finish:chr.pose_finish=True
        for item in world.world['object']:
            if item.name == 'wblock':key=False
        if key and len(world.fragments)==0:tostory(9)
    elif pl==9.5:
        world.busy = True
        if not moveto((2680, 923), 50):
            changeto('nb4', (400,520),True,9.7)
    elif pl==9.7:
        tostory(10)
        world.busy = False
    elif pl==10.5:
        if world.alarm:
            chr.DoPose('shock1')
            world.Talk(chr,'哇!不是教你先破壞監視器了嗎?!')
            world.plot['Eln']=10.6
        else:
            face_to_face(False)
            if chr.touch(role):
                if world.select=='任務說明':
                    world.Talk(chr,'試著在不被警察追的情況下把鑽石拿給我吧~')
                    world.select,world.selecting=None,False
                elif world.select=='遊戲方法':
                    world.select, world.selecting = None, False
                    role.pos[0]=chr.pos[0]-250
                    face_to_face(),world.loading_story('Eln',90)
                    world.plot['Eln'] = 10.5
                elif not world.selecting and len(world.talkbox)==0:
                    world.Select(['任務說明','遊戲方法'])
            elif world.selecting:world.selecting=False
            elif not chr.pose_finish:chr.pose_finish=True
            if in_radius(role.pos,chr.pos,250):
                for item in world.world['object']:
                    if item.name == 'gem' and type(item.hide)==bool and item.hide:
                        tostory(10.7)
                        deity_teleportation('nb_ex', chr.pos, [chr])
                        role.control=False
    elif pl==10.6 and len(world.talkbox)==0:
        if not moveto((-200,0),50,speed=5):
            world.world['object'].remove(chr)
    elif pl==10.8:
        world.busy=True
        role.Flip(role.pos[0]>chr.pos[0]),role.DoPose('normal')
        if not moveto((role.pos[0]+500,520),50,speed=2):
            world.busy=False
            chr.pos[1]+=30
            role.pos[1]+=30
            role.control = True
            tostory(11)
    if pl==101:
        for i in range(6):
            role.Throw()
            draw.rect(world.itemlist_surf, (0, 0, 0), [50 *i, 0, 50, 50])
            draw.rect(world.itemlist_surf, (140, 140,140), [50 * i, 0, 50, 50], 2)
        world.itemlist,terminal.teaching_mode = [None, None, None, None, None, None],False
        deity_teleportation('Initial room',chr.pos),world.play_bgm('interstellar')
        world.plot['Eln'] =102
def display_end(self):
    if self.world.role.live!=1:return
    if self in self.world.world['trigger']: self.world.world['trigger'].remove(self)
    if self.variable=='end1':
        if self.world.role.visible:return
        for i in range(200):
            self.world.role.pos[0]+=4
            self.world.display(),wait_tap()
    if self.variable=='end2':
        for i in range(200):
            if self.world.role.pose_finish:
                self.world.role.DoPose(f'walk{self.world.role.posen%2+1}')
            self.world.role.pos[0]+=3
            self.world.display(),wait_tap()
    terminal.world.alarm,terminal.world.paint_front= False,terminal.world.void
    end_display(self.variable),screen.fill((0,0,0))
    terminal.world.clearance,terminal.unlock_end[self.variable]=int(self.variable[-1]),True
    terminal.save_setting()
def end_display(end):
    black, bg, endlist,bgm_vol=Surface((1280,720)),screen.copy(),Game_setting['ending'][end],terminal.bgm_vol
    for i in range(51):
        sleep(0.03),black.set_alpha(i*5),screen.blit(bg,(0,0)),screen.blit(black,(0,0)),display.update(),wait_tap(),mixer.music.set_volume(bgm_vol*(51-i)/51)
    terminal.world.play_bgm('end')
    bg=transform.scale(image.load(f'{work_dir}scenes/74.jpg').convert(), (1280, 720))
    for i in range(135):
        sleep(0.03),black.set_alpha(255-i),screen.blit(bg, (0, 0)), screen.blit(black, (0, 0)),display.update(),wait_tap(),mixer.music.set_volume(bgm_vol*i/135)
    if terminal.unlock_end[end]:text_render(screen,'skip>>',30,(255,255,255),(1160,670))
    bg2=screen.copy()
    for i in endlist[1:]:
        text_surf=[]
        for j in range(int(len(i)/16)+1):
            text_surf+=[font_dict[70].render(i[j*16:j*16+16], True,(255,255,255))]
        for m in range(2):
            for j in range(255):
                screen.blit(bg2,(0,0))
                for line in range(len(text_surf)):
                    text_surf[line].set_alpha(j if m==0 else (255-j))
                    screen.blit(text_surf[line],(640-int(text_surf[line].get_rect()[2]/2),360-int(80*(len(text_surf)/2-line))))
                wait_tap(),display.update()
            if m==0:
                if terminal.unlock_end[end] and terminal.Wait(skp=(1160,670,120,30)):return
                elif terminal.Wait():return
    for i in range(120):
        sleep(0.03),black.set_alpha(135+i),screen.blit(bg, (0, 0)), screen.blit(black, (0, 0)),display.update(),wait_tap()
    endtext=font_dict2[120].render(endlist[0].upper().replace(' ','   '),True,(255,255,255))
    for m in range(2):
        for j in range(255):
            screen.fill((0,0,0)),endtext.set_alpha(j if m == 0 else (255 - j))
            screen.blit(endtext,(640-int(endtext.get_rect()[2]/2),240))
            wait_tap(), display.update()
        if m == 0:
            if terminal.Wait():return
def wait_talk_end(who,R):
    if type(R)==str:R=[[0,R]]
    for pose,text in R:
        who.DoPose(pose),terminal.world.Talk(who,text)
        while len(terminal.world.talkbox) > 0:
            for event2 in event.get():
                if event2.type == QUIT:
                    terminal.end_game = True
                if event2.type in [MOUSEBUTTONDOWN, KEYDOWN]:
                    for textbox in terminal.world.talkbox:
                        while textbox[0][1] < len(textbox[0][2]):
                            textbox[0][0].blit(textbox[0][2][textbox[0][1]][0], textbox[0][2][textbox[0][1]][1])
                            textbox[0][1] += 1
            terminal.world.display()
        terminal.Wait()
def wait_select(box):
    terminal.world.Select(box), terminal.world.display()
    while terminal.world.selecting or terminal.world.select == None:
        for event2 in event.get():
            if event2.type == QUIT: return
            if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                x, y = mouse.get_pos()
                for i in terminal.world.selectbox:
                    if 0 < x - i[1][0] < 373 and 0 < y - i[1][1] < 57: terminal.world.select, terminal.world.selecting = \
                    i[2], False
        sleep(0.1),terminal.world.display()
def talk_information(e):
    def item_talk(R):
        for i in R:
            e.DoPose(i[0]),wait_talk_end(e,i[1])
    wait_select(['目前線索','手中道具線索','取消'])
    if terminal.world.select=='目前線索':
        wait_talk_end(terminal.world.role,'目前有什麼線索?')
        while True:
            if len(terminal.world.information)==0:
                wait_talk_end(e,[[0,'嗯......'],[8,'目前我想不到'],[3,'先到處找找看好了']])
            else:
                for info in terminal.world.information:
                    wait_talk_end(e,Game_setting['info'][info])
            wait_select(['再說一次','了解!','妳有想法嗎?']),wait_talk_end(terminal.world.role,terminal.world.select)
            if terminal.world.select=='了解!':return
            elif terminal.world.select=='妳有想法嗎?':
                if len(terminal.world.information) == 0:wait_talk_end(e,'先到處找找看好了')
                else:
                    wait_talk_end(e,[[8,'嗯...'],[0,'哪部分呢?']])
                    talk_think(e)
                return
    elif terminal.world.select=='手中道具線索':
        def item_talk_R(R):
            box, n = [], 3
            for i in R:
                if type(i) == int:
                    n = i
                elif type(i) == str:
                    box += [[n, i]]
            item_talk(box)
        wait_talk_end(terminal.world.role, '妳對這個有什麼看法?')
        item=terminal.world.role.Throw(fix_item_pos=True)
        if item==None:item_talk([[0,'......'],[3,'你手上是空的']])
        elif item.name=='note':
            R=[0,'......',3]
            if item.value[:4]=='檔板很大':R+=['應該是說這個檔板易壞吧，如果有什麼衝擊就會壞掉']
            elif item.value[:4] == 'hint': R += ['哦!',3,'這是....這間公司的秘密!',8,'理事長的房間...萬能鑰匙...','......',3,'不過我們還是要能搭電梯上去才行...']
            else: R += ['我們的研究資訊']
            item_talk_R(R)
        elif item.name in Item_hint:
            item_talk_R(Item_hint[item.name])
        else:wait_talk_end(e,'我不知道那是什麼......')
def talk_think(e):
    box,ed=[],{}
    for i in terminal.world.information:
        box+=['關於'+Game_setting['hint'][i][0]]
        ed['關於'+Game_setting['hint'][i][0]]=i
    box += ['沒事了']
    while True:
        wait_select(box)
        if terminal.world.select=='沒事了':
            wait_talk_end(terminal.world.role,'沒事了')
            return
        wait_talk_end(terminal.world.role,terminal.world.select)
        wait_talk_end(e,Game_setting['hint'][ed[terminal.world.select]][1])
def stay(e):
    e.DoPose(20)
def girl_event(self,chr):
    def moveto(pos,radius,speed=3):
        if self.selecting and self.selectbox[0][2] == '?': self.selecting = False
        if abs(pos[0]-chr.pos[0])>radius:
            if chr.pose_finish:
                chr.Flip(chr.pos[0]<pos[0])
                chr.DoPose(f'walk{chr.posen%2+1}')
            chr.pos[0]+=speed*(1 if chr.flip else -1)*terminal.zoom
            chr.eventing=True
            return True
        chr.eventing = False
        return False
    def near(x,radius):
        return abs(chr.pos[0]-x)<radius
    def face_to_face(both=True):
        chr.Flip(self.role.pos[0] > chr.pos[0]),chr.DoPose(0)
        if both:self.role.Flip(self.role.pos[0]>chr.pos[0]),self.role.DoPose('normal')
    def easy_talk(R,talk=0,remove=True,info=None,mode='room_event'):
        if type(R)==str:R=[[0,R]]
        chr.DoPose(R[chr.freeze][0])
        self.Talk(chr,R[chr.freeze][1])
        chr.freeze+=1
        if chr.freeze>=len(R):
            if remove:
                if mode=='room_event':self.people_talk['girl'].remove(self.scenes_name)
                else:self.item_talk['girl'].remove(mode)
            if talk==True:chr.freeze='talk'
            else:chr.freeze=talk
            if info!=None:self.information+=[info]
    def trigger_here(name):
        for i in self.world['trigger']:
            if i.function!=None and name in i.function.__name__:return True
        return False
    def monitor_here():return trigger_here('monitor') and self.computer_setting['power_room']['anti-system']
    def coffer_lock():
        for i in self.world['trigger']:
            if i.function!=None and i.function.__name__=='unlock_coffer' and i.posen==0:
                return True
        return False
    def main_distance(who,other,distance=90):
        if abs(self.role.pos[0] - who.pos[0]) <distance:
            who.pos[0] = max(min(other.pos[0] + distance * (1 if other.pos[0] < who.pos[0] else -1),self.world['background'][2][0] - 100),50)
            other.pos[0] = who.pos[0] - distance * (1 if other.pos[0] < who.pos[0] else -1)
    def select_inspect(text='?'):
        if not chr.eventing:
            if self.select == text:
                self.select, self.selecting = None, False
                main_distance(chr,self.role,90)
                face_to_face()
                chr.tem_cold,chr.jump_warn[4]= 1,'?'
                return True
            elif not self.selecting and len(self.talkbox) == 0 and chr.tem_cold < 1 and not self.instory:self.Select([text])
        return False
    def take_event():
        chr.Insert('right_hand', chr.jump_warn[4])
        chr.jump_warn[4].hide=True
        if chr.jump_warn[4].name == 'gun':
            chr.jump_warn[4].rotate=chr.jump_warn[4].role.rotate=-100
            chr.jump_warn[4].Flip(not chr.flip)
        elif chr.jump_warn[4].name == 'sword':
            chr.jump_warn[4].rotate=chr.jump_warn[4].role.rotate=-40
            chr.jump_warn[4].Flip(chr.flip)
        elif chr.jump_warn[4].name == 'note':
            self.Talk(chr,f'{chr.jump_warn[4].value}......上面是這樣寫的')
        chr.freeze, chr.jump_warn[4], chr.eventing = 0, 0, False
    try:e=chr.jump_warn[0]
    except:chr.jump_warn=[0,0,0,0,0]
    if len(chr.nowdo)>0:
        if 'escape_boom' in chr.nowdo:
            if self.scenes_name == 'c_staircase':
                self.followbox.remove(chr), chr.nowdo.remove('escape_boom'), chr.DoPose(0, 1000), chr.Flip(True), self.Talk(chr, '快躲起來')
                man1 = self.search2('man1')
                if man1 != None: self.Talk(man1, '快點躲到牆後!')
                chr.pos = [400, 1470]
            elif not moveto((-100,0),100,7):
                if self.scenes_name=='c_battle'==chr.room:
                    self.world['object'].remove(chr)
                    chr.chroom, chr.room = 60000, 'c_staircase'
                    self.map['c_staircase']['object']+=[chr]
                elif self.scenes_name=='c_nuclear'==chr.room:
                    self.world['object'].remove(chr)
                    chr.chroom,chr.room=60000,'c_battle'
                    self.map['c_battle']['object']+=[chr]
                    chr.pos=[9990,570]
            elif self.scenes_name=='c_nuclear' and chr.room=='c_battle':chr.pos[0]-=8
        return
    pl=self.plot['girl']
    if pl==0 and chr.touch(self.role) and self.role.tapfloor and not self.alarm and self.scenes_name=='Ward':
        self.loading_story('girl',0.5)
    elif pl<1 and chr.state==0 and chr.tapfloor and len(self.fragments)==0 and self.scenes_name=='Ward':
        if self.scenes_name=='Ward' and chr.pos[1]<530:chr.pos[1]+=3
        else:
            chr.rotate = chr.role.rotate=0
            chr.jump_warn=[0,0,0,0,0]
            main_distance(chr, self.role,100),self.loading_story('girl',1)
    elif pl==3.5:
        if self.select=='?':
            self.select,self.selecting=None,None
            main_distance(chr, self.role, 90)
            self.loading_story('girl',3.6)
        elif abs(chr.pos[0] - self.role.pos[0]) < 100:
            if not self.selecting:self.Select(['?'])
        elif self.selecting and len(self.selectbox)>0 and self.selectbox[0][2] == '?':
            self.selecting = False
    elif pl==6.6:self.loading_story('girl',7)
    elif pl == 6.7:self.loading_story('girl',7.5)
    if chr.state == 1: return
    if 'elevator_card' in self.props and self.scenes_name == 'B1' and self.alarm:
        trigger=self.search_trigger('car_inspect2')
        if trigger!=None:
            self.alarm= False
            if abs(self.role.pos[0] - chr.pos[0]) < 90:
                chr.pos[0] = min(self.role.pos[0] + 90 * (1 if self.role.pos[0] < chr.pos[0] else -1),self.world['background'][2][0] - 100)
                self.role.pos[0] = chr.pos[0] - 90 * (1 if self.role.pos[0] < chr.pos[0] else -1)
            terminal.world.loading_story('girl', 30)
            self.alarm,self.selecting= True,False
            if trigger in self.world['trigger']: trigger.key,trigger.function= 'none',None
        elif self.role.pos[0] < 1850:
            key = False
            for obj in self.world['object']:
                if obj.name in Game_setting['police']:
                    key = True
            if not key:
                if 'elevator_card' in self.item_talk['girl']:
                    self.alarm = False
                    self.item_talk['girl'].remove('elevator_card'),face_to_face(),self.loading_story('girl', 31)
                    self.alarm = True
                elif chr not in self.followbox and len(self.talkbox) == 0 and random()<0.005:self.Talk(chr, '趕快坐電梯逃走!')
    try:e = chr.shotbox
    except:chr.shotbox = [None, 0, (0, 0, 0)]
    if self.scenes_name in ('c_battle','treasure','treasure2'):
        weapon=chr.Throw(fix_item_pos=True)
        if weapon!=None:
            t = time()
            if weapon.name=='sword':
                if chr.shotbox[0]!=None:
                    if not moveto(chr.shotbox[0].pos,100,3):
                        if chr.shotbox[0].live!=1 or chr.shotbox[0] not in self.world['object']:
                            chr.shotbox[0],chr.eventing=None,False
                        elif abs(chr.pos[1]-chr.shotbox[0].pos[1])<150:
                            chr.eventing = True
                            if chr.posen not in (14, 15):
                                chr.DoPose(14), chr.Flip(chr.pos[0] <chr.shotbox[0].pos[0])
                                weapon.rotate = weapon.role.rotate = -50
                            elif chr.posen == 14 and chr.role.posek > 42:chr.DoPose(15)
                            elif chr.posen == 15:
                                if chr.role.posek < 45:
                                    weapon.rotate = weapon.role.rotate = -50 + int(5 * chr.role.posek / 3)
                                else:
                                    weapon.rotate = weapon.role.rotate = -40
                                    chr.DoPose(0)
                                    chr.Flip(chr.pos[0] < chr.shotbox[0].pos[0])
                                    sword_chop(chr, not chr.flip, People)
                            if chr.role.posek < 45: chr.role.posek += 1
                        elif chr.tapfloor:chr.speed[1]=-8
                if chr.shotbox[0] == None:
                    for obj in self.world['object']:
                        if obj.name=='aircraft' and abs(obj.pos[0]-chr.pos[0])<800 and obj.live==1:
                            chr.shotbox[0],chr.eventing=find_closed(chr,obj.name,y=False),True
                            break
            elif weapon.name in ('gun','flame_gun','super_gun','socket'):          #man1.shotbox=[target,time,(x,y,z)]
                if chr.shotbox[0]!=None:
                    if t>chr.shotbox[1]:
                        if chr.shotbox[0].live!=1:
                            chr.shotbox[0],chr.eventing=None,False
                            weapon.rotate = weapon.role.rotate = -100
                        elif chr.pose_finish:
                            posen,chr.shotbox[2]=get_attack_angle(chr,chr.shotbox[0],{60:16,30:17,0:18,-20:19})
                            chr.eventing=True
                            if posen==chr.posen:
                                weapon.rotate = weapon.role.rotate=[150,80,30,10][posen-16]
                                gun_attack(weapon,chr.shotbox[2])
                                chr.shotbox[1]=t+bullet_dictory[weapon.name]['cold']/40
                            else:chr.DoPose(posen,50),chr.Flip(chr.pos[0]<chr.shotbox[0].pos[0])
                if chr.shotbox[0] == None:
                    for obj in self.world['object']:
                        if obj.name=='aircraft' and abs(obj.pos[0]-chr.pos[0])<1000 and obj.live==1:
                            chr.shotbox[0],chr.eventing=find_closed(chr,obj.name),True
                            break
    elif chr.shotbox[0]!=None:chr.eventing,chr.shotbox[0]=False,None
    if chr in self.followbox and len(self.talkbox)==0 and self.role.control and not self.alarm:
        if self.role.speed[1]!=0:
            chr.jump_warn[0]+=1.6
        if chr.jump_warn[0]>0:chr.jump_warn[0]-=1
        if chr.jump_warn[0]>200:
            if self.scenes_name!='staircase': self.Talk(chr,['這樣亂跳是很消耗體力的喔','你幹嘛一直跳'][int(2*random())])
            chr.jump_warn[0]=0
        elif chr.jump_warn[4]!=0 and (type(chr.jump_warn[4])==str or not moveto(chr.jump_warn[4].pos,50)):
            if type(chr.jump_warn[4])==str:
                if chr.jump_warn[4]=='?':
                    chr.jump_warn[4] =0
                    self.loading_story('girl', 9)
                elif chr.jump_warn[4]=='pull' and chr.do_event[0]>60:
                    for i in terminal.world.world['back']:
                        if i[1][0]==1450:i[1][1]=int(305*terminal.zoom)-chr.pos[1]
                    if abs(chr.pos[0]-self.role.pos[0])<1000:
                        if not chr.eventing:chr.DoEvent('use',self.world)
                        if abs(chr.pos[0]-self.role.pos[0])<100:
                            if select_inspect('取消拉繩'):chr.freeze,chr.jump_warn[4],chr.eventing,chr.do_event=0,0,False,None
                            elif chr.tem_cold>0:chr.tem_cold-=1
                        elif self.selecting:self.selecting=False
                    elif chr.tapfloor:chr.freeze,chr.jump_warn[4],chr.eventing,chr.do_event=0,0,False,None
            elif chr.jump_warn[4].hide:
                self.Talk(chr,'你把它拿走了')
                chr.jump_warn[4],chr.eventing,chr.freeze=0,False,0
            else:
                if chr.jump_warn[4] not in self.world['object']:chr.jump_warn[4]=0
                elif chr.jump_warn[4].name == 'rope':
                    chr.DoEvent('use',self.world)
                    if chr.eventing:chr.jump_warn[4]='pull'
                    else:chr.pos[0]+=30
                else:
                    if chr.jump_warn[4].pos[1]<chr.pos[1]-30 and chr.tapfloor and chr.pose_finish:
                        chr.speed[1]=-5
                        chr.DoPose(14)
                    elif abs(chr.jump_warn[4].pos[1]-chr.pos[1])<30:
                        if chr.posen!=14:
                            chr.DoPose(14)
                        elif chr.posen==14:take_event()
                    elif abs(chr.jump_warn[4].pos[1]-chr.pos[1])<130 and chr.jump_warn[4].pos[1]>chr.pos[1]:
                        if chr.posen != 9:
                            chr.DoPose(9)
                        elif chr.posen == 9 and chr.role.posek>47:take_event(),chr.DoPose(0)
                    elif chr.jump_warn[4].pos[1]>chr.pos[1]+60:chr.pos[1]+=3
        elif self.role.speed[1]>9*terminal.zoom:self.Talk(chr,'小心一點!')
        #---------------------------------------------------------------
        elif self.scenes_name in self.people_talk['girl']:
            if self.scenes_name=='Initial room' and near(300,600) and not moveto((300,0),50):
                if trigger_here('shattered'):easy_talk([[13,'嗯...這裡有個裂縫，應該有辦法把它打通才對...'],[0,'......']],True,info='Initial room')
                else:self.people_talk['girl'].remove(self.scenes_name)
            elif self.scenes_name=='staircase' and near(600,600) and abs(chr.pos[1]-4217)<100 and not moveto((750,0),50):
                easy_talk([[3,'哇!是電梯'],[0,'可惡...需要電梯卡...']],True,info='elevator')
            elif self.scenes_name=='power room':
                chr.Flip(True),easy_talk([[3,'哇!是電腦!裡面一定有關於這棟大樓的情報'],[0,'唔...有監視器...' if monitor_here() else '去看一下~']],True,info=('power room' if monitor_here() else (None if self.computer_setting['power_room']['login'] else 'computer')))
            elif self.scenes_name=='Storeroom' and near(150,700) and not moveto((150,0),50):
                if coffer_lock():
                    easy_talk([[3,'哦~是保險櫃!'],[0,'裡面肯定有什麼情報或犯罪證物吧，記錄一下...'],[3,'需要密碼......'],[0,'......']],True,info='coffer')
                else:easy_talk([[3,'哦~是保險櫃!'],[0,'裡面是空的呀......']],True)
            elif self.scenes_name=='Sweep room':
                easy_talk([[10,'嗚...'],[11,'有股怪味......'],[0,'......']],True)
            elif self.scenes_name == 'B2':easy_talk('唔，得小心有沒有人才行呢')
            elif self.scenes_name == 'time_lab':easy_talk('這是甚麼研究機關...'),chr.Flip(True)
            elif self.scenes_name == 'small room' and chr.tapfloor:easy_talk('嗯...這裡或許藏有甚麼秘密......')
            elif self.scenes_name == 'treasure':
                gem=self.search2('gem')
                if gem!=None and gem.state==1:
                    chr.Flip(gem.pos[0]>chr.pos[0]),easy_talk([[3,'啊!這是在博覽會被盜的鑽石'],[8,'經由黑市流到這邊了嗎......']])
                else:self.people_talk['girl'].remove('treasure')
            elif self.scenes_name == 'treasure2':
                aircraft=self.search2('aircraft')
                if aircraft!=None:
                    if 'treasure2_enemy' not in self.people_talk['girl']:
                        self.people_talk['girl']+=['treasure2_enemy']
                        self.Talk(chr,'小心!有機械保全!')
                    elif random()<0.005:self.Talk(chr,'有敵人快離開吧!')
                else:
                    if 'treasure2_enemy' not in self.people_talk['girl']:self.Talk(chr,'這裡是拍電影的嗎...')
                    else:
                        self.Talk(chr,'幹掉了...'),self.people_talk['girl'].remove('treasure2_enemy')
                    self.people_talk['girl'].remove('treasure2')
            elif self.scenes_name == 'B1':easy_talk([[8,'或許可以從停車場出口出去呢']])
            elif self.scenes_name=='mortal room' and near(1080,50):
                easy_talk([[3,'!!!'],[0,'.....好殘忍']])
            elif self.scenes_name == '1F':easy_talk('喂......這裡很多人欸，還是不要來這裡吧')
            elif self.scenes_name == '1F_outside':easy_talk('......')
            elif self.scenes_name == 'c_lab' and chr.state==0 and chr.tapfloor:
                man1=self.search2('man1')
                if man1!=None:
                    self.people_talk['girl'].remove('c_lab'),self.loading_story('girl',40)
            elif self.scenes_name == 'c_corridor':easy_talk('這就是這間大樓隱藏機密的地方啊......'),chr.Flip(True)
            elif self.scenes_name == 'c_Storeroom':easy_talk('嘩!好多武器!'),chr.Flip(True)
            elif self.scenes_name == 'c_nuclear' and near(300,100):
                chr.DoPose(0),self.role.DoPose(0)
                man1=self.search2('man1')
                if man1!=None:man1.DoPose(0),wait_talk_end(man1,'這些桶子...我有不詳的預感')
                chr.DoPose(3),wait_talk_end(chr, '嗚哇......'),self.people_talk['girl'].remove('c_nuclear')
            elif self.scenes_name == 'c_boomhole' and self.role.pos[0]>6300:
                self.people_talk['girl'].remove('c_boomhole'),self.role.DoPose(0)
                while True:
                    if moveto((self.role.pos[0]-100, 0), 50):
                        self.display(),wait_tap()
                    else:break
                get=chr.Throw(fix_item_pos=True)
                if get!=None and get not in self.world['object']:self.world['object']+=[get]
                chr.Throw(),self.loading_story('girl',50)
                display_end(Trigger([0,0,10,10],'display_end',self,'touch',[],{'variable':'end4'}))
        elif abs(chr.pos[0]-self.role.pos[0])<100 and not chr.eventing:select_inspect()
        elif chr.tem_cold>0:chr.tem_cold-=1
        elif self.selecting and self.selectbox[0][2]=='?':self.selecting=False
        elif self.scenes_name=='power room' and time()>chr.jump_warn[2] and monitor_here():
            self.Talk(chr,['如果能躲避監視器就好了......','有辦法可以毀壞監視器嗎...'][int(2*random())]),chr.Flip(True)
            chr.jump_warn[2]=time()+5+int(4*random())
        if len(self.talkbox)==0:
            for item in self.world['object']:
                if item.name in self.item_talk['girl']:
                    if type(item.hide)==bool and item.hide and abs(chr.pos[0]-self.role.pos[0])<200 and self.role.tapfloor:
                        if item.name=='phone':
                            if self.phone_setting['power']<2 and 'phone2' not in self.item_talk['girl']:
                                self.item_talk['girl'] += ['phone2']
                                face_to_face(),self.loading_story('girl',20)
                                self.information+=['phone']
                            elif self.phone_setting['power']>2:
                                face_to_face(),self.item_talk['girl'].remove('phone')
                                if 'phone2' in self.item_talk['girl']:
                                    self.item_talk['girl'].remove('phone2')
                                    self.loading_story('girl', 23)
                                else:self.loading_story('girl', 24)
                                if 'phone' in self.information:self.information.remove('phone')
                    elif not item.hide and abs(item.pos[0]-chr.pos[0])<100:
                        #if item.name=='gun':
                         #   easy_talk([[13,'怎麼有一把槍在地上'],[0,'拿著說不定可以防身用']], mode=item.name)
                        if item.name=='c4':
                            easy_talk([[13,'唔哇!是炸彈'],[0,'好危險']], mode=item.name)
    elif self.alarm and 'elevator_card' not in self.props:
        def talkn(text,n):
            if len(self.talkbox)==0:
                self.Talk(chr, text),face_to_face(False)
                chr.jump_warn[1],self.selecting=n,False
        def get_police():
            m=(None,10000)
            for i in self.world['object']:
                if i.live==1 and i.name in ('mpolice','wpolice','specialforce','preservation') and abs(i.pos[0]-chr.pos[0])<m[1] and abs(chr.pos[1]-i.pos[1])<150:m=(i,abs(i.pos[0]-chr.pos[0]))
            return m[0]
        if chr.jump_warn[1]==0:talkn('糟糕!被發現了',1)
        elif chr.jump_warn[1]==1:talkn('趕快逃',2)
        else:
            police,weapon=get_police(),chr.Throw(fix_item_pos=True)
            if police!=None:
                if chr.jump_warn[1]==2:talkn('完蛋，他們來了',3)
                elif weapon!=None and weapon.name in ('gun','sword'):
                    if chr.jump_warn[1]==3:
                        chr.eventing=True
                        talkn('我來抵擋，你快逃',4)
                    if weapon.name == 'gun':
                        if not moveto(police.pos,500):
                            if chr.posen!=14:
                                chr.DoPose(14),chr.Flip(chr.pos[0]<police.pos[0])
                                weapon.rotate=weapon.role.rotate=40
                            elif chr.role.posek>45 and chr.posen==14:
                                chr.DoPose(0)
                                chr.Flip(chr.pos[0]<police.pos[0])
                                self.bullet += [[bullet_dictory[weapon.name]['bullet'], [weapon.pos[0] + bullet_dictory[weapon.name]['shot_pos2'][0] * (-1 if weapon.flip else 1),weapon.pos[1], bullet_dictory[weapon.name]['size'][0], bullet_dictory[weapon.name]['size'][1]],[bullet_dictory[weapon.name]['speed'] * (-1 if weapon.flip else 1), 0, 0],[weapon.flip, 0, False,0]]]
                    elif weapon.name=='sword':
                        if not moveto(police.pos,150):
                            chr.eventing = True
                            if chr.posen not in (14,15):
                                chr.DoPose(14),chr.Flip(chr.pos[0]<police.pos[0])
                                weapon.rotate=weapon.role.rotate=-30
                            elif chr.posen==14 and chr.role.posek>42:
                                chr.DoPose(15)
                            elif chr.posen==15:
                                if chr.role.posek<45:weapon.rotate = weapon.role.rotate =-30+int(4*chr.role.posek/3)
                                else:
                                    weapon.rotate = weapon.role.rotate =-40
                                    chr.DoPose(0)
                                    chr.Flip(chr.pos[0]<police.pos[0])
                                    sword_chop(chr,not chr.flip,People)
                            if chr.role.posek<45:chr.role.posek+=1
            else:chr.eventing=False
            #if len(self.talkbox)==0 and random()<0.02:self.Talk(chr,['趕快逃','快點!','要躲起來才行'][int(3*random())])
def talk_thing(e,name='girl',pl=6.6):
    black,bg= Surface(screen.get_rect()[2:]),screen.copy()
    for m in range(2):
        for i in range(255):
            wait_tap()
            screen.blit(bg,(0,0))
            black.set_alpha(i if m==0 else (255-i))
            screen.blit(black, (0, 0))
            display.update()
        e.DoPose(0,1000)
        terminal.world.display(False)
        bg=screen.copy()
    terminal.world.plot[name]=pl
def talk_thing2(e):
    talk_thing(e,'man1',4.7)
    terminal.world.loading_story('man1',4.7)
def talk_thing3(e):
    if abs(terminal.world.role.pos[0]-e.pos[0])<200:
        e.pos[0] = min(terminal.world.role.pos[0] + 200 * (1 if terminal.world.role.pos[0] < e.pos[0] else -1),terminal.world.world['background'][2][0] - 100)
        terminal.world.role.pos[0] = e.pos[0] - 200 * (1 if terminal.world.role.pos[0] < e.pos[0] else -1)
    man1=terminal.world.search2('man1')
    if man1!=None and abs(man1.pos[0]-e.pos[0])<100:
        e.pos[0] = min(man1.pos[0] + 100 * (1 if man1.pos[0] < e.pos[0] else -1),terminal.world.world['background'][2][0] - 100)
        man1.pos[0] = e.pos[0] - 100 * (1 if man1.pos[0] < e.pos[0] else -1)
    if man1!=None and abs(man1.pos[0]-terminal.world.role.pos[0])<100:
        man1.pos[0] = terminal.world.role.pos[0] - 100 * (1 if man1.pos[0] < terminal.world.role.pos[0] else -1)
        terminal.world.role.pos[0] = min(man1.pos[0] + 100 * (1 if man1.pos[0] < terminal.world.role.pos[0] else -1),terminal.world.world['background'][2][0] - 100)
    e.Flip(e.pos[0]<terminal.world.role.pos[0])
    talk_thing(e,'girl',42)
    terminal.world.loading_story('girl',42)
def take_elevator_escape(e):
    for police in terminal.world.policebox:
        police.chroom+=1000
    while e in terminal.world.followbox:terminal.world.followbox.remove(e)
    terminal.door_lock=True
def girl_follow(e):
    terminal.world.Add_follow(e)
def stand(e):
    e.freeze='stand'
    wait_talk_end(terminal.world.role,'站著不要動')
def girl_take_item(e):
    box=[]
    screen.blit(terminal.black,(0,0))
    for i in terminal.world.world['object']:
        if not i.hide and not i.fix and i.visible and i!=e and i.name not in Moveable_obj and (i.live!=1 or i.name not in (People+['man1'])):
            pos=(i.pos[0] + terminal.world.world['background'][1][0], i.pos[1] + terminal.world.world['background'][1][1])
            i.Show(pos,runpose=not i.hide)
            box+=[[pos[0]+(-i.rects[i.posen][2] if i.flip else i.rects[i.posen][0]),pos[1]+i.rects[i.posen][1],pos[0]+(-i.rects[i.posen][0] if i.flip else i.rects[i.posen][2]),pos[1]+i.rects[i.posen][3],i]]
    text_render(screen,'Select item',40,(210,210,210),(20,20)),text_render(screen,'canel',30,(255,255,255),(1050,680)),display.update()
    bg,choose=screen.copy(),None
    while True:
        for event2 in event.get():
            if event2.type == QUIT: return
            if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                x, y = mouse.get_pos()
                for i in box:
                    if i[0]<x<i[2] and i[1]<y<i[3]:
                        screen.blit(bg,(0,0)),draw.rect(screen,(255,255,0),[i[0],i[1],i[2]-i[0],i[3]-i[1]],3),text_render(screen,'ok',30,(255,255,255),(1160,680)),display.update()
                        choose=i[4]
                if 1050<x<1120 and 685<y<715:return
                elif 1160<x<1195 and 685<y<715 and choose!=None:
                    for trigger in terminal.world.world['trigger']:
                        if trigger.function!=None and 'monitor' in trigger.function.__name__ and  rect_touch(trigger.variable,choose):
                            wait_talk_end(e,'去撿的話會被監視器拍到......')
                            return None
                    e.jump_warn[4],e.freeze,e.eventing=choose,True,True
                    get=e.Throw(fix_item_pos=True)
                    if get!=None and get not in terminal.world.world['object']:terminal.world.world['object']+=[get]
                    return e.Throw()
        sleep(0.1)
plot_events=[talk_now_do,man1_take_gun,tem_leave,boss_escape,take_elevator_escape,girl_take_item,talk_think,talk_information,stand,girl_follow,talk_thing,talk_thing2,talk_thing3,stay,shot,leave,leave2,Inspect_gem,man1_follow,man1_take_shield,man1_to_5F,man1_walk_to_prison,boss_walk,choose_prison_key,Building_collapsed,drive_helicopter,Building_collapsed_savefile]
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (130,30)
init()
display.set_caption('Skyscraper Escape')
mixer.init()
def wait_tap():
    for event2 in event.get():
        if event2.type == QUIT:return False
        if event2.type == MOUSEBUTTONDOWN:return True
    return None
def role_item(search=None):
    for i in terminal.world.itemlist:
        if i!=None and i.name ==search or search==None:
            return i
    return None
def c4_boom(self,boom=False):
    for chr in terminal.world.world['object']+[terminal.world.role]:
        if chr.id in ['player','flammable'] and rect_touch(self.rect,chr):
            boom=True
    if boom:
        terminal.world.world['trigger'].remove(self)
        explosion(self.picturebox[0], self.rect,target=['flammable']+Cuttable_obj,blood=False,fragments=4)
        explosion(self.picturebox[0],self.rect,fragments=4)
def explosion(explosive_surf,surf_rect,target=People+['specialforce']+Cuttable_obj,blood=True,power=4,effect='fancy boom',fragments=3,sound='boom'):
    def fixbox(box,fix_pos,speed):#[[x-,x+],[y-,y+],[angle-,angle+]]
        for i in box:
            i.setstart()
            i.speed =[speed[0][0]+(speed[0][1]-speed[0][0])*random(),speed[1][0]+(speed[1][1]-speed[1][0])*random(),speed[2][0]+(speed[2][1]-speed[2][0])*random()]
            #i.speed=[0,0,0]
            i.p[0]+=fix_pos[0]
            i.p[1]+=fix_pos[1]
    box,sbox,boom_rect,removebox=splitimage(explosive_surf,3) if explosive_surf!=None else [],[],[surf_rect[0]+min(surf_rect[2]/2-boom_effect_dictory[effect][0]/2,0),surf_rect[1]+min(surf_rect[3]/2-boom_effect_dictory[effect][1]/2,0),max(boom_effect_dictory[effect][0],surf_rect[2]),max(boom_effect_dictory[effect][1],surf_rect[3])],[]
    for chr in terminal.world.world['object']+[terminal.world.role]:
        if (chr.id in target or target=='All') and rect_touch(boom_rect,chr) and (chr.id!='player' or not terminal.player_setting['invincible']) and (chr.live==1 or chr.id!='player'):
            terminal.sound[sound].play()
            if chr.id=='aircraft' and chr.blood<10 and effect==None:continue
            if chr.name == 'girl' and (terminal.world.plot['girl']>26 or terminal.world.scenes_name[:2]=='c_'):continue
            if chr in terminal.world.followbox:terminal.world.followbox.remove(chr)
            if chr.name in Game_setting['police'] and not terminal.world.alarm:
                terminal.sound['alarm'].play(),terminal.world.play_bgm('nervous')
                terminal.world.alarm = True
            chr.role.pos,chr.live=chr.pos,0
            rect,rect2= chr.role.get_rect(),chr.get_rect()
            img = transform.scale(terminal.blank.copy(), (int(rect[2]) + 20, int(rect[3]) + 20))
            chr.Show((chr.pos[0] - rect[0] + 10,chr.pos[1] - rect[1] + 10), surf=img)
            if chr.id!='player':
                terminal.world.guide2_count(chr,'died')
                chr.Throw()
                removebox+=[chr]
                #terminal.world.world['object'].remove(chr)
            else:
                chr.visible=False
                girl,man1=terminal.world.search2('girl'),terminal.world.search2('man1')
                if girl!=None:girl.DoPose('shock',50),terminal.world.Talk(girl,'哇阿!!!')
                if man1!=None:terminal.world.Talk(man1,'哇勒!')
                terminal.world.followbox=[]
            if chr.name in ('wblock','lab_tube'):fragments+=2
            ssbox=splitimage(img,fragments)
            need_blood=(blood and chr.name!='aircraft')
            fixbox(ssbox,(chr.pos[0]+rect2[0]-20-(0 if need_blood else int(rect2[2]/2)),chr.pos[1]+rect2[1]-20-(0 if need_blood else int(rect2[3]/2))),[[-0.75*power,0.75*power],[-power*2,-power],[-1.25*power,1.25*power]])
            if need_blood:
                for i in range(10):
                    terminal.world.world['effect'] += [[f'blood_splash{1+int(2*random())}',0, -1,0.3, [rect[0]+int(rect[2]/2)-250,rect[1]+int(rect[3]/2)-117+int(rect[3]*random()),500,235],1, 1,i*2]]
                terminal.world.world['effect'] += [['blood_drip', 0,-1,0.2,[rect[0]+int(rect[2]/2) - 217,terminal.world.world['floor']-120,435,221,{'stamp':True}],1,0,0]]
            for i in ssbox:i.effect=int(10*random()) if need_blood else -1 #播放禎
            sbox+=ssbox
    while len(removebox)>0:
        for i in removebox:
            if i in terminal.world.world['object']:terminal.world.world['object'].remove(i)
            if i in terminal.world.policebox:terminal.world.policebox.remove(i)
            removebox.remove(i)
    for trigger in terminal.world.world['trigger']:
        if rect_touch2(boom_rect,trigger.rect) and trigger.function!=None and trigger.function.__name__=='c4_boom':
            c4_boom(trigger,boom=True)
    fixbox(box,surf_rect,[[-6,6],[-15,-5],[-20,20]])
    for i in box: i.effect = -1
    terminal.world.fragments+=box+sbox
    if effect!=None:terminal.world.world['effect']+=[[effect,0,-1,0.3 if effect!='fancy boom' else 1,[surf_rect[0]+int(surf_rect[2]/2)-640,surf_rect[1]+int(surf_rect[3]/2)-360,1280,720],1,0,0]]   #名稱,初始,結尾(-1:最後),增量,rect[x,y,w,h,rotate,flip],播放次數(-1:無限),前後(0:後,1:前),計算禎
def Error_hint(text,center_pos=(640,360),size=0.5):
    surf,abc,rect1,rect2,s,tembg=terminal.image['error'],1,[620,0,92,40],[493,283,197,59],0.5,screen.copy()
    text_render(surf,text,30,(0,0,0),(160,135))
    surf,pos=transform.scale(surf,(int(surf.get_size()[0]*size),int(surf.get_size()[1]*size))),(center_pos[0]-int(surf.get_size()[0]*size/2),center_pos[1]-int(surf.get_size()[1]*size/2))
    while s<1:
        surf.set_alpha(120*s),screen.blit(transform.scale(surf,(int(surf.get_size()[0]*s),int(surf.get_size()[1]*s))),(center_pos[0]-int(surf.get_size()[0]*s/2),center_pos[1]-int(surf.get_size()[1]*s/2))),display.update(),screen.blit(tembg,(0,0))
        s+=0.01
    surf.set_alpha(255),screen.blit(surf,pos),display.update(),terminal.sound['warn'].play()
    while abc==1:
        for event2 in event.get():
            if event2.type == QUIT:abc=0
            if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                x, y = mouse.get_pos()
                for i in [rect1,rect2]:
                    if 0<x-pos[0]-i[0]*size<i[2]*size and 0<y-pos[1]-i[1]*size<i[3]*size:abc=0
        sleep(0.2)
def use_computer(self):
    #terminal.world.computer_setting['power_room']['login']=True
    def loading():
        tem_bg, angle = screen.copy(), 0
        for i in range(24):
            img = transform.rotate(transform.scale(terminal.image['loading'], (100, 100)), angle)
            screen.blit(img,(640 - int(img.get_size()[0] / 2), 300 - int(img.get_size()[1] / 2))), display.update(), sleep(0.05), screen.blit(tem_bg, (0, 0))
            angle -= 30
            if random() < 0.1: sleep(0.2)
        sleep(0.5)
    def computer_screen():
        terminal.world.display(False),screen.blit(bg, (172, 30))
        if terminal.world.computer_setting['power_room']['login']:
            screen.blit(surveillance_control,(209,190)),text_render(screen,'[全大樓]監視器警報系統',30,(0,0,0),(230,200),fonttype=1),text_render(screen,'on' if terminal.world.computer_setting['power_room']['anti-system'] else 'off',30,(0,200,0) if terminal.world.computer_setting['power_room']['anti-system'] else (150,150,150),(980,200),fonttype=1)
            screen.blit(surveillance_control, (209, 269)),text_render(screen,'[1F]飛彈防禦系統', 30, (0, 0, 0), (230,280),fonttype=1), text_render(screen, 'on' if terminal.world.computer_setting['power_room']['anti-missile'] else 'off', 30, (0, 200, 0) if terminal.world.computer_setting['power_room']['anti-missile'] else (150, 150, 150), (980, 280), fonttype=1)
            screen.blit(surveillance_control, (209, 350)),text_render(screen,'[4F]武器庫警報系統', 30, (0, 0, 0), (230,360),fonttype=1), text_render(screen, 'on' if terminal.world.computer_setting['power_room']['anti-weapon'] else 'off', 30, (0, 200, 0) if terminal.world.computer_setting['power_room']['anti-weapon'] else (150, 150, 150), (980, 360), fonttype=1)
        else:
            screen.blit(login,(383,230)),login_btn.show()
            account.Show(),password.Show()
        terminal.world.nowbg.blit(transform.scale(screen.subsurface([201,75,877,562]).copy(),(79,52)),(1066,325))
        keyboard.Show()
        display.update()
    abc,bg,login,login_btn,wt,t,surveillance_control,terminal.world.using_computer=1,transform.scale(terminal.image['screen'], (936, 660)),Surface((500,330)),button(' 登入 ',(595,490),ftc=(255,255,0),bgc=(100,100,100)),terminal.world.temsave+[['',0],['',0]],0,Surface((860,60)),True
    bg.blit(transform.scale(image.load(f'{work_dir}scenes/73.jpg'),(877,562)),(29,43)),text_render(bg, '大樓自動保全系統', 80, (255,255,255), (30,30)), draw.line(bg, (255,255,255),(30,140),(907,140),5),surveillance_control.fill((255,255,255)),surveillance_control.set_alpha(200),bg.blit(transform.scale(terminal.image['keyboard'],(40,40)),(50,550))
    account,password,account.point,password.point=Input_box((495,333),(340,35),font_dict2[25],bgc=None,limit='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*/\\,.<>|-+_= '),Input_box((495,403),(340,35),font_dict2[25],bgc=None,limit='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*/\\,.<>|-+_= '),wt[0][1],wt[1][1]
    login.fill((255,255,255)),login.set_alpha(200),draw.rect(login,(0,0,0),login.get_rect(),5),text_render(login,'研究員登入',50,(0,0,0),(10,10)),text_render(login,'帳號',30,(0,0,0),(35,100)),text_render(login,'密碼',30,(0,0,0),(35,170)),account.AddText(wt[0][0]),password.AddText(wt[1][0])
    keyboard,get_key=Virtual_keyboard((202,200),(180,380),hide=True),None
    computer_screen()
    while abc == 1:
        x, y= 0, 0
        for event2 in event.get():
            if event2.type == QUIT:
                abc = 0
            if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                x, y = mouse.get_pos()
                #print(x,y)
                if not keyboard.hide:
                    get_key = keyboard.tap((x, y))
                    if get_key!=None:terminal.sound['button5'].play()
                    account.input(get_key), password.input(get_key)
                else:get_key=None
                if 0<x-50-172<40 and 0<y-550-30<40:
                    keyboard.hide,get_key=not keyboard.hide,0
                    terminal.sound['button4' if keyboard.hide else 'hint'].play()
                if not (172<x<1108 and 30<y<690) and get_key==None:abc=0
                if not terminal.world.computer_setting['power_room']['login']:
                    if get_key==None:
                        account.tap((x,y)),password.tap((x,y))
                        if login_btn.tap(x,y):
                            terminal.sound['button4'].play(),loading()
                            if account.Value==Game_setting['computer_setting']['account'] and password.Value==Game_setting['computer_setting']['password']:
                                terminal.world.computer_setting['power_room']['login'],keyboard.hide=True,True
                                terminal.sound['enter'].play()
                                if 'computer' in self.world.information:self.world.information.remove('computer')
                                girl = self.world.search2('girl')
                                if girl != None:terminal.world.Talk(girl,'哇!登入了!')
                            else:Error_hint('帳號或密碼錯誤')
                elif 509<x<1069 and 190<y<250:
                    terminal.world.computer_setting['power_room']['anti-system']=not terminal.world.computer_setting['power_room']['anti-system']
                elif 509<x<1069 and 269<y<330:
                    t=systeminput('更改此功能需要認證碼[飛彈防禦]')
                    if t!=False:
                        loading()
                        if t==Game_setting['computer_setting']['missile-password']:
                            terminal.world.computer_setting['power_room']['anti-missile']=not terminal.world.computer_setting['power_room']['anti-missile']
                        else:Error_hint('密碼錯誤，變更失敗')
                elif 509<x<1069 and 350<y<410:
                    t=systeminput('更改此功能需要認證碼[武器庫]')
                    if t!=False:
                        loading()
                        if t==Game_setting['computer_setting']['weapon-password']:
                            terminal.world.computer_setting['power_room']['anti-weapon']=not terminal.world.computer_setting['power_room']['anti-weapon']
                        else:Error_hint('密碼錯誤，變更失敗')
            if event2.type==KEYDOWN:
                x,y=-1,-1
                account.input(event2),password.input(event2)
        if not terminal.world.busy and not terminal.world.is_busy and len(terminal.world.talkbox) == 0 and len(terminal.world.bullet)==0 and x==y==0 and time()<t:
            sleep(0.1)
        else:
            t=time()+0.2
            computer_screen()
            sleep(0.1)
        terminal.world.calculate(thread=False,times=1)
    terminal.world.temsave,terminal.world.using_computer=[[account.Value,account.point],[password.Value,password.point]],False
    if 'computer' not in self.world.information and not self.world.computer_setting['power_room']['login']:
        girl=self.world.search2('girl')
        if girl!=None:
            girl.pos[0]=self.world.role.pos[0]-200
            self.world.Talk(girl,'還需要帳號和密碼......好麻煩....'),girl.DoPose(0)
        self.world.information += ['computer']
Trigger_events=[teleport,inspect_aircraft_die,collapse_block,nuclear_boom,puzzle_square,end_battle,wait_role,sensor_door,sensor_door2,display_end,missile_protection,take_elevator,take_elevator2,shattered,hole_paint_back,enterhole,outhole,c4_boom,use_computer,Destroy_the_monitor,charge,block,car_inspect,monitor,export_exit,unlock_coffer,notice_board,plot,smash_obj,alarm,prison_5F,helicopter,cooking,master_key_lock]
#------------------------------------------------------------------------------------------------------------------------------------------工具程式
def Digits_convert(num,digits):
    return str('0'*max(0,digits-len(str(num))))+str(num)
def use_phone():
    def phone_info():
        screen.blit(terminal.image['phone'], (460, 10))
        text_render(screen, f'{int(terminal.world.phone_setting["power"])}%', 15, (255, 255, 255), (700, 71))
        draw.rect(screen, (0, 220, 0), [735, 75, int(terminal.world.phone_setting['power'] / 2), 15]), draw.rect(screen,(255,255,255),[735,75,50, 15],2)
        if terminal.world.phone_setting['link']: screen.blit(transform.scale(terminal.image['wifi'], (17,15)),(485, 76))
        if terminal.world.phone_setting['flymode']: screen.blit(transform.scale(terminal.image['airplanemode'], (15, 15)), (485, 76))
        if terminal.world.phone_setting['gps']: screen.blit(transform.scale(terminal.image['gps'], (12, 15)), (505, 76))
    def mainpage():
        t=localtime(time())
        phone_info(),text_render(screen,f'{Digits_convert(t.tm_year,2)}/{Digits_convert(t.tm_mon,2)}/{Digits_convert(t.tm_mday,2)}',20,(80,80,80),(500,100),fonttype=1)
        text_render(screen, f'{Digits_convert(t.tm_hour, 2)}:{Digits_convert(t.tm_min, 2)}', 120, (80, 80, 80),(500, 100),fonttype=1)
        phone_update()
    def camera():
        pic=screen.copy()
        phone_info(),draw.rect(screen,(0,255,0),[483,92,312,45]),text_render(screen,'相機',40,(255,255,255),(590,90)),draw.rect(screen,(255,255,255),[485,138,310,500])
        screen.blit(transform.scale(pic,(305,180)),(485,200))
        for i in [savepicture,back]:i.show()
        phone_update()
    def take_picture():
        abc,rect= 1,[0,0,1280,720]
        pic=screen.copy()
        while abc == 1:
            x,y=0,0
            for event2 in event.get():
                if event2.type == QUIT:
                    return False
                if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                    if event2.button==5:rect[2],rect[3]=int(rect[2]*0.9),int(rect[3]*0.9)
                    if event2.button ==4: rect[2],rect[3] =min(int(rect[2] *1.09),1280),min(int(rect[3] *1.09),720)
                    if event2.button==1:abc='ok'
                if event2.type==MOUSEMOTION or event2.type == MOUSEBUTTONDOWN:
                    x, y = mouse.get_pos()
                    rect[0], rect[1] = min(max(0, x - int(rect[2] / 2)),1280-rect[2]),min(max(0, y - int(rect[3] / 2)),720-rect[3])
            if not terminal.world.busy and len(terminal.world.talkbox) == 0 and len(terminal.world.bullet) == 0 and x==y==0:sleep(0.1)
            else:
                terminal.world.calculate(),terminal.world.display(update=False)
                pic=screen.copy()
                screen.blit(terminal.black,(0,0)),screen.blit(pic,rect[:2],rect)
                draw.rect(screen,(255,255,255),[rect[0],rect[1],int(rect[2]/3),rect[3]],3),draw.rect(screen,(255,255,255),[rect[0]+int(rect[2]*2/3),rect[1],int(rect[2]/3),rect[3]],3)
                draw.rect(screen, (255, 255, 255), [rect[0], rect[1], rect[2],int(rect[3]/3)], 3), draw.rect(screen,(255,255,255),[rect[0],rect[1]+int(rect[3]*2/3),rect[2],int(rect[3]/3)],3)
                display.update()
        if abc=='ok':
            return pic.subsurface(rect)
    def read_message(title,msg,title_color= (0, 220, 220),pnl_color=(255,255,255)):
        def render_content(pnl,msg):
            box,k,p,lock=[],0,0,0
            while k<len(msg[1]):
                if msg[1][k]=='$':lock=[1,0][lock]
                if msg[1][k] not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' and lock==0:
                    box+=[msg[1][p:k+1]]
                    p=k+1
                k+=1
            text_render(pnl,msg[0].split('_')[0],30,(0,0,0),(0,-2),fonttype=1),draw.line(pnl,(0,0,0),(0,37),(310,37),2)
            if '_' in msg[0]:text_render(pnl, msg[0].split('_')[1], 15, (0, 0, 0), (250, 12), fonttype=1)
            textbox, w, h= [], 0,40
            for i in box:
                if i != '\n':
                    if '$' in i:
                        name,model=i[1:-1].split('_')
#                        print(f'role/{name}/s{model}.png')
                        img=image.load(f'{work_dir}role/{name}/s{model}.png')
                        txt=transform.scale(img,(int(img.get_rect()[2]*0.1),int(img.get_rect()[3]*0.1)))
                    else:txt=font_dict[20].render(i, True,(0, 0,0))
                    width=txt.get_rect()[2]
                    if w+width<310:
                        pnl.blit(txt,(w,h))
                        w+=width
                    else:
                        w,h=width,h+txt.get_rect()[3]+5
                        pnl.blit(txt, (0, h))
                else:w, h = 0, h + 25
            return pnl
        def up():
            phone_info(),draw.rect(screen,title_color, [483, 92, 312, 45]), text_render(screen,str(title), 40, (255, 255, 255),(570, 90))
            if mode==0:
                screen.blit(panel,(483,138),[0,rol_y,310,450])
            else:screen.blit(content,(483,138)),btn1.show(),btn2.show(),text_render(screen,f'{page}/{len(msg)}',20,(0,0,0),(650,600))
            draw.line(screen,(0,0,0),(483,589),(795,589),2),back.show(),phone_update()
        panel,content_blank=Surface((310,max(len(msg)*30,450))),Surface((310,450))
        panel.fill(pnl_color),content_blank.fill(pnl_color)
        for i in range(len(msg)):
            text_render(panel,msg[len(msg)-i-1][0].split('_')[0],20,(0,0,0),(10,30*i),fonttype=1),draw.line(panel,(100,100,100),(0,30+30*i),(310,30+30*i),2)
            if '_' in msg[len(msg) - i - 1][0]:text_render(panel, msg[len(msg) - i - 1][0].split('_')[1], 10, (0, 0, 0), (260,5+30 * i),fonttype=1)
        abc,rol_y,btn1,btn2,page,mode,content=1,0,button('<',(730,595)),button('>',(760,595)),0,0,content_blank.copy()
        up()
        while abc == 1 and terminal.world.phone_setting['power']>1:
            x,y,chpage=0,0,None
            terminal.world.phone_setting['power']-=0.01
            for event2 in event.get():
                if event2.type == QUIT:
                    abc = 0
                if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                    x, y = mouse.get_pos()
                    terminal.world.phone_setting['power'] -= 0.2
                    if event2.button==5 and rol_y<=panel.get_rect()[3]-450:rol_y+=min(50,panel.get_rect()[3]-rol_y-450)
                    if event2.button==4 and rol_y>=0:rol_y-=min(50,rol_y)
                    if back.tap(x,y):
                        mode-=1
                        if mode<0:return
                    if mode==0 and 485<x<795 and 138<y<588 and event2.button==1:
                        for i in range(len(msg)):
                            if 0<y-138+rol_y-30*i<30:
                                chpage=i+1
                                break
                    if btn1.tap(x, y) and page > 1: chpage =page-1
                    if btn2.tap(x, y) and page<len(msg): chpage = page+1
                    if chpage!=None:
                        content=render_content(content_blank.copy(),msg[len(msg)-chpage])
                        mode,page=1,chpage
            if not terminal.world.busy and len(terminal.world.talkbox) == 0 and len(terminal.world.bullet) == 0 and x == y == 0:
                sleep(0.1)
            else:up()
            terminal.world.calculate()
    def setting():
        phone_info(),draw.rect(screen, (130,130,130), [483, 92, 312, 45]), text_render(screen, '設定', 40, (255, 255, 255),(590, 90)), draw.rect(screen, (255, 255, 255),[485, 138, 310, 500]),back.show()
        for i in range(3):
            text_render(screen,['網路連接','GPS定位','飛航模式'][i],30,(0,0,0),(493,138+40*i),fonttype=1),draw.rect(screen,(0,200,0),[720,143+40*i,25,30]),draw.rect(screen,(100,100,100),[720,143+40*i,50,30],4)
            draw.line(screen,(100,100,100),(483,178+40*i),(795,178+40*i),2),draw.rect(screen,(200,200,200),[724+(21 if terminal.world.phone_setting[['link','gps','flymode'][i]] else 0),145+40*i,23,26])
        phone_update()
    def phone_update():
        tembg=screen.subsurface([460,10,359,700]).copy()
        phone.role.mainlimb[0].surfbox[0][0].blit(transform.scale(tembg.subsurface([23,63,312,563]),(23,42)),(2,4)),terminal.world.display(update=False),screen.blit(tembg,(460,10))
        display.update()
    mode=0  #0:主解面,1:相機,2:郵件,3:記事本,4:設定
    #button-------------------------------------------------
    savepicture=button(' 拍照 ',(600,450))
    #picturebtn=button(' 相簿→ ',(670,570))
    back=button(' ←返回 ',(500,595))
    #-------------------------------------------------------
    phone=None
    for i in terminal.world.world['object']:
        if i.name == 'phone': phone = i
    mainpage()
    abc = 1
    while abc == 1 and terminal.world.phone_setting['power']>1:
        terminal.world.phone_setting['power']-=0.01
        for event2 in event.get():
            if event2.type == QUIT:
                abc = 0
            if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                x, y = mouse.get_pos()
                terminal.world.phone_setting['power'] -= 0.2
                #print(x,y)
                if not (460<x<820 and 10<y<710):
                    abc=0
                else:
                    if mode==0:
                        if 491<x<555 and 326<y<391:
                            mode=1
                            camera()
                        if 562<x<630 and 326<y<391:
                            read_message('收件夾',message['Initial']),mainpage()
                        if 642<x<705 and 326<y<391:
                            read_message('記事本',notes,title_color=(99,66,00),pnl_color=(255,255,200)),mainpage()
                        if 716<x<783 and 326<y<391:
                            mode=2
                            setting()
                    if mode==1:
                        if savepicture.tap(x,y):
                            pic=take_picture()
                            if pic==False:return False
                            else:
                                camera(),screen.blit(terminal.black, (0, 0)),draw.rect(screen,(255,255,255),[155,85,970,550]),screen.blit(transform.scale(pic,(960,540)),(160,90))
                                display.update()
                                terminal.Operation_panel([[[0,0,1280,720],'QUIT']]),camera()
                    if mode==2:
                        for i in range(3):
                            if 720<x<770 and 0<y-143-35*i<30:
                                if i==0 and not terminal.world.phone_setting['link'] and terminal.world.phone_setting['flymode']:terminal.world.phone_setting['flymode']=False
                                if i == 2 and not terminal.world.phone_setting['flymode'] and terminal.world.phone_setting['link']: terminal.world.phone_setting['link'] = False
                                terminal.world.phone_setting[['link', 'gps', 'flymode'][i]]=not terminal.world.phone_setting[['link','gps','flymode'][i]]
                        setting()
                if back.tap(x,y):
                    mode=0
                    mainpage()
        if not terminal.world.busy and len(terminal.world.talkbox) == 0 and len(terminal.world.bullet)==0:
            sleep(0.2)
        else:
            if mode == 0:mainpage()
            elif mode == 1:camera()
            elif mode == 2:setting()
        terminal.world.calculate()
#關卡截止縣---------------------------------------------------------------------------------------------------
def zoom_surf(surf,max_length):
    w,h=surf.get_rect()[2:4]
    r = min(max_length /w, max_length /h)
    return transform.scale(surf, (int(w * r), int(h * r)))
def word_rect(surf,text,b,c):
    w,h,mw=0,0,surf.get_rect()[2]
    for t in text:
        text_render(surf,t,b,c,(w,h))
        w+=b+1
        if w+b>mw:w,h=0,h+b+5
    return surf
def systemprogress(t,n,w=500,pos=(400,200)):
    draw.rect(screen,(100,100,100),[pos[0],pos[1],w,130]),ashow(t+f' {round(100*n,1)}%',30,(255,255,0),(pos[0]+10,pos[1]+10)),draw.rect(screen, (0, 200,0), [pos[0]+50, pos[1]+80,int(400*n),40]),draw.rect(screen, (0, 0, 0), [pos[0]+50,pos[1]+80, 400, 40],3),display.update()
class Terminal:
    def __init__(self):
        self.world=World()
        self.image={}
        for i in listdir(f'{work_dir}/object'):
            self.image[i[:-len(i.split('.')[-1])-1]]=image.load(f'{work_dir}object/{i}')
        self.blank=image.load(f'{work_dir}object/original.png')
        self.black=Surface((1280,720))
        self.black2 = Surface((100, 100))
        self.black.set_alpha(100),self.black2.set_alpha(4)
        self.white=Surface((100,100))
        self.white.fill((255,255,255))
        self.effect={}
        self.info={}
        self.limb_ed={}
        self.nowfile=self.next_savefile()
        setting=str_convert(open(f'{work_dir}data/setting.txt','r',encoding='utf-8').read())
        self.last_file=setting['last_file']
        self.unlock_end=setting['ending']
        self.bgm_vol=setting['bgm']
        #mixer.music.set_volume(self.bgm_vol)
        self.sound_vol=setting['sound']
        self.sound_config={}
        for sound in open(f'{work_dir}data/sound.txt','r',encoding='utf-8').read().split('\n'):
            c=sound.split('=')
            self.sound_config[c[0]]=float(c[1])
        self.sound={}
        for i in listdir(f'{work_dir}sound'):
            self.sound[i[:-len(i.split('.')[-1])-1]]=mixer.Sound(f'{work_dir}sound/{i}')
        self.view_mode=setting['mode']  #0全屏 1 1280*720
        self.tem_cold=0
        self.operate_mode=setting['operate'] #觸控,鍵盤
        self.player_setting={'fly':False,'invincible':False,'block':True,'latent':False,'fall':True}
        self.zoom=1.5
        self.re_assign=False
        self.teaching_mode=False
        self.door_lock=False
        self.end_game=False
    def save_setting(self):
        open(f'{work_dir}data/setting.txt', 'w', encoding='utf-8').write(str({'bgm':self.bgm_vol, 'sound':self.sound_vol, 'mode': self.view_mode,'operate': self.operate_mode, 'last_file': self.nowfile,'ending':self.unlock_end}))
    def next_savefile(self):
        k,o=0,listdir(f'{work_dir}data')
        while f'save {k}.txt' in o:k+=1
        return k
    def adjust_sound(self):
        for i in self.sound:
            if i not in self.sound_config:self.sound_config[i]=1
            self.sound[i].set_volume(self.sound_vol*self.sound_config[i])
    def load_data(self,sp_room=None,effect=True,bg=None):
        def get_surf(chr):
            rect = chr.role.get_rect()
            img = transform.scale(terminal.blank.copy(), (int(rect[2]) + 10, int(rect[3]) + 10))
            chr.Show((chr.pos[0] - rect[0] + 5, chr.pos[1] - rect[1] + 5), surf=img)
            return img
        def add_describe(name,posen,surf_rect,dict):
            self.info[name][posen] = [surf_rect,dict[name][0],dict[name][1]]
            if len(dict[name]) == 3 and posen in dict[name][2]:
                self.info[name][posen][1] = dict[name][2][posen][0]
                if len(dict[name][2][posen]) == 2: self.info[name][posen][2] =dict[name][2][posen][1]
            self.info[name][posen][2] = word_rect(wordrect.copy(), self.info[name][posen][2] + '。', 30,(255, 255, 255))
        wordrect=transform.scale(terminal.blank,(360,150))
        self.allbg,o,n,k={},listdir(f'{work_dir}scenes'),0,0
        for room in map:n+=1
        for room in map:
            self.world.extra = []
            if sp_room!=None and room not in sp_room:continue
            if f'{map[room]["background"][0]}.png' in o:
                self.allbg[room] = transform.scale(image.load(f'{work_dir}scenes/{map[room]["background"][0]}.png'),map[room]["background"][2]).convert()
            elif f'{map[room]["background"][0]}.jpg' in o:
                self.allbg[room] = transform.scale(image.load(f'{work_dir}scenes/{map[room]["background"][0]}.jpg'),map[room]["background"][2]).convert()
            for i in range(len(map[room]['back'])):  # ----------------------------------------------------------------------back
                img = self.image[map[room]['back'][i][0]] if len(map[room]['back'][i][1]) == 2 else transform.scale(self.image[map[room]['back'][i][0]], map[room]['back'][i][1][2:])
                if len(map[room]['back'][i])>2:
                    if 'flip' in map[room]['back'][i][2]:img=transform.flip(img,map[room]['back'][i][2]['flip'],False)
                self.allbg[room].blit(img, map[room]['back'][i][1][:2])
            for cmd in map[room]['object']:
                if len(cmd)<5 or 'visible' not in cmd[4] or cmd[4]['visible']:
                    obj=command_to_character(cmd)
                    if len(cmd)>3:obj.DoPose(cmd[3],speed=1000)
                    if obj.name not in self.info:
                        self.info[obj.name]={}
                    if obj.posen not in self.info[obj.name]:
                        add_describe(obj.name,obj.posen,get_surf(obj),Item_dictory)
                    obj.extra_item=self.world.extra
                    if obj.fix:
                        obj.Show(surf=self.allbg[room])
                        obj.pose_finish = True
            for trigger in map[room]['trigger']:
                if type(trigger[1]) == str and trigger[1] in Eevent_dictory and len(trigger)>3 and len(trigger[3])>0:
                    if trigger[1] not in self.info:
                        self.info[trigger[1]]={}
                    if trigger[3][0] not in self.info[trigger[1]]:
                        add_describe(trigger[1],trigger[3][0],self.image[trigger[3][0]],Eevent_dictory)
                if len(trigger)>3 and len(trigger[3])==1:
                    trigger_img=transform.scale(self.image[trigger[3][0]],trigger[0][2:])
                    if len(trigger)>4:
                        if 'rotate' in trigger[4]:trigger_img=transform.rotate(trigger_img,-trigger[4]['rotate'])
                        if 'flip' in trigger[4]: trigger_img = transform.flip(trigger_img, trigger[4]['flip'],False)
                        if trigger[1]=='notice_board':
                            text=trigger[4]['variable'].split('|')
                            for line in range(len(text)):
                                text_render(trigger_img,text[line],trigger[4]['variable2'],(0,0,0),(2,2+trigger[4]['variable2']*line))
                    self.allbg[room].blit(trigger_img,trigger[0][:2])
            map[room]['back'] = []
            if 'text' in map[room]:
                for i in map[room]['text']:
                    text_render(self.allbg[room], i[0], i[1], i[2], i[3])
            self.world.allbackground[room]=self.allbg[room].copy()
            k+=1
            if bg!=None:screen.blit(bg,(0,0))
            draw.rect(screen,(0,200,0),[30,676,int(1000*k/n),10])
            display.update(),wait_tap()
        self.guide_num=0
        for item in self.info:
            for pose in self.info[item]:
                self.guide_num+=1
        if effect:
            n,kc=len(listdir(f'{work_dir}effect')),0
            for i in listdir(f'{work_dir}effect'):
                if path.isdir(f'{work_dir}effect/{i}') and 'not' not in i:
                    k, o, self.effect[i] = 0, listdir(f'{work_dir}effect/{i}'), []
                    while f'{k}.png' not in o: k += 1
                    while f'{k}.png' in o:
                        self.effect[i] += [image.load(f'{work_dir}effect/{i}/{k}.png')]
                        k += 1
                kc+=1
                if bg != None: screen.blit(bg, (0, 0))
                draw.rect(screen, (0, 200, 0), [30,676,1000+int(220 * kc/n), 10])
                display.update(),wait_tap()
    def init_world(self,sp_room=None):
        self.world.load(self.init_info(sp_room=sp_room))
    def init_info(self,sp_room=None):
        info={'bgm':'inception','map': {},'guide': {'kirito':{0:True}},'guide2':{},'props':['kirito'],'max_enemy':2,'shock':[False, 0, 0, 0, 3, 0],'plot':copy_variable(Game_setting['plot']),'scenes_name':'Initial room' if sp_room==None else sp_room[0],'alarm':False,'save_time':nowtime(),'follower':[],'police_comespeed':900,'police':{'mpolice':Game_setting['police']['mpolice']['num'],'wpolice':Game_setting['police']['wpolice']['num'],'specialforce':Game_setting['police']['specialforce']['num'],'specialforce2':Game_setting['police']['specialforce2']['num']},
                'computer_setting':copy_variable(Game_setting['computer_setting']),'phone_setting':copy_variable(Game_setting['phone_setting']),'boom trigger':copy_variable(Game_setting['boom trigger']),'role_state':{'cmd':['kirito',0.4,(200,380)],'room':sp_room[0] if sp_room!=None else 'Initial room','control':True},'itemlist':{},'itemlist_k':0,'zoom':1,'people_talk':copy_variable(Game_setting['people_talk']),'item_talk':copy_variable(Game_setting['item_talk']),'information':[]}
        smap,self.zoom=info['map'],1
        for room in map:                #Chatacters轉化
            if sp_room!=None and room not in sp_room:
                continue
            self.extra=[]
            smap[room]=copy_variable(map[room])
            smap[room]['warn']=False
            for i in range(len(smap[room]['object'])):                       #----------------------------------------------------------------------object
                cmd=smap[room]['object'][i]
                if len(cmd)<4:cmd+=[0]
                smap[room]['object'][i]=command_to_character(smap[room]['object'][i])
            smap[room]['object']+=self.extra
            for i in range(len(smap[room]['trigger'])):                       #----------------------------------------------------------------------trigger
                info2=smap[room]['trigger'][i]
                if len(info2)==2:info2+=['touch']
                if len(info2)==3:info2+=[[]]
                if len(info2) == 4: info2 += [{}]
                smap[room]['trigger'][i] = Trigger(info2[0],info2[1],self.world,info2[2],info2[3],info2[4])
                if smap[room]['trigger'][i].function!=None and smap[room]['trigger'][i].function.__name__=='notice_board':
                    k=0
                    for line in smap[room]['trigger'][i].variable.split('|'):
                        text_render(smap[room]['trigger'][i].picturebox[0],line,smap[room]['trigger'][i].variable2,(0,0,0),(3,5+smap[room]['trigger'][i].variable2*k))
                        k+=1
            for i in range(len(smap[room]['front'])):                       #----------------------------------------------------------------------front
                smap[room]['front'][i][0]=self.image[smap[room]["front"][i][0]]
        info['role']=Character('role/kirito', 0.4)
        for name in self.info:
            info['guide2'][name] = {}
            for posen in terminal.info[name]:
                info['guide2'][name][posen] = {'display': 0, 'used': 0, 'died': 0}
        return info
    def savefile(self,num=None):
        savetext=str(self.world.save())
        open(f'{work_dir}data/save {num if num!=None else self.nowfile}.txt','w').write(savetext)
        self.save_setting()
    def loadfile(self,num,zoom=None,text='載入中...'):
        filedata=open(f'{work_dir}data/save {num}.txt','r').read().replace('\\\\','')
        smap,info,n,k,bg=copy_variable(map),str_convert(filedata),0,0,screen.copy()
        cmd,self.zoom,self.teaching_mode,self.door_lock=info['role_state']['cmd'],info['zoom'] if zoom==None else zoom,info['teach_mode'],False
        cmd[1]*=self.zoom
        if cmd[2]!=None:
            cmd[2][0]=int(cmd[2][0]*self.zoom)
            cmd[2][1]=int(cmd[2][1]*self.zoom)
        role,scenes_name,role.control,role.zoom=command_to_character(cmd),info['role_state']['room'],info['role_state']['control'],self.zoom
        for room in smap:n+=1
        for room in smap:
            smap[room]['background'][1][0]=int(smap[room]['background'][1][0]*self.zoom)
            smap[room]['background'][1][1]=int(smap[room]['background'][1][1]*self.zoom)
            smap[room]['background'][2][0]=int(smap[room]['background'][2][0]*self.zoom)
            smap[room]['background'][2][1]=int(smap[room]['background'][2][1]*self.zoom)
            self.world.allbackground[room]=transform.scale(self.allbg[room],smap[room]['background'][2])
            smap[room]['floor']=int(smap[room]['floor']*self.zoom)
            triggerbox,objectbox=[],[]
            for trigger in info['map'][room]['trigger']:
                trigger[0][0]=int(trigger[0][0]*self.zoom)
                trigger[0][1]=int(trigger[0][1]*self.zoom)
                trigger[0][2]=int(trigger[0][2]*self.zoom)
                trigger[0][3]=int(trigger[0][3]*self.zoom)
                if type(trigger[1])==list:trigger[1][1]=[int(trigger[1][1][0]*self.zoom),int(trigger[1][1][1]*self.zoom)]
                triggerbox+=[Trigger(trigger[0],trigger[1],self.world,key=trigger[2],picturebox=trigger[3],fixed=trigger[4])]
            for obj_cmd in info['map'][room]['object']:
                if obj_cmd[2][0]==None:obj_cmd[2][0]=-10000
                obj_cmd[1]*=self.zoom
                obj_cmd[2][0]=int(obj_cmd[2][0]*self.zoom)
                obj_cmd[2][1]=int(obj_cmd[2][1]*self.zoom)
                objectbox+=[command_to_character(obj_cmd)]
                objectbox[-1].zoom=self.zoom
            if room==scenes_name:
                get = role.Throw(fix_item_pos=True)
                if get != None:objectbox+=[get]
            smap[room]['trigger'],smap[room]['object']=triggerbox,objectbox
            screen.blit(bg,(0,0)),systemprogress(text,k/n)
            k+=1
        info['role'],info['scenes_name'],info['map'],role.visible=role,scenes_name,smap,True
        self.world.load(info)
        self.nowfile=num
        self.save_setting()
    def Operation_panel(self,buttonlist):#[[[x,y,w,h],function]]
        abc=1
        while abc == 1:
            for event2 in event.get():
                if event2.type == QUIT:
                    #abc = 0
                    raise Error
                if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                    x, y = mouse.get_pos()
                    for i in buttonlist:
                        if 0<x-i[0][0]<i[0][2] and 0<y-i[0][1]<i[0][3]:
                            if i[1]=='QUIT':abc=0
                            else:i[1]()
            sleep(0.2)
    def Wait(self,waiting=True,slp=False,skp=(-100,0,10,10)):
        times=1
        while waiting or times>0:
            for event2 in event.get():
                if event2.type == QUIT and yesno('要關閉遊戲嗎?','當前進度可能會丟失'):
                    self.end_game=True
                    return True
                if event2.type in [MOUSEBUTTONDOWN,KEYDOWN]:
                    waiting=False
                    if event2.type==MOUSEBUTTONDOWN:
                        x,y=mouse.get_pos()
                        if 0<x-skp[0]<skp[2] and 0<y-skp[1]<skp[3]:return True
            times-=1
            if slp:sleep(0.1)
        return False
def count_unlock_guide(guide):
    n = 0
    for item in guide:
        if item in terminal.info:
            for pose in guide[item]:
                if pose in terminal.info[item]:n += 1
    return n
def count_explore_rate(info):
    return str(min(round((count_unlock_guide(info['guide'])/126+info['plot']['man1']/60)*50,2),100))+'%'
def game_pause():
    if not terminal.world.alarm and not terminal.teaching_mode: terminal.savefile(terminal.nowfile)
    game_option=['道具圖鑑','我的存檔','遊戲說明','遊戲設定','回主畫面']
    screen.blit(terminal.black,(0,0))
    for i in range(len(game_option)):
        draw.rect(screen,(255,255,255),[30,80+90*i,180,50],3),text_render(screen,game_option[i],30,(255,255,255),(60,85+90*i),1)
    draw.rect(screen, (255, 255, 255), [1100, 600,160, 50], 3), text_render(screen,'繼續',30, (255, 255, 255),(1140,605), 1)
    bg=screen.copy()
    def render_guide():
        screen.blit(guide, (0, 0)),screen.blit(guide_board.subsurface([0,guide_y,guide_size[0],guide_size[1]]),guide_pos)
        text_render(screen,f'{terminal.info[choose_guide[0]][choose_guide[1]][1]}',30,(255,255,255),(680,90))
        screen.blit(terminal.info[choose_guide[0]][choose_guide[1]][2],(680,150))
        img=zoom_surf(terminal.info[choose_guide[0]][choose_guide[1]][0],150)
        screen.blit(img,(350+int((150-img.get_rect()[2])/2),150+int((150-img.get_rect()[3])/2)))
        draw.rect(screen,(100,100,100),[guide_pos[0]+guide_size[0]-4,guide_pos[1]+int(guide_y*guide_size[1]/guide_board.get_rect()[3]),3,int(guide_size[1]*guide_size[1]/guide_board.get_rect()[3])])
    def render_savefile():
        o,k=listdir(f'{work_dir}data'),0
        while k<len(o):
            if o[k][:5]!='save ':del o[k]
            else:k+=1
        k=0
        while k<4:
            if f'save {4*savefile_page+k}.txt' in o:
                info,blank=str_convert(open(f'{work_dir}data/save {4*savefile_page+k}.txt','r').read()),(yellow if 4*savefile_page+k==terminal.nowfile else white).copy()
                text_render(blank,'目前'if 4*savefile_page+k==terminal.nowfile else f'存檔{4*savefile_page+k+1}',30,(0,0,0),(660,40))
                blank.blit(transform.scale(terminal.allbg[info['role_state']['room']],(200,100)),(20,15)),text_render(blank,info['save_time'],25,(0,0,0),(240,12),1),text_render(blank,f'圖鑑: {count_unlock_guide(info["guide"])}/{terminal.guide_num}',25,(0,0,0),(240,48),1)
                text_render(blank, f'探索度: {count_explore_rate(info)}', 25, (0, 0, 0),(240, 85), 1)
                blank.set_alpha(200 if 4*savefile_page+k==terminal.nowfile else 150)
                screen.blit(blank, (280, 60 + 150 * k))
                k+=1
            else:
                blank=white.copy()
                blank.set_alpha(150)
                screen.blit(blank, (280, 60 + 150 * k)),text_render(screen,'新增+',30,(100,100,100),(939,100+150*k))
                break
        text_render(screen,f'{savefile_page+1}/{max((len(o)-1)//4,0)+1}',30,(255,255,255),(1150,280))
        if savefile_page>0:screen.blit(terminal.image['arrowup'],(1150,70))
        if savefile_page<(len(o)-1)//4: screen.blit(terminal.image['arrowdown'],(1150,360))
    def render_instructions():
        for i in range(len(Game_instructions)):
            text_render(screen,Game_instructions[i][0],40,(255,255,255),(300,80+85*i),fonttype=1),text_render(screen,Game_instructions[i][1],40,(255,255,255),(500,80+85*i))
    def get_guide():
        def now_hold(itemname,pose):
            for obj in terminal.world.itemlist:
                if obj!=None and obj.name==itemname and obj.posen==pose:return True
            return False
        guide=transform.scale(terminal.blank,(1280,720))
        text_render(guide, '圖片:', 30, (255, 255, 0), (280, 90)), text_render(guide, f'名稱:', 30, (255, 255, 0),(600, 90)),text_render(guide,'說明:',30,(255,255,0),(600,150))
        draw.rect(guide,(0,0,0),[280,325,785,365])
        guide_board=Surface((785,600))
        for i in range(4):
            draw.rect(guide,[(0,255,0),(255,255,255),(155,155,155),(0,0,0)][i],[1090,350+50*i,20,20])
            text_render(guide,['目前持有中','曾持有過','見過但未持有過','未見過'][i],20,(255,255,255),(1120,345+50*i))
        w, h,terminal.guide_num= 10,10,0
        for item in terminal.info:
            for pose in terminal.info[item]:
                if (item in terminal.world.guide and pose in terminal.world.guide[item]) or item in terminal.world.props:
                    img = zoom_surf(terminal.info[item][pose][0], 50)
                    if item in terminal.world.props or now_hold(item,pose):draw.rect(guide_board, (0, 200, 0), [w, h, 50, 50]), draw.rect(guide_board,(0, 255,0),[w + 1, h + 1, 48, 48], 3)
                    elif terminal.world.guide[item][pose]:draw.rect(guide_board, (200, 200, 200), [w, h, 50, 50]), draw.rect(guide_board,(255, 255,255),[w + 1, h + 1, 48, 48], 3)
                    else:draw.rect(guide_board, (100, 100, 100), [w, h, 50, 50]), draw.rect(guide_board,(155, 155, 155),[w + 1, h + 1, 48, 48], 3)
                    guide_board.blit(img,(w + int((50 - img.get_rect()[2]) / 2), h + int((50 - img.get_rect()[3]) / 2)))
                else:guide_board.blit(transform.scale(terminal.image['unknow'],(50,50)),(w,h))
                w += 55
                if w > 739: w, h = 10, h + 55
                terminal.guide_num+=1
        return guide,guide_board.subsurface([0,0,785,h+55])
    def up():
        screen.blit(bg,(0,0))
        for i in range(len(game_option)):
            if (30<x<210 and 0<y-80-90*i<50) or i==choose:
                draw.rect(screen,(200,200,200) if i==choose else (255, 255, 255), [30, 80 + 90 * i, 180, 50]), text_render(screen,game_option[i], 30,(100,100,100),(60, 85 + 90 * i), 1)
        if 1100<x<1260 and 600<y<650:
            draw.rect(screen, (255, 255, 255), [1100, 600, 160, 50]), text_render(screen, '繼續', 30, (100,100,100),(1140, 605), 1)
        if choose==0:render_guide()
        elif choose == 1:render_savefile()
        elif choose==2:render_instructions()
        elif choose==3:setting.display(False)
        display.update()
    roleitem=terminal.world.role.Throw(fix_item_pos=True)
    roleitem=[roleitem.name,roleitem.posen] if roleitem!=None else [None,None]
    guide,guide_board=get_guide()
    guide_y,guide_pos,guide_size=0,(280,325),(785,365)
    savefile_page=terminal.nowfile//4
    white,yellow=Surface((800,130)),Surface((800,130))
    white.fill((255,255,255)),yellow.fill((255,215,0)),terminal.sound['button'].play()
    choose=0
    setting=Game_set((370,130))
    choose_guide=['exptable',0]
    abc,x,y= 1,0,0
    while abc == 1:
        for event2 in event.get():
            if event2.type == QUIT and yesno('確定要關閉遊戲嗎?','遊戲進度已儲存'):
                return False
            if event2.type == MOUSEBUTTONDOWN:                                                     #滑鼠點擊
                x,y = mouse.get_pos()
                for i in range(len(game_option)):                 #選項
                    if 30 < x < 210 and 0 < y - 80 - 90 * i < 50:
                        terminal.sound['button2'].play()
                        if i==4:
                            if yesno('確定要回主畫面嗎?','遊戲進度會自動保存'):return 'back menu'
                        else:choose=i
                        up()
                if 1100 < x < 1260 and 600 < y < 650:              #繼續
                    terminal.sound['button3'].play()
                    abc=0
                if choose == 0 and 0<x-guide_pos[0]<guide_size[0] and 0<y-guide_pos[1]<guide_size[1]:                                     #選擇guide
                    if event2.button == 4 and guide_y > 0:guide_y=max(0,guide_y-40)
                    elif event2.button==5 and guide_y<guide_board.get_rect()[3]-guide_size[1]:guide_y=min(guide_y+40,guide_board.get_rect()[3]-guide_size[1])
                    elif event2.button==1:
                        w, h = guide_pos[0]+10,guide_pos[1]+10-guide_y
                        for name in terminal.info:
                            for posen in terminal.info[name]:
                                if 0 < x - w < 50 and 0 < y - h < 50 and name in terminal.world.guide and posen in terminal.world.guide[name]:
                                    choose_guide = [name, posen]
                                    up(),terminal.sound['button2'].play()
                                w += 55
                                if w > 1030: w, h = 290, h + 55
                elif choose==1:
                    o, k = listdir(f'{work_dir}data'), 0
                    while k < len(o):
                        if o[k][:5] != 'save ':del o[k]
                        else:k += 1
                    for i in range(4):
                        if 280<x<1080 and 0<y-60-150*i<130:
                            if f'save {4*savefile_page+i}.txt' in o and yesno('讀取存檔',f'確定讀取 "存檔 {4*savefile_page+i+1}"?'):
                                up(),terminal.loadfile(4*savefile_page+i)
                            if f'save {4*savefile_page+i}.txt' not in o and f'save {4*savefile_page+i-1}.txt' in o and yesno('新增存檔','要將目前進度存入新存檔嗎'):
                                terminal.savefile(4*savefile_page+i)
                    if 1150<x<1191 and 70<y<242 and savefile_page>0:
                        terminal.sound['button2'].play()
                        savefile_page-=1
                    if 1150 < x < 1191 and 360 < y < 532 and savefile_page<(len(o)-1)//4:
                        terminal.sound['button2'].play()
                        savefile_page+=1
                elif choose == 3:
                    setting.mainloop((x,y))
                up()
        if key.get_pressed()[K_p]:abc=0
        if (x,y)!=mouse.get_pos():
            x, y = mouse.get_pos()
            up()
        sleep(0.1)
    return 'continue'
check_resources()
font_dict={10:font.Font(f'{work_dir}data/msjh.ttc', 10),
           15:font.Font(f'{work_dir}data/msjh.ttc',15),
           20:font.Font(f'{work_dir}data/msjh.ttc', 20),
           30:font.Font(f'{work_dir}data/msjh.ttc', 30),
           40:font.Font(f'{work_dir}data/msjh.ttc', 40),
           50:font.Font(f'{work_dir}data/msjh.ttc', 50),
           70:font.Font(f'{work_dir}data/msjh.ttc', 70),
           80:font.Font(f'{work_dir}data/msjh.ttc', 80)}
font_dict2={10:font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf',10),
            15:font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf',15),
            20:font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf',20),
            25: font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf', 25),
            30: font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf',30),
            50: font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf', 50),
            80: font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf', 80),
           120:font.Font(f'{work_dir}data/GenJyuuGothic-P-Light.ttf',120)}
def text_render(surf,t,b,c,d,fonttype=0):
    font_dictory=font_dict if fonttype==0 else font_dict2
    if b in font_dictory:surf.blit(font_dictory[b].render(t, True, c),d)
    else:surf.blit(font.Font(f'{work_dir}data/'+('msjh.ttc' if fonttype==0 else 'GenJyuuGothic-P-Light.ttf'), b).render(t, True, c),d)
def Ward_Inspect():
    bed,patent=terminal.world.search2('sickbed'),terminal.world.search2('girl')
    if bed!=None and patent!=None:
        while terminal.world.scenes_name=='Ward':
            if 25<terminal.world.role.posen<29:
                patent.pos=[bed.pos[0],bed.pos[1]-int(115*terminal.zoom)]
                sleep(0.03)
            else:
                sleep(0.2)
                if patent not in terminal.world.world['object']:
                    bed, patent = terminal.world.search2('sickbed'), terminal.world.search2('girl')
                    if bed==None:break
            if patent.state==0:break
def Treasure2_Inspect():
    def rope_linkage(role):
        if role.name=='rope':board_pos[1]=int(305*terminal.zoom)-role.pos[1]
    def picture_render(box,x_pos,direct):
        for m in range(2):
            if (direct==1 and (1450+50*m)*terminal.zoom>x_pos) or (direct==2 and (1450+50*m)*terminal.zoom<x_pos):
                x, y, size,i= int(360*terminal.zoom),int([board_pos[1]+435,380][m]*terminal.zoom),round(360 / abs(1450+50*m - x_pos)*terminal.zoom,3),0
                while i<len(box):
                    if (direct==1 and (1450+50*m)*terminal.zoom<box[i][0]) or (direct==2 and (1450+50*m)*terminal.zoom>box[i][0]):i+=1
                    else:break
                if m==0 or direct==1:
                    if not (m==0 and terminal.world.boom_trigger['treasure2']):
                        box.insert(i,[int((1450+50*m)*terminal.zoom),transform.scale([Surface((100,100)),terminal.image['password2']][m],(int([530,400][m]*size),int([200,109][m]*size))),(x-int([265,200][m]*size),y-int([100,55][m]*size))])
                        if m==0:box.insert(i,[int(1450*terminal.zoom),transform.scale(terminal.image['rope'],(int(10*size),y)),(x-int(205*size),0)]),box.insert(i,[int(1450*terminal.zoom),transform.scale(terminal.image['rope'],(int(10*size),y)),(x+int(205*size),0)])
                if m==1:box.insert(i,[1450+50*m,transform.scale(Surface((100,100)),(int(530*size),int(400*size))),(x-int(265*size),y-int(100*size))]),box[i][1].fill((255,255,255))
    board_pos, terminal.world.pickupevent, rope, coldtime, terminal.world.picture_render,girl=[1450,-65], rope_linkage, terminal.world.GetRole('rope'), 0.3, picture_render,terminal.world.search2('girl')
    if not terminal.world.boom_trigger['treasure2']:
        terminal.world.world['back']=[[terminal.image['board'],board_pos]]
        while terminal.world.scenes_name == 'treasure2':
            sleep(coldtime)
            if girl==None:girl=terminal.world.search2('girl')
            if rope.pos[1]>370*terminal.zoom and terminal.world.role.posen!=5 and (girl==None or girl.posen!=14):
                coldtime,terminal.world.busy=0.03,True
                rope.pos[1]-=int(3*terminal.zoom)
                board_pos[1]+=int(8*terminal.zoom)
            elif coldtime!=0.3:coldtime,terminal.world.busy,terminal.world.eventrole,board_pos[1]=0.3,False,None,int(-65*terminal.zoom)
            for i in terminal.world.world['effect']:
                if i[0]=='fancy boom' and rect_touch2(rect_zoom([board_pos[0],board_pos[1],113,596],terminal.zoom),i[4]):
                    explosion(terminal.world.world['back'][-1][0],zoom_rect([board_pos[0],board_pos[1],113,596],terminal.zoom), target=Cuttable_obj, blood=False, power=0, effect=None, fragments=3)
                    terminal.world.boom_trigger['treasure2'],terminal.world.world['back']=True,[]
                    return
        terminal.world.map['treasure2']['back']=[]
def Stairs_Inspect():
    if terminal.world.scenes_name=='staircase':x,yrect,img=895,[4340,3717,3095,1230,-500],terminal.image['stair_front']
    else:x,yrect,img=726,[1024,425,-500],terminal.image['stair_front2']
    box,terminal.world.modify_scenes,terminal.world.modify_scenery,stairs=zoom_rect(yrect,terminal.zoom),[[img,[x,yrect[0]]]],True,[]
    for i in terminal.world.world['object']:
        if i.name in ['stairs','stairs2']:stairs+=[i]
    while 'staircase' in terminal.world.scenes_name:
        if terminal.world.role.speed[1]>1 and not terminal.world.role.eventing and terminal.world.role.live==1:
            terminal.world.role.DoEvent('climbup',terminal.world.world)
            sleep(0.1)
        else:
            sleep(0.2)
            key=False
            for i in stairs:
                if terminal.world.role.touch(i):
                    key=True
                    for height in box:
                        if height<terminal.world.role.pos[1]+terminal.world.role.rects[terminal.world.role.posen][1]:
                            terminal.world.modify_scenes[0][1][1]=height
                            break
            if not key and terminal.world.role.state==2:terminal.world.role.state=0
            terminal.world.modify_scenery=key
def rect_touch(rect,chr):
    if chr.pos[0] + chr.rects[chr.posen][2] > rect[0] and chr.pos[1] + chr.rects[chr.posen][3] > rect[1] and chr.pos[0] + chr.rects[chr.posen][0] < rect[0] + rect[2] and chr.pos[1] + chr.rects[chr.posen][1] < rect[1] + rect[3]: return True
    return False
def rect_touch2(rect,rect2):
    if rect2[0] + rect2[2] > rect[0] and rect2[1] + rect2[3] > rect[1] and rect2[0]< rect[0] + rect[2] and rect2[1] < rect[1] + rect[3]: return True
    return False
class Trigger:
    def __init__(self,rect,function,world,key='auto',picturebox=[],fixed={}):
        self.rect=rect
        self.world=world
        self.key=key
        self.islaunch=False
        self.flip=fixed['flip'] if 'flip' in fixed else False
        self.rotate = fixed['rotate'] if 'rotate' in fixed and fixed['rotate']!=None else 0
        if type(function)==list:         #傳送
            self.functionkey=function  #[newworld,rolepos]
            function='teleport'
        self.function=None
        for i in Trigger_events:
            if i.__name__==function:
                self.function=i
        if function=='shattered':self.life=3
        self.picturebox=[]
        self.picturename=picturebox
        for i in picturebox:
            self.picturebox+=[transform.rotate(transform.flip(transform.scale(terminal.image[i],rect[2:]),self.flip,False),self.rotate)]
        self.posen=0
        if 'posen' in fixed and type(fixed['posen'])==int:self.posen=fixed['posen']
        self.type=type
        self.cold=1
        self.variable=fixed['variable'] if 'variable' in fixed else 0
        self.variable2 = fixed['variable2'] if 'variable2' in fixed else 0
    def Touch(self,chr):
        try:
            r=rect_touch(self.rect,chr)
            return r
        except:
            print(self.rect,chr)
            e+=1
    def Detect(self,key='touch'):
        if self.key=='auto' and self.function!=None:
            self.function(self)
        if key==self.key:
            if self.Touch(self.world.role) and self.function!=None:
                self.function(self)
                return True
        return False
    def Show(self,relative_pos=(0,0)):
        if len(self.picturebox)>1:
            screen.blit(self.picturebox[self.posen],(relative_pos[0]+self.rect[0],relative_pos[1]+self.rect[1]))
def search_map_entrance(room_name):
    pos=[]
    for trigger in terminal.world.map[room_name]['trigger']:
        if trigger.function!=None and trigger.function.__name__=='teleport':
            pos+=[(trigger.rect[0],trigger.rect[1]+trigger.rect[3])]
    return pos
def search_min_map_entrance(room_name):
    pos_box, pos, s = search_map_entrance(room_name), [0, 0], 1000000
    for p in pos_box:
        if abs(p[0] - terminal.world.role.pos[0]) + abs(p[1] - terminal.world.role.pos[1]) < s:
            pos, s = p, abs(p[0] - terminal.world.role.pos[0]) + abs(p[1] - terminal.world.role.pos[1])
    return [pos[0],pos[1]-150]
def find_chr(name):
    for chr in terminal.world.world['object']:
        if chr.name==name:
            return chr
    return None
def render_time(t):
    m,s=str(int(t//60)),str(int(t%60))
    return '0'*(2-len(m))+m+':'+'0'*(2-len(s))+s
def nowtime():
    t=localtime(time())
    return f'{t.tm_year}/{t.tm_mon}/{t.tm_mday} {t.tm_hour}:{t.tm_min}:{t.tm_sec}'
class World:
    def __init__(self):
        self.allbackground={}
        self.modify_speed=40
        self.modify_y=[0,0]   #次數,y
        self.modify_scenes=[]
        self.modify_scenery=False
        self.selecting=False
        self.selectbox=[]
        self.select=None
        self.paint_back=self.void
        self.paint_front = self.void
        self.pickupevent=self.void
        self.picture_render=self.void
        self.eventrole=None
        self.busy=False
        self.is_busy=False
        self.usemode='use'
        self.useitem=None
        self.triggertime=0
        self.using_phone = False
        self.using_computer=False
        self.alarm=False
        self.fall_sound={}
        self.policebox=[]
        self.computer_setting=copy_variable(Game_setting['computer_setting'])
        self.plot=copy_variable(Game_setting['plot'])
        self.props=[]
        self.temsave=[]
        self.temsave2=[]
        self.fragments=[]
        self.talkbox=[]
        self.broadcast=[]
        self.bullet=[]
        self.picturebg=image.load(f'{work_dir}scenes/72.jpg').convert()
        self.phone_setting=copy_variable(Game_setting['phone_setting'])
        self.police={'mpolice':Game_setting['police']['mpolice']['num'],'wpolice':Game_setting['police']['wpolice']['num'],'specialforce':Game_setting['police']['specialforce']['num'],'specialforce2':Game_setting['police']['specialforce2']['num']}
        self.boom_trigger=copy_variable(Game_setting['boom trigger'])
        self.people_talk=copy_variable(Game_setting['people_talk'])
        self.item_talk = copy_variable(Game_setting['item_talk'])
        self.followbox=[]
        self.events_box=[]
        self.guide = {}
        self.needlight = False
        self.black = Surface((1280, 720))
        self.black.set_alpha(255)
        self.max_enemy = 2
        self.shock = [False, 0, 0, 0, 3, 0]  # 是否啟動，判斷時間，每次搖幾下，幾次,間隔時間,當前模式,剩餘震盪次數
        self.scenes_name='Storeroom'   #---------------------------------------------------------------------------------------------------------------------------------初始場警
        self.fps_skip=0
        self.police_comespeed=900
        self.clearance=0
        self.guide2={}  #演員名單
        self.useitem_cd=0
        self.itemlist=[None,None,None,None,None,None]
        self.itemlist_k=0
        self.itemlist_surf = Surface((50 * len(self.itemlist), 50))
        #terminal.load_data([None,self.scenes_name][0],effect=False)
        #info=terminal.init_info()
        #self.load(info)
        #-------------------------------觸控式按鍵
        blank,direct=image.load(f'{work_dir}object/original.png'),image.load(f'{work_dir}object/direct.png')
        self.direct_btn=transform.scale(direct,(230,230))
        self.else_btn=[transform.scale(blank,(100,100)),transform.scale(blank,(100,100)),transform.scale(blank,(100,100)),transform.scale(blank,(100,100))]#x,z,space
        self.direct_btn_tap,self.else_btn_tap=None,[0,0,0]
        draw.circle(self.direct_btn,(0,0,0),(115,115),113,4),self.direct_btn.set_alpha(100),draw.circle(self.else_btn[-1],(255,255,0),(50,50),50),self.else_btn[-1].set_alpha(100)
        for i in range(len(self.else_btn)-1):
            draw.circle(self.else_btn[i],(0,0,0),(50,50),48,4),text_render(self.else_btn[i],[' X',' Z','空'][i],50,(0,0,0),(25,20),1),self.else_btn[i].set_alpha(100)
        self.zoom_ed={}
        self.information=[]
        self.instory=False
        self.zoom_rate=1
        self.bgm='inception'
       # self.fps=FPS()
        self.fps=80
        self.clock=py_time.Clock()
    def play_bgm(self,bgm=''):
        if bgm!='':self.bgm=bgm
        mixer.music.stop(), mixer.music.load(f'{work_dir}bgm/{self.bgm}.mp3'), mixer.music.play(-1)
    def search(self,itemname,room_info=False):
        if itemname=='player':return self.role
        for room in self.map:
            for obj in self.map[room]['object']:
                if type(obj)==Character and obj.name==itemname:
                    if room_info:return room
                    return obj
        return None
    def search2(self,itemname,inroom=True):
        if itemname=='player':return self.role
        for obj in self.world['object']:
            if obj.name==itemname and obj.live==1:
                return obj
        if not inroom:return self.search(itemname)
    def search_trigger(self,function_name):
        for trigger in self.world['trigger']:
            if trigger.function!=None and trigger.function.__name__==function_name:return trigger
        return None
    def load_bg(self,sp_room=None):
        for room in self.map:
            if sp_room!=None and room not in sp_room:
                continue
            self.allbackground[room]=terminal.allbg[room].copy()
    def obj_to_list(self,obj,force=False):
        result = [obj.name, round(obj.size / terminal.zoom, 2),[int(obj.pos[0] / terminal.zoom), int(obj.pos[1] / terminal.zoom)], obj.posen,{'flip': obj.flip, 'live': obj.live, 'name': obj.name, 'rigid': obj.rigid, 'fix': obj.fix,'state': obj.state, 'visible': obj.visible, 'rotate': obj.rotate, 'value': obj.value,'hide': obj.hide, 'insertpart': obj.insertpart}]
        if obj.id != 'player' or force:
  #          get = obj.Throw(fix_item_pos=True)
 #           if get != None: result[4]['insert'] =[[get.parentname: self.obj_to_list(get)}
#        if obj.id=='player' and force:
            result[4]['insert']=[]
            for i in obj.Inserted_item():
                result[4]['insert']+=[[i.parentname,self.obj_to_list(i)]]
        return result
    def save(self):
        map={}
        pk=0#room:[num1,...]
        for room in self.map:
            map[room]={}
            map[room]['trigger'],map[room]['object']=[],[]
            for trigger in self.map[room]['trigger']:
                map[room]['trigger']+=[[[int(trigger.rect[0]/terminal.zoom),int(trigger.rect[1]/terminal.zoom),int(trigger.rect[2]/terminal.zoom),int(trigger.rect[3]/terminal.zoom)],None,trigger.key,trigger.picturename,{'flip':trigger.flip,'rotate':trigger.rotate,'variable':trigger.variable,'variable2':trigger.variable2,'posen':trigger.posen}]]
                if trigger.function != None and trigger.function.__name__=='teleport':
                    map[room]['trigger'][-1][1]=[trigger.functionkey[0],[int(trigger.functionkey[1][0]/terminal.zoom),int(trigger.functionkey[1][1]/terminal.zoom)]]
                elif trigger.function != None:map[room]['trigger'][-1][1]=trigger.function.__name__
            for obj in self.map[room]['object']:
                if obj.live!=1 and obj.name!='patient':continue
                if obj in self.itemlist:continue
                map[room]['object']+=[self.obj_to_list(obj)]
                if obj in self.followbox:map[room]['object'][-1][4]['follow']=True
        itemlist=[]
        for obj in self.itemlist:
            if obj!=None:
                try:itemlist+=[[obj.parentname,self.obj_to_list(obj)]]
                except:pass
            else:itemlist+=[None]
        followbox=[]
        for chr in self.followbox:followbox+=[{'name':chr.name,'room':chr.room,'chroom':chr.chroom,'speed':chr.follow_speed}]
        return {'bgm':self.bgm,'map':map,'guide':self.guide,'guide2':self.guide2,'props':self.props,'max_enemy':self.max_enemy,'shock':self.shock,'plot':self.plot,'save_time':nowtime(),'alarm':self.alarm,'follower':followbox,'police_comespeed':self.police_comespeed,'police':self.police,
                'computer_setting':self.computer_setting,'phone_setting':self.phone_setting,'role_state':{'cmd':self.obj_to_list(self.role),'room':self.scenes_name,'control':self.role.control},'itemlist':itemlist,'itemlist_k':self.itemlist_k,'boom trigger':self.boom_trigger,
                'zoom':terminal.zoom,'teach_mode':terminal.teaching_mode,'people_talk':self.people_talk,'item_talk':self.item_talk,'information':self.information}
    def load(self,info):
        self.bgm,self.map,self.guide,self.guide2,self.props,self.max_enemy,self.shock,self.plot,self.police_comespeed,self.police=info['bgm'],info['map'],info['guide'],info['guide2'],info['props'],info['max_enemy'],info['shock'],info['plot'],info['police_comespeed'],info['police']
        self.computer_setting,self.phone_setting,scenes_name,self.role,self.alarm,self.events_box,self.clearance,self.itemlist_k,self.boom_trigger=info['computer_setting'],info['phone_setting'],info['scenes_name'],info['role'],info['alarm'],[],0,info['itemlist_k'],info['boom trigger']
        self.people_talk,self.item_talk,self.information=info['people_talk'],info['item_talk'],info['information']
        self.change_scenes(scenes_name,turn_on_inspect=self.scenes_name!=scenes_name),self.play_bgm()
        self.followbox=[]
        for follower_info in info['follower']:
            get=self.search(follower_info['name'])
            if get!=None:self.followbox+=[get]
            get.room,get.chroom,get.follow_speed=follower_info['room'],follower_info['chroom'],follower_info['speed']
        self.itemlist_surf=Surface((50*len(self.itemlist),50))
        self.itemlist_surf.fill((0,0,0))
        for i in range(len(info['itemlist'])):
            if info['itemlist'][i]==None:self.itemlist[i]=None
            else:
                self.itemlist[i]=command_to_character(info['itemlist'][i][1])
                self.map[info['scenes_name']]['object']+=[self.itemlist[i]]
                self.role.Insert(info['itemlist'][i][0],self.itemlist[i])
        for i in range(len(self.itemlist)):
            draw.rect(self.itemlist_surf, (230, 230, 0) if i == self.itemlist_k else (155, 155, 155), [50 * i, 0, 50, 50], 2)
            if self.itemlist[i] != None:
                if self.itemlist[i].posen in terminal.info[self.itemlist[i].name]:
                    self.itemlist_surf.blit(transform.scale(terminal.info[self.itemlist[i].name][self.itemlist[i].posen][0], (50, 50)),(50 * i, 0))
                else:
                    for posen in terminal.info[self.itemlist[i].name]:
                        self.itemlist_surf.blit(transform.scale(terminal.info[self.itemlist[i].name][posen][0], (50, 50)),(50 * i,0))
                        break
    def update_guide(self):
        for obj in self.world['object']:
            if abs(obj.pos[0]-self.role.pos[0])<800 and abs(obj.pos[1]-self.role.pos[1])<300:
                if obj.name not in self.guide:self.guide[obj.name]={}
                if obj.posen not in self.guide[obj.name]:self.guide[obj.name][obj.posen]=False
        for trigger in self.world['trigger']:
            if trigger.function!=None and trigger.function.__name__ in terminal.info and abs(trigger.rect[0]-self.role.pos[0])<800 and abs(trigger.rect[1]-self.role.pos[1])<300:
                if trigger.function.__name__ not in self.guide:self.guide[trigger.function.__name__]={}
                if len(trigger.picturename)>0 and trigger.picturename[0] not in self.guide[trigger.function.__name__]:self.guide[trigger.function.__name__][trigger.picturename[0]]=False
    def Bind(self,name,timing,evt_function,color=(255,0,0)):
        self.events_box+=[[name,color,time()+timing,evt_function]]
    def SetShock(self,power,interval,times=-1):
        self.shock[0]=False
        if power!=False:self.shock=[True,0,power,times,interval,0,power]
    def tem_zoom(self,zoom_rate,hotkey='hotkey'):
        self.zoom_rate*=zoom_rate
        if self.scenes_name=='Ward' and self.zoom_rate<0.9:
            self.zoom_rate=1
            return
        if hotkey not in self.zoom_ed:self.zoom_ed[hotkey]={'objn':0,'obj':{}}
        if self.scenes_name not in self.zoom_ed[hotkey]:self.zoom_ed[hotkey][self.scenes_name]={}
        wb, wt, wo = self.world['background'],self.world['trigger'], self.world['object']
        if 'bg' not in self.zoom_ed[hotkey][self.scenes_name]:self.zoom_ed[hotkey][self.scenes_name]['bg']=transform.scale(self.allbackground[self.scenes_name],(int(wb[2][0] * zoom_rate), int(wb[2][1] * zoom_rate)))
        self.nowbg = self.zoom_ed[hotkey][self.scenes_name]['bg']
        self.world['floor'] *= zoom_rate
        self.world['background'] = [wb[0], [wb[1][0] * zoom_rate, wb[1][1] * zoom_rate],[wb[2][0] * zoom_rate, wb[2][1] * zoom_rate]] + wb[3:]
        for i in range(len(wt)):
            wt[i].rect = [int(wt[i].rect[0] * zoom_rate), int(wt[i].rect[1] * zoom_rate),int(wt[i].rect[2] * zoom_rate), int(wt[i].rect[3] * zoom_rate)]
        def is_item(item):
            for i in range(len(self.itemlist)):
                if self.itemlist[i] is item:return i
            return None
        cmd = self.obj_to_list(self.role,force=True)
        for i in cmd[4]['insert']:
            i[1][1]*=zoom_rate
        self.role = command_to_character([cmd[0], cmd[1] * zoom_rate, [cmd[2][0] * zoom_rate, cmd[2][1] * zoom_rate]] + cmd[3:])
        terminal.re_assign='re_assign'
        #print('------------------------------')
        for i in range(len(wo)):
            #print('第一次確認',wo[i].name)
            get=is_item(wo[i])
            if type(get)==int:
                for j in self.role.Inserted_item():
                    if j.name==wo[i].name:
                        try:
                            if j.item_skip:pass
                        except:
                            j.item_skip=True
                            if get==self.itemlist_k:j.hide,j.visible=True,True
                            self.itemlist[get]=wo[i]=j
                            break
                #print('get到',get)
            else:
                if type(wo[i])==tuple:wo[i]=wo[i][0]
                cmd = self.obj_to_list(wo[i])
                chr=command_to_character([cmd[0], cmd[1] * zoom_rate, [cmd[2][0] * zoom_rate, cmd[2][1] * zoom_rate]] + cmd[3:])
                try:chr.obj_id=wo[i].obj_id
                except:
                    chr.obj_id=f'{wo[i].name}_{wo[i].posen}_'+str(self.zoom_ed[hotkey]['objn'])
                    self.zoom_ed[hotkey]['objn']+=1
                wo[i],posen= self.zoom_ed[hotkey]['obj'][chr.obj_id]=chr,wo[i].posen
                wo[i].role.loadpose(posen,1000)
            if zoom_rate<1:
                for flr in self.followbox:
                    if flr.name==wo[i].name:
                        self.followbox.remove(flr)
                        self.Add_follow(wo[i])
                        break
                #print('正常植入',wo[i].name)
    def loading_story(self,plot_name,plot_num=None):
        self.selecting,self.instory=False,True
        if plot_num!=None:self.plot[plot_name]=plot_num
        def display_story(order):
            if type(order)==list:
                for content in order:
                    self.instory=True
                    if terminal.end_game:return
                    if type(content)==str:
                        if content[:6]=='watch_':
                            other,flip=self.search2(content.split('_')[-1]),Game_setting['watch'][self.who.id]
                            if other!=None:self.who.Flip(flip if self.who.pos[0]<other.pos[0] else (not flip))
                        elif content!='notalk':
                            self.Talk(self.who,content)
                            while len(self.talkbox)>0:
                                for event2 in event.get():
                                    if event2.type == QUIT:
                                        terminal.end_game=True
                                    if event2.type in [MOUSEBUTTONDOWN, KEYDOWN]:
                                        for textbox in self.talkbox:
                                            while textbox[0][1] < len(textbox[0][2]):
                                                textbox[0][0].blit(textbox[0][2][textbox[0][1]][0],textbox[0][2][textbox[0][1]][1])
                                                textbox[0][1] += 1
                                self.display()
                            terminal.Wait()
                    elif type(content)==dict:
                        for person in content:
                            if person=='system':
                                if type(content[person])==list:
                                    for command in content[person]:
                                        if type(command)==list:
                                            self.Broadcast(*command)
                                            while len(self.broadcast) > 0:
                                                self.display(), terminal.Wait(False)
                                            terminal.Wait()
                                        elif type(command)==str:
                                            if command=='shock':
                                                self.SetShock(100,0,1)
                            else:
                                self.who,who=self.search2(person),self.who
                                if self.who!=None:display_story(content[person])
                                self.who=who
                    elif type(content) ==int:
                        for i in range(content):
                            self.calculate(self.scenes_name,thread=False,times=1)
                            self.display(),terminal.Wait(False)
                    elif type(content)==list:
                        if type(content[0])==int:
                            self.who.DoPose(content[0]) if len(content)==1 else self.who.DoPose(content[0],content[1])
                            while not self.who.pose_finish:
                                self.display(),terminal.Wait(False)
                        elif type(content[0]) == bool:
                            self.who.Flip(content[0])
                        elif type(content[0]) == str:
                            self.who.DoEvent(content[0],self.world)
                            if self.who.eventing:
                                while self.who.eventing:
                                    self.display(),terminal.Wait(False)
                            else:
                                self.who.DoPose(content[0])
                                while not self.who.pose_finish:
                                    self.display(), terminal.Wait(False)
                        elif type(content[0])==list:
                            if type(content[0][0])==int:
                                self.role.DoPose(content[0][0])
                                while not self.role.pose_finish:
                                    self.display(),terminal.Wait(False)
                            elif type(content[0][0])==str:
                                if content[0][0] in terminal.sound:terminal.sound[content[0][0]].play()
                                else:
                                    terminal.world.play_bgm(str(content[0][0]))
                        elif type(content[0])==tuple:
                            if type(content[0][1])==str:
                                box,ed=[],{}
                                for i in content:
                                    box+=[i[1]]
                                    ed[i[1]]=i[0]
                                self.Select(box),self.display(),terminal.Wait(False)
                                select=None
                                while self.selecting or select==None:
                                    for event2 in event.get():
                                        if event2.type == QUIT:return
                                        if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                                            x, y = mouse.get_pos()
                                            for i in self.selectbox:
                                                if 0 < x - i[1][0] < 373 and 0 < y - i[1][1] < 57:select,self.selecting = i[2], False
                                    sleep(0.1)
                                self.plot[plot_name]=ed[select]
                                #print('----------------------')
                                #print(self.select)
                                if ed[select] in dialogue[plot_name] and type(dialogue[plot_name][ed[select]])==list and dialogue[plot_name][ed[select]][0]!='notalk':
                                    who2,self.who=self.who,self.role
                                    display_story([select])
                                    self.who=who2
                                self.loading_story(plot_name)
                            elif type(content[0][1])==int:
                                bx,by,xp,yp=self.world['background'][1][0],self.world['background'][1][1],(content[0][0]-self.world['background'][1][0])/40,(content[0][1]-self.world['background'][1][1])/40
                                for i in range(40):
                                    self.world['background'][1][0] = xp * i + bx
                                    self.world['background'][1][1] = yp * i + by
                                    self.display(),terminal.Wait(False)
                    elif type(content) ==tuple:
                        if content[0]=='resize':
                            self.tem_zoom(content[1],f'{self.who.name}_{content[1]}')
                            self.who = self.search2(self.who.name)
                            self.world['background'][1][0]=min(max(640-int((self.role.pos[0]+self.who.pos[0])/2),1280-self.world['background'][2][0]),0)
                            self.world['background'][1][1] =min(max(360-int((self.role.pos[1]+self.who.pos[1])/2),720-self.world['background'][2][1]),0)
                        else:
                            self.plot[plot_name]=content[0]
                            self.loading_story(plot_name)
            elif type(order)==str:
                for evt in plot_events:
                    if evt.__name__==order:
                        evt(self.who)
            #terminal.Operation_panel([[[0,0,1280,720],'QUIT']])
        self.who = self.search2(plot_name)
        self.role.control=False
        if self.who != None and self.plot[plot_name] in dialogue[plot_name]:
            order = dialogue[plot_name][self.plot[plot_name]]
            display_story(order)
        self.role.control,self.instory=True,False
    def Useevent(self,item):
        if item.name=='potion' and self.role.do_event[0]>35:
            if item.posen in [0,1,5,6,7,8,9,10,11,12]:
                item = self.role.Throw(fix_item_pos=True)
                img=terminal.info[item.name][item.posen][0]
                terminal.image['potion'].fill(img.get_at((int(img.get_rect()[2]/2),int(img.get_rect()[3]/4*3))))
                self.bullet+=[['potion',[item.pos[0]-2+int(5*random()),item.pos[1],5,5],[0,0,0],[False,0,True,2]]]
            self.useitem = None
        if item.name=='ironbox' and item.posen!=2:
            if item.value!=None:
                if 'keys' in self.props and yesno('是否使用萬能鑰匙開啟?'):
                    for i in item.value:
                        try:self.world['object'].insert(0,command_to_character(['treasure',0.15,(item.pos[0]-100+int(200*random()),item.pos[1]-20-int(15*random())),i]))
                        except:pass
                    self.Talk(self.role,'箱子解鎖')
                    item.value=None
            elif len(self.talkbox)==0:self.Talk(self.role,'箱子是空的')
            self.useitem=None
        if item.name=='broom' and self.role.do_event[0]>30:
            terminal.sound['sweep'].play()
            self.useitem=None
        if item.name=='ladder' and self.role.do_event[0]>40:
            terminal.sound['place'].play()
            self.useitem=None
        if item.name=='camera' and not item.hide and self.role.do_event[0]>100:
            pic=GetPicture(self,item.pos,direct=2 if self.role.flip else 1)
            terminal.black.set_alpha(100),screen.blit(terminal.black,(0,0)),draw.rect(screen,(255,0,0),[335,55,610,610]),screen.blit(transform.scale(pic,(600,600)),(340,60)),
            draw.rect(screen,(255,0,0),[915,55,30,30]),text_render(screen,'x',30,(255,255,255),(922,45))
            display.update()
            terminal.Operation_panel([[[915,55,30,30],'QUIT']])
            self.useitem=None
        if item.name in bullet_dictory and self.role.do_event[0]>bullet_dictory[item.name]['cold']:
            if self.role.do_event[0] > 70 or not key.get_pressed()[K_z]:self.useitem=None
            if item.role.temangle!=0:item.rotate=item.role.rotate=-item.role.temangle
            if item.st<time() and item.name!='shield':
                item.state = 1
                item.st=time()+bullet_dictory[item.name]['cold']/100
                try:
                    if item.bullet<1:
                        self.role.Throw(fix_item_pos=True),self.Talk(item, f'子彈已用盡',fontsize=20)
                        return
                except:item.bullet=bullet_dictory[item.name]['num']
                terminal.sound['missile' if item.name=='socket' else 'shot'].play()
                item.bullet -= 1
                self.role.Throw(fix_item_pos=True), self.Talk(self.role, f'發射({bullet_dictory[item.name]["num"]-item.bullet}/{bullet_dictory[item.name]["num"]})',fontsize=20)
                self.bullet+=[[bullet_dictory[item.name]['bullet'],[item.pos[0]+bullet_dictory[item.name]['shot_pos'][0]*(-1 if item.flip else 1),item.pos[1]+bullet_dictory[item.name]['shot_pos'][1],bullet_dictory[item.name]['size'][0],bullet_dictory[item.name]['size'][1]],[bullet_dictory[item.name]['speed']*(-1 if item.flip else 1),0,0],[item.flip,0,False,0]]]   #名稱,[x,y,w,h],[spx,spy,spr],[flip,rotate,gravity,0:我方,1:敵方]
        if item.name=='phone' and self.role.do_event[0]>70:
            self.useitem = None
            if  not self.using_computer:
                if self.phone_setting['power']>1:
                    self.using_phone=True
                    use_phone()
                    self.using_phone=False
                else:self.Talk(self.role,'電力不足')
        if item.name=='c4' and item.speed[0]==0 and self.role.do_event[0]>20:
            self.useitem = None
            explosion(item.role.mainlimb[0].surfbox[0][0],[item.pos[0]+item.rects[0][0],item.pos[1]+item.rects[0][1],+item.rects[0][2],+item.rects[0][3]]),self.world['object'].remove(item)
            if item in self.world['object']:self.world['object'].remove(item)
        if item.name in ['sword','knife'] and self.role.do_event[0]>80:
            self.useitem=None
            sword_chop(self.role,self.role.flip,People)
        if item.name in Cookware and len(self.talkbox)==0 and not self.selecting:
            if item.value>0:
                def pot_wait_take():
                    while len(self.talkbox)>0:sleep(0.2)
                    if self.select=='拿出物品':
                        item.Throw()
                        item.value-=1
                    self.selectbox,self.selecting,self.select,self.useitem=[],False,None,None
                item.value=len(item.Inserted_item())
                self.Talk(item,f'裝有{item.value}個物品')
                self.Select(['拿出物品']),Thread(target=pot_wait_take).start()
            else:self.Talk(item,'鍋子是空的')
            item.state=1
        if item.name=='note' and len(self.talkbox)==0:
            self.useitem,text=None,item.value.replace('|','\n')
            cisptext=text.split('$')
            if cisptext[0]=='hint':self.loading_story(cisptext[1],int(cisptext[2]))
            else:self.Talk(self.role,text)
        if time()>self.useitem_cd:
            self.guide2_count(item, 'used')
            self.useitem_cd=time()+0.5
        if item!=None:
            for obj in self.world['object']:
                if self.role.touch(obj):
                    if obj.name in Cookware and not self.selecting and not obj.hide and item.name not in Cookware:
                        def pot_wait_select():
                            while self.selecting:
                                if not self.role.touch(pot):break
                                sleep(0.2)
                            if not self.selecting:
                                if self.select=='放入鍋中':
                                    for obj in self.world['object']:
                                        if obj.hide and type(obj.hide)==bool:
                                            #obj.calculate_rects()
                                            if obj.rects[obj.posen][2]-obj.rects[obj.posen][0]<(pot.rects[pot.posen][2]-pot.rects[pot.posen][0])*2 and obj.rects[obj.posen][3]-obj.rects[obj.posen][1]<(pot.rects[pot.posen][3]-pot.rects[pot.posen][1])*2:
                                                self.role.Throw(),terminal.sound['place2'].play()
                                                pot.Insert(pot.name+(str(2-pot.posen) if pot.name=='pan' else ''),obj,visible=pot.name!='pot')
                                                pot.value+=1
                                                break
                                            else:self.Talk(obj,'太大了裝不下')
                            self.selectbox,self.selecting,self.select,self.useitem=[],False,None,None
                        pot=obj
                        if obj.value<{'pan':1,'pot':5,'steamer':3}[obj.name]:
                            self.Select(['放入鍋中'])
                            Thread(target=pot_wait_select).start()
                        else:self.Talk(obj,'鍋子滿了')
                        break
    def calculate(self,scenes_name='',thread=True,times=-1):
        if scenes_name=='':scenes_name=self.scenes_name
        def count(times=-1):
            needcount=True
            while needcount and times!=0:
                needcount=False
                for i in self.map[scenes_name]['object']:
                    i.calculate(self.map[scenes_name])
                    if i.live == 0 and i.state == 0: change_limb_angle(i.role, 0)
                    if i.speed[0] != i.speed[1] or not i.pose_finish:
                        needcount =True
                times-=1
        if thread:Thread(target=count).start()
        else:count(times)
    def SetLight(self,brightness):
        self.needlight =True
        self.black.set_alpha(brightness)
    def void(self,args1=None,args2=None,args3=None):
        pass
    def GetRole(self,rolename,sceneryname=''):
        if sceneryname=='':sceneryname=self.scenes_name
        for role in self.map[sceneryname]['object']:
            if role.name==rolename:return role
    def change_scenes(self,scenes_name,turn_on_inspect=True):
        self.modify_scenery=self.needlight=False
        self.paint_back=self.paint_front=self.pickupevent=self.picture_render=self.void
        self.useitem=None
        self.temsave,self.temsave2,self.bullet,self.fragments=[],[],[],[]
        self.scenes_name=scenes_name
        self.world,self.talkbox=self.map[scenes_name],[]
        self.nowbg=self.allbackground[scenes_name]
        if turn_on_inspect:
            if scenes_name=='Ward':Thread(target=Ward_Inspect).start()
            if 'staircase' in scenes_name: Thread(target=Stairs_Inspect).start()
            if scenes_name=='treasure2':Thread(target=Treasure2_Inspect).start()
            if scenes_name == 'treasure2': Thread(target=Treasure2_Inspect).start()
        self.world['background'][1][0] = max(min(-self.role.pos[0] + 560, 0),-self.world['background'][2][0] + 1280)
        self.world['background'][1][1] = max(-self.world['background'][2][1] + 720,min(-self.role.pos[1] + 400, 0))
        self.fall_sound = {}
        for item in self.world['object']+[self.role]:
            self.fall_sound[item.name]=[item.tapfloor,0]
            self.guide2_count(item,'display')
        self.selecting,self.selectbox,self.select=False,[],None
    def guide2_count(self,item,way):
        if item.name not in self.guide2:
            self.guide2[item.name]={item.posen:{'display':0,'used':0,'died':0}}
        if item.posen in self.guide2[item.name]:self.guide2[item.name][item.posen][way] += 1
        elif item.name == 'scientist':
            self.guide2[item.name][3*((item.posen // 3) if item.posen<18 else (item.posen-18))][way] += 1
        else:
            for i in self.guide2[item.name]:
                self.guide2[item.name][i][way] += 1
                break
    def Select(self,option):
        self.selectbox,self.selecting,self.select=[],True,None
        for i in range(len(option)):
            opt,text=terminal.image['select'].copy(),font_dict[30].render(option[i], True,(255,255,255))
            opt.blit(text,(int((373-text.get_rect()[2])/2),int((57-text.get_rect()[3])/2)))
            self.selectbox+=[[opt,(455,360-29-35*len(option)+70*i),option[i]]]
    def Talk(self,who,text,st=1,fontsize=30,direct=None):#st:說話完持續時間
        textbox,w,h,mw=[],0,0,-5
        for i in text:
            if i!='\n':
                textbox+=[[(font_dict[fontsize] if fontsize in font_dict else font.Font(f'{work_dir}data/msjh.ttc',fontsize)).render(i,True,(0,0,0)),(w,h)]]
                w+=textbox[-1][0].get_rect()[2]+1
                if w > mw: mw = w
            if w>300 or i=='\n':
                w,h=0,h+fontsize
        blank=transform.scale(terminal.blank.copy(),(mw,h+fontsize+30))
        draw.rect(blank,(255,255,255),[0,0,mw,h+fontsize+10]),draw.polygon(blank,(255,255,255),[(min(fontsize,mw),h+fontsize+10),(min(fontsize,max(mw-fontsize,0)),h+fontsize+30),(min(fontsize+30,mw),h+fontsize+10)])
        self.talkbox+=[[[transform.flip(blank,who.pos[0]+self.world['background'][1][0]>640,False),0,textbox],[who,0 if who.pos[0]+self.world['background'][1][0]<640 else -mw,max(who.rects[who.posen][1]-h-fontsize,-who.pos[1])],[time(),0.1,st]]]#[[板子,顯示的字數],[who,rel_x,rel_y],[判別time,個別字time,持續時間]]
    def Broadcast(self,text,color=(0,0,0),st=1,fontsize=30):
        board,textbox,w,h=transform.scale(terminal.white,(500,100)),[],0,0
        for i in text:
            if i!='\n':
                textbox+=[[(font_dict[fontsize] if fontsize in font_dict else font.Font(f'{work_dir}data/msjh.ttc',fontsize)).render(i,True,color),(w,h)]]
                w+=textbox[-1][0].get_rect()[2]+1
            if w>470 or i=='\n':
                w,h=0,h+fontsize
        self.broadcast+=[[[board,0,textbox],[time(),0.1,st]]]#[[板子,顯示的字數,textbox],[判別time,個別字time,持續時間]]
    def Add_follow(self,chr,speed=3):
        chr.room,chr.chroom,chr.follow_speed,chr.direct,chr.freeze=self.scenes_name,10+int(10*random()),speed,False,0
        self.followbox+=[chr]
    def people_action(self):
        t=time()
        self.is_busy=len(self.world['effect'])>0
        if 'warn' not in self.world:self.world['warn']=False
        for chr in self.world['object']:
            if terminal.teaching_mode and chr.name=='Eln':
                teaching(chr,self)
            if chr.name in People:
                if chr.live==1:
                    if chr.name not in ('girl','man1','kirito') or chr.eventing or not chr.pose_finish:self.is_busy = True
                    if chr.name=='girl':girl_event(self,chr)
                    if chr.name=='preservation' and self.scenes_name=='security_room' and chr.freeze==0:
                        def warn():
                            sleep(1)
                            preservation=self.search2('preservation')
                            if preservation!=None:
                                preservation.DoPose(3),self.Talk(preservation,'嘿!是什麼人，怎麼跑來這裡!')
                                terminal.sound['alarm'].play(),terminal.world.play_bgm('nervous')
                                self.alarm = True
                            else:
                                preservation=self.search('preservation')
                                if preservation!=None:preservation.freeze=0
                        chr.freeze=1
                        Thread(target=warn).start()
                    if chr.name in ['scientist','boss']:
                        if self.world['warn'] or self.shock[0]:
                            if chr.pose_finish and random()<0.8:
                                chr.DoPose(3*(chr.posen//3)+[1,2,1][chr.posen%3])
                                chr.Flip(self.role.pos[0]<chr.pos[0])
                            chr.block=False
                            for trigger in self.world['trigger']:
                                if trigger.function != None and trigger.function.__name__ == 'block' and rect_touch(trigger.rect,chr):
                                    chr.block=True
                            if not chr.block:chr.pos[0]+=3*(1 if chr.flip else -1)
                            if not 80<chr.pos[0]<self.world['background'][2][0]-80:
                                if chr.name=='scientist':
                                    for trigger in self.world['trigger']:
                                        if trigger.function!=None and trigger.function.__name__=='teleport' and trigger.key=='touch' and rect_touch(trigger.rect,chr):
                                            self.world['object'].remove(chr)
                                chr.pos[0]=min(self.world['background'][2][0]-80,max(80,chr.pos[0]))
                                if chr.tapfloor and random()<0.1:
                                    chr.speed[1]-=5
                            if random()<0.005:
                                terminal.sound['scream_'+['m1','m2','w1','w2','m3','m1','m2'][chr.posen//3]].play()
                                self.Talk(chr,['救命啊~~~','快開門----','我還想活啊!','啊--放我出去!','開門哪!','救救我!!!','嗚啊啊啊~~'][int(7*random())] if self.shock[0] else ['救命啊~~~','啊----','我還想活啊!','啊--饒命啊!','別過來!','警衛快來!!!','警衛!警衛!'][int(7*random())])
                        elif chr.name=='scientist':
                            try:
                                if chr.is_working:
                                    for i in [chr.GetLimb('left_sh'),chr.GetLimb('right_sh')]:
                                        if i!=None:
                                            i.angle+=i.amplitude[1]
                                            i.amplitude[0]-=0.5
                                            if i.amplitude[0]<1:
                                                i.amplitude[0]=20
                                                i.amplitude[1]*=-1
                            except:
                                chr.is_working=True
                                for i in range(2):
                                    [chr.GetLimb('left_sh'), chr.GetLimb('right_sh')][i].amplitude=[20,[-0.3,0.3][i]]
                            if not self.alarm and random() < 0.0002:
                                self.Talk(chr,['奇怪，怎麼有受試者進來?','這是誰的實驗者?','快回去，等等警察要來抓你','誰把受實驗者放出來?','嗯...','警衛在哪?快把人抓回去','這個要怎麼辦呢...'][int(7*random())])
                    if chr.name == 'aircraft':
                        if abs(chr.pos[0]-self.role.pos[0])<2000:
                            if chr.state!=1:chr.state=1
                            if chr.tem_cold<0:chr.tem_cold+=1
                            elif chr.tem_cold==0:
                                chr.ny,chr.nr=self.role.pos[1] - 250 + int(200 * random()),1000
                                chr.tem_cold+=1
                            elif chr.tem_cold<1200:
                                chr.tem_cold+=1
                                chr.Flip(self.role.pos[0]>chr.pos[0])
                                if abs(chr.ny - chr.pos[1]) > 10: chr.pos[1] +=0.5 if chr.ny > chr.pos[1] else -0.5
                                elif chr.tem_cold>50 and chr.nr==1000:
                                    x,y=self.role.pos[0]-chr.pos[0],self.role.pos[1]-chr.pos[1]
                                    chr.nr,chr.shot=atan(y/abs(x))/pi*180,atan(y/x)
                                    if abs(chr.pos[0]-self.role.pos[0])<800:terminal.sound['aircraft'].play()
                                elif chr.tem_cold>180 and abs(chr.pos[0]-self.role.pos[0])<800:
                                    if chr.value == 0:
                                        chr.DoPose(1)
                                        chr.rotate=chr.role.rotate=chr.nr
                                        chr.tem_cold = time() + 1
                                    elif chr.value==2:
                                        if chr.posen!=2:
                                            def paint_front():
                                                if chr.live==1:
                                                    for i in range(3):
                                                        draw.circle(screen,(255,255,0),(big_aircraft.pos[0]+self.world['background'][1][0]+40*(1 if big_aircraft.flip else -1),big_aircraft.pos[1]+self.world['background'][1][1]),100-int((big_aircraft.tem_cold-i*30)%100),5)
                                            chr.DoPose(2)
                                            self.paint_front,big_aircraft=paint_front,chr
                                        elif chr.tem_cold>800:chr.tem_cold = time()
                                if abs(chr.pos[0]-self.role.pos[0])>200:
                                    chr.pos[0]+=(0.1 if self.role.pos[0]>chr.pos[0] else -0.1)*(1 if abs(chr.pos[0]-self.role.pos[0])<500 else 8)
                            elif chr.tem_cold<time():
                                chr.tem_cold=0
                                if abs(chr.pos[0]-self.role.pos[0])<1500 and chr.pose_finish:
                                    if chr.posen==1:
                                        chr.tem_cold=-200
                                        terminal.sound['laser'].play()
                                        self.bullet += [[bullet_dictory[chr.name]['bullet'], [
                                            chr.pos[0]+bullet_dictory[chr.name]['shot_pos2'][0] * (1 if chr.flip else -1),chr.pos[1], bullet_dictory[chr.name]['size'][0], bullet_dictory[chr.name]['size'][1]],
                                                         [bullet_dictory[chr.name]['speed'] * (1 if chr.flip else -1)*abs(cos(chr.shot)),bullet_dictory[chr.name]['speed']* (1 if chr.flip else -1)*sin(chr.shot), 0],
                                                         [not chr.flip,-chr.shot/pi*180, False,1]]]
                                    elif chr.posen==2:
                                        chr.tem_cold,self.paint_front=-600,self.void
                                        terminal.sound['laser2'].play()
                                        rect=[chr.pos[0]+(20 if chr.flip else -2500),chr.pos[1]-40,2480,80]
                                        self.world['effect']+=[['laser',0,-1,1,rect+[{'flip':not chr.flip}],1,1,0]]   #名稱,初始,結尾(-1:最後),增量,rect[x,y,w,h,rotate,flip],播放次數(-1:無限),前後(0:後,1:前),計算禎
                                        if rect_touch(rect,self.role):
                                            self.role.live, self.role.speed, self.role.control = 0.5, [8 if self.role.pos[0]>chr.pos[0] else -8, -5,0], False
                                            self.role.rects[self.role.posen][3] -= 120
                                chr.DoPose(0)
                elif chr.live=='blood':
                    if not self.world['warn']:self.world['warn']=True
                    if chr.tapfloor:
                        try:
                            self.nowbg.blit(transform.scale(terminal.image['bld4'],(abs(chr.rects[chr.posen][2]-chr.rects[chr.posen][0]),abs(chr.rects[chr.posen][3]-chr.rects[chr.posen][1]))),(chr.pos[0]+chr.rects[chr.posen][0],chr.pos[1]+chr.rects[chr.posen][1]))
                        except:pass
                        chr.live, chr.state = 0, 1
                elif chr.live==0.8:
                    chr.role.rotate+=2 if self.role.pos[0]>chr.pos[0] else -2
                    chr.pos[1]+=1
                    if abs(chr.role.rotate)>90:
                        chr.live=0.1
                elif chr.live==0.1 and abs(chr.role.rotate)!=0 and chr.tapfloor:
                    if abs(chr.rotate) != 90: self.nowbg.blit(transform.scale(terminal.image['bld7'], (300, 100)),(chr.pos[0] - 130, chr.pos[1] + 120))
                    chr.rotate = chr.role.rotate = int(90*abs(chr.role.rotate)/chr.role.rotate)
                    #chr.rects[chr.posen][3]+=120
                    if chr.speed[0]==0:
                        chr.live,chr.state=0,1
                        self.guide2_count(chr, 'died')
                        if not self.world['warn']:self.world['warn']=True
                        if chr.name in self.police and not self.alarm:
                            terminal.sound['alarm'].play(),terminal.world.play_bgm('nervous')
                            self.alarm=True
            if chr.name=='hyena' and chr.live==1:
                if chr.pose_finish:
                    if chr.value==0 or (random()<0.3 and type(chr.value)!=str):#尋找目標
                        minx=900
                        for obj in self.world['object']+[self.role]:
                            if obj.name in Meat and not obj.hide:
                                if abs(chr.pos[0]-obj.pos[0])<minx:
                                    chr.value,minx=obj.pos,abs(chr.pos[0]-obj.pos[0])
                        if chr.value==0:chr.value=-5
                        elif not self.busy and type(chr.value)==list:self.busy=True
                    if type(chr.value)==int and chr.value<0:
                        chr.value+=1
                        chr.DoPose(1)
                        if self.busy:self.busy=False
                    else:  #有目標
                        if chr.value=='eat': #吃東西中
                            food=chr.Throw(fix_item_pos=True)
                            if food!=None:
                                if food.value<1:
                                    chr.Throw()
                                    self.nowbg.blit(transform.scale(terminal.image['bld4'], (abs(food.rects[food.posen][2] - food.rects[food.posen][0]),
                                    abs(int(food.rects[food.posen][3] - food.rects[food.posen][1])))), (food.pos[0] + food.rects[food.posen][0],food.pos[1] + food.rects[food.posen][1]))
                                    chr.value=0
                                else:
                                    if food.value%4==0:terminal.sound['chew'].play()
                                    chr.DoPose(f'eat{1+food.value%2}')
                                    food.value-=1
                        elif type(chr.value)==list:              #捕獵
                            chr.direct = chr.pos[0] > chr.value[0]
                            if chr.direct != chr.flip: chr.Flip()
                            if abs(chr.pos[0] - chr.value[0]) < 400 and chr.tapfloor and chr.pos[1]>chr.value[1]:
                                chr.DoPose('jump')
                                chr.speed[0]+=min((-1 if chr.flip else 1)*abs(chr.pos[0] - chr.value[0])/50,5)*terminal.zoom
                                chr.speed[1]=-5*terminal.zoom
                            elif chr.tapfloor:
                                chr.posen = [3,2,3,2,3,2,3,2,3,2,3,2,3,2][chr.posen]
                                chr.DoPose(chr.posen)
                                if abs(chr.pos[0] - chr.value[0]) > 400:terminal.sound['barking'].play()
                            elif chr.value[0]<-500:chr.value=0
                elif type(chr.value)==list and abs(chr.pos[0] - chr.value[0]) < 50:
                    for target in self.world['object']+[self.role]:
                        if target.name in Meat and not target.hide and chr.touch(target):
                            if target.live==1:
                                target.rects[target.posen][3] -= 100 * terminal.zoom
                                target.live=0.5
                                chr.DoPose(0)
                                if target.id == 'scientist':target.DoPose(18 + chr.posen // 3)
                                target.speed, target.state=[(-1 if chr.flip else 1) * terminal.zoom, -1, 0], 0
                                chr.speed[0]/=4.5
                            target.control=False
                            cut_order = random_order(['left_sh', 'left_arm', 'left_leg',  'right_sh', 'right_arm', 'right_leg'])
                            terminal.sound['chop'].play(), chr.DoPose('normal')
                            for cut_part in ['breast1','right_sh']+cut_order + ['head','body', '']:
                                k = Split_Character(target, cut_part)
                                if k != None:
                                    if target.live == 1 and target.name=='scientist':
                                        self.Talk(target, ['啊~~~', '救命啊!', '厄啊~'][int(3 * random())]),terminal.sound['scream_w2'].play(),target.Flip(chr.flip)
                                    target.live, k.value, k.live = 0.5, 12/terminal.zoom + size_level(k)+3, 'blood'
                                    k.parent.surfbox[k.parent.surfn][0].blit(
                                        transform.scale(terminal.image['bld1'], (100, 100)), (-30, 20))
                                    k.role.mainlimb[0].surfbox[k.role.mainlimb[0].surfn][0].blit(
                                        transform.scale(terminal.image['bld1'], (50, 50)), (-10, -10))
                                    # k.rects[k.posen][3]-=100
                                    chr.Insert('mouth', k, visible=True)
                                    break
                            if chr.Throw(fix_item_pos=True) == None:
                                target.value = 5 + size_level(target)
                                chr.Insert('mouth', target, visible=True)
                                if target in self.world['object']:self.world['object'].remove(target)
                            chr.speed[1] = -2*terminal.zoom
                            chr.speed[0]/=10
                            chr.value = 'eat'
                            break
                elif chr.posen==4 and chr.tapfloor:chr.DoPose('normal')
                if chr.posen in [2,3]:
                    chr.pos[0] += (-5 if chr.direct else 5)*terminal.zoom
        if self.role.live==0.5:
            self.role.role.rotate -= self.role.speed[0]
            if self.role.speed[0]<0.02:self.role.speed[0]=1
            if abs(self.role.role.rotate) > 90:self.role.live = 0.1
        elif self.role.live == 0.1 and abs(self.role.role.rotate) != 0 and self.role.tapfloor:
            if abs(self.role.rotate) != 90: self.nowbg.blit(transform.scale(terminal.image['bld7'], (300, 100)),(self.role.pos[0] - 130, self.role.pos[1] + 120))
            self.role.rotate = self.role.role.rotate = int(90 * abs(self.role.role.rotate) / self.role.role.rotate)
            # chr.rects[chr.posen][3]+=120
            if self.role.speed[0] == 0:self.role.live, self.role.state = 0, 1
        if self.role.control:
            for chr in self.followbox:              #-----------------------------------------------------follow
                if chr.room == self.scenes_name:
                    if chr.pose_finish and chr.tapfloor:
                        if (len(self.talkbox)==0 or self.alarm) and not chr.eventing:
                            chr.direct = chr.pos[0] > self.role.pos[0]
                            chr.Flip(chr.direct if chr.name=='man1' else  (not chr.direct))
                            if chr.freeze == 0:
                                if abs(chr.pos[0] - self.role.pos[0]) < (280 if chr.name=='girl' or len(self.followbox)<2 else 400):
                                    if chr.posen!=0:chr.DoPose(0)
                                else:
                                    chr.DoPose([1,2][chr.posen%2])
                            elif chr.freeze=='talk' and len(self.talkbox)==0:chr.freeze=0
                    elif chr.posen in [1, 2] and not chr.eventing:
                        self.is_busy = True
                        chr.pos[0] += (-chr.follow_speed if chr.pos[0]>self.role.pos[0] else chr.follow_speed)*(2 if abs(chr.pos[0] - self.role.pos[0])>400 else 1)
                elif chr.chroom > 0:chr.chroom -= 1
                else:
                    chr.chroom= 50 + int(20 * random())
                    if chr.room != None and chr in self.map[chr.room]['object']: self.map[chr.room]['object'].remove(chr)
                    chr.room,chr.freeze= self.scenes_name,0
                    self.world['object'] += [chr]
                if self.scenes_name in ('staircase','treasure','c_staircase') and self.role.pos[1]<chr.pos[1]-120 and chr.tapfloor and not chr.eventing:
                    chr.speed[1]-=6
                    chr.DoPose(1)
                if self.role.pos[1]>chr.pos[1] + 120 and abs(chr.pos[0] - self.role.pos[0])<150:chr.pos[1]+=5
                if chr.name=='man1':
                    man1_action(chr,self)
        if self.alarm:
            self.is_busy = True
            for chr in self.world['object']:
                if chr.name in ['mpolice','wpolice','specialforce'] and chr not in self.policebox and chr.live==1:
                    if chr.Throw(fix_item_pos=True)==None:
                        for part in Game_setting['police'][chr.name]['insert']:
                            chr.GetLimb(part).bring_f += [command_to_character(Game_setting['police'][chr.name]['insert'][part])]
                            chr.GetLimb(part).bring_f[-1].pos[0] =  -1000
                    chr.action,chr.room,chr.direct, chr.chroom= 3,self.scenes_name, chr.pos[0] > self.role.pos[0],120+int(20*random())
                    if chr.direct != chr.flip: chr.Flip()
                    chr.bullet_cd=bullet_dictory[chr.Throw(fix_item_pos=True).name]['cold']*2
                    chr.DoPose(['normal', 'run1', 'run2', 'shot'][chr.action])
                    self.policebox+=[chr]
            if len(self.policebox) < self.max_enemy and random() < 0.5 and (self.police['specialforce']>0 or self.police['specialforce2']>0):
                pos,police_name=search_min_map_entrance(self.scenes_name),(('mpolice' if self.police['mpolice']>0 else 'specialforce') if random()<0.5 else ('wpolice' if self.police['wpolice']>0 else 'specialforce2'))
                self.police[police_name]-=1
                police, police.action, police.room, police.direct,police.chroom= command_to_character([police_name.replace('2',''),Game_setting['police'][police_name]['size'], (pos[0] - 100 + int(200 * random()),pos[1] - 50), 0,{'insert':Game_setting['police'][police_name]['insert']}]), 1 + int(2 * random()), None, pos[0] > self.role.pos[0],self.police_comespeed+int(self.police_comespeed*random()/2)
                police.bullet_cd=bullet_dictory[police.Throw(fix_item_pos=True).name]['cold']*2
                police.DoPose(['normal', 'run1', 'run2', 'shot'][police.action])
                self.policebox += [police]
            for chr in self.policebox:
                if chr.live != 1:
                    self.policebox.remove(chr)
                else:
                    chr.bullet_cd-=1
                    if chr.room == self.scenes_name:
                        chr.direct = chr.pos[0] > self.role.pos[0]
                        if chr.direct != chr.flip: chr.Flip()
                        if chr.pose_finish:
                            girl=self.search2('girl')
                            if (abs(chr.pos[0] - self.role.pos[0]) < 1000 or (girl!=None and abs(chr.pos[0] - girl.pos[0]) < 1000)) and (random()<0.99 or chr.action not in [1, 2]):
                                chr.action = 3
                                if chr.bullet_cd<1:
                                    gun=chr.Throw(fix_item_pos=True)
                                    if gun!=None and gun.name!='shield':
                                        if gun.pos[1]>self.role.pos[1]+self.role.rects[self.role.posen][3] and self.role.live==1:
                                            if chr.speed[1]>=0 and chr.tapfloor:
                                                chr.speed[1]=-5
                                        elif gun.pos[1]<self.role.pos[1]+self.role.rects[self.role.posen][1] and self.role.live==1:
                                            if chr.tapfloor and chr.name!='specalforce':
                                                chr.pos[1]+=6
                                        else:
                                            terminal.sound['shot'].play()
                                            chr.bullet_cd=bullet_dictory[gun.name]['cold']
                                            self.bullet += [[bullet_dictory[gun.name]['bullet'], [gun.pos[0] + bullet_dictory[gun.name]['shot_pos2'][0] * (-1 if gun.flip else 1),gun.pos[1],bullet_dictory[gun.name]['size'][0], bullet_dictory[gun.name]['size'][1]],[bullet_dictory[gun.name]['speed'] * (-1 if gun.flip else 1), 0,0], [gun.flip, 0, False, 1]]]
                                            chr.DoPose(['normal', 'run1', 'run2', 'shot'][chr.action])
                            else:
                                if t>terminal.tem_cold:
                                    terminal.sound['run'].play()
                                    terminal.tem_cold=t+4
                                chr.action = [1, 2, 1, 2][chr.action]
                                chr.DoPose(['normal', 'run1', 'run2', 'shot'][chr.action])
                        if chr.action in [1, 2]: chr.pos[0] += -5 if chr.direct else 5
                    elif chr.chroom>0:chr.chroom-=1
                    else:
                        chr.chroom,chr.pos=self.police_comespeed+int(self.police_comespeed*random()/2),search_min_map_entrance(self.scenes_name)
                        if chr.room!=None and chr in self.map[chr.room]['object']:self.map[chr.room]['object'].remove(chr)
                        chr.room=self.scenes_name
                        self.world['object']+=[chr]
    def display(self,update=True):
        if self.clearance:return
        t = time()
        for obj in self.world['object']+[self.role]:
            if obj.name in self.fall_sound:
                if t>self.fall_sound[obj.name][1] and self.fall_sound[obj.name][1]!=0 and obj.tapfloor and not self.fall_sound[obj.name][0]:
                    if obj.name in ['potion','testtube']:terminal.sound['grass fall'].play()
                    else:terminal.sound['fall2'].play()
                if obj.tapfloor!=self.fall_sound[obj.name][0]:
                    self.fall_sound[obj.name][1] = t + 0.5
                    self.fall_sound[obj.name][0]=obj.tapfloor
        if self.shock[0] and t > self.shock[1]:
            self.is_busy=True
            if self.shock[6] < 1:
                self.shock[1] = t + self.shock[4]
                self.shock[6] = self.shock[2]
                self.shock[3] -= 1
                if self.shock[3] == 0: self.shock[0] = 0
            self.shock[6] -= 1
            self.world['background'][1][0] += [-5, 10, -10, 5][self.shock[5] % 4]
            self.world['background'][1][1] += [-5, 10, -10, 5][self.shock[5] % 4]
            self.shock[5] += 1
        self.people_action()
        def effect_render(i,show=True):
            if show:
                img=transform.scale(terminal.effect[i[0]][int(i[7])],i[4][2:4])
                if len(i[4])==5:
                    if 'flip' in i[4][4]:img=transform.flip(img,i[4][4]['flip'],False)
                    if 'rotate' in i[4][4]:img=transform.rotate(img,i[4][4]['rotate'])
                    if 'alpha' in i[4][4]: img.set_alpha(i[4][4]['alpha'])
                screen.blit(img,(i[4][0]+self.world['background'][1][0],i[4][1]+self.world['background'][1][1]))
            i[7]+=i[3]
            if (i[7]>i[2] and i[2]!=-1) or i[7]>=len(terminal.effect[i[0]]):
                i[5]-=1
                if i[5]==0:
                    terminal.world.world['effect'].remove(i)
                    if len(i[4])==5 and 'stamp' in i[4][4] and show:self.nowbg.blit(img,(i[4][0],i[4][1]))
                else:i[7]=i[1]
        def bullet_effect(self,i,shot=False):
            if i[0] == 'bullet3':
                self.world['effect'] += [['boom', 0, -1, 0.3, [i[1][0] - 50, i[1][1] - 50, 100, 100], 1, 1, 0]]
                if i in self.bullet:self.bullet.remove(i)
                terminal.sound['small boom'].play()
            elif i[0] in ('bullet5','bullet6'):
                self.world['effect'] += [['fancy boom', 0, -1,6, [i[1][0] - 640, i[1][1] - 360, 1280, 720], 1, 1, 0]]
                explosion(None, i[1], target=People[1:] + ['specialforce']+(['player'] if i[0]=='bullet6' else []))
                if i in self.bullet: self.bullet.remove(i)
                terminal.sound['boom'].play()
            elif i[0]=='bullet7':
                if i in self.bullet: self.bullet.remove(i)
            elif not shot:i[2], i[3][2] = [-i[2][0] / (3 + random() * 2), -abs(i[2][0] / 3) - random() * 3, i[2][0] / 2], True
        #---------------------------------------------
        #screen.blit(self.nowbg,(0,0),[-self.world['background'][1][0],-self.world['background'][1][1],1280,720])
        if self.eventrole!=None:self.pickupevent(self.eventrole)
        if self.useitem!=None:self.Useevent(self.useitem)
        if (self.world['background'][1][1]+self.role.pos[1]>500 or self.world['background'][1][1]+self.role.pos[1]<300) and self.modify_y[0]<20:
            self.modify_y=[self.modify_speed,(max(-self.world['background'][2][1]+720,min(-self.role.pos[1]+400,0))-self.world['background'][1][1])/self.modify_speed]
        if self.modify_y[0]>0:
            self.world['background'][1][1]+=self.modify_y[1]
            self.modify_y[0]-=1
        if self.fps_skip==0:
            screen.blit(self.nowbg,self.world['background'][1]),screen.blit(transform.scale(terminal.image['pause'],(40,40)),(1220,20))
        if len(self.fragments)>0:                                           #------------------------------------------------------------------碎片
            self.busy=True
            for i in self.fragments:
                i.speed[1]+=0.1
                if i.effect>=0:
                    screen.blit(transform.rotate(transform.scale(terminal.image['bld9'],(int(i.w),int(i.h))),i.angle),(i.p[0]+self.world['background'][1][0],i.p[1]+self.world['background'][1][1]))
                i.show(self.world['background'][1])
                if (i.p[1]>self.world['floor']-100 and random()<0.05 and i.speed[1]>0) or i.p[1]>self.world['floor']+10:
                    i.show((0,0),surf=self.nowbg)
                    if i.effect>=0:self.nowbg.blit(transform.rotate(transform.scale(terminal.image['bld9'],(int(i.w),int(i.h))),i.angle),i.p),self.nowbg.blit(transform.rotate(transform.scale(terminal.image['bld4'],(int(i.w*3),int(i.h*3))),i.angle),(i.p[0]-i.w,i.p[1]-i.h))
                    self.fragments.remove(i)
            if len(self.fragments)==0: self.busy=False
        if self.fps_skip == 0:
            for i in self.world['trigger']:
                i.Show(self.world['background'][1])
                if i.Detect():break
            for i in self.world['back']: screen.blit(i[0], (self.world['background'][1][0] + i[1][0], self.world['background'][1][1] + i[1][1]))
        for i in self.world['effect']:
            if i[6]==0:effect_render(i,show=self.fps_skip == 0)
        self.paint_back()
        for i in self.world['object']+[self.role]:                                  #-----------------------------------------------------------------------chr.Show
            #if i.name=='gun':print(i.hide,i.fix,i.visible)
            if not i.hide and not i.fix and i.visible:
                try:i.Show((i.pos[0]+self.world['background'][1][0],i.pos[1]+self.world['background'][1][1]),runpose=((i!=self.role and not i.hide) or not self.using_phone))
                except:
                    print(i.pos,self.world['background'])
                    i.Show((i.pos[0] + self.world['background'][1][0], i.pos[1] + self.world['background'][1][1]),
                           runpose=((i != self.role and not i.hide) or not self.using_phone))
        if self.fps_skip == 0:
            for i in self.world['front']:screen.blit(i[0],(self.world['background'][1][0]+i[1][0],self.world['background'][1][1]+i[1][1]))
            if self.modify_scenery:
                for i in self.modify_scenes:screen.blit(i[0], (self.world['background'][1][0] + i[1][0], self.world['background'][1][1] + i[1][1]))
        for i in self.bullet:                                                   #----------------------------------------------------------------------------Bullet
            screen.blit(transform.rotate(transform.flip(transform.scale(terminal.image[i[0]],i[1][2:]),i[3][0],False),i[3][1]),(i[1][0]+self.world['background'][1][0],i[1][1]+self.world['background'][1][1]))
            i[1][0]+=i[2][0]
            i[1][1]+=i[2][1]
            i[3][1]+=i[2][2]
            if i[3][2]:#
                i[2][1]+=0.1
            if i[1][1]+i[1][3]>self.world['floor']:
                if i[0]=='bullet6':bullet_effect(self, i)
                elif i[0]!='bullet7':self.nowbg.blit(transform.rotate(transform.flip(transform.scale(terminal.image[i[0]],i[1][2:]),i[3][0],False),i[3][1]),i[1])
            if (not (0<i[1][0]<self.world['background'][2][0]+300 and -200<i[1][1]<self.world['background'][2][1])) or i[1][1]>self.world['floor']:
                if i in self.bullet:self.bullet.remove(i)
                continue
            if i[3][3]==0:
                for trigger in self.world['trigger']:
                    if trigger.function!=None and trigger.function.__name__=='block' and rect_touch2(trigger.rect,i[1]) and abs(i[2][0])>1:
                        bullet_effect(self, i)
            if i[3][3]==2:
                i[3][3]=-1
                bullet_effect(self, i)
            for chr in self.world['object']:
                if rect_touch(i[1],chr) and ((i[3][3]==0 and chr.name in ('specialforce','aircraft')) or (i[3][3]==1 and chr.name in ('shield','man1'))) and not i[3][2]:
#                if ((i[3][3]==0 and chr.name in ('specialforce','aircraft')) or (chr.name=='shield' and chr.visible and i[0]!='bullet5')) and  and not i[3][2] and (not chr.hide or chr.name=='shield'):
                    if chr.name=='aircraft' and not i[3][2]:
                        chr.pos[0]+=i[2][0]
                        chr.pos[1]+=i[2][1]
                        chr.blood+=1
                        if chr.blood>9:
                            explosion(None,[chr.pos[0]-10,chr.pos[1]-10,20,20], target=Cuttable_obj, blood=False, power=2, effect=None,fragments=0, sound='fragmentation')
                    bullet_effect(self,i)
                    terminal.sound['shield'].play()
                if (i[3][3]==0 or (i[3][3]==1 and chr.name=='girl')) and chr.live==1 and chr.id in People and rect_touch(i[1],chr):
                    if chr.name in ('specialforce','aircraft') and i[0]!='bullet5':
                        continue
                    if chr.name in ('mpolice','wpolice'):
                        chr.freeze+=1
                        if chr.freeze<2:
                            if i in self.bullet:self.bullet.remove(i)
                            bullet_effect(self, i, shot=True)
                            continue
                    if chr.name=='girl':
                        if i[3][3]==1 and chr.state==0:
                            if i[0] == 'bullet7': continue
                            chr.jump_warn[3]+=1
                            if chr.jump_warn[3]<30:
                                self.world['effect'] += [[f'blood_splash{1 + int(2 * random())}', 0, -1, 0.3,[i[1][0] - 50, i[1][1] - 25, 100, 47], 1, 1, 0]]
                                b = chr.GetLimb('head' if i[0] == 'bullet1' and random()<0.5 else 'body')
                                alpha_blit(b.surfbox[b.surfn][0],transform.scale(terminal.image['bld1'], (80,50)), (0 if i[0] == 'bullet1' else 10,int(40*random())),(20,-20,-20))
                                terminal.world.world['effect'] += [['blood_drip', 0,-1,0.2,[chr.pos[0] - 30,chr.pos[1]+chr.rects[chr.posen][3]-20,65,21,{'stamp':True}],1,0,0]]
                                if i in self.bullet:self.bullet.remove(i),bullet_effect(self, i, shot=True)
                                continue
                            elif chr in self.followbox:
                                self.Talk(chr,'我不行了')
                                self.followbox.remove(chr)
                        else:continue
                    if chr.name in Game_setting['police'] and not self.alarm:
                        terminal.sound['alarm'].play(),terminal.world.play_bgm('nervous')
                        self.alarm = True
                    chr.live,chr.speed=0.8,[i[2][0]/5,-5,0]
                    if chr.id=='scientist':chr.DoPose(18+chr.posen//3)
                    for rect in chr.rects:rect[3]-=120
                    self.world['effect'] += [[f'blood_splash{1 + int(2 * random())}', 0, -1, 0.3,[i[1][0] - 50, i[1][1] - 25, 100,47], 1, 1,0]]
                    b=chr.GetLimb('body')
                    if b!=None:b.surfbox[b.surfn][0].blit(transform.scale(terminal.image['bld1'],(80,50)),(-20,20))
                    if i in self.bullet:self.bullet.remove(i),chr.Throw(),chr.Throw()
                    bullet_effect(self,i,shot=True)
                    terminal.sound['hitted'].play()
                    break
            if i[3][3] == 1 and self.role.live == 1 and rect_touch(i[1],self.role) and not terminal.player_setting['invincible']:
                self.world['effect'] += [[f'blood_splash{1 + int(2 * random())}', 0, -1, 0.3, [i[1][0] - 50, i[1][1] - 25, 100, 47], 1, 1,0]]
                self.role.freeze+=1
                if self.role.freeze<5:
                    self.world['effect'] += [[f'blood_splash{1 + int(2 * random())}', 0, -1, 0.3, [i[1][0] - 50, i[1][1] - 25, 100, 47], 1,1, 0]]
                    b = self.role.GetLimb('head' if i[0] == 'bullet1' else 'body')
                    alpha_blit(b.surfbox[b.surfn][0], transform.scale(terminal.image['bld1'], (80, 50)),(0 if i[0] == 'bullet1' else 10, int(40 * random())), (40, -40, -40))
                    terminal.world.world['effect'] += [['blood_drip', 0, -1, 0.2, [self.role.pos[0] - 30,self.role.pos[1] + self.role.rects[self.role.posen][3] - 20, 65,21, {'stamp': True}], 1, 0, 0]]
                    if i in self.bullet:self.bullet.remove(i)
                    bullet_effect(self, i, shot=True)
                    continue
                self.role.live,self.role.speed,self.role.control= 0.5, [i[2][0] / 5, -5, 0],False
                self.role.rects[self.role.posen][3] -= 120
                b = self.role.GetLimb('body')
                b.surfbox[b.surfn][0].blit(transform.scale(terminal.image['bld1'], (80, 50)), (-20, 20))
                if i in self.bullet:self.bullet.remove(i)
                bullet_effect(self, i)
                terminal.sound['hitted'].play()
        for i in terminal.world.world['effect']:
            if i[6]==1:effect_render(i,show=self.fps_skip == 0)
        self.paint_front()
        if self.needlight:screen.blit(self.black,(0,0))
        for i in range(len(self.events_box)):
            if i<len(self.events_box):
                if self.fps_skip == 0:text_render(screen,self.events_box[i][0]+'  '+str(render_time(self.events_box[i][2]-t+1)),30,self.events_box[i][1],(10,105+40*i))
                if t>self.events_box[i][2]:
                    function=self.events_box[i][3]
                    del self.events_box[i]
                    function()
        if len(self.broadcast)>0:
            textbox,self.is_busy=self.broadcast[0],True
            screen.blit(textbox[0][0],(390,70))
            if textbox[0][1] < len(textbox[0][2]):
                if t > textbox[1][0]:
                    textbox[0][0].blit(textbox[0][2][textbox[0][1]][0], textbox[0][2][textbox[0][1]][1])
                    textbox[0][1] += 1
                    textbox[1][0] = t + textbox[1][1]
                if textbox[0][1] >= len(textbox[0][2]): textbox[1][0] = t + textbox[1][2]
            elif t > textbox[1][0]:
                del self.broadcast[0]
        if self.fps_skip == 0:
            if self.selecting:
                for i in self.selectbox: screen.blit(i[0],i[1])
            if terminal.operate_mode==1:
                if self.direct_btn_tap!=None:screen.blit(self.else_btn[-1],(self.direct_btn_tap[0]-50,self.direct_btn_tap[1]-50))
                screen.blit(self.direct_btn,(20,485)),screen.blit(self.itemlist_surf,(245,665))
                for i in range(len(self.else_btn)-1):
                    if self.else_btn_tap[i]:screen.blit(self.else_btn[-1],[(1000,600),(1120,600),(1170,480)][i])
                    screen.blit(self.else_btn[i],[(1000,600),(1120,600),(1170,480)][i])
            else:screen.blit(self.itemlist_surf,(5,665))
        for textbox in self.talkbox:
            if self.fps_skip == 0:screen.blit(textbox[0][0],(max(textbox[1][0].pos[0]+textbox[1][1]+self.world['background'][1][0],5),textbox[1][0].pos[1]+textbox[1][2]+self.world['background'][1][1]))
            if textbox[0][1]<len(textbox[0][2]):
                if t>textbox[2][0]:
                    textbox[0][0].blit(textbox[0][2][textbox[0][1]][0],textbox[0][2][textbox[0][1]][1])
                    textbox[0][1]+=1
                    textbox[2][0]=t+textbox[2][1]
                if textbox[0][1]>=len(textbox[0][2]):textbox[2][0]=t+textbox[2][2]
            elif t>textbox[2][0]:self.talkbox.remove(textbox)
        if update:
     #       if self.fps_skip==0:
            self.clock.tick(self.fps)
            display.update()
 #           self.fps.update()
 #               display.update()
         #   if time()-t>0.06 and len(self.fragments)>0:
          #      self.fps_skip+=3
    #        else:self.fps_skip-=1
def rungame(game_progress,blackeffect=True):
    def change_item(k):
        world.itemlist[world.itemlist_k] = role.Throw(fix_item_pos=True)
        if world.itemlist[world.itemlist_k] != None: world.itemlist[world.itemlist_k].hide = 1
        world.itemlist_k = k
        if world.itemlist[world.itemlist_k] != None: world.itemlist[world.itemlist_k].hide = True
        for i in range(len(world.itemlist)):
            draw.rect(world.itemlist_surf, (230, 230, 0) if i == world.itemlist_k else (140, 140, 140),[50 * i, 0, 50, 50], 2)
    def noitem_render():
        world.itemlist[world.itemlist_k] = None
        draw.rect(world.itemlist_surf, (0,0,0), [50 * world.itemlist_k, 0, 50, 50])
        draw.rect(world.itemlist_surf,(230, 230,230),[50 * world.itemlist_k,0, 50, 50], 2)
    world=terminal.world
    role=terminal.world.role
    #----遊戲變數------------------------------------------------------------------------
    pose = 0
    speed=6
    fall=False
    getupk=0
    inspect_time=0
    tempos=[(0,0),0]
    abc = 1
    #-----------------------------------------------------------------------------------
    black = Surface(screen.get_rect()[2:])
    #role.pos=[1020,430]
    if not game_progress['wake_up']:
        role.pos,role.state,role.role.rotate,cd=[320,430],1,-10,0
        role.role.loadpose(13,1000)
    if blackeffect:
        for i in range(255):
            wait_tap()
            world.display(False)
            black.set_alpha(255 - i)
            screen.blit(black, (0, 0))
            display.update()
    if not game_progress['wake_up']:
        sleep(1)
        while cd==0:
            for event2 in event.get():
                if event2.type in [QUIT,MOUSEBUTTONDOWN,KEYDOWN]:cd=1
            sleep(0.1)
        role.DoAction('wakeup')
        while not role.pose_finish:
            sleep(0)
            world.display()
        role.state,role.role.rotate=0,0
        world.display()
    role.control=True
    deadcd=[True,0]
    change_itemcd=0
    pressmouse=False
    operate_mode_cd=0
    next_jump=0
    keys={K_RIGHT:0,K_LEFT:0,K_UP:0,K_DOWN:0,K_z:0,K_x:0,K_a:0,K_s:0,K_p:0,K_SPACE:0}
    while abc == 1:
        if not game_progress['wake_up']:
            if role.tapfloor:
                world.loading_story('player', 1)
                if yesno('要進入新手教學嗎?'): teaching(0, world)
                game_progress['wake_up']=True
        if terminal.end_game:return False
        for event2 in event.get():
            if event2.type == QUIT and yesno('確定要關閉遊戲嗎','遊戲進度會自動保存'):
                return False
            if event2.type == MOUSEBUTTONDOWN:                                                     #滑鼠點擊
                x,y = mouse.get_pos()
                pressmouse=True
                for i in range(len(world.itemlist)):
                    if 0<x-50*i-[5,245][terminal.operate_mode]<50 and 665<y<715:change_item(i)
                if 1220<x<1260 and 20<y<60:
                    get=game_pause()
                    if get==False :return False
                    elif get=='back menu':return get
                    elif get=='continue':world.display()
                    world=terminal.world
                    role=world.role
                if world.selecting:
                    for i in world.selectbox:
                        if 0<x-i[1][0]<373 and 0<y-i[1][1]<57:
                            world.select,world.selecting,world.useitem=i[2],False,None
                #print(x,y)
        t=time()
        if terminal.operate_mode==1:
            if t>operate_mode_cd:
                keys,operate_mode_cd= {K_RIGHT: 0, K_LEFT: 0, K_UP: 0, K_DOWN: 0, K_z: 0, K_x: 0, K_a: 0, K_s: 0, K_p: 0, K_SPACE: 0},t+0.3
            m,mpos=mouse.get_pressed(),mouse.get_pos()
            if m[0] or pressmouse:
                if 20<mpos[0]<250 and 485<mpos[1]<715:
                    world.direct_btn_tap=mpos
                    if mpos[0]>180:keys[K_RIGHT]=1
                    elif mpos[0]<90:keys[K_LEFT]=1
                    if mpos[1]<555:keys[K_UP]=1
                    elif mpos[1]>645:keys[K_DOWN]=1
                elif world.direct_btn_tap!=None:world.direct_btn_tap=None
                for i in range(len(world.else_btn)-1):
                    if 0<mpos[0]-[1000,1120,1170][i]<100 and 0<mpos[1]-[600,600,480][i]<100:world.else_btn_tap[i],keys[[K_x,K_z,K_SPACE][i]]=1,1
                    else:world.else_btn_tap[i]=0
                keys[1]=None
            else:
                for i in range(len(world.else_btn_tap)):world.else_btn_tap[i]=0
                world.direct_btn_tap=None
            if pressmouse:pressmouse=False
        else:keys = key.get_pressed()
        if 1 in keys:
            if len(role.in_action) == 0 and role.live and role.control and (not role.eventing or (world.world['background'][0] in [20] and world.useitem==None)):
                if keys[K_RIGHT] or keys[K_LEFT]:
                    if keys[K_RIGHT]:
                        if keys[K_z]:
                            role.DoEvent('pull' if role.flip else 'push', world.world)
                        else:
                            role.DoEvent('climbup', world.world)
                            if role.pos[0] > 900 and world.world['background'][1][0]+world.world['background'][2][0]>1280:
                                world.world['background'][1][0] -= speed*terminal.zoom
                            if role.pos[0] + role.rects[role.posen][2]<world.world['background'][2][0] and not role.eventing:role.pos[0] += speed*terminal.zoom
                            if role.flip: role.Flip()
                    if keys[K_LEFT]:
                        if keys[K_z]:
                            role.DoEvent('push' if role.flip else 'pull', world.world)
                        else:
                            role.DoEvent('climbdown', world.world)
                            if role.pos[0] > 360 and role.pos[0] + world.world['background'][1][0] < 360 and not role.eventing:
                                world.world['background'][1][0] += speed*terminal.zoom
                            if role.pos[0] + role.rects[role.posen][0] > 0 and not role.eventing: role.pos[0] -= speed*terminal.zoom
                            if not role.flip: role.Flip()
                    if role.pose_finish and role.tapfloor:
                        pose = [1, 0][pose % 2]
                        role.DoPose(['walk1', 'walk2'][pose])
                if keys[K_UP] and role.tapfloor and time()>next_jump:
                    if role.state in [0, 2]:
                        next_jump=time()+0.5
                        if role.state == 2: role.state, role.speed[1] = 0, 0
                        role.speed[1] =- 5*terminal.zoom
                        role.DoPose('jump')
                        role.tapfloor = False
                    role.DoEvent('climb', world.world)
                if keys[K_DOWN]:
                    role.DoEvent('climb2', world.world)
                    if not role.eventing and role.pose_finish:
                        if terminal.player_setting['latent']:
                            role.pos[1]+=10
                        else:role.DoPose('squat')
                if keys[K_SPACE] and time()>world.triggertime:
                    for i in world.world['trigger']:
                        if i.Detect('space'):
                            world.triggertime=time()+1
                            break
                if keys[K_p]:
                    sleep(0.5)
                    get = game_pause()
                    if get == False:return False
                    elif get == 'back menu':return get
                    elif get == 'continue':world.display()
                    world = terminal.world
                    role = world.role
                if keys[K_x]:
                    role.Throw()
                    noitem_render()
                if keys[K_z]:
                    tkey=0
                    for i in world.world['trigger']:
                        if i.function!=None and i.function.__name__=='shattered':
                            tkey=i
                            break
                        if i.Detect('z'):
                            world.triggertime=time()+1
                            if i.function!=None and i.function.__name__ not in ('shattered','charge') and 'sensor_door' not in i.function.__name__:
                                tkey=1
                            break
                    if tkey!=1:
                        world.useitem=role.DoEvent(world.usemode, world.world)
                        if world.useitem==None:world.useitem=world.role.Throw(fix_item_pos=True)
                        if world.useitem not in world.itemlist:world.useitem=None
                        if not role.eventing:
                            if role.Throw(fix_item_pos=True)==None:
                                world.eventrole=pickitem=role.DoEvent('pickup', world.world)
                                if pickitem!=None and pickitem.name not in Moveable_obj:
                                    world.itemlist[world.itemlist_k]=pickitem
                                    draw.rect(world.itemlist_surf,(0,0, 0),[50 * world.itemlist_k, 0, 50, 50])
                                    if pickitem.posen in terminal.info[pickitem.name]:
                                        world.itemlist_surf.blit(transform.scale(terminal.info[pickitem.name][pickitem.posen][0],(50, 50)), (50 * world.itemlist_k, 0))
                                    else:
                                        for posen in terminal.info[pickitem.name]:
                                            world.itemlist_surf.blit(transform.scale(terminal.info[pickitem.name][posen][0], (50, 50)),(50 * world.itemlist_k, 0))
                                            break
                                    draw.rect(world.itemlist_surf, (230, 230, 0), [50 * world.itemlist_k, 0, 50, 50], 2)
                        elif role.do_event!=None:
                            if role.do_event[2].name in Moveable_obj and t>role.tem_cold:
                                role.tem_cold=t+1
                                terminal.sound['friction'].play()
                    if type(tkey)!=int:tkey.Detect('z')
                    #world.itemlist[world.itemlist_k]=role.Throw(fix_item_pos=True)
                if keys[K_k]:
                    for i in world.world['object']:
                        if i.name=='aircraft':
                            i.live=0
                            world.world['object'].remove(i)
                if keys[K_c]:
                    image.save(screen.copy(),'n.png'),sleep(0.5)
            if keys[K_a] and t>change_itemcd:
                change_item(0 if (world.itemlist_k+1)>=len(world.itemlist) else (world.itemlist_k+1))
                change_itemcd=t+0.3
#                sleep(1)
            if keys[K_s] and terminal.player_setting['fly']:
                role.pos[1]-=15
            needcount = 1
        else:
            needcount = None
        for i in world.world['object'] + [role]:
            i.calculate(world.world)
            if i.live==0 and i.state==0:change_limb_angle(i.role,0)
            if needcount == None and (i.speed[0] != i.speed[1] or not i.pose_finish or i.eventing):
                needcount = 1
        if inspect_time<time():                                                              #定時檢測
            if not world.instory:
                if role.pos[0]!=tempos[0][0] or role.pos[1]!=tempos[0][1]:tempos=[(role.pos[0],role.pos[1]),0]
                else:tempos[1]+=1
                if tempos[1]==1 and role.pose_finish and not role.eventing:role.DoPose(0)
            girl=world.search2('girl')
            if girl in world.followbox and girl.eventing and len(world.talkbox)==0 and not world.alarm and girl.do_event==None:
                girl.eventing=False
            if type(terminal.re_assign)==str:
                if terminal.re_assign=='resize':
                    terminal.loadfile(terminal.nowfile,zoom=terminal.zoom,text='正在重新調整大小...')
                    role, role.live, role.control, world.events_box, world.policebox, role.visible, role.hide,terminal.re_assign= world.role, 1, True, [], [], True, False,False
                elif terminal.re_assign=='re_assign':role,terminal.re_assign=world.role,False
            get,inspect_time= role.Throw(fix_item_pos=True),time()+1
            if not role.eventing and role.Throw(fix_item_pos=True) == None:noitem_render()
            if role.live!=1:
                if deadcd[0]:
                    deadcd[0]=False
                    deadcd[1]=t+5
                elif t>deadcd[1]:role.live=0
            if get != None:
                if get.name == 'keys':
                    world.props += ['keys']
                    role.eventing=False
                    systemhint('獲得道具:「萬能鑰匙」'),role.Throw(),world.world['object'].remove(get)
                else:
                    if get.name not in world.guide:world.guide[get.name]={}
                    if get.posen not in world.guide[get.name]:world.guide[get.name][get.posen]=True
                    else:world.guide[get.name][get.posen]=True
            world.update_guide()
            if role.state==1 and not role.eventing and world.plot['man1']<28:
                state=0
                world.usemode='use'
                for obj in world.world['object']:
                    if obj.name in ['stairs','stairs2','ladder'] and abs(role.pos[0]-obj.pos[0])<200:state=1
                role.state=state
            needcount=1
        if needcount == None and not world.busy:
            if role.posen != 0 and role.state == 0:
                role.DoPose('normal')
                continue
            if len(world.talkbox) == 0 and len(world.bullet)==0 and not world.is_busy:
                sleep(0.1)
            else:needcount=1
        if needcount==1 or world.busy or world.is_busy:
            world.display()
        if role.speed[1]>9*terminal.zoom and not fall:fall=True
        if role.tapfloor and fall and terminal.player_setting['fall']:
            role.DoAction('fall')
            fall,role.control=False,False
        if role.nowaction == 'fall' and getupk < 1: getupk = 100
        if getupk>0:
            getupk-=1
            if getupk<1:
                role.DoAction('getup')
                role.control=True
        if role.live==0 and len(world.fragments)==0:                                                                     #死亡
            world.guide2_count(role, 'died')
            for i in range(510):
                if i==255:
                    guide2=copy_variable(world.guide2)
                    terminal.loadfile(terminal.nowfile,text='正在重生...')
                    role,role.live,role.control,world.events_box,world.policebox,world.guide2,role.visible,role.hide,fall=world.role,1,True,[],[],guide2,True,False,False
                    world.busy=False
                    deadcd = [True, 0]
                    for obj in world.world['object']:
                        if obj.name=='gun':
                            obj.role.rotate=-90 if role.flip else 90
                    #role.rotate=role.role.rotate=0
                world.display(False)
                black.set_alpha(abs(min(i,510-i)))
                screen.blit(black,(0,0))
                display.update()
                wait_tap()
        if world.clearance!=0:
            if world.clearance in (3,4):
                black.set_alpha(240),screen.blit(black,(0,0))
                display_thank()
                white=transform.scale(terminal.white,(1280,720))
                for i in range(510):
                    wait_tap()
                    screen.fill((0,0,0))
                    white.set_alpha(int(i/2))
                    screen.blit(white, (0, 0))
                    display.update()
            return 'back menu'
    return False
def sysinfo(t):
    p,h=400,150
    draw.rect(screen, (255, 255, 255), [p, 100, 500, 300]),screen.blit(transform.scale(terminal.image['sys2'],(500,60)), (p, 100))
    for i in t:
        if i!=None:
            text_render(screen,i[0],i[1],i[2],(p+50,h))
            h+=i[1]+10
    display.update()
def yesno(t,t2='',t3=''):
    bg=screen.copy()
    terminal.sound['button'].play()
    abc=1
    sysinfo([None, (t, 40, (125, 91, 0)),(t2,23,(0,0,0)),(t3,20,(0,0,0))]),draw.rect(screen, (0, 0, 0), [470, 320, 80, 40]),draw.rect(screen, (255, 0, 0), [720, 320, 80, 40]),text_render(screen,'確定                        取消', 30,(255, 255, 255), (475, 320)),display.update()
    sys_board=screen.subsurface([400,100,500,300]).copy()
    for i in range(100):
        screen.blit(bg,(0,0)),screen.blit(transform.scale(sys_board,(5*i,3*i)),(650-int(2.5*i),250-int(1.5*i))),display.update()
    while abc == 1 and type(abc)==int:
        sleep(0.1)
        for event2 in event.get():
            if event2.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if 320 < y < 360:
                    if 470 < x < 550:
                        abc=True
                    if 720 < x < 800:
                        abc=False
    terminal.sound['button3'].play()
    if not abc:
        for i in range(100):
            screen.blit(bg, (0, 0)), screen.blit(transform.scale(sys_board, (5 *(100-i), 3 *(100-i))),(650 - int(2.5 *(100-i)), 250 - int(1.5 *(100-i)))), display.update()
    return abc
def systemhint(t,t2='',t3=''):
    sysinfo([None, (t, 40, (125, 91, 0)),(t2,23,(0,0,0)),(t3,20,(0,0,0))]), draw.rect(screen, (255, 0, 0), [595, 320, 80, 40]),text_render(screen,'確定',30,(255,255,255),(600,320))
    display.update()
    while True:
        for event2 in event.get():
            if event2.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if 595 < x < 675 and 320 < y < 360:
                    terminal.sound['button'].play()
                    return True
        sleep(0.1)
def Main_menu():
    screen.blit(transform.scale(image.load(f'{work_dir}scenes/74.jpg').convert(), (1280, 720)), (0, 0))
    draw.rect(screen, (50, 50, 50), [0, 620, 1280, 100]), text_render(screen, '正在載入...', 25, (255, 255, 255), (15, 630))
    draw.rect(screen, (150, 150, 150), [30, 675, 1220, 12], 1)
    #-----------------------------------------------
    sp_room = [['Ward'],None][1]
    terminal.world.play_bgm('interstellar')
    mixer.music.set_volume(terminal.bgm_vol)
    terminal.load_data(sp_room=sp_room,effect=[True,False][0], bg=screen.copy())
    terminal.adjust_sound()
    white= Surface((800, 130))
    white.fill((255, 255, 255))
    def back_menu(mouse_pos):
        if 1000<mouse_pos[0]<1150 and 570<mouse_pos[1]<620:draw.rect(screen,(0,200,200),[1000,570,150,50])
        draw.rect(screen,(255,255,255),[1000,570,150,50],3)
        text_render(screen,'返回',35,(255,255,255),(1040,570))
    def recover_set(mouse_pos):
        if 150<mouse_pos[0]<300 and 150<mouse_pos[1]<190:draw.rect(screen,(100,100,100),[150,150,150,40])
        draw.rect(screen,(255,255,255),[150,150,150,40],2)
        text_render(screen,'恢復設定',30,(255,255,255),(160,150))
    def clean_data(mouse_pos):
        if 150<mouse_pos[0]<300 and 220<mouse_pos[1]<260:draw.rect(screen,(100,100,100),[150,220,150,40])
        draw.rect(screen,(255,255,255),[150,220,150,40],2)
        text_render(screen,'清除資料',30,(255,255,255),(160,220))
    def render_savefile():
        screen.blit(bg, (0, 0))
        o,k=listdir(f'{work_dir}data'),0
        while k<len(o):
            if o[k][:5]!='save ':del o[k]
            else:k+=1
        k=0
        while k<3:
            if f'save {3*savefilepage+k}.txt' in o:
                info,blank=str_convert(open(f'{work_dir}data/save {3*savefilepage+k}.txt','r').read()),white.copy()
                text_render(blank,f'存檔{3*savefilepage+k+1}',30,(0,0,0),(660,40))
                blank.blit(transform.scale(terminal.allbg[info['role_state']['room']],(200,100)),(20,15)),text_render(blank,info['save_time'],25,(0,0,0),(240,12),1),text_render(blank,f'圖鑑: {count_unlock_guide(info["guide"])}/{terminal.guide_num}',25,(0,0,0),(240,48),1)
                text_render(blank, f'探索度: {count_explore_rate(info)}', 25, (0, 0, 0),(240, 85), 1)
                blank.set_alpha(200 if 3*savefilepage+k==terminal.nowfile else 150)
                screen.blit(blank, (280, 60 + 150 * k))
                k+=1
            else:break
        text_render(screen,f'{savefilepage+1}/{max((len(o)-1)//3,0)+1}',30,(0,0,0),(1150,280))
        if savefilepage>0:screen.blit(terminal.image['arrowup'],(1150,70))
        if savefilepage<(len(o)-1)//3: screen.blit(terminal.image['arrowdown'],(1150,360))
        back_menu(mouse.get_pos())
        display.update()
    def replay_bgm():
        terminal.world.play_bgm('interstellar')
    def display_achieve():
        def end_display2(end):
            bg=screen.copy()
            terminal.sound['button'].play(),end_display(end)
            replay_bgm(),screen.blit(bg,(0,0)),display.update()
        def not_finish(e):terminal.sound['warn'].play(),systemhint('結局未達成')
        panel,buttonlist,k,c=Surface((480,2000)),[],0,0
        panel.fill((100,100,100))
        for i in Game_setting['ending']:
            play_btn=Surface((50,25))
            draw.rect(panel,(180,180,180),[10,10+150*k,460,130])
            if terminal.unlock_end[i]:
                play_btn.fill((255, 255, 0)), text_render(play_btn, '播放', 20, (0, 0, 0), (5, 0))
                panel.blit(transform.scale(image.load(f'{work_dir}data/end/{i}.png'), (160, 120)), (20, 15 + 150 * k)),draw.rect(panel,(230,230,230),[20, 15 + 150 * k,160,120],5),text_render(panel,Game_setting['ending'][i][0], 30, (255, 255, 255), (190, 15 + 150 * k))
                buttonlist += [[play_btn, (410, 110 + 150 * k),end_display2,i]]
                c+=1
            else:
                play_btn.fill((140,140,140)), text_render(play_btn, '播放', 20, (255,255,255), (5, 0))
                panel.blit(transform.scale(terminal.image['not found'],(160,120)),(20,15+150*k)),text_render(panel,'???',30,(255,255,255),(190,15+150*k))
                buttonlist += [[play_btn,(410,110+150*k),not_finish,0]]
            k+=1
        def board_up():
            screen.blit(bg,(385,100))
            board.show(),display.update()
        bg=Surface((510,520))
        text_render(bg,f'已達成結局({c}/{k})',40,(255,255,255),(110,10),1)
        board=rollboard((390,170,480,430),panel.subsurface([0,0,480,20+150*k]),buttonlist)
        board_up()
        abc=1
        while abc == 1:
            if board.rolling():board_up()
            else:sleep(0.1)
            for event2 in event.get():
                if event2.type == QUIT:return False
                if event2.type == MOUSEBUTTONDOWN:  # 滑鼠點擊
                    x, y = mouse.get_pos()
                    if board.contain((x, y)):
                        if event2.button == 1:board.tap((x, y))
                        if event2.button == 5:board.roll(30)
                        if event2.button == 4:board.roll(-30)
                    elif event2.button == 1:abc=0
                    board_up()
        return True
    def up():
        screen.blit(bg,(0,0)),screen.blit(transform.scale(exit_btn,(70,78) if 25<x<89 and 610<y<681 and not mouse_down else (64,71)),(22,606) if 25<x<89 and 610<y<681 and not mouse_down else (25,610))
        screen.blit(
            transform.scale(achieve_btn, (70, 66) if 25 < x < 89 and 530 < y < 601 and not mouse_down else (62,59)),
            (22, 526) if 25 < x < 89 and 530 < y < 601 and not mouse_down else (25, 530))
        for i in range(len(btns)):screen.blit(transform.scale(btns[i],(320,44) if 485<x<795 and 0<y-170-80*i<42 and not mouse_down else (310,42)),(480,169+80*i) if 485<x<795 and 0<y-170-80*i<42 and not mouse_down else (485,170+80*i))
        display.update()
    bg,exit_btn,achieve_btn=transform.scale(image.load(f'{work_dir}scenes/0.jpg').convert(),(1280,720)),transform.scale(terminal.image['exit'],(64,71)),transform.scale(terminal.image['achieve'],(62,59))
    btns=[]
    for i in range(4):
        btns+=[transform.scale(terminal.blank.copy(),(310,42))]
        draw.polygon(btns[-1],(0,230,230),[(5,20),(25,40),(285,40),(305,20),(285,0),(25,0)]),draw.polygon(btns[-1],(0,0,255),[(5,20),(25,40),(285,40),(305,20),(285,0),(25,0)],6)
        text_render(btns[-1],['開始遊戲','繼續遊戲','選擇存檔','遊戲設定'][i],30,(255,255,255),(100,0),1)
        btns[i].set_alpha(220)
    mouse_down=False
    abc,x,y=1,0,0
    savefilepage=None
    set=Game_set((320,150))
    while abc == 1:
        mouse_down=False
        for event2 in event.get():
            if event2.type == QUIT:
                abc = 0
            if event2.type == MOUSEBUTTONDOWN:                                                     #滑鼠點擊
                x,y = mouse.get_pos()
                mouse_down=True
                if 1000<x<1150 and 570<y<620:
                    savefilepage=None
                    sleep(0.2),up(),terminal.sound['button'].play()
                if savefilepage==None:
                    up()
                    for i in range(len(btns)):
                        if 485 < x < 795 and 0 < y - 170 - 80 * i < 42:
                            terminal.sound['button'].play()
                            if i == 1:
                                if f'save {terminal.last_file}.txt' not in listdir(f'{work_dir}data'):
                                    if yesno('是否開始新遊戲'): i = 0
                                elif yesno(f'將載入"存檔{terminal.last_file+1}"'):
                                    terminal.loadfile(terminal.last_file)
                                    r = rungame({'wake_up': True}, blackeffect=False)
                                    if r == False: return False
                                    replay_bgm()
                            if i==0:
                                black,bg2= Surface(screen.get_rect()[2:]),screen.copy()
                                if sp_room==None:
                                    for i in range(255):
                                        wait_tap()
                                        screen.blit(bg2,(0,0))
                                        black.set_alpha(i)
                                        screen.blit(black, (0, 0))
                                        display.update()
                                terminal.nowfile=terminal.next_savefile()
                                terminal.init_world(sp_room=sp_room)
                                r=rungame({'wake_up':False},blackeffect=True)
                                if r==False:return False
                                replay_bgm()
                            elif i==2:
                                savefilepage=0
                                render_savefile()
                            elif i==3:
                                savefilepage='set'
                                screen.blit(bg, (0, 0)),back_menu((x,y)),recover_set((x,y)),clean_data((x,y))
                                set.display()
                    if 25 < x < 89 and 530 < y < 601:
                        terminal.sound['button'].play()
                        if not display_achieve():abc=0
                        terminal.sound['button3'].play()
                    if 25 < x < 89 and 610 < y < 681 and yesno('確定要離開遊戲嗎?'):
                        abc = 0
                elif savefilepage=='set':
                    set.mainloop((x,y))
                    screen.blit(bg,(0,0)),back_menu((x,y)),recover_set((x,y)),clean_data((x,y))
                    set.display()
                    if 150<x<300 and 150<y<190 and yesno('恢復設定','要將設定恢復為預設設定嗎?'):
                        terminal.bgm_vol,terminal.sound_vol,terminal.zoom,0.4,0.5,1
                        mixer.music.set_volume(terminal.bgm_vol),terminal.adjust_sound(),terminal.save_setting()
                    if 150<x<300 and 220<y<260 and yesno('清除資料','要清除成就和存檔資料嗎?'):
                        for i in listdir(f'{work_dir}data'):
                            if 'save '==i[:5]:remove(f'{work_dir}data/{i}')
                        for i in terminal.unlock_end:terminal.unlock_end[i]=False
                        terminal.save_setting()
                elif savefilepage!=None:
                    render_savefile()
                    o, k = listdir(f'{work_dir}data'), 0
                    while k < len(o):
                        if o[k][:5] != 'save ':del o[k]
                        else:k += 1
                    for i in range(3):
                        if 280 < x < 1080 and 0 < y - 60 - 150 * i < 130:
                            if f'save {3 * savefilepage + i}.txt' in o and yesno('讀取存檔',f'確定讀取 "存檔 {3 * savefilepage + i + 1}"?'):
                                terminal.loadfile(3 * savefilepage + i)
                                r=rungame({'wake_up':True},blackeffect=False)
                                if r == False: return False
                                savefilepage=None
                                replay_bgm()
                    if 1150<x<1191 and 70<y<242 and savefilepage>0:
                        savefilepage-=1
                        terminal.sound['button2'].play()
                    if 1150 < x < 1191 and 360 < y < 532 and savefilepage<(len(o)-1)//3:
                        savefilepage+=1
                        terminal.sound['button2'].play()
        sleep(0.1)
        if (x,y) != mouse.get_pos() and savefilepage==None:
            up()
            x, y = mouse.get_pos()
        elif savefilepage == 'set':
            mpos=mouse.get_pos()
            screen.blit(bg, (0, 0)),back_menu(mpos),recover_set(mpos),clean_data(mpos)
            set.display()
        elif savefilepage != None:
            render_savefile()
display.set_icon(image.load(f'{work_dir}object/high-rise.png'))
setting=str_convert(open(f'{work_dir}data/setting.txt','r',encoding='utf-8').read())
if setting['mode']== 0: screen = display.set_mode((1280, 720), FULLSCREEN)
else:screen = display.set_mode((1280,720))#,FULLSCREEN)
terminal = Terminal()
Main_menu()
_exit(0)
