import { ref, reactive } from 'vue'

const FILE_URL = `https://f000.backblazeb2.com/file/xasdmedia/`

/**
 * The search query and results
 * @type {Object}
 * @property {String} query - The search query
 * @property {Array} results - The search results
 * @property {String} filter - The filter to apply to the search results
 * @property {Function} set_filter - Sets the filter to apply to the search results
 */
export const search = reactive({
    query: ref('Earth'),
    results: [],
    filter: ref('all'),
    set_filter(filter) {
        this.filter = filter
    },
})

/**
 * The currently playing track and track list
 * @type {Object}
 * @property {Number} current_track - The index of the currently playing track in the track_list
 * @property {Array} track_list - The list of tracks to play
 * @property {Boolean} playing - Whether or not the player is currently playing
 * @property {String} playing_timestamp - The current timestamp of the playing track
 * @property {String} playing_tracklength - The length of the playing track
 * @property {Number} playing_percentage - The percentage of the playing track that has been played
 */
export const now_playing = reactive({
    // player: new Player(),
    current_track: null,
    track_list: [],
    playing: ref(false),
    playing_timestamp: ref('00:00'),
    playing_tracklength: ref('00:00'),
    playing_percentage: ref(0),
    volume: ref(50),
    update(track) {
        console.log("updating now_playing", track)

        // before playing, pause the current playing tracks and reset it's progress
        if (this.playing) {
            console.log("pausing current track", this.track_list[this.current_track])
            this.pause()
            this.track_list[this.current_track].howl.seek(0)
            // this.track_list.forEach(t => {
            //     if (t.howl) {
            //         t.howl.pause()
            //         t.howl.seek(0)
            //     }
            // })
        }

        // if the track is not already in the track_list, add it
        if (!this.track_list.includes(track)) {
            this.track_list.push(track)
        }
        this.current_track = this.track_list.indexOf(track)

        // set the audio source in the track_list to the given track's file
        this.track_list[this.current_track].audio_src = FILE_URL + track.file.filepath

        this.playing = true

        console.log("track_list", this.track_list)
        this.play()
    },

    play() {
        console.log("playing track", this.track_list[this.current_track])
        const track = this.track_list[this.current_track]

        let sound

        // If we already loaded this track, use the current one.
        // Otherwise, setup and load a new Howl.
        if (track.howl) {
            console.log("howl already exists", track.howl)
            sound = track.howl
        } else {
            console.log("howl does not exist")
            sound = track.howl = new Howl({
                src: [track.audio_src],
                html5: true, // Force to HTML5 so that the audio can stream in (best for large files).
                onplay: () => {
                    // Display the duration.
                    this.playing_tracklength = formatTime(Math.round(sound.duration()))
                    // console.log("Track length: ", self.formatTime(Math.round(sound.duration())))

                    // Start upating the progress of the track.
                    this.step()
                },
                onload: () => {
                },
                onend: () => {
                    // self.skip(obj, 'next');
                },
                onpause: () => {
                },
                onstop: () => {
                },
                onseek: () => {
                }
            });
        }

        // Begin playing the sound.
        sound.play();
    },


    step() {
        const sound = this.track_list[this.current_track].howl
        const seek = sound.seek() || 0

        this.playing_timestamp = formatTime(Math.round(seek))
        this.playing_percentage = (((seek / sound.duration()) * 100) || 0)

        // console.log("step timestamp", formatTime(Math.round(seek)))

        // rerun this function in a second if the sound is still playing
        if (sound.playing()) {
            setTimeout(() => {
                this.step()
            }, 1000)
        }
    },

    /**
     * Pause the currently playing track.
     */
    pause() {
        this.track_list[this.current_track].howl.pause()
    },


    /**
     * Seek to a new position in the currently playing track.
     * @param  {Number} percent Percentage through the song to skip.
     */
    seek() {
        // console.log("seeking", this.playing_percentage)
        const sound = this.track_list[this.current_track].howl

        // Convert the percent into a seek position.
        if (sound.playing()) {
            sound.seek(sound.duration() * (this.playing_percentage / 100));
        }
    },

    update_volume() {
        // console.log("updating volume", this.volume)
        Howler.volume(this.volume / 100)
    },

    toggle_volume() {
        if (this.volume > 0) {
            this.volume = 0
        } else {
            this.volume = 50
        }
        this.update_volume()
    },

    add_to_queue(track) {
        this.track_list.push(track)
    },
    remove_from_queue(track) {
        this.track_list = this.track_list.filter(t => t !== track)
    },
    next_track() {
        console.log("next_track")
        if (this.track_list.length > 0 && this.current_track < this.track_list.length - 1) {
            // this.current_track = this.track_list.shift()
            this.current_track += 1
            // this.update(this.track_list.shift())
            // this.playing = true
        } else {
            this.current_track = null
            // this.playing = false
        }
    },
    toggle_play() {
        if (this.current_track === null) {
            return
        }

        this.playing = !this.playing
        if (this.playing) {
            this.play()
        } else {
            this.pause()
        }
    }
})

/**
 * Get the title of the currently playing track
 * 
 * @returns {String} The title of the currently playing track
 */
export function get_current_track_title() {
    // console.log("get_current_track_title", now_playing.current_track)
    if (now_playing.current_track !== null) {
        return now_playing.track_list[now_playing.current_track].title
    }
}

/**
 * Get the artist of the currently playing track
 * 
 * @returns {String} The artist of the currently playing track
 */
export function get_current_track_artist() {
    if (now_playing.current_track !== null) {
        return now_playing.track_list[now_playing.current_track].artist
    }
}

/**
 * Get the album of the currently playing track
 * 
 * @returns {String} The album of the currently playing track
 */
export function get_current_audio_src() {
    if (now_playing.current_track !== null) {
        return now_playing.track_list[now_playing.current_track].audio_src
    }
}


/**
 * Format the time from seconds to M:SS.
 * @param  {Number} secs Seconds to format.
 * @return {String}      Formatted time.
 */
function formatTime(secs) {
    const minutes = Math.floor(secs / 60) || 0;
    const seconds = (secs - minutes * 60) || 0;

    return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
}