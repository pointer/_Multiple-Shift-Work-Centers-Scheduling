<template>
  <div id="app"></div>
</template>

<script>
import { defineComponent, h } from 'vue'
import { RouterView } from 'vue-router'

export default defineComponent({
  name: 'App',
  setup() {
    return () => h('v-app', {}, [
      h('v-app-bar', { color: 'primary' }, () => [
        h('v-app-bar-title', {}, () => 'Multiple Shift Scheduling System'),
        h('v-spacer'),
        h('v-btn', 
          { to: '/', text: true },
          () => 'Home'
        ),
        h('v-btn',
          { to: '/employees', text: true },
          () => 'Employees'
        ),
        h('v-btn',
          { to: '/work-centers', text: true },
          () => 'Work Centers'
        ),
        h('v-btn',
          { to: '/schedule', text: true },
          () => 'Schedule'
        )
      ]),
      h('v-main', {}, () => [
        h('v-container', { fluid: true }, () => [
          h(RouterView)
        ])
      ])
    ])
  }
})
</script>

<style>
#app {
  font-family: 'Roboto', sans-serif;
}
</style>