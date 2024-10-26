
# Newspaper Agency

The Newspaper Agency project is a Django-based application that manages a digital platform for newspaper publications. 
It includes features to manage topics, newspapers, redactors (editors), 
and an intuitive interface for users to search, create, and update content within the system.

## Features

- **User Authentication**: Users can register, log in, and access personal profiles.
- **Topic Management**: Users can view, create, update, and delete topics.
- **Newspaper Management**: Users can create, search, view, update, and delete newspapers and 
associate them with topics and publishers.
- **Redactor Management**: Users can search, view, create, update, and delete redactors, along with 
managing their years of experience.
- **Dynamic Content Assignment**: Redactors can assign themselves to newspapers, and the assignment status 
is dynamically managed.

## Getting Started

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/arsen-arutiunov/newspaper-agency.git
   cd newspaper-agency
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser to access the admin interface:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. Open the application in your browser at `http://127.0.0.1:8000/`.

## Data Loading

If you'd like to pre-load data into the database, you can use the `load_data.json` file. Run the following command:

```bash
python manage.py loaddata load_data.json
```

## Usage

1. **Register and log in** to access restricted sections.
2. **Browse and search** for topics, newspapers, and redactors using the search bar in each section.
3. **Assign or unassign redactors to newspapers** via the toggle function.
4. **Manage topics and newspapers** in the admin interface at `http://127.0.0.1:8000/admin/`.

## Project Structure

- `newspaper/`: Contains all Django apps related to the Newspaper Agency.
- `templates/`: Holds HTML templates for various views.
- `static/`: Contains CSS, JavaScript, and image files.
