import sys
import os
import re
import shutil
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

videos = ['.MP4', '.MOV']
images = ['.JPG', '.JPEG', '.PNG']
exif_images = ['.JPG', '.JPEG']
regex = re.compile(r"(\d\d\d\d)-(\d\d)-(\d\d) (\d\d)\.(\d\d)\.(\d\d)(.*)?\.")
regex2 = re.compile(r"(\d\d\d\d)-(\d\d)-(\d\d)")
folder = sys.argv[1] if len(sys.argv) > 1 else ""
for root, dirs, files in os.walk(folder):
	for file in files:
		print(file, end='')
		path = os.path.join(folder, file)
		prefix = ''
		#print("\tMATCH", end='')
		if os.path.splitext(file)[1].upper() in images:
			prefix = "IMG"
		elif os.path.splitext(file)[1].upper() in videos:
			prefix = "VID"
		if 'pano' in file.lower() or 'stitch' in file.lower():
			prefix = "PANO"
		rename = prefix
		match = re.match(regex, file)
		match2 = re.match(regex2, file)
		if match:			
			#print('\t', match.groups(), end='')
			year = match.groups()[0]
			month = match.groups()[1]
			day = match.groups()[2]
			hour = match.groups()[3]
			minute = match.groups()[4]
			second = match.groups()[5]
			suffix = match.groups()[6].strip().strip('-_')
			rename += '_'+year+month+day+'_'+hour+minute+second
			if suffix:
				rename += '_'+suffix
		elif match2:
			times = []
			if os.path.splitext(file)[1] in exif_images:
				exif = Image.open(path)._getexif()
				for (k, v) in exif.items():
					# print(TAGS.get(k), '=', v)
					if TAGS.get(k) in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']:
						times.append(datetime.datetime.strptime(v, "%Y:%m:%d %H:%M:%S"))
			times.append(datetime.datetime.fromtimestamp(os.path.getatime(path)))
			times.append(datetime.datetime.fromtimestamp(os.path.getctime(path)))
			times.append(datetime.datetime.fromtimestamp(os.path.getmtime(path)))
			try:
				ymdhms = sorted(times)[0].strftime("%Y%m%d_%H%M%S")
			except IndexError:
				for (k, v) in exif.items():
					print(TAGS.get(k), '=', v)
				exit()
			rename += '_'+ymdhms
		if match or match2:
			rename += os.path.splitext(file)[1].lower()
			print('\tRENAMED', rename, end='')
			shutil.move(path, os.path.join(folder, rename))
			print()
