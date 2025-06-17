import os
import shutil
import subprocess
import sys
import platform
import zipfile
import requests
from time import sleep

def download_extract_xiso(download_url, extract_to):
    zip_path = os.path.join(extract_to, "extract-xiso.zip")
    print(f"Downloading extract-xiso from {download_url} ...")
    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Download complete. Extracting...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        exe_path_in_zip = None
        for member in zip_ref.namelist():
            if member.endswith("extract-xiso.exe") and member.startswith("artifacts/"):
                exe_path_in_zip = member
                break

        if exe_path_in_zip is None:
            raise Exception("extract-xiso.exe not found inside the zip under artifacts/")

        zip_ref.extract(exe_path_in_zip, extract_to)

    extracted_exe_path = os.path.join(extract_to, exe_path_in_zip)
    final_exe_path = os.path.join(extract_to, "extract-xiso.exe")
    shutil.move(extracted_exe_path, final_exe_path)

    artifacts_folder = os.path.join(extract_to, "artifacts")
    if os.path.isdir(artifacts_folder):
        shutil.rmtree(artifacts_folder)

    os.remove(zip_path)
    os.system('cls')
    print("Downloaded extract-xiso.exe into current directory.\n")

def check_and_get_extract_xiso(current_dir):
    extract_xiso_path = os.path.join(current_dir, "extract-xiso.exe")
    if os.path.exists(extract_xiso_path):
        print("Found extract-xiso.exe in the current directory.\n")
        return extract_xiso_path

    print("extract-xiso is required but not found.\n")
    choice = input("Do you want to download it now? (Y/N): ").strip().lower()
    if choice != 'y':
        sys.exit(1)

    arch = platform.architecture()[0]
    if '64' in arch:
        download_url = "https://github.com/XboxDev/extract-xiso/releases/latest/download/extract-xiso-Win64_Release.zip"
    else:
        download_url = "https://github.com/XboxDev/extract-xiso/releases/latest/download/extract-xiso-Win32_Release.zip"

    try:
        download_extract_xiso(download_url, current_dir)
    except Exception as e:
        print(f"Failed to download or extract extract-xiso: {e}")
        sys.exit(1)

    if not os.path.exists(extract_xiso_path):
        print("extract-xiso.exe was not found after extraction. Exiting.")
        sys.exit(1)

    return extract_xiso_path

def get_user_choice():
    while True:
        
        print("Choose the operation:")
        print("1: Extract X/ISO to folder (-x)")
        print("2: Rewrite ISO into XISO (-r)")
        print("3: Create XISO from extracted folder (-c)")
        choice = input("Enter corresponding Number: ").strip()

        if choice == '1':
            return '-x'
        elif choice == '2':
            return '-r'
        elif choice == '3':
            return '-c'
        else:
            os.system('cls')
            print("Invalid choice.\n")

def process_iso(iso_path, operation, extract_xiso_path, delete_choice, delete_rewritten_iso, output_dir):
    if operation == '-x':
        subprocess.run([extract_xiso_path, "-x", iso_path], check=True)
        sleep(3)

        extracted_folder_name = os.path.splitext(os.path.basename(iso_path))[0]
        extracted_folder_path = os.path.join(os.path.dirname(iso_path), extracted_folder_name)

        if os.path.exists(extracted_folder_path):
            destination_folder = os.path.join(output_dir, extracted_folder_name)
            os.makedirs(output_dir, exist_ok=True)
            shutil.move(extracted_folder_path, destination_folder)
        else:
            print(f"Error: Extracted folder not found for {iso_path}")

        if delete_choice:
            os.remove(iso_path)

    elif operation == '-r':
        print(f"Rewriting ISO from: {iso_path}")
        subprocess.run([extract_xiso_path, "-r", iso_path], check=True)

        rewritten_iso_path = os.path.join(output_dir, os.path.basename(iso_path))

        if os.path.exists(iso_path):
            print(f"Moving rewritten ISO to output folder: {rewritten_iso_path}")
            shutil.move(iso_path, rewritten_iso_path)

        old_iso_path = iso_path + ".old"
        if not delete_rewritten_iso and os.path.exists(old_iso_path):
            print(f"Renaming {old_iso_path} back to {iso_path}")
            os.rename(old_iso_path, iso_path)

        if delete_rewritten_iso:
            old_iso_path = iso_path + ".old"
            if os.path.exists(old_iso_path):
                print(f"Deleting original ISO: {old_iso_path}")
                os.remove(old_iso_path)
            else:
                print(f"Warning: Expected old ISO not found at {old_iso_path}")

    elif operation == '-c':

        folder_name = os.path.basename(os.path.normpath(iso_path))
        created_iso_name = folder_name + ".iso"
        created_iso_path = os.path.join(os.path.dirname(iso_path), created_iso_name)
        target_iso_path = os.path.join(output_dir, created_iso_name)

        subprocess.run([extract_xiso_path, "-c", iso_path], check=True)

        if os.path.exists(created_iso_path):
            print(f"Moving created ISO to output folder: {target_iso_path}")
            shutil.move(created_iso_path, target_iso_path)
        else:
            print(f"ISO file not found after creation: {created_iso_path}")

        if delete_choice:
            print(f"Deleting source folder: {iso_path}")
            shutil.rmtree(iso_path)

def main():
    current_dir = os.getcwd()
    extract_xiso_path = check_and_get_extract_xiso(current_dir)

    while True:
        operation = get_user_choice()
        output_dir = os.path.join(current_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        delete_choice = False
        delete_rewritten_iso = False

        if operation == '-c':
            delete_choice = input("Delete extracted folders after creating XISO? (Y/N): ").strip().lower() == 'y'
        elif operation == '-x':
            delete_choice = input("Delete source ISO files after extracting? (Y/N): ").strip().lower() == 'y'
        elif operation == '-r':
            delete_rewritten_iso = input("Delete original ISO after rewriting? (Y/N): ").strip().lower() == 'y'

        targets = []

        if operation == '-c':

            # Include current folder if it contains default.xbe
            if os.path.exists(os.path.join(current_dir, "default.xbe")):
                targets.append(current_dir)

            for root, dirs, files in os.walk(current_dir):
                for d in dirs:
                    folder_path = os.path.join(root, d)
                    print(f"Checking: {folder_path}")
                    if os.path.exists(os.path.join(folder_path, "default.xbe")):
                        print(f"Found valid game folder: {folder_path}")
                        targets.append(folder_path)

        else:
            for root, _, files in os.walk(current_dir):
                # Skip output folder to avoid recursion
                if root.startswith(output_dir):
                    continue
                for file in files:
                    if operation == '-r' and file.endswith(".old"):
                        continue
                    if file.endswith(".iso"):
                        targets.append(os.path.join(root, file))

        # Remove duplicates if any
        targets = list(set(targets))

        if not targets:
            print("\nNo valid files or folders found for the selected operation.")
        else:
            for t in targets:
                print(" -", t)
            print()

            for target in targets:
                process_iso(target, operation, extract_xiso_path, delete_choice, delete_rewritten_iso, output_dir)

            os.system('cls')
            print("Batch XISO processing complete.\n")

if __name__ == "__main__":
    main()
