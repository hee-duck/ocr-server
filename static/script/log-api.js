function login() {
    $.ajax({
        "url": `/api/v1/users/login`,
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        "data": JSON.stringify({
            "username" : $('#username').val(),
            "password" : $('#password').val()
        }),
    }).done(function (response) {
        console.log("response : ", response);

        if (response.login === 'success') {
            location.href = '/mypage';
        } else {
            alert("회원정보를 확인하세요.");
            location.href = '/login';
        }
    }).fail(function (error) {
        console.log("error : ", error);
    })
}