<template>
    <v-container>
      <v-card>
        <v-card-title>
          <h1>Movie List</h1>
        </v-card-title>
        <v-card-text>
          <v-list>
            <MovieItem
              v-for="movie in movies"
              :key="movie.id"
              :movie="movie"
            />
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="prevPage" :disabled="!prevUrl">Previous</v-btn>
          <v-btn @click="nextPage" :disabled="!nextUrl">Next</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </template>
  
  <script>
  import { computed, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import MovieItem from '../components/MovieItem.vue'
  
  export default {
    components: {
      MovieItem
    },
    setup() {
      const store = useStore()
      const movies = computed(() => store.state.movies)
      const nextUrl = computed(() => store.state.nextUrl)
      const prevUrl = computed(() => store.state.prevUrl)
  
      const fetchMovies = (url) => {
        store.dispatch('fetchMovies', url)
      }
  
      const nextPage = () => {
        if (nextUrl.value) {
          fetchMovies(nextUrl.value)
        }
      }
  
      const prevPage = () => {
        if (prevUrl.value) {
          fetchMovies(prevUrl.value)
        }
      }
      
      onMounted(() => {
        fetchMovies('/movies/')
      })
  
      return {
        movies,
        nextUrl,
        prevUrl,
        nextPage,
        prevPage
      }
    }
  }
  </script>
  