const formElement = document.getElementById("registerForm")

formElement.addEventListener("submit", async(e)=>{
    e.preventDefault()

    const formData = new FormData(formElement)
    const data = Object.fromEntries(formData)

    fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data =>{
        if (data.status == "success") {
            alert(data.message)
            formElement.reset()
            location.href = "/login"
        }
        else{
            throw data.message
        }
    })
    .catch(error =>{
        alert(error)
    })
})