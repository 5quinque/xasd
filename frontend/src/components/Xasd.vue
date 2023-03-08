
<script setup>

import Recommended from './Recommended.vue'
import Search from './Search.vue'
import Queue from './Queue.vue'

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

console.log('searchPage', searchPage)

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