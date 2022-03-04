# get-tiktok-user-video-list
scrape tiktok/douyin video list from specific user or keyword

以**https://www.douyin.com/user/MS4wLjABAAAAUpIowEL3ygUAahQB47vy8sbYMB1eIr40qtlDwxhxFGww**为例

## unofficial douyin/tiktok api


## selenium模拟


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
//www.douyin.com/video/7066713226418933026
//www.douyin.com/video/7066253111257615656
//www.douyin.com/video/7065882405076208936
//www.douyin.com/video/7065508466718281001
//www.douyin.com/video/7065140796005059875
//www.douyin.com/video/7064768605967224079
//www.douyin.com/video/7064407900021673256
//www.douyin.com/video/7064124813496896783
//www.douyin.com/video/7064028885922467087
//www.douyin.com/video/7063648631672278272
//www.douyin.com/video/7063287304269466920
//www.douyin.com/video/7062916862664772904
//www.douyin.com/video/7062547710208969984
//www.douyin.com/video/7062169730135641379
//www.douyin.com/video/7061802347550264610
//www.douyin.com/video/7061433682833329423
//www.douyin.com/video/7060688239572618531
//www.douyin.com/video/7060325621901053219
//www.douyin.com/video/7059947762191830306
//www.douyin.com/video/7059568307342544162
//www.douyin.com/video/7058810010070945024
//www.douyin.com/video/7058452571668696361
//www.douyin.com/video/7058093557948747023
//www.douyin.com/video/7057718930990812451
//www.douyin.com/video/7057476115044011299
//www.douyin.com/video/7057449530916113698
//www.douyin.com/video/7057121639795903744
//www.douyin.com/video/7057068942875004195
//www.douyin.com/video/7056608420450946338
//www.douyin.com/video/7056235293313076514
//www.douyin.com/video/7055862917450845474
//www.douyin.com/video/7055595838873144576
//www.douyin.com/video/7055493105805528354
//www.douyin.com/video/7055132125254716707
//www.douyin.com/video/7054750753432292608
//www.douyin.com/video/7054378766310608163
//www.douyin.com/video/7054016818498915624
//www.douyin.com/video/7053637077719682304
//www.douyin.com/video/7053280643110767906
//www.douyin.com/video/7052899676206419234
//www.douyin.com/video/7052524537438571817
//www.douyin.com/video/7052168137545911593
//www.douyin.com/video/7051780577594313984
//www.douyin.com/video/7051408583338003746
//www.douyin.com/video/7051038439419989248
//www.douyin.com/video/7050296303649066280
//www.douyin.com/video/7049928775584222464
//www.douyin.com/video/7049553634085866786
//www.douyin.com/video/7049187543098690816
//www.douyin.com/video/7048812869546167587
//www.douyin.com/video/7048436017979837736
//www.douyin.com/video/7048051190969519400
//www.douyin.com/video/7047786976216370473
//www.douyin.com/video/7047716155213057321
//www.douyin.com/video/7047326256248933647
//www.douyin.com/video/7046956255918722344
//www.douyin.com/video/7046588422722538792
//www.douyin.com/video/7046229768471055651
//www.douyin.com/video/7045837915590593826
//www.douyin.com/video/7045463510012202281
//www.douyin.com/video/7045102266537217295
//www.douyin.com/video/7044730101497433378
//www.douyin.com/video/7044361682386193705
//www.douyin.com/video/7043988108156636450
//www.douyin.com/video/7043620575851334952
//www.douyin.com/video/7043225590278753551
//www.douyin.com/video/7042851891939740962
//www.douyin.com/video/7042502877356543232
//www.douyin.com/video/7042133062850727209
//www.douyin.com/video/7041764151487778089
//www.douyin.com/video/7041390481590258985
//www.douyin.com/video/7041021044072729890
//www.douyin.com/video/7040626133624278306
//www.douyin.com/video/7040260859410631970
//www.douyin.com/video/7039907413788609827
//www.douyin.com/video/7039537046678981888
//www.douyin.com/video/7039165027340913955
//www.douyin.com/video/7038794945322306816
//www.douyin.com/video/7038419781770317056
//www.douyin.com/video/7038032873743584546
//www.douyin.com/video/7037661932563795235
//www.douyin.com/video/7037311342688128256
//www.douyin.com/video/7036944155716668687
//www.douyin.com/video/7036565287759596834
//www.douyin.com/video/7036194299008044303
//www.douyin.com/video/7035825419978853666
//www.douyin.com/video/7035432928653937954
//www.douyin.com/video/7035074563465661736
//www.douyin.com/video/7034708330283044111
//www.douyin.com/video/7034338404863118633
//www.douyin.com/video/7033968103222414627
//www.douyin.com/video/7033597679967964450
//www.douyin.com/video/7033226170464275712?previous_page=others_homepage&modeFrom=userPost&cursor=1637723322000&count=10&secUid=MS4wLjABAAAAUpIowEL3ygUAahQB47vy8sbYMB1eIr40qtlDwxhxFGw&enter_method=post
//www.douyin.com/video/7032943642348178729
//www.douyin.com/video/7032838467142929664
//www.douyin.com/video/7032465998389185827
//www.douyin.com/video/7032110825544469801
//www.douyin.com/video/7031740377644240169
//www.douyin.com/video/7031370069691206912
//www.douyin.com/video/7030998549848427776
//www.douyin.com/video/7030718248521944355
//www.douyin.com/video/7030237961216068898
//www.douyin.com/video/7029865696590908713
//www.douyin.com/video/7029611430198381839
//www.douyin.com/video/7029153627239419171
//www.douyin.com/video/7028778314303065384
//www.douyin.com/video/7028407755274865961
//www.douyin.com/video/7028127328173624611
//www.douyin.com/video/7027751599346961705
//www.douyin.com/video/7027735112372604201
//www.douyin.com/video/7027657854211378447
//www.douyin.com/video/7027385293569297664
//www.douyin.com/video/7027330027893165353
//www.douyin.com/video/7026918425138056448
//www.douyin.com/video/7026547891351211279
//www.douyin.com/video/7026273034784738575
//www.douyin.com/video/7025910122534751528
//www.douyin.com/video/7025529635404287266
//www.douyin.com/video/7025059410657430819
//www.douyin.com/video/7024788171594550528
//www.douyin.com/video/7024672984824679680

....
```

