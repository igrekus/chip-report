<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div class="q-pb-sm">
    <q-table
      dense
      :data="table.data"
      :columns="table.columns"
      row-key="name"
      hide-bottom
    >
      <template v-slot:top>
        <q-item>
          <q-input v-model.number="table.rows" type="number" dense label="Количество строк"
                   @input="onRowNumChanged(table.id)"/>&nbsp;&nbsp;&nbsp;
        </q-item>
        <q-item>
          <q-input v-model="table.header" dense label="Заголовок:"></q-input>
        </q-item>
        <q-item>
          <q-btn round dense icon="file_copy" />
        </q-item>
        <q-item class="absolute-right">
          <q-btn round dense icon="delete" />
        </q-item>
      </template>
      <template v-slot:header-cell="props">
        <q-th :props="props">
          {{ props.col.label }}<br/>
          {{ props.col.condition }}<br/>
          {{ props.col.norms }}
        </q-th>
      </template>
    </q-table>
  </div>
</template>

<script>
export default {
  name: 'report-table',
  props: ['table'],
  data () {
    return {}
  },
  methods: {
    onRowNumChanged (tableId) {
      console.log(tableId)
    }
  }
}
</script>
