"""Qiuby Zhukhi 2020"""
from simplekml import Kml, IconStyle
from subprocess import Popen,PIPE,STDOUT
from shutil import move as pindah
from os import path, listdir,makedirs, scandir
placemark = Kml()

mypath = "E:\\arif data"
last_element = mypath.split("\\")[-1]
deskripsi = ""
file_saved = f"{mypath}/{deskripsi}{last_element}.kml"
move_files_no_coordinate = True

def myplacemark(nama=None, directory_file=None, kordinat=None):
    des = f'<![CDATA[<img style="max-width:500px;" src="file:///{directory_file}">]]>'
    styles = f"""<table border="0">
  <tr><td><b>FileName</b></td><td>{nama}</td></tr>"""
    pl = placemark.newpoint(name=nama,
                       coords=kordinat,
                       description=des)
    #pl.style.iconstyle.icon.href =

def real_path(file_name):
    return path.dirname(path.abspath(__file__)) + file_name

def Mycmd(cmd=None):
    prosess = Popen(
        cmd, stdout=PIPE, stderr=STDOUT,shell=True
    ).stdout
    return prosess

def getGPSPostion(tooldir=real_path("/tools/exiftool.exe"), input_files=None):
    dict = {}
    cmd = f'{tooldir} -filename -GPSPosition -n "{input_files}"'
    for i in Mycmd(cmd):
        keys = i.strip().decode().split(":")[0].strip()
        values = i.strip().decode().split(":")[1].strip()
        dict[keys] = values
    return dict

def scandirs(pathku=None):
    link_files = []
    for entry in listdir(pathku):
        path_files = path.join(pathku, entry)
        if(path.isfile(path_files)):
            link_files.append(path_files)
    return link_files

def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for f in scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

def makedir(target_Files=None, toDir=None):
    makedirs(name=f"{toDir}", exist_ok=True)
    pindah(target_Files, toDir)
    print(f"Move: {target_Files}\n To: {toDir}\r\n")

def get_coordinat_test(list_files=[]):
    for list_path in list_files:
        details_foto = getGPSPostion(input_files=list_path)
        file_name = details_foto.get("File Name")
        try:
            lat, long = details_foto.get("GPS Position").split(" ")
            if (len(lat) and len(long) != 0):
                print(f"Membuat Placemark {file_name}")
                myplacemark(nama=file_name, kordinat=[(long, lat)], directory_file=list_path)
        except:
            print(f"Not Found GPS in: {file_name}")
            if (move_files_no_coordinate):
                link_moved = list_path[:list_path.rfind("\\") or list_path.rfind("/")]
                makedir(target_Files=list_path, toDir=f"{link_moved}/NO COORDINATE")

def getAllFiles():
    subfolders,files = run_fast_scandir(mypath, [".jpg"])
    get_coordinat_test(files)
    placemark.save(file_saved)

def main():
    list_files = scandirs(pathku=mypath)
    get_coordinat_test(list_files)
    print(f"SAVED FILES: {mypath}")
    placemark.save(file_saved)
# main()
getAllFiles()