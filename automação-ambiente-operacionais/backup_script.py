import os
import shutil
from datetime import datetime, timedelta

SOURCE_PATH = "/home/valcann/backupsFrom"
DESTINATION_PATH = "/home/valcann/backupsTo"
LOG_FILE_FROM = "/home/valcann/backupsFrom.log"
LOG_FILE_TO = "/home/valcann/backupsTo.log"

DAYS_THRESHOLD = 3

now = datetime.now()
cutoff_time = now - timedelta(days=DAYS_THRESHOLD)

def get_file_metadata(file_path):
    stats = os.stat(file_path)
    size = stats.st_size
    creation_time = datetime.fromtimestamp(stats.st_ctime)
    modification_time = datetime.fromtimestamp(stats.st_mtime)
    return {
        "size": size,
        "creation_time": creation_time,
        "modification_time": modification_time
    }

def log_file_details(log_file_path, file_details):
    with open(log_file_path, "w") as log_file:
        log_file.write("Nome, Tamanho(Bytes), Data de Criação, Data da Ultima Modificação\n")
        for details in file_details:
            log_file.write(f"{details['name']}, {details['size']}, {details['creation_time']}, {details['modification_time']}\n")

files_from = []
files_to = []

for file_name in os.listdir(SOURCE_PATH):
    file_path = os.path.join(SOURCE_PATH, file_name)

    if os.path.isfile(file_path):
        metadata = get_file_metadata(file_path)
        files_from.append({
            "name": file_name,
            **metadata
        })

        if metadata["creation_time"] < cutoff_time:
            os.remove(file_path)
        else:
            destination_file_path = os.path.join(DESTINATION_PATH, file_name)
            shutil.copy2(file_path, destination_file_path)
            files_to.append({
                "name": file_name,
                **metadata
            })

log_file_details(LOG_FILE_FROM, files_from)
log_file_details(LOG_FILE_TO, files_to)

print("Automação de backup concluída com sucesso.")
