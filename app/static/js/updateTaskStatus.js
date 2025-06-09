const taskContainer = document.getElementById("taskContainer")

const todoContainer = document.getElementById("todoContainer")
const pendingContainer = document.getElementById("pendingContainer")
const doneContainer = document.getElementById("doneContainer")

document.addEventListener('DOMContentLoaded', () => {
    taskContainer.innerHTML = ''
    todoContainer.innerHTML = ''
    pendingContainer.innerHTML = ''
    doneContainer.innerHTML = ''

    fetch('/task/getAllNames?isPage=true')
    .then(res => res.json())
    .then(data => {
        if (data.status == "success") {
            const response = data.data
            response.forEach(task => {
                let taskCard = `
                <div class="card p-0 mb-3 taskCard" data-id=${task.id} style="width: 100; z-index: 1000" !important>
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title">${task.name}</h5>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">${task.description}</h5>
                    </div>
                </div>
            `;
                if (task.status == "todo") {
                    todoContainer.innerHTML += taskCard
                }
                else if (task.status == "pending") {
                    pendingContainer.innerHTML += taskCard
                }
                else if (task.status == "done") {
                    doneContainer.innerHTML += taskCard
                }
                else{
                    taskContainer.innerHTML += taskCard
                }
            });
        }
        else {
            throw data.message
        }
    })
    .catch(error => {
        alert(error)
    })
})