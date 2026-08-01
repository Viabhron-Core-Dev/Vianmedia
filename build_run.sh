kotlinc -cp ~/.gradle/caches/modules-2/files-2.1/androidx.media3/media3-common/1.3.1/3b3c3b067f920261f22d9972304dfa34fa9cd3b4/media3-common-1.3.1.jar get_media3_videosize.kt -include-runtime -d get_media3_videosize.jar
java -cp get_media3_videosize.jar:$(find ~/.gradle/caches/ -name "media3-common-*.jar" | head -n 1) Get_media3_videosizeKt
