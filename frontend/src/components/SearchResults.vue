<script setup>

import { search } from '../utils/state.js'
import Track from './lists/Track.vue';


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
        <Track v-if="search.results" :tracks="search.results.tracks" />
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
        <ul class="list-group">
            <li class="list-group-item" v-for="album in search.results.albums">
                <a :href="album.url" target="_blank" class="title">
                    {{ album.name }} - {{ album.artist.name }}
                </a>
                <img v-if="album.cover_art" :src="'https://f000.backblazeb2.com/file/xasdmedia/' + album.cover_art.filepath"
                    class="album-cover" alt="...">
            </li>
        </ul>
    </div>
</template>

<style scoped></style>