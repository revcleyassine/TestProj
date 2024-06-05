import { createStore } from 'vuex'
import axios from '../plugins/axios'  // Import the Axios plugin

export default createStore({
    state: {
        movies: [],
        nextUrl: null,
        movieDetails: {},
        prevUrl: null
    },
    mutations: {
        SET_MOVIES(state, movies) {
            state.movies = movies
        },
        SET_NEXT_URL(state, nextUrl) {
            state.nextUrl = nextUrl
        },
        SET_PREV_URL(state, prevUrl) {
            state.prevUrl = prevUrl
        },
        SET_MOVIE_DETAILS(state, movieDetails) {
            state.movieDetails = movieDetails
        },
        ADD_REVIEW(state, review) {
            if (state.movieDetails.reviews) {
                state.movieDetails.reviews.push(review)
            }
        },
        UPDATE_ACTOR(state, actor) {
            const actorIndex = state.movieDetails.actors.findIndex(a => a.id === actor.id)
            if (actorIndex !== -1) {
                state.movieDetails.actors.splice(actorIndex, 1, actor)
            }
        }
    },
    actions: {
        fetchMovies({ commit }, url) { // we use this action to load the movies listing paginated
            axios.get(url)
                .then(response => {
                    commit('SET_MOVIES', response.data.results)
                    commit('SET_NEXT_URL', response.data.next)
                    commit('SET_PREV_URL', response.data.previous)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        fetchMovieDetails({ commit }, id) { // we use this action to load the MovieDetails including related actors and reviews agregated grades
            axios.get(`/movies/${id}/`)
                .then(response => {
                    commit('SET_MOVIE_DETAILS', response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        addReview({ commit, dispatch }, review) {
            axios.post('/reviews/', review)
                .then(response => {
                    commit('ADD_REVIEW', response.data)
                    dispatch('fetchMovieDetails', review.movie)  // Refresh movie details to update average grade

                })
                .catch(error => {
                    console.log(error)
                })
        },
        updateActor({ commit }, actor) {  // this can be optimized by using batch update in one api call <should add a new view in the backend to handle that>
            axios.put(`/actors/${actor.id}/`, actor)
                .then(response => {
                    commit('UPDATE_ACTOR', response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
})