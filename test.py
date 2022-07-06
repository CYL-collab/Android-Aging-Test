import uiautomator2 as u2
import time
import re
import os
import subprocess
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import pickle as pkl
import pandas as pd

package_name = ["com.zhihu.android",
                "com.ss.android.ugc.aweme",
                "com.youku.phone",
                "com.taobao.taobao",
                "com.dianping.v1",
                "com.ss.android.article.video"]
activity_name = [None,"com.ss.android.ugc.aweme.splash.SplashActivity",None,None,None]
pss_ss = []
rss_ss = []
pss_sf = []
rss_sf = []
lt = []
FM = []
t = []
pattern_d = re.compile(r'\d+')

d = u2.connect()

# 获取root权限以读取指标
subprocess.call(['adb','root'])

# 监视弹窗并自动跳过
d.watcher.when('安装').click()
d.watcher.when('继续安装').click()
d.watcher.when('完成').click()
d.watcher.when('同意并继续').click()
d.watcher.when("我知道了").click()
d.watcher.when("跳过").click()
d.watcher.when("跳过广告").click()
d.watcher.when("抢红包").press("back")
d.watcher.start()

def init():
    for apk_name in os.listdir('apk'):
        path = 'apk\\' + apk_name
        print('Installing {} ...'.format(apk_name))
        subprocess.call(['adb','install',path])

def collect():   
    sys = d.shell("dumpsys meminfo -s system | grep 'TOTAL PSS'").output
    t.append(time.perf_counter()) 
    pss_ss.append(float(pattern_d.findall(sys)[0])) 
    rss_ss.append(float(pattern_d.findall(sys)[1]))
    
    sf = d.shell("dumpsys meminfo -s surfaceflinger | grep 'TOTAL PSS'").output
    pss_sf.append(float(pattern_d.findall(sf)[0])) 
    rss_sf.append(float(pattern_d.findall(sf)[1])) 
    
    free = d.shell("dumpsys meminfo -c | grep '^ram'").output
    FM.append(float(pattern_d.findall(free)[1]))

def test_zhihu(last_time):
    t_end = time.time() + 60 * last_time
    text = d.shell("am start -W -S com.zhihu.android/.app.ui.activity.MainActivity | grep TotalTime").output
    lt.append(float(pattern_d.search(text).group()))
    collect()
    time.sleep(5)
    while time.time() < t_end:
        # d.widget.click("00010#")
        d.xpath('//*[@resource-id="com.zhihu.android:id/ad_float"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView[1]/android.widget.LinearLayout[2]/android.view.ViewGroup[1]').click()
        time.sleep(2)
        d.swipe(0.5,0.6,0.5,0.2,0.05)
        time.sleep(0.2)
        d.swipe(0.5,0.6,0.5,0.2,0.05)
        d.press("back")
        time.sleep(0.5)
        d.swipe(0.5,0.6,0.5,0.2,0.05)
        time.sleep(2)
    d.app_stop("com.zhihu.android")
    
    
def test_tiktok(last_time):
    t_end = time.time() + 60 * last_time
    text = d.shell("am start -W -S com.ss.android.ugc.aweme/.main.MainActivity | grep TotalTime").output
    lt.append(float(pattern_d.search(text).group()))
    collect()
    time.sleep(3)
    
    while time.time() < t_end:
        d.swipe(0.5,0.6,0.5,0.2,0.05)
        time.sleep(0.5)
    d.app_stop("com.ss.android.ugc.aweme")
  
if __name__ == "__main__":
    # init()
    t_end = time.time() + 60 * 60 * 10
    while time.time() < t_end:
        test_tiktok(5)
    # plt.scatter(t,lt)
    # plt.scatter(t,FM)
    # plt.show()
    
    data = {'t':t,
            'lt':lt,
            'FM':FM,
            'pss_ss':pss_ss,
            'rss_ss':rss_ss,
            'pss_sf':pss_sf,
            'rss_sf':rss_sf
            }
    data = pd.DataFrame(data)
    print(data)
    with open('test_data','wb') as f:
        pkl.dump(data,f)

