# bug reproduction script for bug #5977of antennapod
# 导入必要的库和模块
import sys
import time
import uiautomator2 as u2

def wait(seconds=2):
    for i in range(0, seconds):
        print("wait 1 second...")
        time.sleep(1)

if __name__ == '__main__':
    # 获取 AVD 序列号
    avd_serial = sys.argv[1]
    d = u2.connect(avd_serial)

    # 启动应用
    d.app_start("de.danoeh.antennapod.debug")
    wait()

    # 等待应用启动完成
    current_app = d.app_current()
    print(current_app)
    while True:
        if current_app['package'] == "de.danoeh.antennapod.debug":
            break
        time.sleep(2)
    wait()

    #now begin to reproduce the bug#5977
    # 1. rotate the device to the landscape
    d.orientation = "left"  # or "right"
    print("success: rotating device")

    # 2. click Episodes
    out = d(resourceId="de.danoeh.antennapod.debug:id/txtvTitle", text="Episodes").click()
    if not out:
        print("Success: click Episodes")
    wait()

    # 3. click Filter
    out = d.xpath(
        '//*[@resource-id="de.danoeh.antennapod.debug:id/audioplayerFragment"]/android.widget.RelativeLayout[1]/android.view.ViewGroup[1]/androidx.appcompat.widget.LinearLayoutCompat[1]').click()
    if not out:
        print("Success: click filter")
    wait()

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
