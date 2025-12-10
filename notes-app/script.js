function pop() {
    const popupContainer = document.createElement("div");
    popupContainer.id = "popupContainer";

    popupContainer.innerHTML = `
        <h1>New Note</h1>
        <textarea id="note-text" placeholder="Enter your note ..."></textarea>
        <div id="btn-container">
            <button id="submitBtn" onclick="createNote()">Create Note</button>
            <button id="closeBtn" onclick="closePopup()">Close</button>
        </div>
    `;

    document.body.appendChild(popupContainer);
}

function closePopup() {
    const popupContainer = document.getElementById("popupContainer");
    if (popupContainer) popupContainer.remove();
}

function createNote() {
    const noteText = document.getElementById('note-text').value.trim();

    if (noteText !== '') {
        const note = {
            id: Date.now(),
            text: noteText
        };

        const existingNotes = JSON.parse(localStorage.getItem('notes')) || [];
        existingNotes.push(note);
        localStorage.setItem('notes', JSON.stringify(existingNotes));

        closePopup();
        displayNotes();
    }
}

function displayNotes() {
    const notesList = document.getElementById('notes-List'); 
    notesList.innerHTML = '';

    const notes = JSON.parse(localStorage.getItem('notes')) || [];

    notes.forEach(note => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${note.text}</span>
            <div id="noteBtns-container">
                <button onclick="editNote(${note.id})"> <i class="fa-solid fa-pen"></i> </button>
                <button onclick="deleteNote(${note.id})"> <i class="fa-solid fa-trash"></i> </button>
            </div>
        `;
        notesList.appendChild(li);
    });
}

function editNote(noteId) {
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    const note = notes.find(n => n.id === noteId);

    const editingPopup = document.createElement("div");
    editingPopup.id = "editingPopupContainer";
    editingPopup.setAttribute("data-note-id", noteId);

    editingPopup.innerHTML = `
        <h1>Edit Note</h1>
        <textarea id="note-edit-text">${note.text}</textarea>
        <div id="btn-container">
            <button onclick="saveNote(${noteId})">Save</button>
            <button onclick="closeEditingPopup()">Cancel</button>
        </div>
    `;

    document.body.appendChild(editingPopup);
}

function closeEditingPopup() {
    const editingPopup = document.getElementById("editingPopupContainer");
    if (editingPopup) editingPopup.remove();
}

function saveNote(noteId) {
    const newText = document.getElementById("note-edit-text").value.trim();

    if (newText === "") return;

    let notes = JSON.parse(localStorage.getItem('notes')) || [];

    notes = notes.map(note => 
        note.id === noteId ? { ...note, text: newText } : note
    );

    localStorage.setItem('notes', JSON.stringify(notes));

    closeEditingPopup();
    displayNotes();
}

function deleteNote(noteId) {
    let notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes = notes.filter(note => note.id !== noteId);
    localStorage.setItem('notes', JSON.stringify(notes));
    displayNotes();
}

displayNotes();
