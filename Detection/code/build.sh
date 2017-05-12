
#export PKG_CONFIG_PATH="/mydata/opencv3"
export PKG_CONFIG_PATH="/usr/local/lib"
lBuildOptions=`pkg-config --cflags --libs opencv`
lOutName=LFocr.so

echo $lBuildOptions

g++ -std=gnu++11 -g -shared -fPIC -o $lOutName *.cpp ./common/*.cpp ./dbscan/*.cpp ./json/*.cpp ./mser/*.cpp ./sift/*.cpp $lBuildOptions -Lpython2.7m -DTEST -lc -lstdc++

