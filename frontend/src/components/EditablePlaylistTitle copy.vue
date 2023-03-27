<script setup>
import { ref, nextTick } from 'vue';

import { playlists } from '../utils/state.js'

const isEditing = ref(false);

const props = defineProps(['playlist'])
const playlist_name_input = ref(props.playlist.name)


function startEditing() {
    isEditing.value = true;
    // Using the nextTick method to ensure that the input element is
    // mounted and ready to receive focus before calling the focus method.
    nextTick(() => {
        // Focus on the text input element
        const input = document.querySelector(".editable-text input");
        input.focus();
        // Select the input text
        input.select();
    });
}

async function saveChanges() {
    nextTick(() => {
        if (playlist_name_input.value !== props.playlist.name) {
            console.log("saveChanges: " + playlist_name_input.value, props)
            props.playlist.name = playlist_name_input.value
            playlists.update_playlist_name(props.playlist)
        }
        isEditing.value = false;
    });
}


</script>

<template>
    <div class="editable-text">
        <div class="row">
            <div class="col-5 form-outline">

                <template v-if="!isEditing">
                    <h2 class="playlist-title" @click="startEditing">
                        {{ props.playlist.name }}
                        <span class="icon-pencil"></span>
                    </h2>
                </template>
                <template v-else>

                    <div class="input-group mb-3">
                        <input type="text" v-model="playlist_name_input" class="form-control border-0 fs-5"
                            style="background-color: var(--bs-light-bg-subtle);" @blur="saveChanges"
                            @keydown.enter="saveChanges" />
                        <button class="btn btn-outline-secondary icon-check" type="button" @click="saveChanges"></button>
                    </div>
                </template>
            </div>
        </div>

    </div>
</template>


<style>
.editable-text .icon-pencil,
.editable-text .icon-check {
    cursor: pointer;
}

.editable-text .icon-check {
    font: 1em sans-serif;
}

.editable-text .icon-pencil:before {
    content: "\270E";
}

.editable-text .icon-check:before {
    content: "\2713";
}
</style>