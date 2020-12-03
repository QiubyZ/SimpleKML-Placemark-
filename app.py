"""Qiuby Zhukhi 2020"""
from simplekml import Kml
from subprocess import Popen,PIPE,STDOUT
from shutil import move as pindah
from os import path, listdir,makedirs, scandir
from multiprocessing import Pool, Process
mypath = input("Path Foto: ")
last_element = mypath.split("\\")[-1]

#------------ [ SETTIINGS ] ---------------
add_jpg_to_kmz = False
move_files_no_coordinate = True
no_coordinate_folder = "NO COORDINATE"
titik_direct = f"{mypath}/link_foto_langsung_{last_element}.kml"
titik_kmz = f"{mypath}/link_foto_file_{last_element}.kml"
kompilasi_kmz = f"{mypath}/kompilasi_{last_element}.kmz"
thread = 3
view_photo_no_coordinate = False

#--------- [ KONFIGURASI KML ] ------------
activate_titik_direct = True
activate_titik_kmz = True
activate_kompilasi_kmz = False
#------------------------------------------


placemark = Kml()
kmz_placemark = Kml()
titik_files = Kml()
list_photo_no_coordinate = []
list_photo_yes_coordinate = []
numb_foto_koordinat = 0
numb_tidak_ada = 0
total = None

def logs():
    var = f"\r\n{last_element}\nFOTO BERKOORDINAT: {numb_foto_koordinat}\nTIDAK ADA KOORDINAT: {numb_tidak_ada}\nJumlah semua foto: {total}\n"+"LIST FOTO TIDAK ADA KOORDINAT: \n"+("\n".join([i for i in list_photo_no_coordinate]) if(view_photo_no_coordinate) else "Logs: "+mypath)
    with open(titik_direct.replace(".kml", ".txt"), "w") as catatan:
        catatan.write(var)
        catatan.close()
    print(var)

def myplacemark(nama=None, directory_file=None, kordinat=None):
    des = f'<![CDATA[<img style="max-width:500px;" src="file:///{directory_file}">]]>'
    styles = f"""<table border="0">
  <tr><td><b>FileName</b></td><td>{nama}</td></tr>"""

    #<img style="max-width:500px;" src="files/TimePhoto_20201102_100725.jpg">
    pl = placemark.newpoint(name=nama,
                       coords=kordinat,
                       description=des)

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

def KMZFiles(name=None, kordinat=None, directory_file=None, file_name=None, add_photo=add_jpg_to_kmz):
    kmz_placemark.newpoint(name=name,
             coords=kordinat,
             description=f'<img style="max-width:500px;" src="files/{file_name}">')
    if(add_photo):
        placemark.addfile(directory_file)

def titik_file(name=None, kordinat=None, file_name=None):
    titik_files.newpoint(name=name,
             coords=kordinat,
             description=f'<img style="max-width:500px;" src="files/{file_name}">')

def kml_pilihan(**params):
    nama = params.get("nama")
    directory_file = params.get("directory_file")
    kordinat = params.get("kordinat")

    if(activate_titik_direct):
        myplacemark(nama=nama, directory_file=directory_file, kordinat=kordinat)
    if(activate_titik_kmz):
        titik_file(name=nama, kordinat=kordinat, file_name=nama)
    if(activate_kompilasi_kmz):
        KMZFiles(name=nama, kordinat=kordinat, directory_file=directory_file, add_photo=add_jpg_to_kmz)

def save_files_kml():
    if(activate_titik_direct):
        placemark.save(titik_direct)
    if(activate_titik_kmz):
        titik_files.save(titik_kmz)
    if(activate_kompilasi_kmz):
        kmz_placemark.save(kompilasi_kmz)

process_thread = []
Pool(thread)
def get_coordinat_test(list_files=[]):
    global numb_tidak_ada, numb_foto_koordinat, total
    for list_path in list_files:
        details_foto = getGPSPostion(input_files=list_path)
        file_name = details_foto.get("File Name")
        if(no_coordinate_folder not in list_path):
            try:
                lat, long = details_foto.get("GPS Position").split(" ")
                if (len(lat) and len(long) != 0):
                    numb_foto_koordinat += 1
                    print(f"Membuat Placemark {file_name}")
                    kml_pilihan(nama=file_name, kordinat=[(long,lat)], directory_file=list_path)
                    #myplacemark(nama=file_name, kordinat=[(long, lat)], directory_file=list_path)
                    # titik_file(name=file_name,
                    #          kordinat=[(long, lat)],
                    #          directory_file=list_path,
                    #          file_name=file_name.split("\\")[-1],
                    #     )
#                     pross = Process(target=myplacemark(), args=(file_name, [(long, lat)], list_path)).start()
                    # KMZFiles(name=file_name,
                    #          kordinat=[(long, lat)],
                    #          directory_file=list_path,
                    #          file_name=file_name.split("\\")[-1],
                    #     )
                    list_photo_yes_coordinate.append(list_path)
            except:
                print(f"Not Found GPS in: {file_name}")
                numb_tidak_ada += 1
                list_photo_no_coordinate.append(list_path)
                if (move_files_no_coordinate):
                    link_moved = list_path[:list_path.rfind("\\") or list_path.rfind("/")]
                    makedir(target_Files=list_path, toDir=f"{link_moved}/{no_coordinate_folder}")
    total = numb_tidak_ada + numb_foto_koordinat
    logs()

def getAllFiles():
    subfolders,files = run_fast_scandir(mypath, [".jpg"])
    get_coordinat_test(files)
    if(numb_foto_koordinat > 0):
        save_files_kml()
        # placemark.save(titik_direct)
        # titik_files.save(titik_kmz)
#        kmz_placemark.savekmz(kompilasi_kmz, format=False)

def main():
    list_files = scandirs(pathku=mypath)
    get_coordinat_test(list_files)
    print(f"SAVED FILES: {mypath}")

getAllFiles()

