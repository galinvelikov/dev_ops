import os
import logging
import datetime
import tarfile


class Arthas:

    def __init__(self):
        self.backup_source = '/etc'
        self.backup_location = '/bkp/'
        self.backup_log = '/var/log/lich_backup_logger'
        self.lock_file = '/bkp/lich_locker'
        self.extension = '.tar.gz'
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d%s")
        self.backup_name = f'backup_etc_{self.timestamp}.tar.gz'
        logging.basicConfig(filename=self.backup_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def fall_of_the_king(self):
        # Creating a lock to insure only one process is running

        if os.path.exists(self.lock_file):
            logging.warning('A duplicate instance has been spawned')
            exit(logging.warning('The script is already active, Abort the duplicated process!'))
        else:
            with open(self.lock_file, 'w') as file:
                file.write('The LichKing is alive!')
                logging.info('The script has been started!')
                logging.info('No running instance found! Checking the available slots ...')
            lich_king.slot_checker()

    def slot_checker(self):
        #Method that will perform counting and removing of backups (if neccessary)
        backup_counter = 0
        for backup in os.listdir(self.backup_location):
            if backup.endswith(self.extension) and os.path.isfile(os.path.join(self.backup_location, backup)):
                backup_counter += 1
        if backup_counter >= 10:
            logging.info(f'Allowed slots for backups - 10, current number of backups {backup_counter}')
            backup_files = [backup for backup in os.listdir(self.backup_location) if backup.endswith(self.extension)]
            if backup_files:
                oldest_backup = min(backup_files, key=lambda f: os.path.getctime(os.path.join(self.backup_location, f)))
                logging.info(f'Removing the oldest backup {self.backup_location}{oldest_backup}')
                os.remove(f'{self.backup_location}{oldest_backup}')
        else:
            logging.info(f'There are {10 - backup_counter} slots available')
        lich_king.arise()

    def arise(self):
        #The main backup generator
        creation_path = os.path.join(self.backup_location, self.backup_name)
        with tarfile.open(creation_path, 'w:gz') as tar:
            tar.add(self.backup_source, arcname=os.path.basename(self.backup_source))
            logging.info(f'A new backup is being created {self.backup_name}')
        if os.path.exists(self.lock_file):
            logging.info('Removing the lock file')
            os.remove(f'{self.backup_location}lich_locker')
            logging.info('Backup of /etc has been completed!')


lich_king = Arthas()
lich_king.fall_of_the_king()
