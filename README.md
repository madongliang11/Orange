#                                                 OrangeMall（橘子商城）开发说明


----------------------------------------------------------项目开发文档----------------------------------------------------------

1.环境
    python 版本 3.6.0以上3.7.0以下
    django 版本 1.11.12

    需要自己创建运行环境，github上不上传，手动创建运行环境方法（windows）：
        cmd下：
            1.pip install virtualenv
            下载慢可加源：（pip install virtualenv -i http://pypi.douban.com/simple/）
            2.virtualenv  查看是否安装成功
            3.virtualenv [虚拟环境根目录名称] --python=python3
            4.激活  进入创建好的环境变量根目录scripts中去，cmd中输入activate.bat运行    （windows）
    
    数据库 mysql （连接远程数据库服务器命令：mysql -u[账号] -p[密码] -P[端口号] -h[IP地址]）
        name： omdb
        host： 192.168.50.16
        port：3306
        username：   root
        password：   root


2.数据库表命名说明
    查看群内上传
    数据库迁移命令:python manage.py makemigrations [app名称]
    数据库同步命令:python manage.py migrate [app名称]
    # 参照群内上传的数据库表


--------------------------------------------------------------------------------------------------------
    类型参照表
--------------------------------------------------------------------------------------------------------
                                    models                                            mysql/oracle
    
    自增类型                       AutoField
    整数           IntegerField/TinyintField/BigIntegerField                             int/number
    单精度浮点                    FloatField/                                              float
    高精度浮点                    DecimalField                                            decimal
    
                                                                                          char
    字符                           CharField
                                                                                          varchar/varchar2
    
    文本域                        TextField                                               text
    日期                          DateField                                               date
    时间                        DateTimeField                                           datetime/timestamp
---------------------------------------------------------------------------------------------------------
    字段约束参照表
---------------------------------------------------------------------------------------------------------
    主键约束       primary_key = True
    唯一约束       unique = True | False
    最大长度       max_length =
    默认值         default = 0 | True | False
    空值约束       null = True | False
    索引字段        db_index = True

                    DateTimeField(auto_now=True | auto_now_add=True)    auto_now每次更新数据库重新赋予时间
    时间约束                                                            auto_now_add 永远为第一次创建的时间
                    DateField

    外键约束

---------------------------------------------------------------------------------------------------------


3.第三方库资源说明

    基础库已导出到根目录requirements.txt，根据自己需求添加
    已安装：框架版本控制  django=1.11.12

                            pymysql
            数据库模型相关   Pillow  （用于模型层ImageField）


            会话
            缓存

            后台

    
    环境导出命令: pip freeze > requirements.txt
    批量环境安装：pip install requirements.txt

4.项目文件夹说明

    4.1 模块功能apps
        所有功能模块集合
        创建app命令: python manage.py startapp [app名称]


    4.2 静态资源文件夹static,建议不同模块创建不同static文件夹
        所有的css，js 资源初步建议直接调用网上cdn
    
    4.3 模板建议一个功能模块一个templates文件夹


5.后台账户

    创建超级管理员
     run manage.py tools:  createsuperuser
