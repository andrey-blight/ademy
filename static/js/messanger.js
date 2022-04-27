$(document).ready(() => {
    const API_URI = "http://localhost:8080/api/v1"
    const IMAGE_PATH = "/static/user_images/"

    function main() {
        chatsInit()
    }

    async function chatsInit() {
        const dialogs = await fetch(
            API_URI + `/chats/${getCookie("user_id").user_id}`,
            {
                headers: {
                    "x-access-tokens": getCookie("access_token").access_token
                }
            }
        ).then((response) => {
            return response.json()
        })
        let userAvatar = document.getElementById("userAvatar")
        let userNameSurname = document.getElementById("userNameSurname")
        let lastMessage = document.getElementById("lastMessage")
        let lastMessageTime = document.getElementById("lastMessageTime")
        for (let dialog of dialogs) {
            userAvatar.src = IMAGE_PATH + dialog.users[0].images[0].image_href
            for (let user of dialog.users) {
                if (user.id !== getCookie("user_id").user_id) {
                    userNameSurname.textContent = `${user.name} ${user.surname}`
                }
            }
            lastMessage.textContent = dialog.last_message
        }
        console.log(dialogs)
    }

    function getCookie(cookieName) {
        let cookies = document.cookie.split(';')
        let result = {}
        for (let cookie of cookies) {
            if (cookie.includes(cookieName)) {
                let dataOfCookie = cookie.split('=')
                let cookieValue = dataOfCookie.slice(1).join('=')
                result[cookieName] = cookieValue
                console.log(result)
                return result
            }
        }
        // console.log(result)
        return result
    }

    main()
})