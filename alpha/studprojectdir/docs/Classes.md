# Classes/Functions

## models.py
1. User class has property of id, username, email, image_file, password, data_created, notes, flashcards, events
* login.html
* registration.html
* change_password.html
2. TimerDetails class has property of id, time, date, user_id
* timer.html
* visualizeblocks.html
* study_completed.html
* study.html
* rest.html
3. Note class has property of id, title, date, content, user_id
* notes.html
* note.html
* createNote.html
* shareNote.html
* searched_notes.html
* uploadnote.html
* pdf.html
4. Flashcard class has property of id, date, front, back, user_id
* createFlashcard.html
* createMDFlashcard.html
* flashcard.html
* flashcards.html
* memorize.html
* searched_flashcards.html
5. Events class has property of id, title, start, end, url, user_id
* calendar.html
* add_event.html

## forms.py
1. RegistrationForm
2. LoginForm
3. ResetPasswordForm
4. ResetRequestForm
5. AccountUpdateForm
6. DeleteAccountForm
7. PomodoroAndBlockForm
8. NewFlashCard
9. NoteForm
10. ShareForm

# functions from routes.py
1. home (splash page)
2. save_image (profile picture)
3. account (user settings)
4. (delete account from database)
* delete_account
* delete_successful
5. login (login to with database user)
6. logout (get back to splash page)
7. registration (create an account)
8. (flashcard functionality)
* flashcards
* show_flashcard
* memorize
* update_flashcard
* create_flashcard
* delete_flashcard
* share_flashcard
* flashcard_pdf
* add_flashcard
* f_search
9. (notes functionality)
* notes
* n_search
* note
* add_note
* upload_note
* update_note
* delete_note
* share_note
* pdf
10. (timer functionality)
* time
* rest
* study
* study_completed
* visualize_blocks
11. send_mail (get email to password)
12. reset_request (request to change password)
13. reset_token
14. calendar
15. add_calendar_event
