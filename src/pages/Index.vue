<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <q-page>
    <div class="row">
      <div class="col-lg-3 q-pa-sm">
        <q-toolbar>
          <q-btn round dense icon="add" @click="newColumn"/>&nbsp;&nbsp;&nbsp;
          <q-btn round dense icon="save" @click="exportExcel"></q-btn>
        </q-toolbar>
        <q-scroll-area style="height: 800px;">
          <q-list bordered>
            <q-item v-for="col in columns.slice(1)" v-bind:key="col.name" clickable>
              <q-item-section top>
                <q-item-label lines="1">
                  <span class="text-grey-10">{{ col.label }}</span>
                </q-item-label>
                <q-item-label caption lines="1">
                  {{ col.condition }}
                </q-item-label>
                <q-item-label lines="1" class="q-mt-xs">
                  {{ col.norms }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                  <div class="col-sm">среднее={{ col.mid }}</div>
                  <div class="col-sm">разброс={{ col.spread }}</div>
                  <div class="col-sm">шаг={{ col.step }}</div>
              </q-item-section>
              <q-item-section side>
                <div class="text-grey-8 q-gutter-xs">
                  <q-btn class="gt-xs" size="12px" flat dense round icon="edit" @click="onEditColumn(col)"/>
                  <q-btn class="gt-xs" size="12px" flat dense round icon="delete" @click="onDeleteColumn(col)"/>
                </div>
              </q-item-section>
            </q-item>

            <q-separator/>

          </q-list>
        </q-scroll-area>
      </div>
      <div class="col-lg-9 q-pa-sm">
        <q-toolbar>
          <q-btn round dense icon="add" @click="addTable"/>&nbsp;&nbsp;&nbsp;
          <q-btn round dense icon="delete" @click="delTable"/>&nbsp;&nbsp;&nbsp;
        </q-toolbar>
        <div v-for="table in tables" v-bind:key="table.id" class="q-pb-sm">
          <q-table
            title="Отчёт"
            dense
            :data="table.data"
            :columns="columns"
            row-key="name"
            :pagination="pagination"
            hide-bottom
          >
            <template v-slot:top>
              <q-item>
                <q-input v-model.number="table.rows" type="number" dense label="Количество строк" @input="onRowNumChanged(table.id)"/>&nbsp;&nbsp;&nbsp;
              </q-item>
              <q-item>
                <q-input v-model="table.header" dense label="Заголовок:"></q-input>
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
      </div>
    </div>

    <q-dialog v-model="dlgEditColumn">
      <q-card style="width: 500px" class="q-px-sm">

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.label" label="Параметр:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.condition" label="Условие:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.norms" label="Норма:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.mid" type="number" label="Среднее:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.spread" type="number" label="Разброс:" dense/>
          </q-item-section>
        </q-item>

        <q-item dense>
          <q-item-section>
            <q-input v-model="columnEditObj.step" type="number" label="Шаг:" dense/>
          </q-item-section>
        </q-item>

        <q-item>
          <q-btn primary small color="primary" label="ОК" @click="onDlgAccept"/>
        </q-item>
      </q-card>

    </q-dialog>
  </q-page>
</template>

<script>
import XLSX from 'xlsx'

export default {
  data () {
    return {
      leftDrawer: true,
      dlgEditColumn: false,
      pagination: {
        rowsPerPage: 0
      },
      columnEditObj: {
        name: null,
        label: '',
        align: 'left',
        field: row => {},
        condition: '',
        norms: '',
        colIndex: 0,
        mid: 0,
        spread: 0,
        step: 0
      },
      columns: [
        { name: 0, label: '№ изделия', norms: 'Норма', condition: '', field: 'name', align: 'left', colIndex: 'name' }
      ],
      tables: []
    }
  },
  methods: {
    onEditColumn (col) {
      this.dlgEditColumn = true
      this.columnEditObj = { ...col }
    },
    onDeleteColumn (col) {
      this.columns.splice(this.columns.indexOf(col), 1)
    },
    onDlgAccept (event) {
      this.dlgEditColumn = false
      let index = this.columns.findIndex(el => this.columnEditObj.name === el.name)
      if (index === -1) {
        this.addColumn()
        return
      }
      this.editColumn(index)
    },
    newColumn () {
      this.columnEditObj = {
        name: null,
        label: '',
        condition: '',
        norms: '',
        colIndex: 0,
        mid: 0,
        spread: 0,
        step: 0
      }
      this.dlgEditColumn = true
    },
    editColumn (index) {
      let found = this.columns[index]
      found.label = this.columnEditObj.label
      found.condition = this.columnEditObj.condition
      found.norms = this.columnEditObj.norms
      found.mid = parseFloat(this.columnEditObj.mid)
      found.spread = parseFloat(this.columnEditObj.spread)
      found.step = parseFloat(this.columnEditObj.step)
    },
    addColumn () {
      const [lastItem] = this.columns.slice(-1)
      const [index] = [lastItem.name]
      const newColumn = {
        name: lastItem.name + 1,
        label: this.columnEditObj.label,
        condition: this.columnEditObj.condition,
        norms: this.columnEditObj.norms,
        mid: parseFloat(this.columnEditObj.mid),
        spread: parseFloat(this.columnEditObj.spread),
        step: parseFloat(this.columnEditObj.step),
        colIndex: index,
        field: row => row[index]
      }
      this.columns.push(newColumn)
    },
    exportExcel () {
      const filename = 'out'

      const data = []
      let headerRow = []
      let indexes = []

      this.columns.forEach(col => {
        headerRow.push(`${col.label}\n${col.condition}`)
        indexes.push(col.colIndex)
      })
      data.push(headerRow)

      let normsRow = []
      this.columns.forEach(col => {
        normsRow.push(col.norms)
      })
      data.push(normsRow)

      let colNumberRow = []
      for (let i = 0; i < headerRow.length; i++) {
        colNumberRow.push(i + 1)
      }
      data.push(colNumberRow)

      data.push([this.measureSetHeader])

      this.data.forEach(row => {
        let newRow = []
        indexes.forEach(i => {
          newRow.push(row[i])
        })
        data.push(newRow)
      })

      const book = XLSX.utils.book_new()
      const sheet = XLSX.utils.aoa_to_sheet(data)
      XLSX.utils.book_append_sheet(book, sheet, 'sheet1')
      XLSX.writeFile(book, `${filename}.xlsx`)
    },
    generateValue (mid, spread, step) {
      let randint = (min, max) => {
        return Math.floor(Math.random() * (max - min + 1) + min)
      }
      if (!mid || !spread || !step) { return 0 }
      const min = mid - spread
      const max = mid + spread
      let res = randint(0, (max - min) / step) * step + min
      return res.toFixed(1)
    },
    onRowNumChanged (tableId) {
      let table = this.tables[tableId]
      let rows = table.rows
      let result = []
      for (let i = 0; i < rows; i++) {
        let newRow = {}
        this.columns.forEach(col => {
          if (typeof col.colIndex === 'undefined') {
            return
          }
          newRow[col.colIndex] = this.generateValue(col.mid, col.spread, col.step)
        })
        newRow['name'] = i + 1
        result.push(newRow)
      }
      table.data = result
    },
    addTable () {
      let newId = this.tables.length ? this.tables[this.tables.length - 1].id + 1 : 0
      this.tables.push({
        id: newId,
        rows: 0,
        header: '',
        data: []
      })
    },
    delTable () {
      if (this.tables.length) {
        this.tables.pop()
      }
    }
  },
  mounted () {
    [
      {
        name: 1,
        label: 'F1, ГГц',
        align: 'left',
        field: row => row[0],
        condition: 'Uп = 4,5В',
        norms: 'не более 1,9',
        colIndex: 0,
        mid: 1.5,
        spread: 0.5,
        step: 0.1
      },
      {
        name: 2,
        label: 'f2, ГГЦ',
        field: row => row[1],
        align: 'center',
        condition: 'Uп = 4.5 В',
        norms: 'не менее 12,3',
        colIndex: 1,
        mid: 2.5,
        spread: 0.1,
        step: 0.1
      },
      {
        name: 3,
        label: 'D, дБ',
        field: row => row[2],
        condition: 'Uп = 4.5 В',
        norms: 'не менее 51',
        colIndex: 2,
        mid: 1.5,
        spread: 0.5,
        step: 0.1
      },
      {
        name: 4,
        label: 'Pвх мин, дБм',
        field: row => row[3],
        condition: 'Uп = 4.5 В',
        norms: 'не более -41',
        colIndex: 3,
        mid: 1.5,
        spread: 0.5,
        step: 0.1
      },
      {
        name: 5,
        label: 't1, нс',
        field: row => row[4],
        condition: 'Uп = 4.5 В',
        norms: 'не более 25',
        colIndex: 4,
        mid: 1.5,
        spread: 0.5,
        step: 0.1
      },
      {
        name: 6,
        label: 'I, мА',
        field: row => row[5],
        condition: 'Uп = 5.5 В',
        norms: 'не более 100',
        colIndex: 5,
        mid: 1.5,
        spread: 0.5,
        step: 0.1
      }
    ].forEach(el => {
      this.columns.push(el)
    })
  }
}
</script>
