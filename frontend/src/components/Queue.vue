<script setup>

import { now_playing, search } from '../utils/state.js'

</script>

<template>
    <h2>Queue:</h2>
    <ul class="list-group list-group-flush">
        <li class="list-group-item" v-if="now_playing.track_list" v-for="track in now_playing.track_list">
            <a :href="track.url" target="_blank" class="title" @click.prevent="now_playing.update(track)">
                {{ track.title }}
            </a> -
            <span class="author">
                <a :href="track.url" target="_blank">{{ track.artist.name }}</a>
            </span>
        </li>
    </ul>
</template>