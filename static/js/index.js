$(document).ready(() => {
    const API_URI = "http://localhost:8080/api/v1"
    // RegisterScript
    // Создать куки и добавлять туда данные, по мере их поступления
    function registerFormComponent() {
        paginateComponent()
        fillInterests()
        formComponents(action = 'prepare')
    }

    function paginateComponent() {
        let counter = 1
        const FIRST_PAGE = 1
        const LAST_PAGE = 9
        let coefficient = 100 / LAST_PAGE
        let buttonPrevious = document.getElementsByClassName('prev')[0]
        let buttonNext = document.getElementsByClassName('next')[0]
        const ACTION_PREV = buttonPrevious.className
        const ACTION_NEXT = buttonNext.className
        let buttons = [buttonNext, buttonPrevious]
        for (let button of buttons) {
            button.addEventListener("click", (event) => {
                // Если мы дошли до последней страницы
                if (event.path[0].className === ACTION_NEXT && counter !== LAST_PAGE) {
                    // Если нажата кнопка next и это не последняя страница
                    formComponents(action = 'next', counter)
                    ++counter
                    progressBarComponent(counter, coefficient)
                } else if (event.path[0].className === ACTION_PREV && counter !== FIRST_PAGE) {
                    // Если нажата кнопка prev и это не первая страница
                    --counter
                    formComponents(action = 'prev', counter)
                    progressBarComponent(counter, coefficient)
                }
                console.log(counter, event.path[0].className)
            })
        }
    }

    function progressBarComponent(counter, coefficient) {
        if (counter * coefficient >= 100) {
            document.getElementsByClassName("progress-bar")[0].style.width = "100%"
        } else {
            document.getElementsByClassName("progress-bar")[0].style.width = `${counter * coefficient}%`
        }
    }

    function formComponents(action = "prepare", counter) {
        let listComponents = document.getElementsByClassName("register__component")
        if (action === "prepare") {
            for (let index = 1; index < listComponents.length; index++) {
                listComponents[index].style.display = "none"
            }
        } else if (action === "next") {
            listComponents[counter - 1].style.display = "none"
            listComponents[counter].style.display = "flex"
        } else if (action === "prev") {
            listComponents[counter - 1].style.display = "flex"
            listComponents[counter].style.display = "none"
        }
    }

    async function fillInterests() {
        const access_token = getCookie("access_token").access_token
        let listInterests = document.getElementsByClassName("list__interests")[0]
        const interests = await fetch(
            API_URI + "/interests",
            {
                headers: {
                    "x-access-tokens": access_token
                }
            }
        ).then((response) => {
            return response.json()
        })
        let counter = 0
        for (let value of interests) {
            let checkInputElement = document.createElement("input")
            checkInputElement.setAttribute("type", "checkbox")
            console.log(value)
            checkInputElement.setAttribute("name", `interest_${value.name}`)
            const checkDescription = document.createElement("span")
            checkDescription.appendChild(document.createTextNode(value.name))
            const wrapInput = document.createElement("label")
            wrapInput.setAttribute("class", "checkbox")
            wrapInput.appendChild(checkInputElement)
            wrapInput.appendChild(checkDescription)
            listInterests.appendChild(wrapInput)
            counter += 1
        }
    }

    function getCookie(cookieName) {
        let cookies = document.cookie.split(';')
        let result = {}
        for (let cookie of cookies) {
            if (cookie.includes(cookieName)) {
                let dataOfCookie = cookie.split('=')
                let cookieValue = dataOfCookie.slice(1).join('=')
                result[cookieName] = cookieValue
                return result
            }
        }
        return result
    }

    let fileInput = document.getElementById("file");
    fileInput.addEventListener("change", () => {
        let iconFileInput = document.getElementsByClassName("icon-file-upload")[0]
        let textFileInput = document.getElementsByClassName("js-file")[0]
        iconFileInput.src = "/static/img/check.svg"
        textFileInput.textContent = fileInput.value.split("\\").pop()
    });
    registerFormComponent()
})