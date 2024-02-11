const BASE_URL = `http://127.0.0.1:5000`





function login() {
   var email = document.getElementById('loginEmail').value;
   var password = document.getElementById('loginPassword').value;

   var data = {
       email: email,
       password: password
   };
   console.log(data);
   fetch(`${BASE_URL}/login`, {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
   })
   .then(response => response.json())
   .then(data => {
       document.getElementById('message').innerText = data.message;
       console.log(data)  // log the response
   })
   .catch(error => {
       console.error('Error:', error);
   });


}

function register() {
   var name = document.getElementById('registerName').value;
   var email = document.getElementById('registerEmail').value;
   var password = document.getElementById('registerPassword').value;

   var data = {
       name: name,
       email: email,
       password: password
   };

   fetch(`${BASE_URL}/register`, {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
   })
   .then(response => response.json())
   .then(data => {
       document.getElementById('message').innerText = data.message;
       console.log(data); // log the response
   })
   .catch(error => {
       console.error('Error:', error);
   });
}


