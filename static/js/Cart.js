const updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    
    updateBtns[i].addEventListener('click',function(e){
        // e.preventDefault()
        const productId = this.dataset.product
        const action = this.dataset.action
        console.log('productId:', productId, '\nAction:', action);

        console.log('USER:', user)
        if (user === 'AnonymousUser'){
            addCookieItem(productId,action)
        }else {
            updateUserOrder(productId,action)
        }
    })
}

function addCookieItem(productId,action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] +=1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -=1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item');
            delete cart[productId]
        }
    }
    console.log("Cart:", cart)
    document.cookie =  'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

function updateUserOrder(productId,action){
    console.log('User is authenticated, sending data...');

    const url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then(res=>{
        return res.json()
    })
    .then(data=>{
        console.log(data);
        location.reload()
    })
}