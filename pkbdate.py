import os
import re
import subprocess


'''problem to be resolved
1. mp4 files are skipped => may need to manipulate thru exiftool directly in command line
    done by executing
    #exiftool -*Date="2016:10:23 20:06:34.33-08:00" vid.mp4

2. png file comes in but can't be processed by piexif
   could save to jpg first & encode the exif to attach on it
   ==> need to save png to jpg

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


def composeDateStr( date_dct ):
    composed_date="{0}:{1}:{2} {3}:{4}:{5}".format(date_dct['yy'],date_dct['mm'],date_dct['dd'],
                                                  date_dct['hh'],date_dct['mn'],date_dct['sc'])
    return composed_date




'''"0Y1M20D-20160520-1-001"'''
pkb_jpg=re.compile("[\d]+Y[\d]+M[\d]+D-([\d]+)-[\d]+-[\d]+.[jJ][pegPEG]+")
pkb_png=re.compile("[\d]+Y[\d]+M[\d]+D-([\d]+)-[\d]+-[\d]+.[PNGpng]+")
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
for dirPath, dirNames, fileNames in os.walk("scan_fold/"):
    #print dirPath
    for (i,f) in enumerate(fileNames):

        print '----------------START-------------({0},{1})--'.format(i,len(fileNames))

        png_exist = pkb_png.search(f)
        jpg_exist = pkb_jpg.search(f)
        mp4_exist = pkb_mp4.search(f)
        if jpg_exist or png_exist or mp4_exist:
            print "JPG/PNG/MP4 File to be Handled: "+ f
            full_path = os.path.join(dirPath,f)


            dateTimeOrigin = exifToolextractField("-DateTimeOriginal", full_path)


            if len(dateTimeOrigin) >0 :

                date_time_ar = dateTimeOrigin.split()
                date_ar = date_time_ar[-2].split(':')
                time_ar = date_time_ar[-1].split(':')
                #print (date_time_ar, date_ar, time_ar)
                date_dct['yy'] = date_ar[0]
                date_dct['mm'] = date_ar[1]
                date_dct['dd'] = date_ar[2]

                date_dct['hh'] = time_ar[0]
                date_dct['mn'] = time_ar[1]
                date_dct['sc'] = time_ar[2]

                print "Date exists: " + str(date_ar) + str(time_ar)
                print "No further actions"

            else:
                if jpg_exist:
                    file_name_date=jpg_exist.group(1)
                elif png_exist:
                    file_name_date=png_exist.group(1)
                elif mp4_exist:
                    file_name_date=mp4_exist.group(2)

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
                exifToolsetField('-CreateDate="{0}"'.format(composed_date), full_path)
                exifToolsetField('-ModifyDate="{0}"'.format(composed_date), full_path)
                exifToolsetField('-dateTimeOriginal="{0}"'.format(composed_date), full_path)


        elif 0 : #mp4_exist:
            print "mp4 File to be Handled: "+ f
            full_path = os.path.join(dirPath,f)

            dateTimeOrigin = exifToolextractField("-DateTimeOriginal", full_path)


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
