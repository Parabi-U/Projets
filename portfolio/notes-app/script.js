
let currentEditNoteId = null;


function openPopup() {
    const popupContainer = document.getElementById("popupContainer");
    document.getElementById("note-text").value = "";
    popupContainer.style.display = "flex";
}


function closePopup() {
    const popupContainer = document.getElementById("popupContainer");
    popupContainer.style.display = "none";
}


function createNote() {
    const noteText = document.getElementById('note-text').value.trim();

    if (noteText !== '') {
        const note = {
            id: Date.now(),
            text: noteText,
            timestamp: new Date().toLocaleString()
        };

        const existingNotes = JSON.parse(localStorage.getItem('notes')) || [];
        existingNotes.push(note);
        localStorage.setItem('notes', JSON.stringify(existingNotes));

        closePopup();
        displayNotes();
    } else {
        alert("Please enter some text for your note!");
    }
}

function displayNotes() {
    const notesList = document.getElementById('notes-list'); // Correction: 'notes-List' -> 'notes-list'
    notesList.innerHTML = '';

    const notes = JSON.parse(localStorage.getItem('notes')) || [];

    if (notes.length === 0) {
        notesList.innerHTML = '<p>No notes yet. Click the + button to create one!</p>';
        return;
    }

    notes.forEach(note => {
        const li = document.createElement('li');
        li.className = 'note-item';
        li.innerHTML = `
            <span class="note-content">${note.text}</span>
            <small>${note.timestamp || ''}</small>
            <div class="note-buttons">
                <button class="edit-btn" onclick="editNote(${note.id})">
                    <i class="fa-solid fa-pen"></i> Edit
                </button>
                <button class="delete-btn" onclick="deleteNote(${note.id})">
                    <i class="fa-solid fa-trash"></i> Delete
                </button>
            </div>
        `;
        notesList.appendChild(li);
    });
}


function editNote(noteId) {
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    const note = notes.find(n => n.id === noteId);

    if (note) {
        currentEditNoteId = noteId;
        const editingPopup = document.getElementById("editingPopupContainer");
        document.getElementById("note-edit-text").value = note.text;
        editingPopup.style.display = "flex";
    }
}


function closeEditingPopup() {
    const editingPopup = document.getElementById("editingPopupContainer");
    editingPopup.style.display = "none";
    currentEditNoteId = null;
}

function saveNote() {
    if (!currentEditNoteId) return;

    const newText = document.getElementById("note-edit-text").value.trim();

    if (newText === "") {
        alert("Note cannot be empty!");
        return;
    }

    let notes = JSON.parse(localStorage.getItem('notes')) || [];

    notes = notes.map(note => {
        if (note.id === currentEditNoteId) {
            return { 
                ...note, 
                text: newText,
                timestamp: new Date().toLocaleString() // Mettre à jour le timestamp
            };
        }
        return note;
    });

    localStorage.setItem('notes', JSON.stringify(notes));
    closeEditingPopup();
    displayNotes();
}


function deleteNote(noteId) {
    if (confirm("Are you sure you want to delete this note?")) {
        let notes = JSON.parse(localStorage.getItem('notes')) || [];
        notes = notes.filter(note => note.id !== noteId);
        localStorage.setItem('notes', JSON.stringify(notes));
        displayNotes();
    }
}


document.addEventListener('DOMContentLoaded', function() {
    
    document.addEventListener('click', function(event) {
        const popupContainer = document.getElementById("popupContainer");
        const editingPopup = document.getElementById("editingPopupContainer");
        const addNoteDiv = document.getElementById("addNoteDiv");

        if (popupContainer.style.display === "flex" && 
            !popupContainer.contains(event.target) && 
            event.target !== addNoteDiv) {
            closePopup();
        }

        if (editingPopup.style.display === "flex" && 
            !editingPopup.contains(event.target)) {
            closeEditingPopup();
        }
    });


    displayNotes();
});