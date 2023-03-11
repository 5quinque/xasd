<script setup>

import { ref, watchEffect } from 'vue'

import { now_playing, get_current_track_title, get_current_track_artist } from '../utils/state.js'

import IconPause from './icons/player/IconPause.vue';
import IconPlay from './icons/player/IconPlay.vue';
import IconSkipBackward from './icons/player/IconSkipBackward.vue';
import IconSkipForward from './icons/player/IconSkipForward.vue';

import IconVolumeMute from './icons/player/IconVolumeMute.vue';
import IconVolumeDown from './icons/player/IconVolumeDown.vue';
import IconVolumeUp from './icons/player/IconVolumeUp.vue';

const audio = ref(null)

// const sound = ref(null)

// watchEffect(async () => {
//     console.log('now_playing.current_track changed to', now_playing.track_list[now_playing.current_track])
//     // Setup the new Howl.
//     const sound = new Howl({
//         src: now_playing.get_current_audio_src(),
//         // src: [now_playing.audio_src],
//         html5: true
//     });
//     sound.play()
//     // Howler.volume(0.5)

//     // if (now_playing.current_track) {
//     //     // console.log("playing audio", audio.value)
//     //     audio.value.play()
//     // }
// }, {
//     flush: 'post',
// })

// watchEffect(async () => {
//     // watch percentage range and trigger seek function
//     console.log('now_playing.playing_percentage changed to', now_playing.playing_percentage)
//     now_playing.seek(now_playing.playing_percentage)
// })

// keep this
// watchEffect(async () => {
//     if (!sound) return

//     console.log('now_playing.playing changed to', now_playing.playing)
//     if (now_playing.playing) {
//         sound.play()
//     } else {
//         sound.pause()
//     }
// })

</script>

<template>
    <footer class="d-flex flex-wrap justify-content-between align-items-center py-0 my-0 vh-10">
        <p class="col-md-4 mb-0 text-muted">
            <span class="text-white" v-if="now_playing.current_track !== null">
                <span class="title">{{ get_current_track_title() }}</span> by {{
                    get_current_track_artist().name }}
            </span>
            <span v-else>Nothing playing 😢</span>
        </p>
        <div
            class="col-md-4 d-flex align-items-center justify-content-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">

            <div class="container-fluid">
                <div class="row g-0 text-center">
                    <div class="col-12 pt-2">
                        <button class="btn text-white" @click="now_playing.previous_track()">
                            <IconSkipBackward width="35px" height="35px" />
                        </button>
                        <button class="btn text-white" @click="now_playing.toggle_play()">
                            <template v-if="now_playing.playing">
                                <IconPause width="35px" height="35px" />
                            </template>
                            <template v-else>
                                <IconPlay width="35px" height="35px" />
                            </template>
                        </button>
                        <button class="btn text-white" @click="now_playing.next_track()">
                            <IconSkipForward width="35px" height="35px" />
                        </button>
                    </div>
                </div>
                <div class="row g-0 pb-1">
                    <div class="d-flex align-items-center">
                        <!-- <div class="col-6 d-flex justify-content-start"> -->
                        <small class="text-muted px-2">{{ now_playing.playing_timestamp }}</small>
                        <!-- </div> -->
                        <!-- <div class="col-6 text-right d-flex justify-content-end"> -->
                        <!-- </div> -->
                        <input type="range" class="w-100 form-range" min="0" max="100"
                            v-model="now_playing.playing_percentage" @click="now_playing.seek()">
                        <!-- <div class="w-100 progress" role="progressbar" aria-label="Example 1px high" aria-valuenow="25"
                                                                                                                                                                aria-valuemin="0" aria-valuemax="100" style="height: 5px">
                                                                                                                                                                <div class="progress-bar" style="width: 25%"></div>
                                                                                                                                                            </div> -->
                        <small class="text-muted px-2">{{ now_playing.playing_tracklength }}</small>
                    </div>

                </div>
            </div>

            <!-- <audio ref="audio" controls :src="now_playing.audio_src" @ended="now_playing.next_track()"></audio> -->
        </div>
        <div class="col-md-4 d-flex justify-content-end">
            <div class="d-flex align-items-center">
                <button class="btn text-white" @click="now_playing.toggle_volume()">
                    <template v-if="now_playing.volume == 0">
                        <IconVolumeMute width="25px" height="25px" />
                    </template>
                    <template v-else-if="now_playing.volume < 40">
                        <IconVolumeDown width="25px" height="25px" />
                    </template>
                    <template v-else>
                        <IconVolumeUp width="25px" height="25px" />
                    </template>
                </button>
                <input type="range" class="w-100 form-range" min="0" max="100" v-model="now_playing.volume"
                    @click="now_playing.update_volume()">
            </div>
        </div>
    </footer>
</template>
