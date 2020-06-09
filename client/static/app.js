console.log('client side javascript file is loaded')

s1 = document.getElementById("s1")
s2 = document.getElementById("s2")
s3 = document.getElementById("s3")
s4 = document.getElementById("s4")

s1.addEventListener('submit', (e) => {
    e.preventDefault()
    axios({
        method: 'get',
        url: 'http://127.0.0.1:5000/api/users/'
      }).then((response) => {
        console.log(response.data);
        a = response.data;
        document.getElementById("users-all").innerHTML = JSON.stringify(a);
      }, (error) => {
        console.log(error);
      });    
})

s2.addEventListener('submit', (e) => {
    e.preventDefault()
    user_id = document.getElementById("student_id_view").value
    if (user_id) {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/api/users/' + user_id +'/'
          }).then((response) => {
            console.log(response.data);
            a = response.data;
            document.getElementById("view-user").innerHTML = JSON.stringify(a);
          }, (error) => {
            a = error.response.data
            document.getElementById("view-user").innerHTML = JSON.stringify(a);
          }); 
    }
       
})

s3.addEventListener('submit', (e) => {
    e.preventDefault()
    user_id = document.getElementById("user_id_post").value
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/api/users/',
            data: {
                student_id: user_id
            }
        }).then((response) => {
            // console.log(response.data);
            a = response.data;
            document.getElementById("add-user").innerHTML = a;
        }).catch ((error) => {
            a = error.response.data
            document.getElementById("add-user").innerHTML = a;
        });
})

s4.addEventListener('submit', (e) => {
    e.preventDefault()
    old_student_id = document.getElementById("old_student_id").value
    updated_student_id = document.getElementById("updated_student_id").value
        axios({
            method: 'put',
            url: 'http://127.0.0.1:5000/api/users/'+ old_student_id +'/',
            data: {
                student_id: updated_student_id
            }
        }).then((response) => {
            // console.log(response.data);
            a = response.data;
            document.getElementById("edit-user").innerHTML = a;
        }).catch ((error) => {
            a = error.response.data
            document.getElementById("edit-user").innerHTML = a;
        });
})





