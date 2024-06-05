import { createRouter, createWebHistory } from 'vue-router'
import MovieList from '../views/MovieList.vue'
import MovieDetail from '../views/MovieDetail.vue'

const routes = [
    { // route for Movie Listing
        path: '/',
        name: 'MovieList',
        component: MovieList
    },
    { // route for Movie Details 
      path: '/movies/:id',
      name: 'MovieDetail',
      component: MovieDetail
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router