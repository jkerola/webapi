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
        url: 'http://127.0.0.1:5000/api/reviews/'
      }).then((response) => {
        console.log(response.data);
        a = response.data;
        document.getElementById("reviews-all").innerHTML = JSON.stringify(a);
      }, (error) => {
        console.log(error);
      });    
})

s2.addEventListener('submit', (e) => {
    e.preventDefault()
    review_id = document.getElementById("review_id_view").value
    if (review_id) {
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/api/reviews/' + review_id +'/'
          }).then((response) => {
            console.log(response.data);
            a = response.data;
            document.getElementById("view-review").innerHTML = JSON.stringify(a);
          }, (error) => {
            a = error.response.data
            document.getElementById("view-review").innerHTML = JSON.stringify(a);
          });
    }
        
})

s3.addEventListener('submit', (e) => {
    e.preventDefault()
    batch_id = document.getElementById("batch_id_post").value
    student_id = document.getElementById("student_id_post").value
    review_value = document.getElementById("review_value_post").value

        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/api/batches/' + batch_id + '/reviews/',
            data: {
                value: review_value,
	            student_id: student_id
            }
        }).then((response) => {
            // console.log(response.data);
            a = response.data;
            document.getElementById("add-review").innerHTML = a;
        }).catch ((error) => {
            a = error.response.data
            document.getElementById("add-review").innerHTML = a;
        });
})

s4.addEventListener('submit', (e) => {
    e.preventDefault()
    old_review_id = document.getElementById("old_review_id").value
    batch_id_edit = document.getElementById("batch_id_edit").value
    student_id_edit = document.getElementById("student_id_edit").value
    value_edit = document.getElementById("value_edit").value
        axios({
            method: 'put',
            url: 'http://127.0.0.1:5000/api/reviews/'+ old_review_id +'/',
            data: {
                value: value_edit,
                student_id: student_id_edit,
                batch_id: batch_id_edit
            }
        }).then((response) => {
            // console.log(response.data);
            a = response.data;
            document.getElementById("edit-review").innerHTML = a;
        }).catch ((error) => {
            a = error.response.data
            document.getElementById("edit-review").innerHTML = a;
        });
})


s5.addEventListener('submit', (e) => {
    e.preventDefault()
    review_id = document.getElementById("review_id_delete").value
    axios({
        method: 'delete',
        url: 'http://127.0.0.1:5000/api/reviews/' + review_id +'/'
      }).then((response) => {
        console.log(response.data);
        a = response.data;
        document.getElementById("delete-review").innerHTML = JSON.stringify(a);
      }, (error) => {
        a = error.response.data
        document.getElementById("delete-review").innerHTML = JSON.stringify(a);
      });    
})



