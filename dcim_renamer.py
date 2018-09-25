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
re_ymdhms = re.compile(r"(\d\d\d\d)-(\d\d)-(\d\d) (\d\d)\.(\d\d)\.(\d\d)(.*)?\.")

folder = sys.argv[1] if len(sys.argv) > 1 else ""
for root, dirs, files in os.walk(folder):
	for file in files:
		print(file, end='')
		path = os.path.join(folder, file)
		rename = ''
		times = []

		prefix = ''
		if os.path.splitext(file)[1].upper() in images:
			prefix = "IMG"
		elif os.path.splitext(file)[1].upper() in videos:
			prefix = "VID"
		if 'pano' in file.lower() or 'stitch' in file.lower():
			prefix = "PANO"
		rename = prefix

		ymdhms = re.match(re_ymdhms, file)
		if ymdhms:
			year = ymdhms.groups()[0]
			month = ymdhms.groups()[1]
			day = ymdhms.groups()[2]
			hour = ymdhms.groups()[3]
			minute = ymdhms.groups()[4]
			second = ymdhms.groups()[5]
			time = year+month+day+hour+minute+second
			times.append(datetime.datetime.strptime(time, "%Y%m%d%H%M%S"))

		if os.path.splitext(file)[1] in exif_images:
			exif = Image.open(path)._getexif()
			for (k, v) in exif.items():
				# print(TAGS.get(k), '=', v)
				if TAGS.get(k) in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']:
					times.append(datetime.datetime.strptime(v, "%Y:%m:%d %H:%M:%S"))

		times.append(datetime.datetime.fromtimestamp(os.path.getatime(path)))
		times.append(datetime.datetime.fromtimestamp(os.path.getctime(path)))
		times.append(datetime.datetime.fromtimestamp(os.path.getmtime(path)))

		if times:
			try:
				retime = sorted(times)[0].strftime("%Y%m%d_%H%M%S")
				rename += '_'+retime
			except IndexError:
				for (k, v) in exif.items():
					print(TAGS.get(k), '=', v)
				exit()

			ext = os.path.splitext(file)[1].lower()

			new_path = os.path.join(folder, rename+ext)
			if os.path.exists(new_path):
				suffix = 1
				while os.path.exists(new_path):
					new_path = os.path.join(folder, rename+'_'+str(suffix)+ext)
					suffix += 1

			shutil.move(path, new_path)
			print('\tRENAMED', rename+ext, end='')			
		print()
