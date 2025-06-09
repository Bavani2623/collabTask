fetch('/dashboard/analytics')
.then(res => res.json())
.then(data => {

    const response = data.data
    if (data.status == "success") {
        console.log(data)
        
        document.getElementById('taskCount').textContent = response.taskCount
        document.getElementById('projectCount').textContent = response.projectCount
    }
    else {
        throw data.message
    }
})
.catch(error => {
    alert(error)
})
    