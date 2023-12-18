const hash = window.location.pathname.split("/")[2];

const getNote = async () => {
    const password = prompt("Enter password");
    const response = await fetch(`/api/notes/${hash}`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "password": password
        })
    });
    const note = await response.json();
    document.querySelector("#contenido").textContent = note.note;
}

window.onload = () => {
    getNote().catch(err => {
        console.log(err);
    });
}