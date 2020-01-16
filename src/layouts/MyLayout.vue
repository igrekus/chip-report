<template>
  <q-layout view="hHh lpR fFf">

    <q-page-container>
      <router-view/>
    </q-page-container>

  </q-layout>
</template>

<script>
export default {
  name: 'MyLayout',

  data () {
    return {
      leftDrawer: true,
      text: '',
      dense: true
    }
  }
}
</script>
