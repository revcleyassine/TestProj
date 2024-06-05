<template>
    <v-list-item>
        <v-list-item-content>
            <v-form>
                <v-text-field v-model="actorData.first_name" label="First Name"></v-text-field>
                <v-text-field v-model="actorData.last_name" label="Last Name"></v-text-field>
            </v-form>
        </v-list-item-content>
    </v-list-item>
</template>

<script>
import { defineComponent, toRefs } from 'vue'

export default defineComponent({
    name: 'ActorItem',
    props: {
        actor: {
            type: Object,
            required: true
        }
    },
    setup(props) {
        const { actor } = toRefs(props)

        return {
            actorData: actor
        }
    }
})
</script>