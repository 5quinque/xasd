<script setup>

import { ref } from 'vue'
import { auth } from '../utils/state.js'


const username = ref('')
const password = ref('')


// on submit send post request as json to /token
async function submit() {
    console.log('submit', username.value, password.value)

    const body = new URLSearchParams();
    body.append('username', username.value);
    body.append('password', password.value);


    const requestOptions = {
        method: "POST",
        headers: { "accept": "application/json", "Content-Type": "application/x-www-form-urlencoded" },
        body: body
    };
    const response = await fetch("http://localhost:8000/token", requestOptions);
    const data = await response.json();

    // if response status code not 201 then throw error and display error message on page
    // if (response.status !== 200) {
    if (!response.ok) {
        throw new Error(data.message)
    }

    // get current user from /user/me
    const userResponse = await fetch("http://localhost:8000/user/me", {
        headers: {
            "accept": "application/json",
            "Authorization": `Bearer ${data.access_token}`
        }
    })

    const userData = await userResponse.json()

    // set auth token in local storage
    auth.login(userData, data.access_token)

}

</script>

<template>
    <div class="login-form w-100 m-auto mt-5 text-center">
        <form>
            <h1 class="h3 mb-3 fw-normal">Log in</h1>
            <div class="form-floating">
                <input v-model="username" type="text" name="username" class="form-control" id="username"
                    placeholder="username">
                <label for="username">Username</label>
            </div>
            <div class="form-floating">
                <input v-model="password" type="password" name="password" class="form-control" id="password"
                    placeholder="Password">
                <label for="password">Password</label>
            </div>

            <button class="w-100 btn btn-lg btn-primary" type="submit" @click.prevent="submit">Log in</button>
        </form>
    </div>
</template>

<style scoped>
.login-form {
    max-width: 450px;
    padding: 15px;
}

.login-form #username {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}

.login-form #password {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}

.form-floating>label {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    padding: 1rem .75rem;
    overflow: hidden;
    text-align: start;
    text-overflow: ellipsis;
    white-space: nowrap;
    pointer-events: none;
    border: var(--bs-border-width) solid transparent;
    transform-origin: 0 0;
    transition: opacity .1s ease-in-out, transform .1s ease-in-out;
}

.form-floating {
    position: relative;
}
</style>