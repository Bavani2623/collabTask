const formElement = document.getElementById("projectForm")

/* ========== Project Add ========== */

formElement.addEventListener("submit", async (e) => {
    e.preventDefault()

    const formData = new FormData(formElement)
    const data = Object.fromEntries(formData)

    const projectId = document.getElementById("editProjectId").value

    if (projectId) {
        fetch(`/project/update?id=${projectId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(data => {
                if (data.status == "success") {
                    alert(data.message)
                    formElement.reset()
                    location.reload()
                }
                else {
                    throw data.message
                }
            })
            .catch(error => {
                alert(error)
            })
    } else {

        fetch('/project/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(data => {
                if (data.status == "success") {
                    alert(data.message)
                    formElement.reset()
                    location.reload()
                }
                else {
                    throw data.message
                }
            })
            .catch(error => {
                alert(error)
            })
    }

})



/* ========== Project Update ========== */

document.querySelector('#projectTable tbody').addEventListener('click', async (event) => {
    if (event.target.classList.contains('edit-btn')) {
        let id = event.target.getAttribute('data-id')

        fetch(`/project/getSingle?id=${id}`)
            .then(res => res.json())
            .then(data => {
                const response = data.data
                if (data.status == "success") {
                    document.getElementById("name").value = response.name
                    document.getElementById("description").value = response.description
                    document.getElementById("editProjectId").value = response.id
                }
                else {
                    throw data.message
                }
            })
            .catch(error => {
                alert(error)
            })
    }
})

/* ========== Project Delete ========== */

document.querySelector('#projectTable tbody').addEventListener('click', async (event) => {
    if (event.target.classList.contains('delete-btn')) {
        let id = event.target.getAttribute('data-id')
        const response = confirm("Are you sure want to delete this project?")

        if (response) {
            fetch(`project/delete?id=${id}`, {
                method: 'DELETE'
            })
            .then(res => res.json())
            .then(data =>{
                if (data.status == "success") {
                    alert(data.message)
                    location.reload()
                }
                else {
                    throw data.message
                }
            })
            .catch(error => {
                alert(error)
            })
        }
    }
});