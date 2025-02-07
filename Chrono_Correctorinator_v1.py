import os
import ctypes
import datetime
from ctypes import wintypes
import shutil
import time

print("*" * 150)
print("\n\t\t\t\t\t\tCHRONO CORRECTORINATOR\t\t\t\t\t\t\n")
print("*" * 150)

print("\nPlease use in full or wider window for best experience.")


# Get this block from the Internet to change the creation date of file
def set_creation_time_windows(file_path, creation_time):
    FILE_WRITE_ATTRIBUTES = 0x0100

    handle = ctypes.windll.kernel32.CreateFileW(
        file_path, FILE_WRITE_ATTRIBUTES, 0, None, 3, 0x80, None
    )

    if handle == -1:
        raise ctypes.WinError()

    timestamp = int(creation_time.timestamp() * 10 ** 7) + 116444736000000000
    filetime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)

    success = ctypes.windll.kernel32.SetFileTime(handle, ctypes.byref(filetime), None, None)
    ctypes.windll.kernel32.CloseHandle(handle)

    if not success:
        raise ctypes.WinError()


# Input
print("\n\nEnter the path of the folder including the pictures needed date correction (e.g. C:/Users/user/Pictures).")
print("Hint: It may be copied from the Address Bar on the File Explorer.")
inpt = input("\nInput direction:")

switch2 = True
while switch2:

    if os.path.exists(inpt):
        switch2 = False

    else:
        inpt = input("Invalid path, please try again.\nInput direction:")

os.chdir(inpt)
input_list = os.listdir(inpt)
input_list = tuple(input_list)


# Output
print("\n\nEnter the preferred output path.")
print("If it left blank the Downloads folders is going to be chosen automatically.")
output = input("\nOutput direction:")

switch3 = True
while switch3:

    if len(output) == 0:
        output = "C:\\Users\\user\\Downloads\\Corrected"
        switch3 = False

    elif not os.path.exists(output):
        output = input("Invalid path, please try again.\nOutput direction:")

    elif os.path.exists(output):
        output = output + "\Corrected"
        switch3 = False


start_t = time.time()


# Output folder generation
n = 0
switch1 = True
while switch1:

    if os.path.exists(output):
        n = int(n)
        n += 1
        n = str(n)
        output = output + "(" + n + ")"
        continue

    else:
        os.makedirs(output)
        print(output, "generated\n")
        switch1 = False

temp = output + "\\Temp"
suc = output + "\\Successful"
fail = output + "\\Failure"
suc_im = suc + "\\WA Images"
suc_vid = suc + "\\WA Videos"
suc_sam_im = suc + "\\Samsung Images"
suc_sam_vid = suc + "\\Samsung Videos"

os.makedirs(temp)
os.makedirs(suc)
os.makedirs(fail)


# Progress_counter starting from 1 to avoid 0/0 uncertainty
progress_counter = 1

# Time correction (creation, modification, and access time)
for i in input_list:
    shutil.copy(inpt + "\\" + i, temp)

    try:
        # WhatsApp type image
        if (i[13:15] == "WA") and i[:3] == "IMG":
            if not os.path.exists(suc_im):
                os.makedirs(suc_im)

            y = int(i[4:8])
            m = int(i[8:10])
            d = int(i[10:12])
            shutil.move(temp + "\\" + i, suc_im)

            try:
                new_date = datetime.datetime(y, m, d, tzinfo=datetime.timezone.utc)
                timestamp = new_date.timestamp()
                set_creation_time_windows(suc_im + "\\" + i, new_date)
                os.utime(suc_im + "\\" + i, (timestamp, timestamp))
                print("{:.1f} % \t\t DONE \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, suc_im))

            except:
                shutil.move(suc_im + "\\" + i, fail)
                print("{:.1f} % \t\t ERROR   \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, fail))

        # Whatsapp type video
        elif (i[13:15] == "WA") and i[:3] == "VID":
            if not os.path.exists(suc_vid):
                os.makedirs(suc_vid)

            y = int(i[4:8])
            m = int(i[8:10])
            d = int(i[10:12])
            shutil.move(temp + "\\" + i, suc_vid)

            try:
                new_date = datetime.datetime(y, m, d, tzinfo=datetime.timezone.utc)
                timestamp = new_date.timestamp()
                set_creation_time_windows(suc_vid + "\\" + i, new_date)
                os.utime(suc_vid + "\\" + i, (timestamp, timestamp))
                print("{:.1f} % \t\t DONE \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, suc_vid))

            except:
                shutil.move(suc_vid + "\\" + i, fail)
                print("{:.1f} % \t\t ERROR   \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, fail))

        # Samsung type image
        elif ((i[8] == "_") and (int(i[9:15]) <= 240000)) and (
                os.path.splitext(i)[1] in (".jpg", ".JPG", ".jpeg", ".JPEG")):
            if not os.path.exists(suc_sam_im):
                os.makedirs(suc_sam_im)

            y = int(i[0:4])
            m = int(i[4:6])
            d = int(i[6:8])

            h = int(i[9:11])
            mnt = int(i[11:13])
            sec = int(i[13:15])
            shutil.move(temp + "\\" + i, suc_sam_im)

            try:
                new_date = datetime.datetime(y, m, d, h, mnt, sec, tzinfo=datetime.timezone.utc)
                timestamp = new_date.timestamp()
                set_creation_time_windows(suc_sam_im + "\\" + i, new_date)
                os.utime(suc_sam_im + "\\" + i, (timestamp, timestamp))
                print("{:.1f} % \t\t DONE \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, suc_sam_im))

            except:
                shutil.move(suc_sam_im + "\\" + i, fail)
                print("{:.1f} % \t\t ERROR   \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, fail))

        #Samsung type video
        elif ((i[8] == "_") and (int(i[9:15]) <= 240000)) and (os.path.splitext(i)[1] == (".mp4")):
            if not os.path.exists(suc_sam_vid):
                os.makedirs(suc_sam_vid)

            y = int(i[0:4])
            m = int(i[4:6])
            d = int(i[6:8])

            h = int(i[9:11])
            mnt = int(i[11:13])
            sec = int(i[13:15])
            shutil.move(temp + "\\" + i, suc_sam_vid)

            try:
                new_date = datetime.datetime(y, m, d, h, mnt, sec, tzinfo=datetime.timezone.utc)
                timestamp = new_date.timestamp()
                set_creation_time_windows(suc_sam_vid + "\\" + i, new_date)
                os.utime(suc_sam_vid + "\\" + i, (timestamp, timestamp))
                print("{:.1f} % \t\t DONE \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, suc_sam_vid))

            except:
                shutil.move(suc_sam_vid + "\\" + i, fail)
                print("{:.1f} % \t\t ERROR   \t\t {} moved to {}.".format(
                    progress_counter * 100 / len(input_list), i, fail))

        else:
            shutil.move(temp + "\\" + i, fail)
            print("{:.1f} % \t\t ERROR \t\t {} moved to {}.".format(progress_counter * 100 / len(input_list), i,
                                                                    fail))

    except:
        shutil.move(temp + "\\" + i, fail)
        print("{:.1f} % \t\t ERROR \t\t {} moved to {}.".format(progress_counter * 100 / len(input_list), i,
                                                                fail))

    progress_counter += 1


# normalize progress_counter
progress_counter -= 1


# Deletion of empty folders & generation of archives
if len(os.listdir(temp)) == 0:
    os.rmdir(temp)
else:
    print("\n\n", temp, "is not empty please check the folder.")

if len(os.listdir(fail)) == 0:
    os.rmdir(fail)
else:
    print("\n\nDO NOT CLOSE the page. Archives on progress...")
    shutil.make_archive(output + "\\Failure", 'zip', fail)
    print("Failure archive is completed.")

check_list = [suc_im, suc_vid, suc_sam_im, suc_sam_vid]
for x in check_list:
    if os.path.exists(x) and len(os.listdir(x)) == 0:
        os.rmdir(x)

if len(os.listdir(suc)) == 0:
    os.rmdir(suc)
    print("\nCorrection failed")
else:
    print("\nDO NOT CLOSE the page. Archives on progress...")
    shutil.make_archive(output + "\\Successful", 'zip', suc)
    print("Successful archive is completed.")

end_t = time.time()


# End
print("*" * 150)
print("\t\t\t\t\t\tCOMPLETED\t\t\t\t\t\t")
print("*" * 150)


# Stats
print("\n\nStats:")
delta_t = end_t - start_t
print("Completed in {:.0f} min. {:.1f} sec.".format(delta_t // 60, delta_t % 60))

successfully_corrected = 0
if os.path.exists(suc):
    for i in check_list:
        if os.path.exists(i):
            successfully_corrected += len(os.listdir(i))

success_rate = (successfully_corrected / progress_counter) * 100
print("Success rate: {:.1f} %".format(success_rate))

if os.path.exists(fail):
    print("Number of fails:", len(os.listdir(fail)))


# Quit
switch_q = True
while switch_q:
    q = input("\n\nPress Q then Enter to leave:")

    if q in ("Q", "q"):
        print("Quiting...")
        time.sleep(2)
        switch_q = False
        print("myt")
    else:
        continue




























































# Date_Correctorinator v1.2 => Chrono_Correctorinator v.1.0 (name change)
# 250-130-1748 => 250-207-0150
# M. Y. Turkmen
