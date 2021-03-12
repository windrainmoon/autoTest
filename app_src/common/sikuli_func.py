import os
import win32api, win32con


cwd = os.getcwd() + "\\"
pic_path = cwd + 'app_src\\temp_pic\\'

x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
print("x: %d, y: %d" % (x, y))

# 将jvm.dll 的路径加入系统变量，两者加任意一个即可，
# 也可以将其配置到系统变量中，就不必每次运行脚本时设置了

# os.environ["JAVA_HOME"] = r"E:\Program Files\Java\jdk-11.0.9\bin\server"
# os.environ["JDK_HOME"] = r"E:\Program Files\Java\jdk-11.0.9"
JAVA_ENV_PASS = 0

# 将sikuli的jar包引入到CLASSPATH中
os.environ["CLASSPATH"] = cwd + r'app_src\common\javaapi.jar'
try:
    from jnius import autoclass
    import jnius_config  # 打包时用到

    JAVA_ENV_PASS = 1
    # 调用Java jar中的类
    Screen = autoclass("org.sikuli.script.Screen")
    App = autoclass("org.sikuli.script.App")
    Region = autoclass("org.sikuli.script.Region")
    Key = autoclass("org.sikuli.script.Key")
    pattern = autoclass("org.sikuli.script.Pattern")


    def Pattern(pic):
        if pic.__class__ == str and ".png" in pic:
            pic = pic_path + pic
        return pattern(pic)


    s = Screen()
    r = Region.create(0, 0, x, y)


    # wait = r.wait
    def wait(*args):
        if args[0].__class__ == str and ".png" in args[0]:
            args = list(args)
            args[0] = pic_path + args[0]
            # print(args[0])
        return r.wait(*args)


    # click = s.click
    def click(*args):
        if args[0].__class__ == str and ".png" in args[0]:
            args = list(args)
            args[0] = pic_path + args[0]
            # print(args[0])
        return s.click(*args)


    paste = r.paste


    # type = r.type
    def type_in(*args):
        if args[0].__class__ == str and ".png" in args[0]:
            args = list(args)
            args[0] = pic_path + args[0]
            # print(args[0])
        return r.type(*args)
except Exception as e:
    print("import GUI lib error!", e)


