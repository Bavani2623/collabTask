const userId = document.getElementById("editUserProfile").value  
fetch(`/user/getSingle?id=${userId}`)
.then(res => res.json())
.then(data => {

    const response = data.data
    if (data.status == "success") {
        console.log(data)
        
        document.getElementById('name').value = response.name
        document.getElementById('email').value = response.email
        document.getElementById('mobile').value = response.mobileNumber
        document.getElementById('password').value = response.password
    }
    else {
        throw data.message
    }
})
.catch(error => {
    alert(error)
})

const formElement = document.getElementById("userForm")
formElement.addEventListener("submit", async(e)=>{
    e.preventDefault()

    const formData = new FormData(formElement)
    const data = Object.fromEntries(formData)

    fetch(`/user/update?id=${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data =>{
        if (data.status == "success") {
            alert(data.message)
            window.location.reload()
        }
        else{
            throw data.message
        }
    })
    .catch(error =>{
        alert(error)
    })
})