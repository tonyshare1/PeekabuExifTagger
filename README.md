# Peekabu Photo EXIF modifier

  Some user of Peekabu backup their photos to their own disk.
  These backed up photo may or may NOT have proper EXIF, but they do have proper DATE file name.
  This python script does following things.

  For all jpg, png, mp4 files, if exif date/time doesn't exist, script will parse DATE on file name & put it into EXIF tag.

  jpg includes jpg, JPG, jpeg, JPEG.
  png includes png, PNG.
  mp4 includes mp4, MP4

  File names may looks like:
  *Y*M*D-YYYYMMDD-*-***.jpg

# Require
  1. Python 2.7
  2. Exiftool, need to install 
     https://www.sno.phy.queensu.ca/~phil/exiftool/

# How to use?
  1. Place all backed up file inside scan_fold
  2. run > python pkbdate.py
  3. Wait till it's finish
