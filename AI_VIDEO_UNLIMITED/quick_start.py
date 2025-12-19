من moviepy.editor import * 
print("🎬 نظام مونتاج الفيديو جاهز!") 
clip = ColorClip(size=(1280,720), color=(40,60,120), duration=3) 
clip.write_videofile("videos/output/test_video.mp4") 
print("✅ تم إنشاء أول فيديو") 
