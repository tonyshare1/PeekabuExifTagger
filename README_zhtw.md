# Peekabu Photo EXIF modifier
  此script用於處理由Peekabu備份器取得的照片，EXIF資訊時有時無問題。修正後可於Google Photo以正確的時間順序顯示  
  Peekabu:
    https://peekaboomoments.com/  
  備份器文章 & SW:
    https://www.ptt.cc/bbs/BabyMother/M.1492746862.A.F94.html  
    Backup SW: https://goo.gl/2mZpuk  
  照片可能有正確的EXIF，也可能沒有EXIF，但都存在正確的時間檔名。修正後上傳至Google Photo可以有正確的時間順序  
  照片的檔名長:  
    *Y*M*D-YYYYMMDD-*-***.jpg

  Python將會最下列步驟  
  對所有的jpg, png, mp4檔案:  
  + 如果沒有exif的時間日期資訊，則擷取日期檔名，造出時間放入EXIF中
  + 如果有exif的時間日期資訊，維持原樣

  jpg包含jpg, JPG, jpeg, JPEG.  
  png包含png, PNG.  
  mp4包含mp4, MP4.  



# Require
  1. Python 2.7 (需要自行安裝)
  2. Exiftool, (WINDOWS不需安裝, macosX需要自行安裝)
     https://www.sno.phy.queensu.ca/~phil/exiftool/

# 如何使用
  1. 將要處理的照片放入scan_fold
  2. in WINDOWS: 執行exec_pkbdate.bat  
     in MAC: 在terminal中執行: python pkbdate.py
  3. Wait till it's finish

# Credit:
  Exiftool出自https://www.sno.phy.queensu.ca/~phil/exiftool/