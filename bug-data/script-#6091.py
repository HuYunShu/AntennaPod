# bug reproduction script for bug #6091of antennapod
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

    # 1. click Queue
    out = d(resourceId="de.danoeh.antennapod.debug:id/txtvTitle", text="Queue").click()
    if not out:
        print("Success: click Episodes")
    wait()

    # 2. drag an episode to change the position with another episode
    out = d.xpath(
        '//*[@resourceId=""de.danoeh.antennapod.debug:id/recyclerView"] / android.widget.FrameLayout[1]').drag_to(
        500, 500)
    if not out:
        print("Success: drag episode to a new position")

    wait()

    # 获取新位置的 episode 元素
    new_position_episode = d.xpath(
        '//*[@resourceId=""de.danoeh.antennapod.debug:id/recyclerView"] / android.widget.FrameLayout[1]')

    # 计算拖拽的起始坐标和结束坐标
    start_x = (bounds1['left'] + bounds1['right']) // 2
    start_y = (bounds1['top'] + bounds1['bottom']) // 2
    end_x = (bounds2['left'] + bounds2['right']) // 2
    end_y = (bounds2['top'] + bounds2['bottom']) // 2
    out = d.drag(start_x, start_y, end_x, end_y, steps=10)
    
    wait()

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)
