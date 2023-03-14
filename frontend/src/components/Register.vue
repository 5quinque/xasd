<script setup>

import { ref } from 'vue'

const username = ref('')
const email_address = ref('')
const password = ref('')

// on submit send post request as json to /token
async function submit() {
    console.log('submit', username.value, email_address.value, password.value)

    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
            {
                "name": username.value,
                "email_address": email_address.value,
                "plaintext_password": password.value,
            }
        )
    };
    const response = await fetch("http://localhost:8000/user", requestOptions);
    const data = await response.json();

    // if response status code not 201 then throw error and display error message on page
    if (response.status !== 201) {
        throw new Error(data.message)
    }

    console.log('data', data)
    // const x = await fetch("/token")
}

</script>

<template>
    <h2>Register</h2>

    <form class="register-form">
        <div class="mb-3">
            <label for="Email" class="form-label">Username</label>
            <input v-model="username" type="text" class="form-control" name="username" id="username"
                aria-describedby="emailHelp">
        </div>
        <div class="mb-3">
            <label for="Email" class="form-label">Email address</label>
            <input v-model="email_address" type="email" class="form-control" name="email_address" id="email_address"
                aria-describedby="emailHelp">
        </div>
        <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" id="exampleInputPassword1">
        </div>
        <button type="submit" class="btn btn-primary" @click.prevent="submit">Register</button>
    </form>
</template>