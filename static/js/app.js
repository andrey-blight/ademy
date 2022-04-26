$(document).ready(() => {
    const API_URI = "http://localhost:8080/api/v1"

    function main() {
        if (checkViewUsers()) {
            getUsers()
            handleClickUser()
        } else {
            setAnimation()
        }
    }

    async function getUsers() {
        // TODO: что - то с API, отбивает разное кол-во пользователей
        const USER_COUNT = 2
        console.log("Filling users...")
        const users = await fetch(
            API_URI + `/recommend_user/${USER_COUNT}/${getCookie("user_sex").user_sex}`,
            {
                headers: {
                    "x-access-tokens": getCookie("access_token").access_token
                }
            }
        ).then((response) => {
            return response.json()
        })
        console.log(users)
        // Заполняем пользователей
        localStorage.setItem("users", JSON.stringify(users))
        // Устанавливаем текущего пользователя на 0
        localStorage.setItem("currentUser", `${USER_COUNT - 1}`)
        // console.log(JSON.parse(localStorage.getItem("users")))
        // Заполняем пользователя id: = 0
        fillUser(localStorage.getItem("currentUser"))
    }

    async function handleClickUser() {
        document.getElementById("eventLike").addEventListener("click", async () => {
            console.log("eventLike")
            let to_id = JSON.parse(localStorage.getItem("users"))[localStorage.getItem("currentUser")]?.id
            if (!to_id) {
                document.cookie = "checked=true; max-age=3600"
                setAnimation()
                return false
            }
            console.log(`Like to ${to_id} from ${getCookie("user_id").user_id}`)
            const like = await fetch(
                API_URI + `/like/${getCookie("user_id").user_id}/${to_id}`,
                {
                    method: "POST",
                    headers: {
                        "x-access-tokens": getCookie("access_token").access_token
                    }
                }
            ).then((response) => {
                return response.json()
            })
            console.log(`Filling user: id = ${localStorage.getItem("currentUser")}`)
            fillUser(parseInt(localStorage.getItem("currentUser")))
        })
        document.getElementById("eventDislike").addEventListener("click", () => {
            console.log("eventDislike")
            fillUser(parseInt(localStorage.getItem("currentUser")))
        })
    }

    function fillUser(id) {
        console.log(`Filling user with localId = ${id}`)
        const IMAGE_PATH = "/static/user_images/"
        let currentUser = JSON.parse(localStorage.getItem("users"))[id]
        if (!currentUser) {
            document.cookie = "checked=true; max-age=3600"
            setAnimation()
            return false
        }
        let userAvatarImage = document.getElementById("userAvatarImage")
        let userName = document.getElementById("userName")
        let userAge = document.getElementById("userAge")
        let userDescription = document.getElementById("userDescription")
        let userInterests = document.getElementById("userInterests")
        if (currentUser?.images[0]?.image_href) {
            userAvatarImage.src = IMAGE_PATH + currentUser.images[0].image_href
        }
        userName.textContent = currentUser.name
        userAge.textContent = currentUser.age
        userDescription.textContent = currentUser.about_yourself
        userInterests.textContent = ""
        for (let interest of currentUser.interests) {
            userInterests.textContent += `[tag] ${interest.name}`
        }
        // Удаляем этого пользователя из даты
        let usersData = JSON.parse(localStorage.getItem("users"))
        usersData.pop(id)
        localStorage.setItem("users", JSON.stringify(usersData))
        // Увеличиваем на 1, чтобы потом достать следующего пользователя
        localStorage.setItem("currentUser", `${parseInt(localStorage.getItem("currentUser")) - 1}`)
    }

    function setAnimation() {
        document.getElementById("endUsers").style.display = "block"
        document.getElementsByClassName("user__description")[0].style.display = 'none'
    }

    function checkViewUsers() {
        const isChecked = (getCookie("checked")?.checked === 'true');
        return !isChecked;
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