# Chrono-Correctorinator
Chrono Correctorinator is a Python-based automation tool designed to fix corrupted timestamps in images and videos.

Some applications, like WhatsApp and Samsung's default Android camera app, name the created files according to their creation date. Due to various reasons, such as downloading a backup or transferring between different devices, timestamps may get corrupted. Chrono Correctorinator was developed to correct the corrupted timestamps of the media created by these applications. 

Please note that this tool cannot extract the absolute original creation time of the media delivered via WhatsApp. For example, if a photo was sent to you the day after it was actually taken, WhatsApp names it according to the delivery date (the date it was created on your device), not the original creation date of the sender. Therefore, this software extracts and applies the date of your specific copy based on its filename.

## Python libraries (built-in)
- os
- ctypes
- wintypes
- datetime
- shutil
- time

## How it works
Chrono-Correctorinator runs in the command-line interface (CLI). It guides the user while working. Firstly, it expects the user to enter the directory path of the source folder, which includes misdated media files. After that, it asks the user to enter an output directory. If no output path is specified, the Downloads folder will be chosen by default. 

This software creates temporary copies of the original files and adjusts the dates of these copies to protect the original ones. During the adjustment, the software displays the progress percentage, the file status (done/error), the name of the current file, and the output directory. When it is completed, an archived ``.zip`` version will also be provided for future file transfers. Finally, stats like time and success rate will be provided, and the application will be turned off when the user presses "q". 

## Warning & limitations
- Chrono-Correctorinator uses the European date format (**DD/MM/YYYY**).
- The source folder must only and directly include the misdated files.
- This software can work with only WhatsApp and Samsung media files (images and videos) and **requires a Windows OS**.
- Even though the software creates temporary copies, it is strongly suggested that users should create a manual backup of their source materials before the process.
- This software does not control available storage space. It is the user's responsibility to ensure they have enough free storage space equal to at least twice the size of the source material.
- For the WhatsApp files, this software is only able to fix the creation date (day, month, year). The exact creation time cannot be restored (hour, minute, second), since it is not included in the file names.

## Note about Windows API 
The function that manipulates the file attributes on the Windows API level is created by an AI model. 

## License
This software is licensed under the [MIT License](LICENSE).

## Contribution
If you want to contribute to the project, feel free to send a pull request. It can be adapted to other messaging applications like Telegram or Signal.
