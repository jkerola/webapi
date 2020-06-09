console.log('client side javascript file is loaded')

s1 = document.getElementById("s1")
s2 = document.getElementById("s2")
s3 = document.getElementById("s3")
s4 = document.getElementById("s4")
s5 = document.getElementById("s5")

s1.addEventListener('submit', (e) => {
    e.preventDefault()
    axios({
        method: 'get',
        url: 'http://127.0.0.1:5000/api/batches/'
      }).then((response) => {
        console.log(response.data);
        a = response.data;
        document.getElementById("batches-all").innerHTML = JSON.stringify(a);
      }, (error) => {
        console.log(error);
      });    
})

s2.addEventListener('submit', (e) => {
    e.preventDefault()
    batch_id = document.getElementById("batch_id_view").value
    if (batch_id) {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/api/batches/' + batch_id +'/'
          }).then((response) => {
            console.log(response.data);
            a = response.data;
            document.getElementById("view-batch").innerHTML = JSON.stringify(a);
          }, (error) => {
            a = error.response.data
            document.getElementById("view-batch").innerHTML = JSON.stringify(a);
          }); 
    }
       
})

s3.addEventListener('submit', (e) => {
    e.preventDefault()
    user_id = document.getElementById("user_id_post").value
    locations = document.getElementById("location_post").value
    amount = document.getElementById("amount_post").value
    coffee = document.getElementById("coffee_post").value
    date_brewed = document.getElementById("date_brewed_post").value
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/api/users/' + user_id + '/batches/',
            data: {
                location : locations,
                amount: amount,
                coffee: coffee,
                date_brewed: date_brewed
            }
        }).then((response) => {
            // console.log(response.data);
            a = response.data;
            document.getElementById("add-batch").innerHTML = a;
        }).catch ((error) => {
            a = error.response.data
            document.getElementById("add-batch").innerHTML = a;
        });
})

s4.addEventListener('submit', (e) => {
    e.preventDefault()
    old_batch_id = document.getElementById("old_batch_id").value
    location_edit = document.getElementById("location_edit").value
    amount_edit = document.getElementById("amount_edit").value
    coffee_edit = document.getElementById("coffee_edit").value
    date_brewed_edit = document.getElementById("date_brewed_edit").value
        axios({
            method: 'put',
            url: 'http://127.0.0.1:5000/api/batches/'+ old_batch_id +'/',
            data: {
                location: location_edit,
                amount: amount_edit,
                coffee: coffee_edit,
                date_brewed: date_brewed_edit
            }
        }).then((response) => {
            // console.log(response.data);
            a = response.data;
            document.getElementById("edit-batch").innerHTML = a;
        }).catch ((error) => {
            a = error.response.data
            document.getElementById("edit-batch").innerHTML = a;
        });
})


s5.addEventListener('submit', (e) => {
    e.preventDefault()
    batch_id = document.getElementById("batch_id_delete").value
    axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/api/batches/' + batch_id +'/'
      }).then((response) => {
        console.log(response.data);
        a = response.data;
        document.getElementById("delete-batch").innerHTML = JSON.stringify(a);
      }, (error) => {
        a = error.response.data
        document.getElementById("delete-batch").innerHTML = JSON.stringify(a);
      });    
})


