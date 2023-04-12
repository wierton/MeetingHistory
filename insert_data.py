import os
import re
import sys
import pathlib
import pandas as pd
from app import app, db, SpeechPaper
from werkzeug.utils import secure_filename

# Read the table from the Markdown file
def read_table_from_md(file_path):
    '''example md
    | speech_time      | speecher | title                                                      |
    |------------------|----------|--------------------------------------------------------------
    | 2021-07-21-OXF   | 欧先飞   | PLDI'15@Provably Correct Peephole Optimizations with Alive |
    '''
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')[2:]

    table_data = []
    for line in lines:
        if not line.strip():
            continue
        row_data = [cell.strip() for cell in line.split('|') if cell.strip()]
        date_file_srch = re.search(r'\[(.*)-\w+\]\((.*)\)', row_data[0])
        date = date_file_srch.group(1)
        fname = date_file_srch.group(2)
        title_srch = re.search(r'\[(.*)\]', row_data[2])
        title = title_srch.group(1) if title_srch else row_data[2]
        table_data.append({
          "speech_time": date,
          "speecher": row_data[1],
          "title": title,
          "ppt_file": fname,
          })

    return table_data

def main():
    # Read the table from the Markdown file
    mddir = sys.argv[1]
    data = read_table_from_md(f'{mddir}/README.md')

    # Insert the data into the database
    with app.app_context():
      for entry in data:
          speech_time = entry["speech_time"]
          speecher = entry["speecher"]
          title = entry["title"]
          ppt_file = entry["ppt_file"] 

          # Make sure the PPT file is in the 'uploads' directory
          os.system(f'cp {mddir}/{ppt_file} uploads')

          speech_paper = SpeechPaper(time=speech_time, speecher=speecher, title=title, ppt_file=ppt_file)
          db.session.add(speech_paper)
          db.session.commit()

          print(f"Inserted: {speech_time} - {speecher} - {title} - {ppt_file}")

if __name__ == "__main__":
    main()
