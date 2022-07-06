# 实验平台
## ADB 无线调试
1. 安装 [Android-SDK](https://developer.android.google.cn/studio/releases/platform-tools?hl=zh-cn).安装完成后，在命令行下执行``adb``命令验证。
2. 手机设置 > 开发者选项 中启用 USB 调试和无线调试
3. 参考链接 [USB连接至PC](https://developer.android.google.cn/studio/command-line/adb?hl=zh_cn#wireless) 进行无线调试连接：
   1. 将 Android 设备和 adb 主机连接到这两者都可以访问的同一 Wi-Fi 网络。请注意，并非所有接入点都适用；您可能需要使用防火墙已正确配置为支持 adb 的接入点。
   2. 使用 USB 线将设备连接到主机。
   3. 设置目标设备以监听端口 5555 上的 TCP/IP 连接。
    ``adb tcpip 5555``
   4. 拔掉连接目标设备的 USB 线,找到 Android 设备的 IP 地址,通过 IP 地址连接到设备。
    ``adb connect device_ip_address:5555``
    5. 确认主机已连接到目标设备：
        `````bash
        $ adb devices
        List of devices attached
        device_ip_address:5555 device
        `````
## 基于[uiautomator2](https://github.com/openatx/uiautomator2)的安卓自动化测试
1. 保证``adb``已连接
2. 运行``pip install -U uiautomator2`` 安装 uiautomator2
3. python运行:
    `````python
    import uiautomator2 as u2

    d = u2.connect() # connect to device
    print(d.info)
    `````
    观察到手机相应信息即可

常用操作可参考 [QUICK_REFERENCE](https://github.com/openatx/uiautomator2/blob/master/QUICK_REFERENCE.md) ,如需进行快速的元素定位和调试可配合使用 [weditor](https://github.com/alibaba/web-editor)。

在实验中，我们定时运行主流app，模拟用户操作，并测量各系统指标。
`````python
def test_zhihu(last_time):
    t_end = time.time() + 60 * last_time
    launch = d.shell("am start -W -S com.zhihu.android/.app.ui.activity.MainActivity").output.split('\n')
    lt.append(float(pattern_d.search(launch[5]).group()))
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
`````
各指标收集方法可参考[Cotroneo et al_2016_Software Aging Analysis of the Android Mobile OS](https://ieeexplore.ieee.org/abstract/document/7774545)

## Perfetto
[Pefetto](https://perfetto.dev/) 是 Google 开发的系统追踪工具。
启动trace：``cat config.pbtx | adb shell perfetto -c - --txt -o /data/misc/perfetto-traces/trace.perfetto-trace``
其中配置文件参考 [record](https://ui.perfetto.dev/#!/record) 填写。
完成后，使用``adb pull  /data/misc/perfetto-traces/trace.perfetto-trace ./``将 trace 文件 pull 至电脑上，并在 [Trace Viewer](https://ui.perfetto.dev/#!) 中查看。