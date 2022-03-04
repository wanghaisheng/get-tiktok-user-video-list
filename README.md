# get-tiktok-user-video-list
scrape tiktok/douyin video list from specific user or keyword

以**https://www.douyin.com/user/MS4wLjABAAAAUpIowEL3ygUAahQB47vy8sbYMB1eIr40qtlDwxhxFGww**为例

## feautures    

*  support batch download from user realtime and archives
*  support batch download from search page realtime and archives
*  support batch download from tags realtime and archives
*  support  tiktok/douyin username nickname fuzzy search
*  support tiktok/douyin shared message,shorten url,normal url and batch urls
*  support unofficial API mixed with selenium 
*  support popular free cloud video storage platform mirror/backup

## 1. unofficial douyin/tiktok api


## 2. selenium模拟


## 手动过程
1.打开url
https://www.douyin.com/user/MS4wLjABAAAAUpIowEL3ygUAahQB47vy8sbYMB1eIr40qtlDwxhxFGw
2.不停的下拉，刷新出所有视频
这里我用了自动下拉的插件

3.找到视频的xpath
//*[@id="root"]/div/div[2]/div/div/div[4]/div[1]/div[2]/ul/li/a/@href

4.爬取所有的视频url
```
Text
//www.douyin.com/video/7069979868804418851
//www.douyin.com/video/7069604646809062690
//www.douyin.com/video/7069229735154306344
//www.douyin.com/video/7068854242823441704
//www.douyin.com/video/7068483482254642447
//www.douyin.com/video/7068109876249070863
//www.douyin.com/video/7067740251527105827
//www.douyin.com/video/7067364826183519523
//www.douyin.com/video/7067009589950090530
//www.douyin.com/video/7024672984824679680
.........
.........
```

