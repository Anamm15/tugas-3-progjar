import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def upload(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                raise Exception('filename tidak boleh kosong')
            
            if (params[1] == ''):
                raise Exception('isi file tidak boleh kosong')
            
            fp = open(f"{filename}",'wb+')
            fp.write(base64.b64decode(params[1]))
            fp.close()
            data_message = f"{filename} berhasil diupload"
            return dict(status='OK', data=data_message)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def delete(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                raise Exception('filename tidak boleh kosong')
            
            os.remove(filename)
            data_message = f"{filename} berhasil dihapus"
            return dict(status='OK',data=data_message)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))