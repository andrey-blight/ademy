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
        console.log(dialogs)
        let counter = 0
        for (let dialog of dialogs) {
            console.log(dialog)
            let newDialog = document.getElementsByClassName("dialog")[0].cloneNode(true)
            let hr = document.createElement("hr")
            let userAvatar = document.getElementsByClassName("userAvatar")[counter]
            let userNameSurname = document.getElementsByClassName("userNameSurname")[counter]
            let lastMessage = document.getElementsByClassName("lastMessage")[counter]
            let lastMessageTime = document.getElementsByClassName("lastMessageTime")[counter]
            let dialogsContainer = document.getElementsByClassName("list__dialogs")[0]
            dialogsContainer.appendChild(hr)
            document.querySelector(".list__dialogs").appendChild(newDialog)
            console.log(dialog, userNameSurname)
            userAvatar.src = IMAGE_PATH + dialog.users[0].images[0].image_href
            for (let user of dialog.users) {
                if (user.id !== parseInt(getCookie("user_id").user_id)) {
                    console.log(user.id, getCookie("user_id").user_id)
                    newDialog.href = `/messanger/chat/${user.id}`
                    userNameSurname.textContent = `${user.name} ${user.surname}`
                }
            }
            lastMessage.textContent = dialog.last_message
            lastMessageTime.textContent = dialog.last_message_created_at
            counter += 1
        }
        let dialog = document.getElementsByClassName("dialog")
        dialog[dialog.length - 1].remove()
    }

    function getCookie(cookieName) {
        let cookies = document.cookie.split(';')
        let result = {}
        for (let cookie of cookies) {
            if (cookie.includes(cookieName)) {
                let dataOfCookie = cookie.split('=')
                let cookieValue = dataOfCookie.slice(1).join('=')
                result[cookieName] = cookieValue
                // console.log(result)
                return result
            }
        }
        // console.log(result)
        return result
    }

    main()
})