#OCR 字符检测

请在这里介绍代码用途和用法
第一个更新说明：此次添加了用sift特征进行定位并判断是否是驾驶证然后进行文本检测的简单流程
1.代码放在了／code目录下，／img_correct目录下是测试的图片，／template目录是两个行驶证的模板，／locate为定位图片
2.／code 目录下，如果没有运行过cv的环境，需要首先执行“./setenv.sh”
3.执行“./build.sh”，会重新生成LFocr.so
4.打开test.py文件，在加载so包的时候改为正确的路径，然后在“LFocr.textCrop(）”的调用时分别传入定位图片／模板文件／测试图片的完整路径，即可return到一个元素为int的list，每四个int表示一个rectangle，顺序依次为top-left-bottom-right.