# Peekabu Photo EXIF modifier

  Some user of Peekabu backup their photos to their own disk.  
    https://peekaboomoments.com/  
    How to backup (Chinese Only): https://www.ptt.cc/bbs/BabyMother/M.1492746862.A.F94.html  
    Backup SW: https://goo.gl/2mZpuk  
  These backed up photo may or may NOT have proper EXIF, but they do have proper DATE file name. 
    File names may looks like:  
    *Y*M*D-YYYYMMDD-*-***.jpg  

  This python script does following things.  
  For all jpg, png, mp4 files,  
  + if exif date/time doesn't exist, script will parse DATE on file name & put it into EXIF tag.
  + if exif date/time exists, do nothing. Keep the original TAG date/time.

  jpg includes jpg, JPG, jpeg, JPEG.  
  png includes png, PNG.  
  mp4 includes mp4, MP4.  



# Require
  1. Python 2.7  
  2. Exiftool, (Windows user not required, already placed 1 copy, exiftool_win.   
     Mac osX user needs to install)   
     https://www.sno.phy.queensu.ca/~phil/exiftool/

# How to use?
  1. Place all backed up file inside scan_fold
  2. In Windows: execute exec_pkbdate.bat  
     In mac osX: run in terminal > python pkbdate.py  
  3. Wait till it's finish

# Credit:
  Exiftool belongs to https://www.sno.phy.queensu.ca/~phil/exiftool/