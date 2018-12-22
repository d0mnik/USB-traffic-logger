#!venv/bin/python3.6

# imports
import psutil
import inotify.adapters
import sys
from multiprocessing import Process, Manager
import datetime


class Device:
    def __init__(self,mountpoint,partition):
        self.mountpoint = mountpoint
        self.partition = partition

def list_usb_devices():
    devices = []
    for p in psutil.disk_partitions():
        #name = p.mountpoint.split("/")[-1] # get device name
        if p.mountpoint == '/': # skip /
            continue
        devices.append(Device(p.mountpoint,p.device))
    return devices


def listener(mount,partition,control_list):
    try:
        i = inotify.adapters.InotifyTree(mount)
        with open("/root/Documents/{}.log".format(datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")),"w") as delog:
            delog.write("USB data log for {} at {}\n\n".format(mount,datetime.datetime.now().isoformat()))
            for event in i.event_gen(yield_nones=False):
                (_,type_names,path,filename) = event
                if "IN_CREATE" in type_names:
                    delog.write(filename + " was created\n")
            delog.close()
    except inotify.adapters.TerminalEventException: # on umount
        control_list.remove(partition)
        return
    else:
        i = inotify.adapters.Inotify()
        i.add_watch(mount)
        with open("/root/Documents/{}.log".format(datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S") + mount),"w") as delog:
            delog.write("USB data log for {} at {}\n\n".format(mount,datetime.datetime.now().isoformat()))
            for event in i.event_gen(yield_nones=False):
                (_,type_names,path,filename) = event
                #print("Path: {} filename: {} event_type: {}".format(path,filename,type_names))
                if "IN_CREATE" in type_names:
                    delog.write(filename + " was created\n")
            delog.close()
def main():
    manager = Manager()
    control_devices = manager.list([])
    while True:        
        new_devices = list_usb_devices()
        final = [i for i in new_devices if i.partition not in control_devices]
        for device in final:
            control_devices.append(device.partition)
            p = Process(target=listener,args=(device.mountpoint,device.partition,control_devices,))
            p.start()
if __name__ == "__main__":
    main()
    #test()