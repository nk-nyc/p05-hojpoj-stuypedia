function deleteClass(classId) {
    fetch(`/delete_class/${classId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting class.');
    });
}

function deleteStudentClass(classId) {
    fetch(`/delete_student_class/${classId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting class.');
    });
}

function approveClass(classId) {
    fetch(`/approve_class/${classId}`, {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error approving class.');
    });
}

