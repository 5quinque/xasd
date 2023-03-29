<script setup>

import { watchEffect } from 'vue'
import { search } from '../utils/state.js'
import SearchResults from './SearchResults.vue'

const SEARCH_API_URL = `http://localhost:8000/search/any/`

watchEffect(async () => {
    // this effect will run immediately and then
    // re-run whenever searchQuery.value changes
    const url = `${SEARCH_API_URL}${search.query}`
    search.results = await (await fetch(url)).json()
})

</script>

<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-5 form-outline">
                <input name="query" v-model="search.query" type="search" class="form-control border-0 rounded-pill fs-5"
                    id="search-input" style="background-color: var(--bs-light-bg-subtle);" placeholder="🔎 Search">
            </div>
        </div>
        <div class="row py-3">
            <SearchResults />
        </div>
    </div>
</template>