# Classes/Functions

## models.py
### User class has property of id, username, email, image_file, password, data_created, notes, flashcards, events
* login.html
* registration.html
* change_password.html
### TimerDetails class has property of id, time, date, user_id
* timer.html
* visualizeblocks.html
* study_completed.html
* study.html
* rest.html
### Note class has property of id, title, date, content, user_id
* notes.html
* note.html
* createNote.html
* shareNote.html
* searched_notes.html
* uploadnote.html
* pdf.html
### Flashcard class has property of id, date, front, back, user_id
* createFlashcard.html
* createMDFlashcard.html
* flashcard.html
* flashcards.html
* memorize.html
* searched_flashcards.html
### Events class has property of id, title, start, end, url, user_id
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

## functions from routes.py
* home (splash page)
* save_image (profile picture)
* account (user settings)
#### (delete account from database)
* delete_account
* delete_successful
5. login (login to with database user)
6. logout (get back to splash page)
7. registration (create an account)
#### (flashcard functionality)
* flashcards
* show_flashcard
* memorize
* update_flashcard
* create_flashcard
* delete_flashcard
* share_flashcard
* flashcard_pdf
* add_flashcard
* choose
* f_search
#### (notes functionality)
* notes
* n_search
* note
* add_note
* upload_note
* update_note
* delete_note
* share_note
* pdf
#### (timer functionality)
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
