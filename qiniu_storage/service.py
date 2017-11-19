# -*- coding: utf-8 -*-
import os, time, random, math
from django.utils import timezone
def writeFile(f):
    baseDir = os.path.dirname(os.path.abspath(__name__));
    jpgdir = os.path.join(baseDir, 'static', 'upload');
    random_num = int(math.floor(time.mktime(timezone.now().timetuple()))) + random.randint(0,1000)
    f_split = f.name.split('.')
    extension = ''
    if len(f_split) > 1:
        extension = '.' + f_split[1]
    new_name = str(random_num) + extension
    filePathName = os.path.join(jpgdir, new_name);
    with open(filePathName,'wb') as fobj:
        for chrunk in f.chunks():
            fobj.write(chrunk);
    from upload import qiniu_upload
    qiniu_upload(new_name)
    return new_name