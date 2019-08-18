---
title: linux-0.1-系统安装
date: 2016-12-16 13:52:20
updated: 2018-08-29 23:07:31
tags: Linux
---

# 系统安装

### 挂载建议： 

Linux只要求两个基本分区 `／` 和 `swap`； 

如果`／`足够的，可以在桌面放很多东西而不影响进入 Linux 的速度； 

| 分区       | 大小     | 格式 |
| ---------- | -------- | ---- |
| /boot1⃣️ | 128MB    | ext3 |
| swap       | 2⃣️   |      |
| ／         | 8GB      | ext3 |
| ／home     | 余下全部 | ext3 |

若要安装很多软件最好分配个 `/usr`； 

若要作服务器最好分配较大的 `/var`； 



1⃣️.  `/boot`： 

2018年后的新版本都可以不分； 

可以分配10MB-100MB 

如果硬盘不支持LBA模式，最好挂载/boot于第一个分区，以保稳妥。 

参考：[https://wapbaike.baidu.com/item/boot分区/16830421?ms=1&rid=8645769021174590193](https://wapbaike.baidu.com/item/boot分区/16830421?ms=1&rid=8645769021174590193)



2⃣️. `swap`： 

![Image 20180817 230902](http://ww1.sinaimg.cn/large/006tNc79gy1g60bdmoskaj30d108xglx.jpg)

| 物理内存  | swap   | swap(开启休眠) |
| --------- | ------ | -------------- |
| 2GB       | 2倍RAM | 3倍RAM         |
| >2GB-8GB  | =RAM   | 2倍RAM         |
| >8GB-64GB | 4GB+   | 1.5倍RAM       |
| >64GB     | 4GB+   | 不建议休眠     |



参考：[https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/installation_guide/s2-diskpartrecommend-ppc#id4394007](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/installation_guide/s2-diskpartrecommend-ppc#id4394007) 



开始的几个服务配置：

- 检查*telnet*服务是否启动： 
  
```
# chkconfig telnet --list
```

- 启动*telnet*服务： 
  
```
# chkonfig telnet on
```

开启telnet后在win下可用"> telnet $IP"连接Linux。 

- 检验*FTP*服务当前状态： 
  
```
# service vsftpd status 
```

- 开启*FTP*服务： 
  
```
# service vsftpd start
```
