<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Player from './components/Player.vue'

import IconHome from './components/icons/IconHome.vue'
import IconSearch from './components/icons/IconSearch.vue'
import IconViewList from './components/icons/IconViewList.vue'

</script>

<template>
    <main>
        <div class="container-fluid h-100 d-flex flex-column">
            <!-- <div class="row flex-shrink-0">
                                                                                                                                                                            <div class="col-12">Navbar </div>
                                                                                                                                                                        </div> -->
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
                    <div class="dropdown">
                        <a href="#" class="d-flex align-items-center text-light text-decoration-none dropdown-toggle"
                            data-bs-toggle="dropdown" aria-expanded="false">
                            <img src="https://loremflickr.com/g/320/320/girl/all" alt="" class="rounded-circle me-2"
                                width="32" height="32">
                            <strong>user</strong>
                        </a>
                        <ul class="dropdown-menu dropdown-menu-dark text-small shadow">
                            <li><a class="dropdown-item" href="#">Settings</a></li>
                            <li><a class="dropdown-item" href="#">Profile</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a class="dropdown-item" href="#">Sign out</a></li>
                        </ul>
                    </div>
                </div>

                <div class="col-10 mh-100 py-3" style=" overflow-y: scroll;">
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

