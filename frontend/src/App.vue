<script setup>
import { RouterLink, RouterView } from 'vue-router'

import { alert, auth } from './utils/state.js'

import Player from './components/Player.vue'

import IconHome from './components/icons/IconHome.vue'
import IconSearch from './components/icons/IconSearch.vue'
import IconViewList from './components/icons/IconViewList.vue'

</script>

<template>
    <main>
        <div class="container-fluid h-100 d-flex flex-column">
            <div class="row flex-fill" style="min-height:0">
                <div class="col-2 mh-100 d-flex flex-column flex-shrink-0 p-3"
                    style="background-color: var( --bs-dark-bg-subtle );">
                    <a href=" /" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-light text-decoration-none">
                        <img alt="logo" class="logo" src="@/assets/logo.svg" width="60" height="60" />
                        <span class="fs-4">Xasd</span>
                    </a>
                    <hr>
                    <ul class="nav nav-pills flex-column mb-auto">
                        <li class="nav-item">
                            <RouterLink class="nav-link" active-class="active" to="/">
                                <IconHome />
                                Home
                            </RouterLink>
                        </li>
                        <li>
                            <RouterLink class="nav-link" active-class="active" to="/search">
                                <IconSearch />
                                Search
                            </RouterLink>
                        </li>
                        <li>
                            <RouterLink class="nav-link" active-class="active" to="/queue">
                                <IconViewList />
                                Queue
                            </RouterLink>
                        </li>
                    </ul>
                    <hr>
                    <strong v-if="auth.user" class="d-flex align-items-center justify-content-between text-light">
                        <img :src="'https://loremflickr.com/g/320/320/' + auth.user.name + '/all'" alt=""
                            class="rounded-circle me-2" width="32" height="32">
                        {{ auth.user.name }}
                        <a href="#" class="ms-2" @click="auth.logout()">
                            Logout
                        </a>
                    </strong>
                    <div v-else class="d-flex align-items-center justify-content-between">
                        <RouterLink to="/login" class="link-primary">
                            Login
                        </RouterLink>
                        <RouterLink to="/register" class="link-primary">
                            Register
                        </RouterLink>
                    </div>
                </div>

                <div class="col-10 mh-100 py-3" style=" overflow-y: scroll;">
                    <div v-if="alert.is_visible()" :class="alert.alert_class()" role="alert">
                        <strong>{{ alert.type }}</strong> {{ alert.message }}
                        <button type="button" class="btn-close" aria-label="Close" @click.prevent="alert.hide()"></button>
                    </div>

                    <RouterView />
                </div>
            </div>
            <div class="row flex-shrink-0  border-top" style="background-color: var(--bs-tertiary-bg);">
                <div class="col-12">
                    <Player />
                </div>
            </div>
        </div>
    </main>
</template>

