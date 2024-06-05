<template>
    <v-list-item>
      <v-list-item-content>
        <router-link :to="'/movies/' + movie.id">{{ movie.title }}</router-link>
      </v-list-item-content>
    </v-list-item>
  </template>
  
  <script>
  import { defineComponent } from 'vue'
  
  export default defineComponent({
    name: 'MovieItem',
    props: {
      movie: {
        type: Object,
        required: true
      }
    }
  })
  </script>