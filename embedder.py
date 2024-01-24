# -*- coding: utf-8 -*-
"""
Created on Fri May 26 22:56:29 2023

@author: Nicholas Gower
"""
openFiles=True
download_videos=False
delete_invalid_videos=False
convert_videos=False
make_backup=False
append_embedded_videos=True
restore_backup=False

import pathlib
import bs4
import os
path=pathlib.Path("lindyhopmoves.com")



#https://realpython.com/get-all-files-in-directory-python/
for file in path.rglob("*"):
    
    
    fileSplitted=os.path.splitext(file)
    extension=fileSplitted[-1]
    
    if extension==".html" and "index" in fileSplitted[0]:
        print(file)
        try:
            
            #print(file)
            backup_location=pathlib.Path(file.parent,"backup.html")
            if openFiles:
                if restore_backup:
                    try:
                        backup=open(backup_location,'r')
                        text=open(file,'w')
                        text.write(backup.read())
                        backup.close()
                        text.close()
                    except FileNotFoundError:
                        pass
                text=open(file,'r')
                if make_backup:
                   
                    text_backup=open(backup_location,'w')
                    text_new=open(file,'r')
                    text_backup.write(text_new.read())
                    text_new.close()
                    text_backup.close()
                    
                    
                soup=bs4.BeautifulSoup(text.read(),'html.parser')
                text.close()
                embedded_videos=soup.find_all("iframe")
                
                if len(embedded_videos)>0:
                    #print(embedded_videos)
                    for frame in embedded_videos:
                        src=frame['src']
                        if "www.youtube.com" in src:
                            print(frame)
                            parent=frame.parent
                            video_url=src
                            video_id=src[30:41]
                            embedded_video_location=  "video_archive/{}".format(video_id)
                            checked_file="lindyhopmoves.com/{}".format(embedded_video_location)
                            if not os.path.isfile(checked_file+".webm") and delete_invalid_videos:
                                try:
                                    if os.path.getsize(checked_file+".webm")<500:
                                        #print("{} deleted".format(video_id))
                                        os.remove("lindyhopmoves.com/video_archive/{}.webm".format(video_id))
                                        #os.remove("lindyhopmoves.com/video_archive/{}.webm".format(video_id))
                                        os.remove("lindyhopmoves.com/video_archive/{}.txt".format(video_id))
                                except FileNotFoundError:
                                    pass
                                #print("video not found:{}".format(video_id))
                            if download_videos:
                                #video_url=frame['src']
                                os.system('yt-dlp {} -o "%(id)s" -f "bv[ext=webm]+ba[ext=webm]" --remux-video "webm" --download-archive "lindyhopmoves.com/video_archive/{}.txt"  --write-description --write-info-json --write-playlist-metafiles -P "lindyhopmoves.com/video_archive"'.format(src,video_id))
                            if convert_videos:
                                os.system("ffmpeg -i lindyhopmoves.com/video_archive/{}.mkv lindyhopmoves.com/video_archive/{}.webm".format(video_id,video_id))
                           
                                print("backup made:{}".format(file))
                            if append_embedded_videos:
                                if len(parent)==1 or True:
                                    text_write=open(file,'wb')
                                    #video_embed_format="""<video width="560px" height="315px" controls="controls"/><source src="../video_archive/{}.webm"type="video/webm"> </video>""".format(video_id)
                                    
                                    new_soup=bs4.BeautifulSoup("",'html.parser')
                                    #embedded_video=bs4.BeautifulSoup(video_embed_format.format(video_id),'html.parser')
                                    
                                    embedded_video=new_soup.new_tag("video",width="560px",height="315px",controls="controls")
                                    
                                    embedded_video.append(new_soup.new_tag("source",src="""../video_archive/{}.webm""".format(video_id),type="video/webm"))
                                    
                                    print("video could be embedded!")
                                    
                                    new_soup.append(embedded_video)
                                    parent.append(new_soup.new_tag("br"))
                                    parent.append(embedded_video)
                                    
                                    
                                    text_write.write(str(soup).encode('utf-8'))
                                    text_write.close()
                            
                            
                                
                            
                                
                
        except UnicodeDecodeError:
            print("UnicodeError")
    