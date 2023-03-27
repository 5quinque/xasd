<script setup>

import { computed, watchEffect, ref } from 'vue'
import { playlists } from '../utils/state.js'
import { useRoute } from 'vue-router'
import Track from './lists/Track.vue';
import EditablePlaylistTitle from "./EditablePlaylistTitle.vue";

const route = useRoute()
const playlist = ref(playlists.playlists.find(playlist => playlist.name === route.params.playlist))

watchEffect(() => {
    playlist.value = playlists.playlists.find(playlist => playlist.name === route.params.playlist)
})


</script>

<template>
    <EditablePlaylistTitle v-if="playlist" :playlist="playlist" />
    <Track v-if="playlist" :tracks="playlist.tracks" />
</template>
