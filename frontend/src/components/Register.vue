<script setup>

import { alert } from '../utils/state.js'

import { ref } from 'vue'

const username = ref('')
const email_address = ref('')
const password = ref('')

// on submit send post request as json to /token
async function submit() {
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

    if (!response.ok) {
        console.log('error', data.detail)
        alert.show(data.detail[0].msg, 'error')
        return
    }

    console.log('data', data)

    alert.show('Registered successfully', 'success')
}

</script>

<template>
    <div class="register-form w-100 m-auto mt-5 text-center">
        <form>

            <h1 class="h3 mb-3 fw-normal">Register</h1>
            <div class="form-floating">
                <input v-model="username" type="text" name="username" class="form-control" id="username"
                    placeholder="username">
                <label for="username">Username</label>
            </div>
            <div class="form-floating">
                <input v-model="email_address" type="text" name="email_address" class="form-control" id="email_address"
                    placeholder="email address">
                <label for="email_address">Email Address</label>
            </div>
            <div class="form-floating">
                <input v-model="password" type="password" name="password" class="form-control" id="password"
                    placeholder="Password">
                <label for="password">Password</label>
            </div>
            <button class="w-100 btn btn-lg btn-primary" type="submit" @click.prevent="submit">Register</button>
        </form>
    </div>
</template>

<style scoped>
.register-form {
    max-width: 450px;
    padding: 15px;
}

.register-form #username {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}

.register-form #email_address {
    margin-bottom: -1px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}

.register-form #password {
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