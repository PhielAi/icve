from DrissionPage import ChromiumPage, ChromiumOptions
import re
import sys
import time

# 学习的课程
your_class=''
your_account=''
your_password=''
# img
img='icve/image.png'

def login(url):
    page.get(url=url,retry=3,interval=2,timeout=10)
    page.wait.load_start()
    if page.ele('开启教学').click():
        # login
        # 第一次登陆
        if page.ele('请先登录'):
            page.ele('确定').click()
            page.wait.load_start()

            # 输入账号密码
            page.ele('xpath://input[@placeholder="请输入账号"]').input(your_account)
            page.ele('xpath://input[@placeholder="请输入密码"]').input(your_password)
            page.ele('xpath://span[@class="el-checkbox__inner"]').click()
            for i in page.eles('xpath://form[@class="el-form demo-ruleForm"]/div'):
                if i.text == '登录':
                    i.click()
            print(i)
            page.wait.load_start()
            query()
            
        # 已经处于登录状态
        else:
            query()
    
    else:
        print('网页未加载成功，请检查网址是否正确')
            
def query():
    page.ele('我的课程').click()
    obj=page.ele('xpath://div[@class="el-tab-pane"]')
    # 遍历
    for course in obj.eles('xpath://div[@class="case"]'):
        # 找课程
        if course.ele(your_class):
            print(f'已找到课程，准备开始学习：{your_class}')
            course.ele('查看').click()
            find()
            return
        else:
            print(f'未找到{your_class}，查看下一个目录')
            print('loading...')
            continue
            
def find():
    # 学习进度
    page.wait(2)
    obj=page.ele('xpath://div[@class="coursePreviewIndex"]')
    
    # 遍历
    for title in obj.eles('xpath://div[@class="listItem"]'):
        
        # 判断当前课程是否完成 100%
        if title.ele('xpath://div[@class="el-progress__text"]').text != "已学：100%":
            
            # 输出当前课程学习进度
            print('\n'+title.ele('xpath://div[@class="tit"]').text+title.ele('xpath://div[@class="el-progress__text"]').text)
            print('start learning...')
            
            # 打开子目录
            title.ele('xpath://div[@class="ts"]').click()
            
            # 遍历子目录
            print('learning...')
            for row in title.eles('xpath://div[@class="items iChild"]'):
                row.ele('xpath://div[@class="ts"]').click()
                page.wait(0.1)
                
                # 遍历学习目录
                for study in title.eles('xpath://div[@class="fwenjianjia"]'):
                    
                    # 匹配是否完成 
                    if not study.ele(' 已学：100% '):
                        # 进入页面
                        study.ele('xpath://div[@class="fwi"]').click()
                                       
                        # start to learn
                        learn()
                        
            print('\ndone')
            print('本目录学习完毕，开始学习下一个目录...')
            
        else:
            if title ==  obj.eles('xpath://div[@class="listItem"]')[len(obj.eles('xpath://div[@class="listItem"]'))-1]:
                print('\n已检测到所有进度学习完毕！')
                print(r'''       
                 (__)
                 (oo) 
           /------\/ 
          / |    ||   
         *  /\---/\ 
            ~~   ~~   
.........."Good job!"..........''')
                return
            else:
                # 输出当前课程学习进度
                print('\n'+title.ele('xpath://div[@class="tit"]').text+title.ele('xpath://div[@class="el-progress__text"]').text)
                print('当前学习进度已完成，查看下个章节')
                print('loading...')
                continue       
                
def learn():
    while True:
        page.wait(1)
        # 固定区域
        obj=page.ele('xpath://div[@class="courseDetails"]')
        
        # video
        if obj.ele('xpath://div[@class="video-player video-player vjs-custom-skin"]'):
            print('\nstart to learn video...')
            page.wait(0.5)
            # 弹窗
            if not pop_ups():
                # play
                obj.ele('xpath://button[@title="Play Video"]').click()
            page.wait(1)
            # wait
            
            time_cur=obj.ele('xpath://span[@class="vjs-current-time-display"]').text
            time_cur=time_to_seconds(time_cur)
            time_all=obj.ele('xpath://span[@class="vjs-duration-display"]').text
            time_all=time_to_seconds(time_all)
            
            wait_time=time_all-time_cur+1
            for i in range(wait_time,0,-1):
                sys.stdout.write(f"\rPlease wait: {i} second")
                sys.stdout.flush()  # 刷新输出，使其立即显示
                time.sleep(1)
            
            # next
            if obj.ele('xpath://div[@class="next"]/a[@class="el-link el-link--primary"]/span[@class="el-link--inner"]').text != '暂无':
                obj.ele('xpath://div[@class="next"]/a[@class="el-link el-link--primary"]').click()
                print('complete')
                continue
            else:
                page.ele(' 课程首页 ').click()
                find()  
        
        # ppt & word
        elif obj.ele('xpath://div[@class="el-carousel el-carousel--horizontal"]'):
            print('\nstart to learn ppt & word...')
            page.wait(0.5)
            # 弹窗
            pop_ups()
            # 寻找页数
            text=obj.ele('xpath://div[@class="page"]').text
            result=re.match(pattern='.+\d+ / (\d+).+',string=text)
            obj_num=result.group(1)
            
            # 翻页
            for page_num in range(1,eval(obj_num)):
                
                if page_num == obj_num:
                    break
                else:
                    obj.ele('下一页').click()
            
            # next
            if obj.ele('xpath://div[@class="next"]/a[@class="el-link el-link--primary"]/span[@class="el-link--inner"]').text != '暂无':
                obj.ele('xpath://div[@class="next"]/a[@class="el-link el-link--primary"]').click()
                print('complete')
                continue
            else:
                page.ele(' 课程首页 ').click()
                find()
        
        else:
            print('未找到元素，请检查代码是否出错！')
            
def pop_ups():
    if page.ele('xpath://div[@class="el-message-box__wrapper"]'):
        str=page.ele('xpath://div[@class="el-message-box__wrapper"]').attr('style')
        result=re.match(pattern='.+\d+;(.*)',string=str)
        ture=result.group(1)
        if ture:
            return False
        else:
            page.ele('xpath://button[@class="el-button el-button--default el-button--small el-button--primary "]').click()
            return True
    else:
        pass
    
    
def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    total_seconds = minutes * 60 + seconds
    return total_seconds

if __name__=='__main__':
    # 请改为你电脑内Chrome可执行文件路径
    co=ChromiumOptions().set_browser_path(path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe").incognito()
    page = ChromiumPage(addr_or_opts=co)
    # ocr=ddddocr.DdddOcr(use_gpu=True) 
    url='https://zjy2.icve.com.cn/index'
    login(url)


