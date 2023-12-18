const getNotes = async () => {
    const response = await fetch('/api/notes');
    const notes = await response.json();
    for(let i in notes){
        let note = notes[i];
        let noteElement = document.createElement('div');
        noteElement.innerHTML = `
        <li><a href="/notes/${note.hash}">${note.id} - ${note.hash}</a></li>
        `;
        document.querySelector("#noteplaceholder").appendChild(noteElement);
    }
    document.querySelector("#placeholder").remove();
}

window.onload = () => {
    getNotes().catch(err => {
        console.log(err);
    });
}