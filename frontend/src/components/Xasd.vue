
<script setup>

import Recommended from './Recommended.vue'
import Search from './Search.vue'
import Queue from './Queue.vue'
import Artist from './Artist.vue'
import Login from './Login.vue'
import Register from './Register.vue'

import { useRoute } from 'vue-router'
import { ref, computed, watch } from 'vue'

const route = useRoute()

const searchPage = computed(() => {
    return route.path === '/search'
})


const homePage = computed(() => {
    return route.path === '/'
})

const queuePage = computed(() => {
    return route.path === '/queue'
})

const artistPage = computed(() => {
    return route.name === 'artist'
})

const loginPage = computed(() => {
    return route.name === 'login'
})

const registerPage = computed(() => {
    return route.name === 'register'
})


</script>

<template>
    <div>
        <header>
            <!-- Header content here -->
        </header>
        <main>
            <Recommended v-if="homePage" />
            <Search v-if="searchPage" />
            <Queue v-if="queuePage" />
            <Artist v-if="artistPage" />
            <Login v-if="loginPage" />
            <Register v-if="registerPage" />
        </main>
    </div>
</template>

<style>
a {
    text-decoration: none;
    color: #42b883;
}

li {
    line-height: 1.5em;
    margin-bottom: 20px;
}

.title {
    font-weight: bold;
}
</style>