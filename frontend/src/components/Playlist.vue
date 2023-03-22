<script setup>

import { computed, ref, watch } from 'vue'
import { playlists } from '../utils/state.js'
import { useRoute } from 'vue-router'
import Track from './lists/Track.vue';


const route = useRoute()

const playlist_name = ref(route.params.playlist)
watch(() => route.params.playlist, () => {
    playlist_name.value = route.params.playlist
})


const playlist = computed(() => {
    return playlists.playlists.find(playlist => playlist.name === playlist_name.value)
})

</script>

<template>
    <h2>{{ playlist_name }}</h2>
    <Track v-if="playlist" :tracks="playlist.tracks" />
</template>
