$(document).ready(() => {
    const API_URI = "http://localhost:8080/api/v1"
    const IMAGE_PATH = "/static/user_images/"

    function main() {
        prepare()
        fillUserInfo()
        fillMessages()
    }

    function prepare() {
        // auto adjust textarea
        $('body').on('keyup', 'textarea', function () {
            $(this).height(0);
            $(this).height(this.scrollHeight);
        });
        $('body').find('textarea').keyup();
        document.getElementById("sendMessage").addEventListener("click", sendMessage)
    }

    async function fillUserInfo() {
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
            let userAvatar = document.getElementsByClassName("userAvatar")[counter]
            let userNameSurname = document.getElementsByClassName("userNameSurname")[counter]
            userAvatar.src = IMAGE_PATH + dialog.users[0].images[0].image_href
            for (let user of dialog.users) {
                if (user.id !== parseInt(getCookie("user_id").user_id)) {
                    userNameSurname.textContent = `${user.name} ${user.surname}`
                }
            }
            counter += 1
        }
    }

    function clearMessages() {
        // Clearing messages
        let listMessages = document.getElementsByClassName("list__messages")[0].children
        for (let i = listMessages.length - 1; i >= 0; --i) {
            listMessages[i].remove();
        }
    }

    async function fillMessages() {
        let listMessages = document.getElementsByClassName("list__messages")[0]
        let url = document.URL.split("/")
        let chat_id = url[url.length - 1]
        const messages = await fetch(
            API_URI + `/message/${chat_id}`,
            {
                headers: {
                    "x-access-tokens": getCookie("access_token").access_token
                }
            }
        ).then((response) => {
            return response.json()
        })
        console.log(messages)
        // Creating numbers of messages for next fillable
        for (let message of messages) {
            // Creating div with class
            let messageChat = document.createElement("div")
            // Detect type of message (from or to)
            if (message.user_id !== parseInt(getCookie("user_id").user_id)) {
                messageChat.setAttribute("class", "chat-message chat-message-from")
            } else {
                messageChat.setAttribute("class", "chat-message chat-message-to")
            }
            // Creating paragraph (content of message)
            let chatMessageContent = document.createElement("p")
            chatMessageContent.setAttribute("class", "chatMessageContent")
            // Creating span (content of time message)
            let chatMessageCreatedAt = document.createElement("span")
            chatMessageCreatedAt.setAttribute("class", "chat-message-created-at")
            // Adding properties to container of message
            messageChat.appendChild(chatMessageContent)
            messageChat.appendChild(chatMessageCreatedAt)
            listMessages.appendChild(messageChat)
        }
        let counter = 0
        for (let message of messages) {
            let chatMessage = document.getElementsByClassName("chat-message")[counter]
            // Message content
            chatMessage.children[0].textContent = message.text
            // Message created_at, getting only hour and minutes
            timeMessage = message.created_at.split(" ")[1].split(":")
            timeMessage.pop(2)
            chatMessage.children[1].textContent = timeMessage.join(":")
            counter += 1
        }
    }

    async function sendMessage() {
        let url = document.URL.split("/")
        let chat_id = parseInt(url[url.length - 1])
        let data = {
            "text": document.getElementById("messageText").value,
            "chat_id": chat_id,
            "user_id": parseInt(getCookie("user_id").user_id)
        }
        console.log(data)
        await fetch(
            API_URI + `/message/${chat_id}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-access-tokens": getCookie("access_token").access_token
                },
                body: JSON.stringify(data)
            }
        )
        location.reload()
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

