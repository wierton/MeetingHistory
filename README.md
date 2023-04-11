# Paper Discussion Web Application

This web application allows users to submit and manage speech papers and recommended papers for a paper discussion group. The application is built using the Flask framework and stores data in an SQLite database.

## Features

- Submit and manage speech papers with title, speecher, speech time, and PPT file.
- Submit and manage recommended papers with title and author.
- Edit and delete functionality for both speech and recommended papers.
- Responsive and visually appealing table-based layout for displaying submissions.

## Setup and Installation

1. Clone the repository:

```
git clone https://github.com/your-username/your-repo-name.git
```

2. Navigate to the project directory:

```
cd your-repo-name
```

3. Create a virtual environment:

```
python3 -m venv venv
```

4. Activate the virtual environment:

- On Windows:

```
venv\Scripts\activate
```

- On macOS/Linux:

```
source venv/bin/activate
```

5. Install the required packages:

```
pip install -r requirements.txt
```

6. Set the environment variables:

- On Windows:

```
set FLASK_APP=app.py
set FLASK_ENV=development
```

- On macOS/Linux:

```
export FLASK_APP=app.py
export FLASK_ENV=development
```

7. Run the application:

```
flask run
```

8. Open your web browser and visit `http://127.0.0.1:5000` to access the application.

## License

This project is licensed under the MIT License.
