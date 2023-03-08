<script setup>

import { now_playing, search } from '../utils/state.js'

// import bootstrap from 'bootstrap'
// // import bootstrap from 'bootstrap'
// import 'bootstrap/dist/js/bootstrap.min.js'

// const popover = new bootstrap.Popover('.popover-dismiss', {
//     trigger: 'focus'
// })

// import Popover from bootstrap
// import Popover from 'bootstrap/dist/js/bootstrap.bundle.min.js'

// const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
// const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

const filter_class = function (filter) {
    return {
        'text-bg-primary': search.filter === filter,
        'text-bg-secondary': search.filter !== filter
    }
}

</script>

<template>
    <div class="">
        <span class="badge rounded-pill m-1" :class="filter_class('all')"
            @click.prevent="search.set_filter('all')">All</span>
        <span class="badge rounded-pill m-1" :class="filter_class('songs')"
            @click.prevent="search.set_filter('songs')">Songs</span>
        <span class="badge rounded-pill m-1" :class="filter_class('artists')"
            @click.prevent="search.set_filter('artists')">Artists</span>
        <span class="badge rounded-pill m-1" :class="filter_class('albums')"
            @click.prevent="search.set_filter('albums')">Albums</span>
    </div>
    <div v-if="search.filter === 'all' || search.filter === 'songs'">
        <h2>Tracks:</h2>
        <ul class="list-group list-group-flush">
            <li class="list-group-item" v-if="search.results" v-for="track in search.results.tracks">
                <a :href="track.url" target="_blank" class="title" @click.prevent="now_playing.update(track)">
                    {{ track.title }}
                </a> -
                <span class="author">
                    <a :href="track.url" target="_blank">{{ track.artist.name }}</a>
                </span>
                <a tabindex="0" class="btn btn-sm btn-primary" role="button" data-bs-toggle="popover"
                    data-bs-trigger="focus" data-bs-title="Dismissible popover" data-bs-content="Added to queue"
                    @click.prevent="now_playing.add_to_queue(track)">
                    Add to queue
                </a>
                <!-- <button type="button" class="btn btn-lg btn-danger" data-bs-toggle="popover" data-bs-title="Popover title"
                                                                                                                                                                    data-bs-content="And here's some amazing content. It's very engaging. Right?">Click to toggle
                                                                                                                                                                    popover</button> -->
                <!-- <a href="#" class="btn btn-primary btn-sm" @click.prevent="now_playing.add_to_queue(track)">Add to queue</a> -->
            </li>
        </ul>
    </div>

    <div v-if="search.filter === 'all' || search.filter === 'artists'">
        <h2>Artists:</h2>
        <ul class="list-group list-group-flush">
            <li class="list-group-item" v-for="artist in search.results.artists">
                <a :href="artist.url" target="_blank" class="title">
                    {{ artist.name }}
                </a>
            </li>
        </ul>
    </div>

    <div v-if="search.filter === 'all' || search.filter === 'albums'">
        <h2>Albums:</h2>
        <ul class="list-group list-group-flush">
            <li class="list-group-item" v-for="album in search.results.albums">
                <a :href="album.url" target="_blank" class="title">
                    {{ album.name }} - {{ album.artist.name }}
                </a>
            </li>
        </ul>
    </div>
</template>