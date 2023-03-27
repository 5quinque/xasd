<script setup>

import { playlists } from '../utils/state.js'
import IconThreeDotsVertical from './icons/IconThreeDotsVertical.vue'


const props = defineProps(['playlist'])


</script>

<template>
    <VTooltip class="d-inline" :triggers="['click']" :autoHide="true">
        <a href="#" class="text-secondary bg-transparent">
            <IconThreeDotsVertical />
        </a>
        <template #popper>
            <ul class="list-group">
                <li class="list-group-item mb-0">
                    <a href="#" class="text-white popover-link bg-transparent"
                        @click.stop="playlists.delete_playlist(props.playlist)">Delete Playlist</a>
                </li>
            </ul>
        </template>
    </VTooltip>
</template>