<script setup>

import { now_playing } from '../../utils/state.js'
import IconPlayFill from '../icons/IconPlayFill.vue'
import IconThreeDotsVertical from '../icons/IconThreeDotsVertical.vue'


const props = defineProps(['tracks'])

</script>
<template>
    <ul class="list-group">
        <li class="list-group-item" :class="{ 'text-white': now_playing.is_track_playing(track) }" v-for="track in tracks">

            <VTooltip class="d-inline" :triggers="['click']" :autoHide="true">
                <a href="#" class="text-secondary bg-transparent">
                    <IconThreeDotsVertical />
                </a>
                <template #popper>
                    <ul class="list-group">
                        <li v-if="now_playing.is_track_queued(track)" class="list-group-item mb-0">
                            <a href="#" class="text-white popover-link bg-transparent"
                                @click.stop="now_playing.remove_from_queue(track)">Remove from Queue</a>
                        </li>
                        <li v-else class="list-group-item mb-0">
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
                        <hr class="my-0">
                        <li class="list-group-item mb-0">
                            <a href="#" class="text-white popover-link bg-transparent">Add to playlist</a>
                        </li>
                    </ul>
                </template>
            </VTooltip>

            <span v-if="now_playing.is_track_playing(track)" class="text-white">
                <IconPlayFill style="margin-left: -5px" />
            </span>

            <img v-if="track.album.cover_art"
                :src="'https://f000.backblazeb2.com/file/xasdmedia/' + track.album.cover_art.filepath" class="album-cover"
                alt="...">
            <a href="#" target="_blank" class="title" @click.prevent="now_playing.update(track)">
                {{ track.title }}
            </a> -
            <span class="author">
                <RouterLink active-class="active" :to="{ name: 'artist', params: { artist: track.artist.name } }">
                    {{ track.artist.name }}
                </RouterLink>
            </span>
        </li>
    </ul>
</template>