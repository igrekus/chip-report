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
          <q-btn @click="onAddColumnClicked" round dense icon="add">
            <q-tooltip :delay="300" content-style="font-size: 12px">Добавить колонку к таблице</q-tooltip>
          </q-btn>
        </q-item>
        <q-item>
          <q-btn @click="copyTable(table.id)" round dense icon="file_copy">
            <q-tooltip :delay="300" content-style="font-size: 12px">Добавить копию таблицы</q-tooltip>
          </q-btn>
        </q-item>
        <q-item class="absolute-right">
          <q-btn @click="deleteTable" round dense icon="delete">
            <q-tooltip :delay="300" content-style="font-size: 12px">Удалить таблицу</q-tooltip>
          </q-btn>
        </q-item>
      </template>
      <template v-slot:header-cell="props">
        <q-th @click="onEditColumnClicked(props.col.name)" :props="props">
          {{ props.col.label }}<br/>
          {{ props.col.condition }}<br/>
          {{ props.col.norms }}<br/>
          ср={{ props.col.mid }}&nbsp;&nbsp;&nbsp;разбр={{ props.col.spread }}&nbsp;&nbsp;&nbsp;шаг={{ props.col.step }}
        </q-th>
      </template>
    </q-table>

    <q-dialog v-model="columnEditDialog">
      <q-card style="width: 500px" class="q-px-sm">

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObject.label" label="Параметр:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input filled autogrow v-model="columnEditObject.condition" label="Условие:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObject.norms" label="Норма:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model.number="columnEditObject.mid" type="number" label="Среднее:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model.number="columnEditObject.spread" type="number" label="Разброс:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model.number="columnEditObject.step" type="number" label="Шаг:" dense/>
          </q-item-section>
        </q-item>

        <q-item>
          <q-btn primary small color="primary" label="ОК" @click="onDlgAccept"/>
        </q-item>
      </q-card>

    </q-dialog>

  </div>
</template>

<script>
export default {
  name: 'report-table',
  props: ['table'],
  data () {
    return {
      columnEditDialog: false,
      columnEditObject: {
        name: null,
        label: '',
        align: 'center',
        field: null,
        condition: '',
        norms: '',
        index: 0,
        mid: 0,
        spread: 0,
        step: 0
      }
    }
  },
  methods: {
    onRowNumChanged (tableId) {
      console.log(tableId)
    },
    copyTable (tableId) {
      console.log('copy', tableId)
    },
    deleteTable () {
      console.log('delete', this.table.id)
    },
    onAddColumnClicked () {
      this.columnEditObject = {
        name: null,
        label: '',
        align: 'center',
        field: null,
        condition: '',
        norms: '',
        index: 0,
        mid: 0,
        spread: 0,
        step: 0
      }
      this.columnEditDialog = true
    },
    onEditColumnClicked (colId) {
      let colToEdit = this.table.columns.find(col => {
        return col.name === colId
      })
      this.columnEditObject.name = colToEdit.name
      this.columnEditObject.label = colToEdit.label
      this.columnEditObject.condition = colToEdit.condition
      this.columnEditObject.norms = colToEdit.norms
      this.columnEditObject.mid = colToEdit.mid
      this.columnEditObject.spread = colToEdit.spread
      this.columnEditObject.step = colToEdit.step

      this.columnEditObject.index = colToEdit.index
      this.columnEditObject.field = colToEdit.field
      this.columnEditObject.align = colToEdit.align

      this.columnEditDialog = true
    },
    onDlgAccept () {
      this.columnEditDialog = false
      let index = this.table.columns.findIndex(el => this.columnEditObject.name === el.name)
      if (index === -1) {
        this.addColumn()
        return
      }

      this.editColumn(index)
    },
    addColumn () {
      console.log(this.table.columns)

      let newColumn = {
        label: this.columnEditObject.label,
        condition: this.columnEditObject.condition,
        norms: this.columnEditObject.norms,
        mid: this.columnEditObject.mid,
        spread: this.columnEditObject.spread,
        step: this.columnEditObject.step,
        align: this.columnEditObject.align,
        name: null,
        index: this.columnEditObject.index,
        field: this.columnEditObject.field
      }

      const [lastItem] = this.table.columns.slice(-1)
      const [index] = [lastItem.name]
      newColumn.name = lastItem.name + 1
      newColumn.index = index
      newColumn.field = row => row[index]

      this.table.columns.push(newColumn)
    },
    editColumn (colIndex) {
      let colToEdit = this.table.columns[colIndex]

      colToEdit.name = this.columnEditObject.name
      colToEdit.label = this.columnEditObject.label
      colToEdit.condition = this.columnEditObject.condition
      colToEdit.norms = this.columnEditObject.norms
      colToEdit.mid = this.columnEditObject.mid
      colToEdit.spread = this.columnEditObject.spread
      colToEdit.step = this.columnEditObject.step

      colToEdit.index = this.columnEditObject.index
      colToEdit.field = this.columnEditObject.field
      colToEdit.align = this.columnEditObject.align
    }
  }
}
</script>
