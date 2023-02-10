//Returns a collection of all elements in the document with the specified class name, update-cart
//and assign to variable updateBtns
var updateBtns = document.getElementsByClassName('update-cart') 

for (var i = 0; i < updateBtns.length; i++){
    //When the updateBtns (Buttons) is clicked, execute the command below
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product        //Get the data of product(productID) and assign to variable productID
        var action = this.dataset.action            //Get the data of action(remove/delete/add) and assign to variable action
        
        console.log('productId: ', productId, ' action: ', action)
        console.log("USER:", user)

        updateUserOrder(productId, action)

    })
}

function updateUserOrder(productId, action){
    var url = "/update_item/"
    fetch(url,{
        method: 'POST', //explicitly tell it to make a POST request because fetch defaults to making a GET request
        headers: {
            'X-CSRFToken': csrftoken, //prevent Cross Site Request Forgery attacks
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'productId': productId, 'action': action}) //productID and Action is JavaScript object of the data we want to send
    })
    .then((response) =>{
        if (!response.ok) {
            // error processing
            throw 'Error';
        }
        return response.json() //Convert response to JSON
    })
    .then((data) =>{
        //Perform actions with the response data from the view
        console.log('data', data)
        location.reload()
    })
}