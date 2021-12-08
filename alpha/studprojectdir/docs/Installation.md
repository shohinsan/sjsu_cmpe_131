# Installation

Required apps to install:

1. email-validator ==1.1.3
2. Flask-Bcrypt==0.7.1
3. flask-pagedown==0.4.0
4. DateTime==4.3
5. Flask-SQLAlchemy==2.5.1
6. Flask-Bcrypt==0.7.1
7. Flask-Login==0.5.0
8. Flask-Mail==0.9.1
9. WTForms~=2.3.3
10. Flask~=2.0.1
11. itsdangerous~=2.0.1
12. pdfkit~=1.0.0

# How to install apps

### Example

* Step 1: Open command line
* Step 2: In command line type: pip install insert application name
* Continue step 2 until you have downloaded all 12 of the applications

# Running Apps

* run.py

## Project layout

    alpha/
        instance/
            /uploads
                .md (uploaded file)
        projectdir/
            /database
                notetaking.db
            /static
                /js
                    main.js
                /css
                    main.css
                    registration.css  
                    timexx.css
                    flipcard.css
                /profile_pics
                    .jpg/.png (uploaded picture profile 200x200)
            /templates
                /flashcardz
                    createFlashcard.html
                    createMDFlashcard.hmtl
                    flashcard.html
                    flashcards.html
                    memorize.html
                    searched_flashcards.html
                    selectcard.html
                /general
                    account.html
                    change_password.html
                    login.html
                    registration.html
                    reset_request.html 
                    signup.html
                /notes
                    createNote.html
                    note.html
                    notes.html
                    pdf.html
                    searched_notes.html
                    shareNote.html
                    uploadnote.html
                /timing 
                    add_event.html
                    calendar.html
                    rest.html
                    study.html
                    study_completed.html
                    timer.html
                    visualizeblocks.html
            homepage.html
            layouts.html
        __init__.py
        forms.py
        models.py
        routes.py
    output_flashcard.pdf (saved as pdf + download)
    output_notes.pdf (saved as pdf + download)
    run.py (server runner file)