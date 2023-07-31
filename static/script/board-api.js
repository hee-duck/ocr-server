const board_number = window.location.pathname.split('/board/')[1]

$.ajax({
    "url": `/api/v1/boards/board/${board_number}`,
    "method": "GET",
    "timeout": 0,
}).done(function (board) {
    console.log(board);                 // 확인용
    $('#author').text(board.author === null ? 'anonymous' : board.author.username);
    $('#title').val(board.title);
    $('#contents').val(board.contents);
    $('#loaded_file').attr('src', board.loaded_file);
    $('#created_at').val(board.created_at);
    $('#modified_at').val(board.modified_at);

    // 이미지 파일 있으면 텍스트 변환 버튼 보여주기
    if (board.loaded_file) {
        $('#ocr-btn').show();
    } else {
        $('#ocr-btn').hide();
    }
});

// 언어 팩 선택
function selectLanguages() {
    // checkbox에서 선택된 값 가져오기
    const selectedLanguages = Array.from(document.querySelectorAll('input[name="language"]:checked')).map((checkbox) => checkbox.value);
    return selectedLanguages;
}

// 텍스트 변환 버튼을 클릭했을 때 실행되는 함수
function clickOcrBtn() {
    const selectedLanguages = selectLanguages();
    const image_file = document.getElementById("image-file").files[0];

    if (selectedLanguages.length < 1) {
        alert("적어도 하나 이상의 언어 팩을 선택해야 합니다.");
        return;
    }

    const data = new FormData();
    data.append('image', image_file);
    data.append('lang', selectedLanguages);

    $.ajax({
        url: `/api/v1/boards/board/${board_number}`,
        method: "POST",
        data: data,
        processData: false,
        contentType: false,
    })
    .done((data) => {
        if (data.data) {
            // 반환된 텍스트가 있는 경우, 해당 텍스트를 화면에 표시 -> 파일로 바꾸기 
            const ocr_result = data.data;
            document.getElementById("ocr-result").innerText = ocr_result;
        } else {
            alert("텍스트 변환에 실패했습니다.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}
