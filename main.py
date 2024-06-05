from tkinter import *
from tkinter import filedialog
import os
import time

from send2trash import send2trash

window = Tk()
window.iconbitmap('icon.ico')
window.geometry('800x500')
window.resizable(0, 0)
window.title('Lightroom toolkit')

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()
        
def back_to_main_button():
    back_btn = Button(window, text='Go to main screen', bg='black', fg='white', font='Adobe 10', command=main_window)
    back_btn.place(x=20, y=450)
    
def get_folder_directory():
    global path_label
    folder_dir = filedialog.askdirectory()
    path_label.configure(text=folder_dir)
    path_label.update()
    return folder_dir

def delete_nr_images(directory: str):
    global path_label, progress_label
    try:
        progress_label.destroy()
    except Exception:
        pass
    
    if not directory or directory.strip() == '':
        path_label.configure(text='Please select a folder', fg='red')
        return
    
    files = []
    error_files = 0
    print('-------------------initial-------------------')
    
    progress_label = Label(window, text='Going thru images...', font='Adobe 15')
    progress_label.pack(pady=10)
    
    for index, filename in enumerate(os.listdir(directory)):
        if 'Enhanced-NR' in os.listdir(directory)[index]:
            file_name = filename.split('-Enhanced-NR')[0]
            file_extension = filename.split('.')[-1]
            files.append(os.path.join(directory, file_name + '.' + file_extension).replace('/', '\\'))

    print('-----------------filtered-------------------')
    progress_label.configure(text=f"Found {len(files)} denoised images.")
    progress_label.update()
    
    if len(files) > 0:
        for index, file in enumerate(files):
            try:
                send2trash(file)
                time.sleep(0.1)
                progress_label.configure(text=f"Deleted {index + 1}/{len(files)} images.")
                progress_label.update()
                pass
            except FileNotFoundError:
                print(file)
                error_files += 1
        
        if error_files:
            progress_label.configure(text=f'Deleted all images except {error_files}.\nThese images couldn"t be found')
        else:
            progress_label.configure(text='Deleted all images.')
        progress_label.update()
    

def main_window():
    clear_window()
    title = Label(window, text='Lightroom toolkit', fg='Black', font='Adobe 30')
    title.pack()
    nr_button = Button(window, text='Delete copies of denoised images', bg='black', fg='white', font='Adobe 10', command=nr_window)
    nr_button.place(x=100, y=100)
    
    
def nr_window():
    global path_label
    clear_window()
    title = Label(window, text='Delete copies of denoised images', fg='Black', font='Adobe 30')
    title.pack()
    path_input = Button(window, text='Select folder', bg='black', fg='white', font='Adobe 10', command=get_folder_directory)
    path_input.pack(pady=20)
    path_label = Label(window, text='', fg='Black', font='Adobe 10')
    path_label.pack()
    delete_btn = Button(window, text='Delete images', bg='black', fg='white', font='Adobe 10', command=lambda: delete_nr_images(path_label.cget('text')))
    delete_btn.pack(pady=10)
    back_to_main_button()
    
# Stored for dynamic updating
path_label = None
progress_label = None

main_window()
window.mainloop()