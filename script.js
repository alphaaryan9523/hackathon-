// script.js

const apiUrl = 'http://127.0.0.1:5000/inventory';

async function fetchInventory() {
    const response = await fetch(apiUrl);
    const inventory = await response.json();
    displayInventory(inventory);
}

async function addItem() {
    const id = document.getElementById('itemId').value;
    const name = document.getElementById('itemName').value;
    const quantity = document.getElementById('itemQuantity').value;

    if (!id || !name || !quantity) {
        alert("Please fill out all fields.");
        return;
    }

    const newItem = { id: parseInt(id), name, quantity: parseInt(quantity) };
    await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newItem)
    });

    document.getElementById('itemId').value = '';
    document.getElementById('itemName').value = '';
    document.getElementById('itemQuantity').value = '';
    fetchInventory();
}

async function deleteItem(id) {
    await fetch(`${apiUrl}/${id}`, {
        method: 'DELETE'
    });
    fetchInventory();
}

function displayInventory(inventory) {
    const inventoryList = document.getElementById('inventoryList');
    inventoryList.innerHTML = '';

    inventory.forEach(item => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `${item.name} (Quantity: ${item.quantity})`;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.innerText = 'Delete';
        deleteBtn.className = 'deleteBtn';
        deleteBtn.onclick = () => deleteItem(item.id);

        listItem.appendChild(deleteBtn);
        inventoryList.appendChild(listItem);
    });
}

document.getElementById('addItemBtn').addEventListener('click', addItem);
window.onload = fetchInventory;
