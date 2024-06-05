<template>
    <v-list-item>
        <v-list-item-content>
            Grade: {{ review.grade }}
        </v-list-item-content>
    </v-list-item>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    name: 'ReviewItem',
    props: {
        review: {
            type: Object,
            required: true
        }
    }
})
</script>