# Remove reports older than 30 days
# and remove videos older than 2 business days.

import os
import shutil
from datetime import datetime, timedelta

def delete_videos_dir(root_dir):
  for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
    if 'videos' in dirnames:
      videos_folder_path = os.path.join(dirpath, 'videos')
      try:
        if os.path.exists(videos_folder_path):
          shutil.rmtree(videos_folder_path)
          print(f"Deleted videos folder in: {videos_folder_path}")
      except OSError as e:
        print(f"Error deleting videos folder in {videos_folder_path}: {e}")

def cleanup_reports_and_videos(folder_path, is_monday_or_tuesday):
  for dir_name in os.listdir(folder_path):
    dir_path = os.path.join(folder_path, dir_name)

    if os.path.isdir(dir_path) and all(char.isdigit() or char == '-' for char in dir_name):
      dir_date = datetime.strptime(dir_name, '%Y-%m-%d').date()
      days_elapsed = (datetime.today().date() - dir_date).days

      print(f"Folder '{dir_path}' is {days_elapsed} days old")

      if days_elapsed > 18:
        print(f"Deleting folder 18+ days old: '{dir_path}'")
        shutil.rmtree(dir_path)
      else:
        if (is_monday_or_tuesday and days_elapsed > 4) or (not is_monday_or_tuesday and days_elapsed > 2):
          delete_videos_dir(dir_path)

if __name__ == "__main__":
  current_directory = os.path.join(os.getcwd(), "reports");
  is_monday_or_tuesday = datetime.today().weekday() in [0, 1]  # Monday and Tuesday

  cleanup_reports_and_videos(current_directory, is_monday_or_tuesday)
