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
    <h2>Login</h2>

    <form class="login-form">
        <div class="mb-3">
            <label for="Email" class="form-label">Username</label>
            <input v-model="username" type="text" class="form-control" name="username" id="username"
                aria-describedby="emailHelp">
        </div>
        <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" id="exampleInputPassword1">
        </div>
        <button type="submit" class="btn btn-primary" @click.prevent="submit">Login</button>
    </form>
</template>