<script setup>

import { now_playing, search } from '../utils/state.js'

import IconThreeDotsVertical from './icons/IconThreeDotsVertical.vue'

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
                <a href="#" target="_blank" class="title" @click.prevent="now_playing.update(track)">
                    {{ track.title }}
                </a> -
                <span class="author">
                    <a :href="track.url" target="_blank">{{ track.artist.name }}</a>
                </span>

                <VTooltip class="d-inline" :triggers="['click']" :autoHide="true">
                    <a href="#" class="text-secondary bg-transparent">
                        <IconThreeDotsVertical />
                    </a>
                    <template #popper>
                        <ul class="list-group">
                            <li class="list-group-item mb-0">
                                <a href="#" class="text-white popover-link bg-transparent"
                                    @click.stop="now_playing.add_to_queue(track)">Add to
                                    Queue</a>
                            </li>
                            <li class="list-group-item mb-0">
                                <a href="#" class="text-white popover-link bg-transparent">Go to artist</a>
                            </li>
                            <li class="list-group-item mb-0">
                                <a href="#" class="text-white popover-link bg-transparent">Go to album</a>
                            </li>
                        </ul>
                    </template>
                </VTooltip>
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