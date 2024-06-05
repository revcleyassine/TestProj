<template>
    <v-container>
      <v-card>
        <v-card-title>
          <h1>{{ movie.title }}</h1>
        </v-card-title>
        <v-card-text>
          <p>{{ movie.description }}</p>
          <h2>Actors</h2>
          <v-list>
            <ActorItem
              v-for="actor in movie.actors"
              :key="actor.id"
              :actor="actor"
            />
          </v-list>
          <v-btn @click="saveAllActors">Save All Actors</v-btn>
          <h2>Average Grade</h2>
          <p>{{ movie.average_grade }}</p>
          <h2>Reviews</h2>
          <v-list>
            <ReviewItem
              v-for="review in movie.reviews"
              :key="review.id"
              :review="review"
            />
          </v-list>
          <h2>Add Review</h2>
          <v-form @submit.prevent="addReview">
            <v-text-field
              v-model="newReview.grade"
              label="Grade"
              type="number"
              :rules="gradeRules"
              required
            ></v-text-field>
            <v-btn type="submit" :disabled="!isFormValid">Add Review</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import { useRoute } from 'vue-router'
  import ActorItem from '../components/ActorItem.vue'
  import ReviewItem from '../components/ReviewItem.vue'
  
  export default {
    components: {
      ActorItem,
      ReviewItem
    },
    setup() {
      const store = useStore()
      const route = useRoute()
      const movieId = route.params.id
      const movie = computed(() => store.state.movieDetails)
      const newReview = ref({ grade: null, movie: movieId })
  
      const gradeRules = [
        v => v >= 0 || 'Grade must be at least 0',
        v => v <= 5 || 'Grade must be at most 5'
      ]
  
      const isFormValid = computed(() => {
        return gradeRules.every(rule => rule(newReview.value.grade) === true)
      })
  
      const fetchMovieDetails = (id) => {
        store.dispatch('fetchMovieDetails', id)
      }
  
      const addReview = () => {
        if (isFormValid.value) {
          store.dispatch('addReview', newReview.value)
          newReview.value.grade = null  // Reset the grade input
        }
      }
  
      const saveAllActors = () => { // this can be optimized by using the batch update using a single api call
        movie.value.actors.forEach(actor => {
          store.dispatch('updateActor', actor)
        })
      }
  
      onMounted(() => {
        fetchMovieDetails(movieId)
      })
  
      return {
        movie,
        newReview,
        gradeRules,
        isFormValid,
        addReview,
        saveAllActors
      }
    }
  }
  </script>
  