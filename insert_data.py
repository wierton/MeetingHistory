import pandas as pd
from app import db, SpeechPaper
import os
from werkzeug.utils import secure_filename

# Read the table from the Markdown file
def read_table_from_md(file_path):
    '''example md
    | speech_time      | speecher | title                                                       |
    |------------------|----------|--------------------------------------------------------------
    | 2021-07-21-OXF   | 欧先飞   | PLDI'15@Provably Correct Peephole Optimizations with Alive |
    '''
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    header_line = lines.pop(0).strip()
    separator_line = lines.pop(0).strip()

    headers = [header.strip() for header in header_line.split('|') if header.strip()]
    separators = [sep.strip() for sep in separator_line.split('|') if sep.strip()]

    if len(headers) != len(separators):
        raise ValueError('Incorrect table format in the Markdown file.')

    table_data = []
    for line in lines:
        if not line.strip():
            continue
        row_data = [cell.strip() for cell in line.split('|') if cell.strip()]
        if len(row_data) != len(headers):
            raise ValueError('Incorrect table format in the Markdown file.')
        table_data.append(row_data)

    df = pd.DataFrame(table_data, columns=headers)
    return df

def main():
    # Read the table from the Markdown file
    df = read_table_from_md('data.md')
    data = df.to_dict(orient='records')

    # Insert the data into the database
    for entry in data:
        speech_time = entry["speech_time"]
        speecher = entry["speecher"]
        title = entry["title"]
        ppt_file = f"{speech_time}.pptx"  # Assuming PPT files are named with the speech_time

        # Make sure the PPT file is in the 'uploads' directory
        if not os.path.exists(os.path.join('uploads', secure_filename(ppt_file))):
            print(f"Error: PPT file '{ppt_file}' not found in 'uploads' directory.")
            continue

        speech_paper = SpeechPaper(speech_time=speech_time, speecher=speecher, title=title, ppt_file=ppt_file)
        db.session.add(speech_paper)
        db.session.commit()

        print(f"Inserted: {speech_time} - {speecher} - {title} - {ppt_file}")

if __name__ == "__main__":
    main()
