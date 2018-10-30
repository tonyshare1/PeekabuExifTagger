import os
import re
import subprocess
import piexif
from PIL import Image

'''problem to be resolved
1. mp4 files are skipped => may need to manipulate thru exiftool directly in command line
    done by executing
    #exiftool -*Date="2016:10:23 20:06:34.33-08:00" vid.mp4

2. png file comes in but can't be processed by piexif
   could save to jpg first & encode the exif to attach on it

3. may directly call exif tool without importing piexif????

'''

#exiftool -ExifIFD:DateTimeOriginal hasExif.JPG
def exifToolextractField(field_item, file_name):
    out = subprocess.check_output(["exiftool", field_item, file_name])
    return out

def exifToolsetField(field_item, file_name):
    out = subprocess.check_output(["exiftool", field_item, file_name,'-overwrite_original'])

def checkExifDateExist( file_name ):
    date_pat = re.compile("[\w]+([\d]+\:[\d]+\:[\d]+ [\d]+\:[\d]+\:[\d]+)")
    out = exifToolextractField("DateTimeOriginal", file_name)
    result = date_pat.search(out)

    if result:
        if result.group(1)=="0000:00:00 00:00:00":
            print result.group(1)
            return False
        else:
            print result.group(1)
            return True
    else:
        #Not even have Date TAG
        print "not even have tag"
        return False



print exifToolextractField("-ExifIFD:DateTimeOriginal", "hasExif.mp4")
print checkExifDateExist("hasExif.mp4")
exit()

def setNullExifTime( composed_date ):
    zeroth_ifd = {piexif.ImageIFD.Make: u"Canon",
              piexif.ImageIFD.XResolution: (96, 1),
              piexif.ImageIFD.YResolution: (96, 1),
              piexif.ImageIFD.Software: u"piexif"
              }
    exif_ifd = {piexif.ExifIFD.DateTimeOriginal: composed_date,
            piexif.ExifIFD.LensMake: u"LensMake",
            piexif.ExifIFD.Sharpness: 65535,
            piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
            }
    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           piexif.GPSIFD.GPSAltitudeRef: 1,
           piexif.GPSIFD.GPSDateStamp: composed_date,
           }
    first_ifd = {piexif.ImageIFD.Make: u"pkbdate_conversion",
             piexif.ImageIFD.XResolution: (40, 1),
             piexif.ImageIFD.YResolution: (40, 1),
             piexif.ImageIFD.Software: u"piexif"
             }

#exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd}
    exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd}
    return exif_dict

def composeDateStr( date_dct ):
    composed_date="{0}:{1}:{2} {3}:{4}:{5}".format(date_dct['yy'],date_dct['mm'],date_dct['dd'],
                                                  date_dct['hh'],date_dct['mn'],date_dct['sc'])
    return composed_date




'''"0Y1M20D-20160520-1-001"'''
pkb_jpg=re.compile("[\d]+Y[\d]+M[\d]+D-([\d]+)-[\d]+-[\d]+.[jJ][pegPEG]+")
pkb_png=re.compile("([\d]+Y[\d]+M[\d]+D-([\d]+)-[\d]+-[\d]+).[PNGpng]+")
pkb_mp4=re.compile("([\d]+Y[\d]+M[\d]+D-([\d]+)-[\d]+-[\d]+).[mp4]+")

file_list = []
date_dct={
    'yy':"2000",
    'mm':"01",
    'dd':"01",
    'hh':"00",
    'mn':"00",
    'sc':"00",
}
for dirPath, dirNames, fileNames in os.walk("pngdata/"):
    #print dirPath
    for (i,f) in enumerate(fileNames):

        print '----------------START-------------({0},{1})--'.format(i,len(fileNames))
        ''' Read PNG, save to JPG'''
        png_exist=pkb_png.search(f)
        if png_exist:
            full_path = os.path.join(dirPath,f)
            img = Image.open(full_path)
            f = png_exist.group(1)+".jpg"

            sv_full_path = os.path.join(dirPath,f)
            print "===Convert PNG to JPG=== "+f
            img.save(sv_full_path)

        ''' Read JPG, convert to exif embedded JPG'''
        jpg_exist = pkb_jpg.search(f)
        mp4_exist = pkb_mp4.search(f)
        if jpg_exist:
            print "JPG File to be Handled: "+ f
            full_path = os.path.join(dirPath,f)


            # Extract existing exif
            exif_dict = piexif.load(full_path)

            if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:

                exif_date = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]
                date_time_ar = exif_date.split()
                date_ar = date_time_ar[0].split(':')
                time_ar = date_time_ar[1].split(':')
                date_dct['yy'] = date_ar[0]
                date_dct['mm'] = date_ar[1]
                date_dct['dd'] = date_ar[2]

                date_dct['hh'] = time_ar[0]
                date_dct['mn'] = time_ar[1]
                date_dct['sc'] = time_ar[2]

                print "Date exists: " + exif_date
                print "No further actions"

            else:
                if exif_dict == None:
                    print "EXIF is NONE"
                file_name_date=jpg_exist.group(1)
                date_dct['yy'] = file_name_date[0:4]
                date_dct['mm'] = file_name_date[4:6]
                date_dct['dd'] = file_name_date[6:8]
                ''' No change
                date_dct['hh']
                date_dct['mn']
                date_dct['sc']
                '''
                composed_date= composeDateStr(date_dct)
                print "Date NOT exists: composed date: " + composed_date

                #write EXIF in
                im = Image.open(full_path)



                exif_bytes = piexif.dump(setNullExifTime(composed_date))
                im.save(full_path, exif=exif_bytes)
                print "jpg saved"

        elif mp4_exist:
            print "mp4 File to be Handled: "+ f
            full_path = os.path.join(dirPath,f)
            file_name_date=mp4_exist.group(2)
            print file_name_date
            date_dct['yy'] = file_name_date[0:4]
            date_dct['mm'] = file_name_date[4:6]
            date_dct['dd'] = file_name_date[6:8]

            composed_date = composeDateStr(date_dct)
            print "Date NOT exists: composed date: " + composed_date

            #exiftool -xmp:CreateDate="2016:10:23 20:06:34.33" vid.mp4
            #exiftool -xmp:ModifyDate="2016:10:23 20:06:34.33" vid.mp4
            #exiftool -xmp:dateTimeOriginal="2016:10:23 20:06:34.33-08:00" vid.mp4
            #exiftool -QuickTime:ModifyDate="2016:10:23 20:06:34.33-08:00" vid.mp4

            #all time
            #exiftool -*Date="2016:10:23 20:06:34.33-08:00" vid.mp4

            #subprocess.check_call(["exiftool", '-xmp:CreateDate="{0}"'.format(composed_date), full_path ,'-overwrite_original'])
            #subprocess.check_call(["exiftool", '-xmp:ModifyDate="{0}"'.format(composed_date), full_path ,'-overwrite_original'])
            #subprocess.check_call(["exiftool", '-xmp:dateTimeOriginal="{0}"'.format(composed_date), full_path ,'-overwrite_original'])

            exifToolsetField('-*Date="{0}"'.format(composed_date), full_path)
            #subprocess.check_call(["exiftool", '-*Date="{0}"'.format(composed_date), full_path ,'-overwrite_original'])
            print "mp4 saved"
        #print '----------------END---------------'
