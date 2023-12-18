const sendNote = async () => {
    let content = document.querySelector("#editable").textContent;
    let response = await fetch("/api/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "password": prompt("Enter password"),
            "note": content
        })
    });
    let note = await response.json();
    window.location.href = `/notes/${note.note_hash}`;
}


document.querySelector("#save").onclick = () => {
    sendNote().catch(err => {
        console.log(err);
    });
}