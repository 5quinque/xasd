/**
 * Player class containing the state of our playlist and where we are in it.
 * Includes all methods for playing, skipping, updating the display, etc.
 */
const Player = function () {
};


export default Player

Player.prototype = {
    /**
     * Play a song in the playlist.
     * @param  {object} obj Track to play. Must contain the following: audio_src, title, artist. Optionally, can contain: howl (Howl object). If not, a new Howl will be created and saved to this track.
     */
    play: function (obj) {
        var track = obj.track_list[obj.current_track]
        // obj.playing_timestamp

        var self = this
        var sound

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
                onplay: function () {
                    // Display the duration.
                    obj.playing_tracklength = self.formatTime(Math.round(sound.duration()))
                    // console.log("Track length: ", self.formatTime(Math.round(sound.duration())))

                    // Start upating the progress of the track.
                    self.step(obj)
                },
                onload: function () {
                },
                onend: function () {
                    self.skip(obj, 'next');
                },
                onpause: function () {
                },
                onstop: function () {
                },
                onseek: function () {
                }
            });
        }

        // Begin playing the sound.
        sound.play();

        // console.log("sound state", sound.state())
    },

    /**
     * Pause the currently playing track.
     */
    pause: function (track) {
        track.howl.pause()
    },

    /**
     * Skip to the next or previous track.
     * @param  {String} direction 'next' or 'prev'.
     */
    skip: function (obj, direction) {
        var self = this;

        // Get the next track based on the direction of the track.


        // Get the next track based on the direction of the track.3
        // var index = 0;
        // if (direction === 'prev') {
        //     index = self.index - 1;
        //     if (index < 0) {
        //         index = self.playlist.length - 1;
        //     }
        // } else {
        //     index = self.index + 1;
        //     if (index >= self.playlist.length) {
        //         index = 0;
        //     }
        // }

        // self.skipTo(index);
    },

    /**
     * Skip to a specific track based on its playlist index.
     * @param  {Number} index Index in the playlist.
     */
    skipTo: function (index) {
        var self = this;

        // Stop the current track.
        if (self.playlist[self.index].howl) {
            self.playlist[self.index].howl.stop();
        }

        // Play the new track.
        self.play(index);
    },

    /**
     * Set the volume and update the volume slider display.
     * @param  {Number} val Volume between 0 and 1.
     */
    volume: function (val) {
        var self = this;

        // Update the global volume (affecting all Howls).
        Howler.volume(val);

        // Update the display on the slider.
        // var barWidth = (val * 90) / 100;
    },

    /**
     * Seek to a new position in the currently playing track.
     * @param  {Number} per Percentage through the song to skip.
     */
    seek: function (per) {
        var self = this;

        // Get the Howl we want to manipulate.
        var sound = self.playlist[self.index].howl;

        // Convert the percent into a seek position.
        if (sound.playing()) {
            sound.seek(sound.duration() * per);
        }
    },

    /**
     * The step called within requestAnimationFrame to update the playback position.
     */
    step: function (obj) {
        var self = this
        var track = obj.track_list[obj.current_track]


        // Get the Howl we want to manipulate.
        // var sound = self.playlist[self.index].howl;

        // Determine our current seek position.
        // var seek = sound.seek() || 0;
        // timer.innerHTML = self.formatTime(Math.round(seek));
        // progress.style.width = (((seek / sound.duration()) * 100) || 0) + '%';

        // console.log("track", track)
        var sound = track.howl
        var seek = sound.seek() || 0

        obj.playing_timestamp = self.formatTime(Math.round(seek))
        obj.playing_percentage = (((seek / sound.duration()) * 100) || 0)


        console.log("step..", self.formatTime(Math.round(seek)))

        // rerun this function in a second if the sound is still playing
        if (sound.playing()) {
            console.log("sound is playing")
            setTimeout(function () {
                self.step(obj)
            }, 1000)
        }

    },

};



























// photo,sharp focus, upper body shot, closeup