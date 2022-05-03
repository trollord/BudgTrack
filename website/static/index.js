function deleteNote(noteId) {
    fetch('/deleteNote', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = '/';
    });
}