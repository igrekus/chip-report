<template>
  <q-layout view="lHh lpR lFf" class="WAL position-relative bg-grey-4">

    <q-drawer v-model="leftDrawer" side="left" behavior="desktop" bordered>
      <q-toolbar>
        <q-btn round icon="add"/>
      </q-toolbar>
      <ul>
        <li>table column</li>
      </ul>
    </q-drawer>

    <q-page-container class="bg-grey-2">
      <router-view/>
    </q-page-container>

  </q-layout>
</template>

<script>
export default {
  name: 'MyLayout',

  data () {
    return {
      leftDrawer: true
    }
  }
}
</script>
