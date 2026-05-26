function addClass(class_id) {
    fetch(`/addclass/${class_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Class added or already in list');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding class.');
    });
}