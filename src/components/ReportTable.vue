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
          <q-btn @click="addColumn(table.id)" round dense icon="add">
            <q-tooltip :delay="300" content-style="font-size: 12px">Добавить колонку к таблице</q-tooltip>
          </q-btn>
        </q-item>
        <q-item>
          <q-btn @click="copyTable(table.id)" round dense icon="file_copy">
            <q-tooltip :delay="300" content-style="font-size: 12px">Добавить копию таблицы</q-tooltip>
          </q-btn>
        </q-item>
        <q-item class="absolute-right">
          <q-btn @click="deleteTable(table.id)" round dense icon="delete">
            <q-tooltip :delay="300" content-style="font-size: 12px">Удалить таблицу</q-tooltip>
          </q-btn>
        </q-item>
      </template>
      <template v-slot:header-cell="props">
        <q-th @click="editColumn(table.id, props.col.name)" :props="props" class="q-hoverable">
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
    },
    copyTable (tableId) {
      console.log('copy', tableId)
    },
    deleteTable (tableId) {
      console.log('delete', tableId)
    },
    addColumn (tableId) {
      console.log('add column to', tableId)
    },
    editColumn (tableId, colId) {
      console.log('edit column', tableId, colId)
    }
  }
}
</script>
