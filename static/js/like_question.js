function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const init = () => {
    const cards = document.querySelectorAll('.card')

    for (const card of cards) {
        const likeButton = card.querySelector('.like-question-button')
        const likeCounter = card.querySelector('.like-question-counter')
        const questionId = card.dataset.questionId

        likeButton.addEventListener('click', () => {
            const request = new Request(`/${questionId}/like_question`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    key: 'value',
                    anotherKey: 'anotherValue'
                })
            })
            fetch(request)
                .then((response) => response.json())
                .then((data) => likeCounter.innerHTML = data.likes_count)
        })
    }
}

init()