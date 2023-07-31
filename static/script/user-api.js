const code = $('form').attr('id');

$.ajax({
    'url': `/api/v1/users/user/${code}`,
    'method' : 'GET'
}).done(user => {
    $('#username').val(user.username);
    $('#name').val(user.name);
    $('#email').val(user.email);
})

function join() {
    username = $('#username').val();
    name = $('#name').val();
    email = $('#email').val();
    password = $('#password').val();

    data = {}

    if(username !== '') {
        data['username'] = username;
    } else {
        alert('아이디를 입력해주세요.');
        $('#username').focus();
        return;
    }

    if (name !== '') {
        data['name'] = name;
    }

    if (email !== '') {
        data['email'] = email;
    }

    if (password !== '') {
        data['password'] = password;
    } else {
        alert('비밀번호를 입력해주세요.');
        $('#password').focus();
        return;
    }

    $.ajax({
        "url": `/api/v1/users/`,
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        "data": JSON.stringify(data),
    }).done(function (response) {
        console.log(response);

        if(response.username === username) {
            location.href = "/login";
        } else {
            alert("중복되는 아이디입니다.");
            location.href = "/join";
        }
    }).fail(function (error) {
        console.log(error);
    })
}

function update_user() {
    name = $('#name').val();
    email = $('#email').val();
    password = $('#password').val();

    data = {}

    if(name !== '') {
        data['name'] = name;
    }
    if(email !== '') {
        data['email'] = email;
    }
    if(password !== '') {
        data['password'] = password;
    }

    $.ajax({
        "url": `/api/v1/users/user/${code}`,
        "method": "PUT",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        "data": JSON.stringify(data),
    }).done(function (response) {
        console.log(response);
    }).fail(function(error) {
        console.log(error);
    })
}
