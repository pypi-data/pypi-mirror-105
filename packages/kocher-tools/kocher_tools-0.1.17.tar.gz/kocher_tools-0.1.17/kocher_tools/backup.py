import os
import sys
import datetime
import pytz
import logging
import random
import string

#from kocher_tools.database import backupDatabase

class Backups (list):
	def __init__ (self, *arg, out_dir = None, log_file = '', file_limit = 10, day_cutoff = 120, **kw):
		super(Backups, self).__init__(*arg, **kw)
		self.out_dir = out_dir
		self.log_file = log_file
		self.file_limit = int(file_limit)
		self.str_format = '%Y-%m-%d'
		self.date = datetime.datetime.now()
		self.date_cutoff = self.date - datetime.timedelta(days = day_cutoff)
		self.oldest_backup = None
		self.most_recent_backup = None

		# Check if data was not assigned
		if not self: self.assignBackups()

	def __str__ (self):
		return f'{[str(_b) for _b in self]}'

	@property
	def date_str (self):

		# Return the date as a string of Year-Month-Day-Seconds
		return self.date.strftime(self.str_format)

	def assignBackups (self):

		# Assign an empty object to store the oldest and newest backups
		oldest_backup = None
		most_recent_backup = None
        
		# Loop the files within the backup dir
		for backup_file in os.listdir(self.out_dir):

			# Assign the backup file path
			backup_file_path = os.path.join(self.out_dir, backup_file)

			# Assign the file modification date
			#try: past_backup_date = datetime.datetime.fromtimestamp(os.path.getmtime(backup_file_path))
			#except: raise Exception(f'Unable to assign modification date for: {backup_file_path}')

			# Assign the backup
			past_backup = Backup(backup_file_path)
			self.append(past_backup)

			# Check if the current backup is older than the stored oldest backup
			if not oldest_backup or past_backup < oldest_backup: 
				oldest_backup = past_backup

			# Check if the current backup is older than the stored oldest backup
			if not most_recent_backup or past_backup > most_recent_backup: 
				most_recent_backup = past_backup

		# Assing the oldest backup and the most recent date
		self.oldest_backup = oldest_backup
		self.most_recent_backup = most_recent_backup

	def updateBackups (self):

		# Check if the number of backups exceeds the backup limit
		if len(self) > self.limit:

			# Delete the oldest backup
			self.deleteBackup(self.oldest_backup)

			# Assign an empty object to store the oldest backup
			oldest_backup = None

			# Assign an empty object to store the newest backup
			most_recent_backup = None
	        
			# Loop the backups, backup by backup
			for current_backup in self:

				# Check if the oldest backup has been defined
				if not oldest_backup:

					# Assign the current backup
					oldest_backup = current_backup

				else:

					# Check if the current backup is older than the stored oldest backup
					if current_backup < oldest_backup:

						# Assign the current backup
						oldest_backup = current_backup

				# Check if the newest backup has been defined
				if not most_recent_backup:

					# Assign the current backup
					most_recent_backup = current_backup

				else:

					# Check if the current backup is older than the stored oldest backup
					if current_backup > most_recent_backup:

						# Assign the current backup
						most_recent_backup = current_backup

			# Assing the oldest backup and the most recent date
			self.oldest_backup = oldest_backup
			self.most_recent_backup = most_recent_backup

	def newBackup (self, database):

		# Assign the database basename and file extension
		database_basename = os.path.basename(database)
			
		# Create random string for database filename
		random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))

		# Assign the backup filename
		backup_file = os.path.join(self.out_dir, '%s.%s.%s.backup' % (database_basename, random_str, self.date_str))

		# Create the database
		backupDatabase(database, backup_file)

		# Assign the new backup
		new_backup = Backup(backup_file, self.date)

		# Append the new backup
		self.append(new_backup)

		# Update the most recent backup
		self.most_recent_backup = new_backup

		# Update the backups
		self.updateBackups()

	def backupfromConfig (self, config_data):

		# Assign the arg list
		if config_data.type == 'postgresql':
			backup_file = os.path.join(self.out_dir, f'{config_data.schema}.{self.randStr()}.{self.date_str}.dmp')
			backup_call_args = ['pg_dump', '-U', config_data.user, '-d', config_data.database, '-n', config_data.schema, '-h', config_data.host, '-Fc']
			#executeBackup('pg_dump', backup_call_args, backup_file)
		if config_data.type == 'sqlite': raise Exception('In Development')

	def deleteBackup (self, backup_to_delete):

		# Assign the file path of the backup file
		backup_file_path = str(backup_to_delete)

		# Confirm the file exists, otherwise raise an error
		if not os.path.isfile(backup_file_path):
			raise Exception('Backup file (%s) not found' % backup_file_path)

		# Remove the file
		os.remove(backup_file_path)

		# Loop the backups by index
		for backup_pos in range(len(self)):

			# Check if the current backup is the one to remove
			if self[backup_pos] == backup_to_delete:

				# Remove the backup object
				del self[backup_pos]
				break

	@classmethod
	def fromConfig (cls, config_data):
		return cls(out_dir = config_data.backup_dir, log_file = config_data.log_file, file_limit = config_data.max_files, day_cutoff = config_data.max_days_old)

	@staticmethod
	def randStr (str_len = 6):
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(str_len))

	@staticmethod
	def executeBackup (backup_executable_str, backup_call_args, backup_output):

		# Find the blast executable
		backup_executable = confirmExecutable(backup_executable_str)

		# Check if executable is installed
		if not backup_executable:
			raise IOError(f'{backup_executable_str} not found. Please confirm the executable is installed')

		# Open the output file
		backup_output_file = open(backup_output, 'w')

		# Check if a header was specified
		if header:
			
			# Write the head to the output file
			backup_output_file.write(header + '\n')

			# Flush the file
			backup_output_file.flush()

		# blast subprocess call
		backup_call = subprocess.Popen([backup_executable] + backup_call_args, stderr = subprocess.PIPE, stdout = backup_output_file)

		# Get stdout and stderr from subprocess
		backup_stdout, backup_stderr = backup_call.communicate()

		# Check if code is running in python 3
		if sys.version_info[0] == 3:
			
			# Convert bytes to string
			backup_stderr = backup_stderr.decode()

		# Report any errors
		if backup_stderr: raise Exception(backup_stderr)

		# Close the file
		backup_output_file.close()

class Backup ():
	def __init__ (self, file_path):

		# Confirm the file exists
		if not os.path.isfile(file_path): raise Exception(f'Backup file ({file_path}) not found')

		# Assign the file modification date
		try: backup_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
		except: raise Exception(f'Unable to assign modification date for: {file_path}')

		self.file_path = file_path
		self.backup_date = backup_date

	def __str__ (self):

		# str() returns the file path
		return self.file_path

	def __gt__ (self, other_backup):

		# Check if the stored date is more recent
		return self.backup_date > other_backup.backup_date

	def __lt__ (self, other_backup):

		# Check if the stored date is older
		return self.backup_date < other_backup.backup_date


