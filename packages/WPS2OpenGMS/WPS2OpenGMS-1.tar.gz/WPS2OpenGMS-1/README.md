该程序用于使用OpenGMS方法实现对52° North WPS模型的自动化封装。

#### 一、输入参数：

1、WPS服务的网络地址：

​	eg：http://geoprocessing.demo.52north.org/latest-wps/WebProcessingService

2、某一模型执行请求XML文件：

​	eg：echo.xml

#### 二、使用方法：

```python
from WPS2OpenGMS.wps2opengms import createWPS2OpenGMS 

createWPS2OpenGMS(“your_wps_url”,"wps_execute.xml")
```


